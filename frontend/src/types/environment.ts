export interface Pollutants {
  pm25?: number | null;
  pm10?: number | null;
  no2?: number | null;
  o3?: number | null;
  co?: number | null;
}

export interface EnvironmentData {
  location: { lat: number; lon: number };
  air_quality: {
    aqi: number | null;
    station: string;
    time: string;
    station_lat?: number;
    station_lon?: number;
    pollutants: Pollutants;
  };
  weather: {
    temperature?: number;
    humidity?: number;
    pressure?: number;
    wind_speed?: number;
    rain?: number;
    description?: string;
  };
  traffic?: { density?: number | null } | null;
  timestamp: string;
}
