import Image from "next/image";
import learningBoy from "@/public/images/learning_boy.webp"; // Ensure correct path
import Link from "next/link";

export default function Home() {
  return (
    <section className="flex flex-col md:flex-row items-center justify-center min-h-screen bg-gray-100 px-6">
      {/* Left Section - Image */}
      <div className="w-full md:w-1/2 flex justify-center">
        <Image
          src={learningBoy}
          alt="Learning Boy"
          width={500} // Adjust size as needed
          height={500}
          className="rounded-lg shadow-lg"
        />
      </div>

      {/* Right Section - Content */}
      <div className="w-full md:w-1/2 flex flex-col items-center text-center md:text-left">
        <h1 className="text-3xl md:text-5xl font-bold text-gray-900 leading-snug text-center">
          Welcome
        </h1>
        <p className="mt-4 text-lg text-gray-700">
          Join our Video streaming in Python Flask.
        </p>
        <Link href="/fileupload">
          <button className="mt-6 px-6 py-3 bg-red-600 text-white border border-yellow-400 rounded-lg text-lg md:text-xl transition-all hover:bg-blue-900">
            Join Us
          </button>
        </Link>
      </div>
    </section>
  );
}
