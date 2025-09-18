"use client";
import React from "react";

const Footer: React.FC = () => {
  const currentYear: number = new Date().getFullYear();
  return (
    <footer className="bg-black text-white text-center py-4">
      <div className="container mx-auto  flex justify-between items-center px-20">
        <p>&copy; {currentYear} aneelakheli. All rights reserved.</p>
        <p>Developed by: </p>
      </div>
    </footer>
  );
};

export default Footer;
