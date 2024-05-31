import React, { useState, useEffect, useRef } from "react";
import { MapContainer, TileLayer, Polyline } from "react-leaflet";
import axios from "axios";
import "leaflet-arrowheads";

function ArrowheadsPolyline({ positions, arrowheads, ...props }) {
  const polylineRef = useRef(null);

  useEffect(() => {
    const polyline = polylineRef.current;
    const updateArrowheads = () => {
      if (arrowheads) {
        polyline.arrowheads(arrowheads);
        polyline._update();
      }
    };

    const mapContainer = polyline._map;
    if (mapContainer) {
      mapContainer.on("zoom", updateArrowheads);
    }

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

function GeneralMigrationMap({ selectedBird }) {
  const [segmentedPolylines, setSegmentedPolylines] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [mapCenter, setMapCenter] = useState([40, -100]); // Center over North America

  useEffect(() => {
    const baseUrl = "http://localhost:8000";
    const getMigrationPattern = async () => {
      setLoading(true);
      try {
        const response = await axios.get(`${baseUrl}/get_general_migration?bird=${selectedBird}`);
        if (response && response.data && response.data.segmented_polylines) {
          setSegmentedPolylines(response.data.segmented_polylines);
        } else {
          throw new Error("Unexpected API response structure");
        }
      } catch (error) {
        setError("An error occurred while fetching migration patterns: " + (error.response?.data?.error || error.message));
      }
      setLoading(false);
    };

    if (selectedBird) {
      getMigrationPattern();
    }
  }, [selectedBird]);

  return (
    <div>
      {loading && <p>Loading...</p>}
      {error && <p>{error}</p>}
      {!loading && !error && (
        <MapContainer
            data-testid="map-container"
            center={mapCenter}
            zoom={3}
            style={{ height: "600px", width: "100%" }}
        >
          <TileLayer
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          />
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
