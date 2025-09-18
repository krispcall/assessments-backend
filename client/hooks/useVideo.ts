import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import {
  addVideo,
  deleteVideo,
  getAllVideos,
  getOneVideo,
  updateVideo,
} from "@/services/videoService";
import { CreateVideo } from "@/types/videoType";

// export const useVideoById = (id: string) => {
//   const { data: video, isLoading, error } = useVideo(id);

//   if (isLoading) return { video: null, isLoading: true, error: null };
//   if (error) return { video: null, isLoading: false, error };

//   return { video, isLoading: false, error: null };
// };

export const useAddVideo = () => {
  return useMutation({
    mutationFn: (payload: CreateVideo) => addVideo(payload),
    mutationKey: ["addVideo"],
  });
};
