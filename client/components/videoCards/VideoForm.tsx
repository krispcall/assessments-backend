"use client";
import React, { useState } from "react";
import axiosInstance from "@/services/apiClient";
import { v4 as uuidv4 } from "uuid";

const VideoForm: React.FC = () => {
  // const router = useRouter();
  const [uploadProgress, setUploadProgress] = useState(0);

  const handleFileChange = async (
    event: React.ChangeEvent<HTMLInputElement>
  ) => {
    const file = event.target.files?.[0] ?? null;
    if (file) {
      await sendFileAndGetVideoId(file);
    }
  };

  const sendFileAndGetVideoId = async (file: File) => {
    const chunkSize = 2 * 1024 * 1024;
    const totalChunks = Math.ceil(file.size / chunkSize);
    const file_id = uuidv4();

    for (let i = 0; i < totalChunks; i++) {
      const start = i * chunkSize;
      const end = Math.min((i + 1) * chunkSize, file.size);
      const chunk = file.slice(start, end);

      const formData = new FormData();
      formData.append("chunk", chunk);
      formData.append("chunk_number", String(i));
      formData.append("total_chunks", String(totalChunks));
      formData.append("filename", file.name);
      formData.append("file_id", file_id);

      try {
        const response = await axiosInstance.post("/fileupload/", formData, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
          onUploadProgress: () => {
            const progress = ((i + 1) / totalChunks) * 100;
            setUploadProgress(progress);
          },
        });

        if (response.status === 201 && i === totalChunks - 1) {
          alert("Upload complete!");
        }
      } catch (error) {
        console.error(`Chunk ${i + 1} upload failed:`, error);
        alert("Upload failed. Please try again.");
        break;
      }
    }
  };

  const radius = 45;
  const circumference = 2 * Math.PI * radius;
  const strokeDashoffset =
    circumference - (uploadProgress / 100) * circumference;

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-100 py-8 px-4">
      <div className="border p-6 text-blue-800 bg-white rounded-lg shadow-lg w-full max-w-md">
        <h2 className="text-xl font-semibold mb-4">Upload Video</h2>

        <div className="relative w-full max-h-34 flex items-center justify-center border-2 p-4 border-dashed rounded-lg">
          <svg
            width="120"
            height="120"
            viewBox="0 0 120 120"
            className="transform rotate-90"
          >
            <circle
              cx="60"
              cy="60"
              r={radius}
              stroke="#ddd"
              strokeWidth="10"
              fill="none"
            />
            <circle
              cx="60"
              cy="60"
              r={radius}
              stroke={uploadProgress === 100 ? "green" : "blue"}
              strokeWidth="10"
              fill="none"
              strokeDasharray={circumference}
              strokeDashoffset={strokeDashoffset}
              style={{
                transition: "stroke-dashoffset 0.5s ease, stroke 0.5s ease",
              }}
            />
          </svg>
          <div className="absolute text-center text-sm font-semibold">
            {uploadProgress === 100
              ? "Uploaded"
              : `${Math.round(uploadProgress)}%`}
          </div>

          <input
            type="file"
            name="video"
            id="video"
            onChange={handleFileChange}
            className="absolute opacity-0 w-full h-full cursor-pointer"
            accept="video/*"
          />
        </div>

        <p className="text-sm text-gray-500 text-center mt-2">
          Click or drag a video file here to upload
        </p>
      </div>
    </div>
  );
};

export default VideoForm;
