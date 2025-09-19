import { storage } from "@/utils/Storage";

function setCookie(name: string, value: string, days = 7) {
  if (typeof document === "undefined") return;
  const expires = new Date(Date.now() + days * 24 * 60 * 60 * 1000).toUTCString();
  document.cookie = `${name}=${encodeURIComponent(value)}; Expires=${expires}; Path=/; SameSite=Lax`;
}

function getCookie(name: string): string | null {
  if (typeof document === "undefined") return null;
  const match = document.cookie.match(new RegExp("(?:^|; )" + name.replace(/([.$?*|{}()\[\]\\/+^])/g, "\\$1") + "=([^;]*)"));
  return match ? decodeURIComponent(match[1]) : null;
}

function deleteCookie(name: string) {
  if (typeof document === "undefined") return;
  document.cookie = `${name}=; Expires=Thu, 01 Jan 1970 00:00:00 GMT; Path=/; SameSite=Lax`;
}

export function saveTokens(access: string, refresh?: string) {
  storage.set("accessToken", access);
  if (refresh) storage.set("refreshToken", refresh);
  setCookie("accessToken", access);
  if (refresh) setCookie("refreshToken", refresh);
}

export function getAccessToken(): string | null {
  return storage.get("accessToken") || getCookie("accessToken");
}

export function clearTokens() {
  storage.remove("accessToken");
  storage.remove("refreshToken");
  deleteCookie("accessToken");
  deleteCookie("refreshToken");
}

