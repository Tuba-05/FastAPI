import { React } from "react";


const BASE_URLS = import.meta.env.VITE_API_URL.split(",").map(url => url.trim());

export async function getWorkingBaseURL() {
  for (const url of BASE_URLS) {
    try {
      const res = await fetch(url);

      if (res.ok) return url;
    } catch (e) {
      continue;
    }
  }

  throw new Error("No backend server is reachable");
}
