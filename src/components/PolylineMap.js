import React, { useState, useEffect, useRef, useCallback } from "react";
import axios from "axios";
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import "leaflet-polylinedecorator";

function calculateBearing(startPoint, endPoint) {
  const startLat = startPoint.lat * (Math.PI / 180);
  const startLng = startPoint.lng * (Math.PI / 180);
  const endLat = endPoint.lat * (Math.PI / 180);
  const endLng = endPoint.lng * (Math.PI / 180);

  const dLng = endLng - startLng;
  const y = Math.sin(dLng) * Math.cos(endLat);
  const x =
    Math.cos(startLat) * Math.sin(endLat) -
    Math.sin(startLat) * Math.cos(endLat) * Math.cos(dLng);
  let bearing = Math.atan2(y, x);
  bearing = bearing * (180 / Math.PI);
  bearing = (bearing + 360) % 360;
  return bearing;
}

function PolylineMap({ selectedBird }) {
  const mapRef = useRef(null);

  const birdName = selectedBird;
  const [trajectoryData, setTrajectoryData] = useState({});
  const [selectedBirdIDs, setSelectedBirdIDs] = useState([]);
  const [allBirdIDs, setAllBirdIDs] = useState([]);

  const fetchAllBirdIDs = useCallback(() => {
    const baseUrl = "http://localhost:8000";
    axios
      .get(`${baseUrl}/get_bird_ids?bird=${birdName}`)
      .then((response) => {
        if (Array.isArray(response.data)) {
          setAllBirdIDs(response.data);
          setSelectedBirdIDs([response.data[0]]); // Initially select the first bird ID
        } else {
          console.log(response.data);
          console.error("Error: Response data is not an array", response.data);
          setAllBirdIDs([]);
        }
      })
      .catch((error) => {
        console.error("Error fetching bird IDs", error);
        setAllBirdIDs([]);
      });
  }, [birdName]);

  const getTrajectoryData = () => {
    const baseUrl = "http://localhost:8000";
    const firstBirdID = selectedBirdIDs[0];
    axios
      .get(
        `${baseUrl}/get_trajectory_data?bird=${birdName}&birdID=${firstBirdID}`
      )
      .then((response) => {
        setTrajectoryData(response.data);
      })
      .catch((error) => {
        console.error("Error fetching trajectory data", error);
        setTrajectoryData({});
      });
  };

  const handleDropdownChange = (event) => {
    setSelectedBirdIDs([event.target.value]);
  };

  useEffect(() => {
    // Fetch all available bird IDs and populate the dropdown options
    fetchAllBirdIDs();
  }, [fetchAllBirdIDs]);

  useEffect(() => {
    if (selectedBirdIDs.length > 0) {
      getTrajectoryData();
    }
  }, [selectedBirdIDs, birdName]);

  useEffect(() => {
    if (!trajectoryData || !Array.isArray(trajectoryData)) return;
    if (!mapRef.current) return;

    // Initialize Leaflet map centered over North America
    var map = L.map(mapRef.current).setView([40, -100], 2); // Centered over North America
    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
      attribution:
        '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
    }).addTo(map);

    const validData = trajectoryData.filter(
      (d) => !isNaN(d.LATITUDE) && !isNaN(d.LONGITUDE) && d.TIMESTAMP
    );

    if (validData.length === 0) {
      console.error("No valid trajectory data found.");
      return;
    }

    const latLngs = validData.map((d) => [
      parseFloat(d.LATITUDE),
      parseFloat(d.LONGITUDE),
    ]);

    // Create polyline and add it to the map with a specific color
    const polyline = L.polyline(latLngs, {
      color: "darkblue",
      weight: 4,
    }).addTo(map);
    // Add marker for the start point
    const startTimestamp = validData[0].TIMESTAMP;
    const startMonth = new Date(startTimestamp).toLocaleString("en-US", {
      month: "long",
    });
    const startMarker = new L.popup()
      .setLatLng(latLngs[0])
      .setContent(`Start Point - ${startMonth}`);

    // Add marker for the end point
    const endTimestamp = validData[validData.length - 1].TIMESTAMP;
    const endMonth = new Date(endTimestamp).toLocaleString("en-US", {
      month: "long",
    });
    const endMarker = new L.popup()
      .setLatLng(latLngs[latLngs.length - 1])
      .setContent(`End Point - ${endMonth}`);

    map.addLayer(startMarker).addLayer(endMarker);
    // Calculate bearings for each segment of the polyline
    const bearings = [];
    for (let i = 0; i < latLngs.length - 1; i += 150) {
      const startPoint = L.latLng(latLngs[i]);
      const endPoint = L.latLng(latLngs[i + 1]);
      const bearing = calculateBearing(startPoint, endPoint);
      bearings.push(bearing);
    }

    // Create polyline decorator and add it to the map
    L.polylineDecorator(polyline, {
      patterns: bearings.map((bearing, index) => ({
        offset: 10,
        repeat: 150,
        symbol: L.Symbol.arrowHead({
          pixelSize: 6,
          polygon: false,
          pathOptions: { color: "blue" }, // Customize arrow color if needed
        }),
      })),
    }).addTo(map);

    // Clean up map instance if component unmounts
    return () => {
      map.remove();
    };
  }, [trajectoryData]);

  return (
    <div>
      <div ref={mapRef} className="TrajectoryMap">
        <div style={{ position: "absolute", top: 0, right: 0, zIndex: 999 }}>
          <select onChange={handleDropdownChange} value={selectedBirdIDs[0]}>
            <option value="">Select {birdName} ID</option>
            {allBirdIDs.map((birdID, index) => (
              <option key={birdID} value={birdID}>
                {birdName.toUpperCase()} {index + 1}
              </option>
            ))}
          </select>
        </div>
      </div>
    </div>
  );
}

export default PolylineMap;
