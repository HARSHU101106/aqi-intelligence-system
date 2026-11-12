import { useLocation } from "./hooks/useLocation";
import { useEnvironment } from "./hooks/useEnvironment";
import AqiCard from "./components/AqiCard";
import PollutantGrid from "./components/PollutantGrid";
import WeatherCard from "./components/WeatherCard";
import MapView from "./components/MapView";
import Spinner from "./components/Spinner";
import ErrorBanner from "./components/ErrorBanner";

export default function App() {
  const { coords, error: locError, request } = useLocation();
  const { data, loading, error } = useEnvironment(coords);

  return (
    <div className="layout">
      <aside className="sidebar">
        <h2>AirAware</h2>
        <p>Home</p>
        <p>Map</p>
        <p>Weather</p>
        <p>Analytics (soon)</p>
      </aside>
      <main className="content">
        <header style={{ display: "flex", justifyContent: "space-between" }}>
          <h1>Environmental Dashboard</h1>
          <button onClick={request}>📍 Share my location</button>
        </header>

        {locError && <ErrorBanner message={locError} />}
        {error && <ErrorBanner message={error} />}
        {loading && <Spinner />}

        {coords && (
          <div className="card">
            <h3>Your location</h3>
            Latitude: {coords.lat.toFixed(4)}, Longitude:{" "}
            {coords.lon.toFixed(4)}
          </div>
        )}

        {data && (
          <>
            <AqiCard
              aqi={data.air_quality.aqi}
              station={data.air_quality.station}
              time={data.air_quality.time}
            />
            <PollutantGrid data={data.air_quality.pollutants} />
            <WeatherCard w={data.weather} />
            <MapView data={data} />
          </>
        )}
      </main>
    </div>
  );
}
