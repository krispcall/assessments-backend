import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import Header from "@/components/header/Header";
import Footer from "@/components/footer/Footer";
/*import { useState } from "react";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";*/
import Providers from "@/providers/Providers";
import { Toaster } from "sonner";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Kantipur Education Development Council learning platform",
  description:
    "This is the kantipur education development council learning platform where multiple tutorials are found. all subject video are mentioned here.",
  icons: "./fav.ico",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  // const [queryClient] = useState(() => new QueryClient());
  return (
    // <QueryClientProvider client={queryClient}>
    <html lang="en">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
      >
        <Providers>
          <div className="flex flex-col min-h-screen  ">
            <Header />
            <main className="flex flex-col flex-1 "> {children}</main>
            <Footer />
            <Toaster richColors position="top-center" />
          </div>
        </Providers>
      </body>
    </html>
    // </QueryClientProvider>
  );
}
