import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

// This function can be marked `async` if using `await` inside
const publicRoutes = ["/login", "/register", "/", "/learning"];
export function middleware(request: NextRequest) {
  const url = request.nextUrl.pathname.replace(/\/+$/, "");
  const token =
    (request.cookies.get("accessToken")?.value ||
      request.headers.get("Authorization")) ??
    "";

  /* The commented code block you provided is a conditional check in the middleware function to handle
route redirection based on the user's authentication status and the requested URL path. */
  // if (!token && !publicRoutes.includes(url)) {
  //   // If the user is not authenticated and trying to access a protected route
  //   return NextResponse.redirect(new URL("/learning", request.url));
  // }
  // if (token && publicRoutes.includes(url)) {
  //   return NextResponse.redirect(new URL("/dashboard", request.url));
  // }

  return NextResponse.next();
}

export const config = {
  matcher: [
    "/((?!api|_next/static|_next/image|favicon.ico|sitemap.xml|robots.txt).*)",
  ],
};
