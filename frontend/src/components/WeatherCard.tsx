import type { EnvironmentData } from "../types/environment";

export default function WeatherCard({ w }: { w: EnvironmentData["weather"] }) {
  return (
    <div className="card">
      <h3>Weather</h3>
      <p style={{ textTransform: "capitalize" }}>{w.description ?? "N/A"}</p>
      <ul>
        <li>🌡️ Temperature: {w.temperature ?? "N/A"} °C</li>
        <li>💧 Humidity: {w.humidity ?? "N/A"} %</li>
        <li>💨 Wind: {w.wind_speed ?? "N/A"} m/s</li>
        <li>⏲️ Pressure: {w.pressure ?? "N/A"} hPa</li>
        <li>🌧️ Rain (1h): {w.rain ?? 0} mm</li>
      </ul>
    </div>
  );
}
