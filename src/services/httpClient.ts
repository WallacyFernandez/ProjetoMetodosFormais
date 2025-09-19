import { storage } from "@/utils/Storage";
import { env } from "@/config/env";
import { showHttpErrorToast } from "@/utils/httpErrorToast";

type HttpMethod = "GET" | "POST" | "PUT" | "PATCH" | "DELETE";

export interface RequestOptions {
  headers?: Record<string, string>;
  query?: Record<string, string | number | boolean | undefined | null>;
  body?: unknown;
  suppressErrorToast?: boolean;
  context?: string;
}

function buildUrl(path: string, query?: RequestOptions["query"]): string {
  const base = env.apiUrl.replace(/\/$/, "");
  const normalizedPath = path.startsWith("/") ? path : `/${path}`;
  const url = new URL(`${base}${normalizedPath}`);
  if (query) {
    Object.entries(query).forEach(([key, value]) => {
      if (value !== undefined && value !== null) {
        url.searchParams.append(key, String(value));
      }
    });
  }
  return url.toString();
}

export interface HttpError extends Error {
  status?: number;
  body?: unknown;
}

async function request<T>(method: HttpMethod, path: string, options: RequestOptions = {}): Promise<T> {
  const { headers = {}, query, body, suppressErrorToast, context } = options;

  const accessToken = storage.get("accessToken");
  const finalHeaders: Record<string, string> = {
    "Content-Type": "application/json",
    ...headers,
  };

  if (accessToken) {
    finalHeaders["Authorization"] = `Bearer ${accessToken}`;
  }

  const response = await fetch(buildUrl(path, query), {
    method,
    headers: finalHeaders,
    body: body !== undefined ? JSON.stringify(body) : undefined,
  });

  const isJson = response.headers.get("content-type")?.includes("application/json");
  const data = isJson ? await response.json().catch(() => null) : null;

  if (!response.ok) {
    const message = (data && ((data as any).message || (data as any).detail || (data as any).error)) || response.statusText || "Request failed";
    const error: HttpError = new Error(typeof message === "string" ? message : JSON.stringify(message));
    error.status = response.status;
    error.body = data;
    if (!suppressErrorToast) {
      showHttpErrorToast(error, context);
    }
    throw error;
  }

  return data as T;
}

export const http = {
  get: <T>(path: string, options?: RequestOptions) => request<T>("GET", path, options),
  post: <T>(path: string, body?: unknown, options?: Omit<RequestOptions, "body">) =>
    request<T>("POST", path, { ...(options || {}), body }),
  put: <T>(path: string, body?: unknown, options?: Omit<RequestOptions, "body">) =>
    request<T>("PUT", path, { ...(options || {}), body }),
  patch: <T>(path: string, body?: unknown, options?: Omit<RequestOptions, "body">) =>
    request<T>("PATCH", path, { ...(options || {}), body }),
  del: <T>(path: string, options?: RequestOptions) => request<T>("DELETE", path, options),
};

