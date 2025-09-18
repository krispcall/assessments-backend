"use client";
import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
// import { fetchVideo } from "@/services/videoService"; // Custom function to fetch a video
import { CreateVideo } from "@/types/videoType";
import { useUpdateVideo } from "@/hooks/useVideo";

export const EditVideoInfo = () => {
  const router = useRouter();
  const { mutate, isPending, error } = useUpdateVideo();
  const [formData, setFormData] = useState<CreateVideo>({
    title: "",
    description: "",
    fileId: "",
    author: "",
  });

  // If the video is fetched, populate the form
  useEffect(() => {
    if (video) {
      setFormData({
        title: video.title,
        description: video.description || "",
        filePath: video.filePath || "",
      });
    }
  }, [video]);

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await mutate({ id: videoId, payload: formData });
      router.push(`/learning/${videoId}`); // Redirect to the video detail page after updating
    } catch (err) {
      console.error("Error updating video:", err);
    }
  };

  if (isPending) return <div>Loading...</div>;
  if (error) return <div>Error loading video data</div>;

  return (
    <div className="max-w-2xl mx-auto px-4 py-8">
      <h1 className="text-2xl font-bold text-gray-800 mb-4">Edit Video</h1>
      <form onSubmit={handleSubmit} className="space-y-6">
        <div>
          <label
            htmlFor="title"
            className="block text-sm font-medium text-gray-700"
          >
            Title
          </label>
          <input
            type="text"
            id="title"
            name="title"
            value={formData.title}
            onChange={handleChange}
            className="mt-1 block w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            required
          />
        </div>

        <div>
          <label
            htmlFor="description"
            className="block text-sm font-medium text-gray-700"
          >
            Description
          </label>
          <textarea
            id="description"
            name="description"
            value={formData.description}
            onChange={handleChange}
            rows={4}
            className="mt-1 block w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>

        <div>
          <label
            htmlFor="filePath"
            className="block text-sm font-medium text-gray-700"
          >
            Video File URL
          </label>
          <input
            type="url"
            id="filePath"
            name="filePath"
            value={formData.fileId}
            onChange={handleChange}
            className="mt-1 block w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            required
          />
        </div>

        <div className="flex justify-end space-x-4">
          <button
            type="submit"
            className="bg-blue-600 text-white px-6 py-2 rounded hover:bg-blue-700 transition"
          >
            Save Changes
          </button>
          <button
            type="button"
            onClick={() => router.push(`/learning/${video}/${id}`)}
            className="bg-gray-400 text-white px-6 py-2 rounded hover:bg-gray-500 transition"
          >
            Cancel
          </button>
        </div>
      </form>
    </div>
  );
};
