"use client";
import Link from "next/link";
import React from "react";
import { FaFacebookSquare, FaInstagramSquare } from "react-icons/fa";
import { FaLinkedin } from "react-icons/fa6";

const Header: React.FC = () => {
  // const [sidebarOpen, setSidebarOpen] = useState(false);
  return (
    <div className="flex justify-center">
      <div className="container flex flex-col justify-between items-center py-2 px-4 max-w-screen-xl sm:flex-row">
        <Link href="/" className="text-center flex items-center">
          Assignment -1
        </Link>
        <div className="flex items-center  text-blue-400 my-4">
          <div className="flex items-center my-1"></div>
          <div className="mx-1">
            <Link href={"/"}>Login</Link>
          </div>

          <div className="flex ml-2 pl-2 border-l-2 border-blue-900 text-xl">
            <div className="mx-1">
              <FaLinkedin />{" "}
            </div>
            <div className="mx-1">
              <FaInstagramSquare />
            </div>
            <div className="mx-1">
              <FaFacebookSquare />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Header;
