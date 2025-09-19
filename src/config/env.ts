export const env = {
  apiUrl: process.env.NEXT_PUBLIC_URL_API as string,
};

if (!env.apiUrl || env.apiUrl.trim().length === 0) {
  throw new Error(
    "Environment variable NEXT_PUBLIC_URL_API is not defined. Configure it in your .env.local file."
  );
}

