import React, { useEffect, useState } from "react";
import {
  MapContainer,
  TileLayer,
  Polyline,
  Marker,
  Popup,
} from "react-leaflet";
import axios from "axios";
import { Icon } from "leaflet";
import markerIconPng from "leaflet/dist/images/marker-icon.png";

function GeneralMigrationMap() {
  const birdName = "anser";
  const [generalizedRoute, setGeneralizedRoute] = useState([]);
  const [arrows, setArrows] = useState([]);
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
        setGeneralizedRoute(response.data.generalized_route);
        setArrows(response.data.arrows);
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
          style={{ height: "400px", width: "100%" }}
        >
          <TileLayer
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          />
          {/* Render generalized route as Polyline */}
          <Polyline positions={generalizedRoute} color="blue" />

          {/* Render arrows representing direction */}
          {arrows.map((arrow, index) => (
            <Marker
              key={index}
              position={arrow[0]}
              icon={
                new Icon({
                  iconUrl: markerIconPng,
                  iconSize: [25, 41],
                  iconAnchor: [12, 41],
                })
              }
              rotationAngle={arrow[2]} // Set the rotation angle for the arrow
            >
              <Popup>{`Arrow pointing in direction ${arrow[2]} degrees`}</Popup>
            </Marker>
          ))}
        </MapContainer>
      )}
    </div>
  );
}

export default GeneralMigrationMap;
