"use client";
// import { useAuth } from "@/contexts/AuthContext";
// import Image from "next/image";
import { useVideo } from "@/hooks/useVideo";
// import { useRouter } from "next/navigation";
import { QRCodeSVG } from "qrcode.react";
import { useRef } from "react";

export type ImageSetting = {
  src: string;
  height: string;
};

function ErrorComponent({ errorMessage }: { errorMessage: string }) {
  return (
    <div
      className="p-4 mb-4 text-sm text-red-700 bg-red-100 rounded-lg dark:bg-red-200 dark:text-red-800"
      role="alert"
    >
      <svg
        className="inline mr-2 w-5 h-5"
        fill="currentColor"
        viewBox="0 0 20 20"
        xmlns="http://www.w3.org/2000/svg"
      >
        <path
          fillRule="evenodd"
          d="M10 18a8 8 0 100-16 8 8 0 000 16zm.93-11.412a.75.75 0 00-1.36 0l-3 6.5a.75.75 0 001.36.64l.784-1.697h3.433l.784 1.696a.75.75 0 001.36-.638l-3-6.5zM9.25 12a.75.75 0 101.5 0 .75.75 0 00-1.5 0z"
          clipRule="evenodd"
        />
      </svg>
      {errorMessage}
    </div>
  );
}

function VideoDetail({ id }: { id: string }) {
  // const router = useRouter();
  const {
    data: videoData,
    isSuccess,
    isLoading,
    error,
    isError,
    // refetch
  } = useVideo(id as string);

  const qrRef = useRef<HTMLDivElement>(null);

  const handleDownloadQR = () => {
    if (!qrRef.current) return;

    const svg = qrRef.current.querySelector("svg"); // Select the QR Code SVG
    if (!svg) return;

    const serializer = new XMLSerializer();
    const svgString = serializer.serializeToString(svg);
    const blob = new Blob([svgString], { type: "image/svg+xml" });
    const url = URL.createObjectURL(blob);

    const link = document.createElement("a");
    link.href = url;
    link.download = "qrcode.svg";
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  };

  return (
    <>
      <div className="flex flex-col flex-1 p-6 bg-gray-800 ">
        {/* <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">
          {"Learning Video"}
        </h2> */}

        {isLoading && (
          <div className="w-full flex justify-center items-center my-16">
            <div className="h-48">
              <div className="rounded-md h-12 w-12 border-4 border-t-4 border-blue-500 animate-spin absolute"></div>
            </div>
            <div className="text-xl font-semibold my-4 ">
              Loading <span className="animate-ping">...</span>
            </div>
          </div>
        )}

        {isError && <ErrorComponent errorMessage={error.message} />}

        {isSuccess && videoData && (
          <div>
            <div className="grid  md:grid-rows-1 grid-cols-1 md:grid-cols-2 gap-6">
              <div className="relative h-full w-full">
                <video controls preload="none" className="h-full w-full">
                  <source src={videoData.filePath} type="video/mp4" />
                  <track
                    src="/path/to/captions.vtt"
                    kind="subtitles"
                    srcLang="en"
                    label="English"
                  />
                  Your browser does not support the video tag.
                </video>
              </div>
              <div className="flex flex-col">
                <div className="mb-4">
                  <span className="font-semibold text-gray-700 dark:text-gray-300">
                    Title:
                  </span>
                  <span className="ml-2 text-gray-900 dark:text-white">
                    {videoData.title}
                  </span>
                </div>
                <div className="mb-4">
                  <span className="font-semibold text-gray-700 dark:text-gray-300">
                    Author:
                  </span>
                  <span className="ml-2 text-gray-900 dark:text-white">
                    {videoData.author}
                  </span>
                </div>
                <div className="mb-4">
                  <span className="font-semibold text-gray-700 dark:text-gray-300">
                    Description:
                  </span>
                  <span className="ml-2 text-gray-900 dark:text-white">
                    {videoData.description}
                  </span>
                </div>
                {/* <div className="mb-4">
                  <span className="font-semibold text-gray-700 dark:text-gray-300">
                    Category:
                  </span>
                  <span className="ml-2 text-gray-900 dark:text-white">
                    {videoData.category}
                  </span>
                </div> */}
                <div className="mb-4">
                  {/* <span className="font-semibold text-gray-700 dark:text-gray-300">
                    Duration:
                  </span> */}
                  {/* <span className="ml-2 text-gray-900 dark:text-white">
                    {videoData.alt}
                  </span> */}
                </div>
                <div ref={qrRef} className="">
                  <QRCodeSVG
                    value={`https://learning.kedc.edu.np/learning/${videoData._id}`}
                    title={videoData.title}
                    size={200}
                  />
                </div>
                <div className="m-3 rounded ">
                  <button
                    onClick={handleDownloadQR}
                    className="border rounded-lg p-4 bg-blue-600 text-white hover:bg-red-600"
                  >
                    Download QR
                  </button>
                </div>
                {/* <div className="mb-4">
                  <span className="font-semibold text-gray-700 dark:text-gray-300">
                    Views:
                  </span>
                  {/* <span className="ml-2 text-gray-900 dark:text-white">
                    {videoData.views}
                  </span> */}
                {/* </div> */}
              </div>
            </div>
          </div>
        )}

        {!videoData && (
          <div className="w-full flex justify-center items-center my-16">
            <div className="text-xl font-semibold my-4 ">No video found</div>
          </div>
        )}
      </div>
    </>
  );
}

export default VideoDetail;
