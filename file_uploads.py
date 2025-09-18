import os
import shutil
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from config import Config
from models import Files, db
from api_limiter import rate_limit_and_security

upload_bp = Blueprint('upload', __name__)

def combine_chunks(file_id, filename, total_chunks):
    """Combines all uploaded chunks into a single final file."""
    try:
        file_dir = os.path.join(Config.CHUNK_DIR, file_id)
        if not os.path.isdir(file_dir):
            return {"error": "Chunk directory not found."}, 404

        # Verify all chunks exist before combining
        for i in range(total_chunks):
            chunk_path = os.path.join(file_dir, f"chunk_{i}")
            if not os.path.exists(chunk_path):
                return {"error": f"Missing chunk {i}."}, 400

        final_dir = Config.FINAL_DIR
        os.makedirs(final_dir, exist_ok=True)
        final_path = os.path.join(final_dir, filename)

        with open(final_path, "wb") as final_file:
            for i in range(total_chunks):
                part_path = os.path.join(file_dir, f"chunk_{i}")
                with open(part_path, "rb") as part_file:
                    final_file.write(part_file.read())

        file_size = os.path.getsize(final_path)
        # Clean up the temporary chunk directory
        shutil.rmtree(file_dir, ignore_errors=True)

        return {"final_path": final_path, "size": file_size}, 200

    except Exception as e:
        # Clean up on error to prevent junk files
        shutil.rmtree(file_dir, ignore_errors=True)
        return {"error": str(e)}, 500

@upload_bp.route("/fileupload/", methods=["POST"])
@rate_limit_and_security
def upload_chunk():
    if request.method == "OPTIONS":
        # Handle CORS preflight request
        return jsonify({}), 200

    required_fields = ["file_id", "chunk_number", "total_chunks", "filename", "chunk"]
    if not all(field in request.form or field in request.files for field in required_fields):
        return jsonify({"error": "Missing required form data."}), 400

    try:
        file_id = request.form["file_id"]
        chunk_number = int(request.form["chunk_number"])
        total_chunks = int(request.form["total_chunks"])
        filename = secure_filename(request.form["filename"])
        chunk = request.files["chunk"]
        
        file_dir = os.path.join(Config.CHUNK_DIR, file_id)
        os.makedirs(file_dir, exist_ok=True)
        chunk_path = os.path.join(file_dir, f"chunk_{chunk_number}")
        chunk.save(chunk_path)

        if chunk_number == total_chunks - 1:
            # All chunks are uploaded, now combine them
            combine_result, status_code = combine_chunks(file_id, filename, total_chunks)
            if status_code != 200:
                return jsonify(combine_result), status_code
            
            # Now that the full file is created, insert into the database
            upload = Files(
                file_id=file_id,
                filename=filename,
                size=combine_result["size"],
                mime_type=chunk.mimetype,
            )
            db.session.add(upload)
            db.session.commit()
            
            return jsonify({
                "message": "Upload complete",
                "file_id": upload.file_id,
                "filename": upload.filename,
                "size": upload.size,
                "mime_type": upload.mime_type,
            }), 201

        # Not the last chunk -> still uploading
        return jsonify({
            "message": f"Chunk {chunk_number} uploaded",
            "file_id": file_id,
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500



# from flask import Blueprint, request, jsonify
# from werkzeug.utils import secure_filename
# import os
# from models import db, Files
# from config import Config
# import shutil

# upload_bp = Blueprint('upload', __name__)

# @upload_bp.route("/fileupload/", methods=["POST", "GET", "OPTIONS"])
# def upload_chunk():
#     try:
#         file_id = request.form["file_id"]
#         chunk_number = int(request.form["chunk_number"])  # 0-based index
#         total_chunks = int(request.form["total_chunks"])
#         filename = secure_filename(request.form["filename"])
#         chunk = request.files["chunk"]
#         file_dir = os.path.join(Config.CHUNK_DIR, file_id)
#         os.makedirs(file_dir, exist_ok=True)

#         # Save chunk file to temporary storage
#         chunk_path = os.path.join(file_dir, f"chunk_{chunk_number}")
#         chunk.save(chunk_path)

#         # Insert into DB only after all chunks are uploaded
#         if chunk_number == total_chunks - 1:
#             # All chunks are uploaded, now combine them into the final file
#             final_path = os.path.join(Config.FINAL_DIR, filename)
#             os.makedirs(Config.FINAL_DIR, exist_ok=True)

#             with open(final_path, "wb") as final_file:
#                 # Write all chunks into the final file
#                 for i in range(total_chunks):
#                     part_path = os.path.join(file_dir, f"chunk_{i}")
#                     with open(part_path, "rb") as part_file:
#                         final_file.write(part_file.read())

#             # Clean up the chunk directory
#             shutil.rmtree(file_dir)

#             # Now that the full file is created, insert into the database
#             file_size = os.path.getsize(final_path)
#             upload = Files(
#                 file_id=file_id,
#                 filename=filename,
#                 size=file_size,  # Now we know the full file size
#                 mime_type=chunk.mimetype,  # Use mime type from first chunk
#             )
#             db.session.add(upload)
#             db.session.commit()

#             return jsonify({
#                 "message": "Upload complete",
#                 "file_id": upload.file_id,
#                 "filename": upload.filename,
#                 "size": upload.size,
#                 "mime_type": upload.mime_type,
#             }), 201

#         # Not last chunk → still uploading
#         return jsonify({
#             "message": f"Chunk {chunk_number} uploaded",
#             "file_id": file_id,
#         }), 200

#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# # @upload_bp.route('/upload-status/<file_id>', methods=['GET'])
# # def upload_status(file_id):
# #     upload = Files.query.filter_by(file_id=file_id).first()
# #     if not upload:
# #         return jsonify({'status': 'not_found'}), 404

# #     return jsonify({
# #         message:"successfy"
# #     })

# # @upload_bp.route('/finalize-upload', methods=['POST'])
# # def finalize_upload():
# #     file_id = request.form['file_id']
# #     upload = Files.query.filter_by(file_id=file_id).first()

# #     if not upload:
# #         return jsonify({'error': 'Upload not found'}), 404

# #     if upload.received_chunks < upload.total_chunks:
# #         return jsonify({'error': 'Not all chunks uploaded'}), 400

# #     chunk_dir = os.path.join(Config.CHUNK_DIR, file_id)
# #     final_path = os.path.join(Config.FINAL_DIR, upload.filename)

# #     with open(final_path, 'wb') as final_file:
# #         for i in range(1, upload.total_chunks + 1):
# #             chunk_path = os.path.join(chunk_dir, f"chunk_{i}")
# #             with open(chunk_path, 'rb') as chunk_file:
# #                 final_file.write(chunk_file.read())

# #     upload.is_complete = True
# #     db.session.commit()

# #     return jsonify({'message': 'Upload complete', 'file_path': final_path}), 200