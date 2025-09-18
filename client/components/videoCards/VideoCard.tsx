import Link from "next/link";
import React from "react";
import { Video } from "@/types/videoType";

interface CardProps {
  video: Video;
}

const VideoCard: React.FC<CardProps> = ({ video }) => {
  return (
    <div className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition duration-300">
      <Link href={`/learning/${video._id}`}>
        <div className="relative">
          <video className="w-full h-48 object-cover" controls preload="none">
            <source src={video.filePath} type="video/mp4" />
            <track
              src="/path/to/captions.vtt"
              kind="subtitles"
              srcLang="en"
              label="English"
            />
            Your browser does not support the video tag.
          </video>
        </div>
        <div className="p-4">
          <h2 className="text-lg font-semibold text-gray-800 mb-1">
            {video.title}
          </h2>
          <p className="text-sm text-gray-600">by {video.author}</p>
        </div>
      </Link>
    </div>
  );
};

export default VideoCard;
