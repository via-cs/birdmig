import React, { useState, useEffect, useRef, useCallback } from "react";
import axios from "axios";
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import "leaflet.heat/dist/leaflet-heat.js";

function Heatmap({ data }) {
  const mapRef = useRef(null);
  const birdName = data;
  const [heatmapData, setHeatmapData] = useState([]);
  const mapInstance = useRef(null);

  const getHeatmapData = useCallback(() => {
    const baseUrl = "http://localhost:8000";
    axios
      .get(`${baseUrl}/get_heatmap_data?bird=${birdName}`)
      .then((response) => {
        setHeatmapData(response.data);
      })
      .catch((error) => {
        console.error("Error fetching heatmap data:", error);
        setHeatmapData([]);
      });
  }, [birdName]);

  useEffect(() => {
    getHeatmapData();
  }, [birdName, getHeatmapData]);

  useEffect(() => {
    if (!heatmapData || !Array.isArray(heatmapData)) return;
    if (!mapRef.current) return;

    if (!mapInstance.current) {
      mapInstance.current = L.map(mapRef.current).setView([40, -100], 2);
    }
    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
      attribution:
        '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
    }).addTo(mapInstance.current);

    const latLngArray = heatmapData.map((point) => [
      parseFloat(point[0]),
      parseFloat(point[1]),
    ]);

    const customGradient = {
      0.1: "purple",
      0.3: "blue",
      0.5: "lime",
      0.7: "yellow",
      0.9: "red",
    };

    const heatLayer = L.heatLayer(latLngArray, {
      radius: 20,
      gradient: customGradient,
    }).addTo(mapInstance.current);

    return () => {
      mapInstance.current.removeLayer(heatLayer);
    };
  }, [heatmapData]);

  return (
    <div>
      <div ref={mapRef} className="TrajectoryMap"></div>
    </div>
  );
}

export default Heatmap;
