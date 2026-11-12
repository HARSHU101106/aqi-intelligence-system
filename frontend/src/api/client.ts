import type { EnvironmentData } from "../types/environment";

const BASE = import.meta.env.VITE_API_URL;

export async function fetchEnvironment(
  lat: number,
  lon: number,
): Promise<EnvironmentData> {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), 15000); // give up after 15s
  try {
    const res = await fetch(`${BASE}/environment?lat=${lat}&lon=${lon}`, {
      signal: controller.signal,
    });
    if (!res.ok) {
      const body = await res.json().catch(() => ({}));
      throw new Error(body.detail ?? `Server error (${res.status})`);
    }
    return await res.json();
  } catch (e: any) {
    if (e.name === "AbortError")
      throw new Error("The server took too long to respond.");
    if (e instanceof TypeError)
      throw new Error("Cannot reach the backend. Is it running?");
    throw e;
  } finally {
    clearTimeout(timer);
  }
}
