import { aqiInfo } from "../utils/aqi";

export default function AqiCard({
  aqi,
  station,
  time,
}: {
  aqi: number | null;
  station: string;
  time: string;
}) {
  const info = aqiInfo(aqi);
  return (
    <div className="card" style={{ borderLeft: `8px solid ${info.color}` }}>
      <h3>Air Quality Index</h3>
      <div style={{ fontSize: 56, fontWeight: 700, color: info.color }}>
        {aqi ?? "--"}
      </div>
      <strong>{info.label}</strong>
      <p>{info.advice}</p>
      <small>
        Station: {station}
        <br />
        Updated: {new Date(time).toLocaleString()}
      </small>
    </div>
  );
}
