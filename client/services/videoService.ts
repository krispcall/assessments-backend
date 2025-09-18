import { CreateVideo, Video, PaginatedVideosResponse } from "@/types/videoType";
import axiosInstance from "./apiClient";

export const getAllVideos = async (): Promise<PaginatedVideosResponse> => {
  const response = await axiosInstance.get<PaginatedVideosResponse>(
    `/fileupload`,
    {}
  );
  return response.data;
};

export const getOneVideo = async (id: string): Promise<Video | null> => {
  try {
    const response = await axiosInstance.get<{ data: Video }>(
      `/fileupload/${id}`
    );
    return response.data.data;
  } catch (error) {
    console.error(`Error fetching video ${id}`, error);
    return null;
  }
};

// export const getOneVideo = async (id: string): Promise<Video | null> => {
//   const videos = await getAllVideos();
//   return videos.data.find((video) => video._id!.toString() === id) || null;
// };

export const addVideo = async (videoData: CreateVideo) => {
  try {
    const response = await axiosInstance.post("/fileupload/", videoData);
    return response.data;
  } catch (error) {
    throw error;
  }
};

export const updateVideo = async (id: string, videoData: CreateVideo) => {
  try {
    const response = await axiosInstance.patch(`/video/${id}`, videoData);
    return response.data;
  } catch (error) {
    console.error("Error updating video:", error);
  }
};

export const deleteVideo = async (id: string) => {
  try {
    const response = await axiosInstance.delete(`/video/${id}`);
    return response.data;
  } catch (error) {
    console.error("Error deleting video:", error);
  }
};
