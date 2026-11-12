const API = import.meta.env.VITE_API_URL;

export type Pollutant = { value: number; unit: string } | null;

export type AirQuality = {
  location: { lat: number; lon: number };
  aqi: number | null;
  pollutants: Record<string, Pollutant>;
  station: { name: string | null; lat: number | null; lon: number | null };
  sources_used: string[];
  timestamp: string | null;
};

export async function fetchAirQuality(
  lat: number,
  lon: number,
): Promise<AirQuality> {
  const res = await fetch(`${API}/air-quality?lat=${lat}&lon=${lon}`);
  if (!res.ok) {
    const err = await res.json().catch(() => null);
    throw new Error(err?.detail ?? "Could not load air quality data.");
  }
  return res.json();
}
