export function aqiInfo(aqi: number | null | undefined) {
  if (aqi == null)
    return {
      label: "No data",
      color: "#9ca3af",
      advice: "AQI is not available right now.",
    };
  if (aqi <= 50)
    return {
      label: "Good",
      color: "#22c55e",
      advice: "Air is clean. Enjoy the outdoors!",
    };
  if (aqi <= 100)
    return {
      label: "Moderate",
      color: "#eab308",
      advice: "Sensitive people should limit long outdoor activity.",
    };
  if (aqi <= 150)
    return {
      label: "Unhealthy for sensitive groups",
      color: "#f97316",
      advice: "Asthmatic, elderly and children should stay indoors.",
    };
  if (aqi <= 200)
    return {
      label: "Unhealthy",
      color: "#ef4444",
      advice: "Everyone should reduce outdoor activity.",
    };
  if (aqi <= 300)
    return {
      label: "Very unhealthy",
      color: "#a855f7",
      advice: "Avoid going outside.",
    };
  return { label: "Hazardous", color: "#7f1d1d", advice: "Stay indoors." };
}
