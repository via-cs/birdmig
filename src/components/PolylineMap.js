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
          setSelectedBirdIDs([response.data[0]]);
        } else {
          setAllBirdIDs([]);
        }
      })
      .catch((error) => {
        console.error("Error fetching bird IDs", error);
        setAllBirdIDs([]);
      });
  }, [birdName]);

  const getTrajectoryData = useCallback(() => {
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
  }, [birdName, selectedBirdIDs]);

  const handleDropdownChange = (event) => {
    setSelectedBirdIDs([event.target.value]);
  };

  useEffect(() => {
    fetchAllBirdIDs();
  }, [fetchAllBirdIDs]);

  useEffect(() => {
    if (selectedBirdIDs.length > 0) {
      getTrajectoryData();
    }
  }, [selectedBirdIDs, getTrajectoryData]);

  useEffect(() => {
    if (!trajectoryData || !Array.isArray(trajectoryData)) return;
    if (!mapRef.current) return;

    var map = L.map(mapRef.current).setView([40, -100], 2);
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

    const polyline = L.polyline(latLngs, {
      color: "darkblue",
      weight: 4,
    }).addTo(map);

    const startTimestamp = validData[0].TIMESTAMP;
    const startDate = new Date(startTimestamp);

    const startMonth = startDate.toLocaleString("en-US", { month: "long" });
    const startYear = startDate.getFullYear();

    console.log(`Month: ${startMonth}, Year: ${startYear}`);
    const startMarker = new L.popup()
      .setLatLng(latLngs[0])
      .setContent(`Start Point - ${startMonth} ${startYear}`);

    const endTimestamp = validData[validData.length - 1].TIMESTAMP;
    const endDate = new Date(endTimestamp);
    const endMonth = endDate.toLocaleString("en-US", {
      month: "long",
    });
    const endYear = endDate.getFullYear();
    const endMarker = new L.popup()
      .setLatLng(latLngs[latLngs.length - 1])
      .setContent(`End Point - ${endMonth} ${endYear}`);

    map.addLayer(startMarker).addLayer(endMarker);

    const bearings = [];
    for (let i = 0; i < latLngs.length - 1; i += 150) {
      const startPoint = L.latLng(latLngs[i]);
      const endPoint = L.latLng(latLngs[i + 1]);
      const bearing = calculateBearing(startPoint, endPoint);
      bearings.push(bearing);
    }

    L.polylineDecorator(polyline, {
      patterns: bearings.map((bearing, index) => ({
        offset: 10,
        repeat: 150,
        symbol: L.Symbol.arrowHead({
          pixelSize: 6,
          polygon: false,
          pathOptions: { color: "blue" },
        }),
      })),
    }).addTo(map);

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
