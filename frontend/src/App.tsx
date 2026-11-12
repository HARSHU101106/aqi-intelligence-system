import { useEffect, useState } from "react";

export default function App() {
  const [status, setStatus] = useState("checking...");
  useEffect(() => {
    fetch(`${import.meta.env.VITE_API_URL}/health`)
      .then((r) => r.json())
      .then((d) => setStatus(d.status))
      .catch(() => setStatus("backend not reachable"));
  }, []);
  return <h1>Backend status: {status}</h1>;
}
