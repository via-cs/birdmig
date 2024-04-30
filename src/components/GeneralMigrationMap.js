import React, { useEffect, useState, useRef } from "react";
import { MapContainer, TileLayer, Polyline } from "react-leaflet";
import axios from "axios";
import "leaflet-arrowheads";

function ArrowheadsPolyline({ positions, arrowheads, ...props }) {
  const polylineRef = useRef(null);

  useEffect(() => {
    const polyline = polylineRef.current;

    // Function to update arrowheads
    const updateArrowheads = () => {
      if (arrowheads) {
        polyline.arrowheads(arrowheads);
        polyline._update();
      }
    };

    // Update arrowheads when the map zoom level changes
    const mapContainer = polyline._map;
    if (mapContainer) {
      mapContainer.on("zoom", updateArrowheads);
    }

    // Clean up event listener
    return () => {
      if (mapContainer) {
        mapContainer.off("zoom", updateArrowheads);
      }
    };
  }, [arrowheads]);
  return (
    <Polyline
      smoothFactor={5}
      positions={positions}
      ref={polylineRef}
      color={"darkblue"}
      arrowheads={{ size: "10px", color: "green" }}
    />
  );
}

function GeneralMigrationMap() {
  const birdName = "whimbrel";
  const [segmentedPolylines, setSegmentedPolylines] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [mapCenter, setMapCenter] = useState([40, -100]); // Center over North America

  useEffect(() => {
    const getMigrationPattern = async () => {
      const baseUrl = "http://localhost:5000";
      try {
        const response = await axios.get(
          `${baseUrl}/get_general_migration?bird=${birdName}`
        );
        setSegmentedPolylines(response.data.segmented_polylines);
        setLoading(false);
      } catch (error) {
        setError(error.response.data.error || "An error occurred");
        setLoading(false);
      }
    };

    getMigrationPattern();
  }, []);

  return (
    <div>
      {loading && <p>Loading...</p>}
      {error && <p>{error}</p>}
      {!loading && !error && (
        <MapContainer
          center={mapCenter}
          zoom={3} // Adjust the zoom level as needed
          style={{ height: "600px", width: "100%" }}
        >
          <TileLayer
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          />
          {/* Render segmented polylines as ArrowheadsPolyline */}
          {segmentedPolylines.map((segment, index) => (
            <ArrowheadsPolyline
              key={index}
              positions={segment.coordinates}
              arrowheads={[segment.direction]}
            />
          ))}
        </MapContainer>
      )}
    </div>
  );
}

export default GeneralMigrationMap;
