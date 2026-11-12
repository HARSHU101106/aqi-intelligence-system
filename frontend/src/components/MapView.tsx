import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import markerIcon from "leaflet/dist/images/marker-icon.png";
import markerShadow from "leaflet/dist/images/marker-shadow.png";
import type { EnvironmentData } from "../types/environment";

// Fix for the invisible-marker problem in Vite
const icon = L.icon({
  iconUrl: markerIcon,
  shadowUrl: markerShadow,
  iconAnchor: [12, 41],
});

export default function MapView({ data }: { data: EnvironmentData }) {
  const { lat, lon } = data.location;
  const aq = data.air_quality;
  return (
    <MapContainer
      center={[lat, lon]}
      zoom={12}
      style={{ height: 400, borderRadius: 12 }}
    >
      <TileLayer
        attribution="&copy; OpenStreetMap contributors"
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      <Marker position={[lat, lon]} icon={icon}>
        <Popup>📍 You are here</Popup>
      </Marker>
      {aq.station_lat != null && aq.station_lon != null && (
        <Marker position={[aq.station_lat, aq.station_lon]} icon={icon}>
          <Popup>
            <strong>{aq.station}</strong>
            <br />
            AQI: {aq.aqi ?? "N/A"}
            <br />
            PM2.5: {aq.pollutants.pm25 ?? "N/A"}
            <br />
            PM10: {aq.pollutants.pm10 ?? "N/A"}
          </Popup>
        </Marker>
      )}
    </MapContainer>
  );
}
