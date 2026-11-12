import { useEffect, useState } from "react";
import { useLocation } from "./hooks/useLocation";
import { fetchAirQuality, type AirQuality } from "./api";

export default function App() {
  const {
    coords,
    error: locError,
    loading: locLoading,
    request,
  } = useLocation();
  const [aq, setAq] = useState<AirQuality | null>(null);
  const [aqError, setAqError] = useState<string | null>(null);
  const [aqLoading, setAqLoading] = useState(false);

  useEffect(() => {
    if (!coords) return;
    setAqLoading(true);
    setAqError(null);
    fetchAirQuality(coords.lat, coords.lon)
      .then(setAq)
      .catch((e) => setAqError(e.message))
      .finally(() => setAqLoading(false));
  }, [coords]);

  return (
    <div style={{ padding: 24, fontFamily: "sans-serif" }}>
      <h1>Air Quality Dashboard</h1>

      <section>
        <h2>Current Location</h2>
        <button onClick={request} disabled={locLoading}>
          {locLoading ? "Finding you..." : "Share my location"}
        </button>
        {coords && (
          <p>
            Latitude: {coords.lat.toFixed(5)} | Longitude:{" "}
            {coords.lon.toFixed(5)}
          </p>
        )}
        {locError && <p style={{ color: "crimson" }}>{locError}</p>}
      </section>

      <section>
        <h2>Air Quality</h2>
        {aqLoading && <p>Loading air quality...</p>}
        {aqError && <p style={{ color: "crimson" }}>{aqError}</p>}
        {aq && (
          <>
            <p>
              <strong>AQI: {aq.aqi ?? "N/A"}</strong>
            </p>
            <p>Station: {aq.station.name ?? "Unknown"}</p>
            <p>
              Updated:{" "}
              {aq.timestamp
                ? new Date(aq.timestamp).toLocaleString()
                : "Unknown"}
            </p>
            <p>Source: {aq.sources_used.join(", ")}</p>
            <ul>
              {Object.entries(aq.pollutants).map(([name, p]) => (
                <li key={name}>
                  {name.toUpperCase()}:{" "}
                  {p ? `${p.value} ${p.unit}` : "not available"}
                </li>
              ))}
            </ul>
          </>
        )}
      </section>
    </div>
  );
}
