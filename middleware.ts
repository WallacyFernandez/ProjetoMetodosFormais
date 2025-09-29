import { NextRequest, NextResponse } from "next/server";

const PUBLIC_PATHS = ["/", "/login", "/cadastro", "/_next", "/public", "/favicon.ico"];

function isPublicPath(pathname: string): boolean {
  return PUBLIC_PATHS.some((p) => pathname === p || pathname.startsWith(p + "/"));
}

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;

  if (pathname === "/current-url" || pathname === "/.identity") {
    return new NextResponse(null, { status: 404 });
  }
  
  if (isPublicPath(pathname)) {
    return NextResponse.next();
  }

  const hasToken = Boolean(request.cookies.get("accessToken"));

  if (!hasToken && pathname.startsWith("/dashboard")) {
    const url = request.nextUrl.clone();
    url.pathname = "/login";
    return NextResponse.redirect(url);
  }

  return NextResponse.next();
}

export const config = {
  matcher: ["/dashboard/:path*"],
};

