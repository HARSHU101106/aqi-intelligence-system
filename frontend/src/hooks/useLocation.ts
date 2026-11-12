import { useState } from "react";

export type Coords = { lat: number; lon: number };

export function useLocation() {
  const [coords, setCoords] = useState<Coords | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const request = () => {
    setError(null);

    // Case 1: browser too old
    if (!("geolocation" in navigator)) {
      setError("Your browser does not support location. Please use Chrome.");
      return;
    }

    setLoading(true);

    navigator.geolocation.getCurrentPosition(
      // Success
      (pos) => {
        const lat = pos.coords.latitude;
        const lon = pos.coords.longitude;

        // Case 2: coordinates are nonsense
        if (
          Number.isNaN(lat) ||
          Number.isNaN(lon) ||
          Math.abs(lat) > 90 ||
          Math.abs(lon) > 180
        ) {
          setError("Received invalid coordinates. Please try again.");
        } else {
          setCoords({ lat, lon });
        }
        setLoading(false);
      },
      // Failure
      (err) => {
        if (err.code === err.PERMISSION_DENIED) {
          setError(
            "Permission denied. Click the lock icon in the address bar and allow location.",
          );
        } else if (err.code === err.POSITION_UNAVAILABLE) {
          setError("Your location is unavailable. Check your GPS or internet.");
        } else if (err.code === err.TIMEOUT) {
          setError("Finding your location took too long. Please try again.");
        } else {
          setError("Something went wrong while getting your location.");
        }
        setLoading(false);
      },
      { enableHighAccuracy: true, timeout: 10000, maximumAge: 0 },
    );
  };

  return { coords, error, loading, request };
}
