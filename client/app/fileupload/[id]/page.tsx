import VideoDetail from "@/components/videoCards/VideoDetails";

export default async function Videopage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;
  return <VideoDetail id={id} />;
}
