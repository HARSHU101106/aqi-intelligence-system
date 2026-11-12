import { useEffect, useState } from "react";
import { fetchEnvironment } from "../api/client";
import type { EnvironmentData } from "../types/environment";

export function useEnvironment(coords: { lat: number; lon: number } | null) {
  const [data, setData] = useState<EnvironmentData | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!coords) return;
    setLoading(true);
    setError(null);
    fetchEnvironment(coords.lat, coords.lon)
      .then(setData)
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, [coords]);

  return { data, loading, error };
}
