import type { Pollutants } from "../types/environment";

const ITEMS: { key: keyof Pollutants; label: string; unit: string }[] = [
  { key: "pm25", label: "PM2.5", unit: "µg/m³" },
  { key: "pm10", label: "PM10", unit: "µg/m³" },
  { key: "no2", label: "NO₂", unit: "µg/m³" },
  { key: "o3", label: "O₃", unit: "µg/m³" },
  { key: "co", label: "CO", unit: "mg/m³" },
];

export default function PollutantGrid({ data }: { data: Pollutants }) {
  return (
    <div className="grid">
      {ITEMS.map(({ key, label, unit }) => (
        <div className="card small" key={key}>
          <h4>{label}</h4>
          <div className="value">{data[key] ?? "N/A"}</div>
          <small>{data[key] != null ? unit : "not reported"}</small>
        </div>
      ))}
    </div>
  );
}
