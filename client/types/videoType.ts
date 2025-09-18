export type CreateVideo = {
  _id?: number;
  title: string;
  description: string;
  fileId: string;
  author: string;
  /* alt: string;
  // thumbnailUrl: string;
  // duration: string;
  // views: string;
  // category: string; */
};

export type Video = {
  _id: string;
  alt: string;
  author: string;
  description: string;
  filePath: string;
  title: string;
};

export type PaginatedVideosResponse = {
  data: Video[];
  total: number;
  page: number;
  limit: number;
};
