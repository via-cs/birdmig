import React, { useState, useEffect, useRef } from "react";
import axios from "axios";
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import "leaflet.heat/dist/leaflet-heat.js";

function Heatmap({ data }) {
  const mapRef = useRef(null);
  const birdName = data;
  console.log(birdName);
  const [heatmapData, setHeatmapData] = useState([]);

  const getHeatmapData = () => {
    const baseUrl = "http://localhost:5000";
    axios
      .get(`${baseUrl}/get_heatmap_data?bird=${birdName}`)
      .then((response) => {
        setHeatmapData(response.data);
      })
      .catch((error) => {
        console.error("Error fetching heatmap data:", error);
        setHeatmapData([]);
      });
  };

  useEffect(() => {
    getHeatmapData();
  }, [birdName]);

  useEffect(() => {
    if (!heatmapData || !Array.isArray(heatmapData)) return;
    if (!mapRef.current) return;
    // Initialize Leaflet map
    const map = L.map(mapRef.current).setView([40, -100], 2);

    // Add tile layer
    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
      attribution:
        '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
    }).addTo(map);

    // Convert heatmap data to LatLng array
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

    // Create heatmap layer
    L.heatLayer(latLngArray, { radius: 20, gradient: customGradient }).addTo(
      map
    );

    console.log(map);
    // Clean up map instance if component unmounts
    return () => {
      map.remove();
    };
  }, [heatmapData]);

  return (
    <div>
      <div ref={mapRef} className="TrajectoryMap"></div>
    </div>
  );
}

export default Heatmap;
