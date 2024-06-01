import React from "react";

// Inside the SDMChart component
function SDMChart({ prediction }) {
  console.log(prediction);
  return (
    <div>
      {prediction && (
        <div>
          <img
            className="SDMChart"
            src={
              prediction
                ? `data:image/png;base64, ${prediction}`
                : "publiclogo192.png"
            }
          />
        </div>
      )}
    </div>
  );
}

export default SDMChart;
/*import React, { useRef, useEffect } from "react";
import PropTypes from "prop-types";
import "leaflet/dist/leaflet.css";
import GeoRasterLayer from "georaster-layer-for-leaflet";
import L from "leaflet";
import "proj4";
import "proj4leaflet";
import { scaleSequential } from "d3-scale";
import { interpolateViridis } from "d3-scale-chromatic";

function convertCoordinates(lon, lat) {
  var x = (lon * 20037508.34) / 180;
  var y = Math.log(Math.tan(((90 + lat) * Math.PI) / 360)) / (Math.PI / 180);
  y = (y * 20037508.34) / 180;
  return [x, y];
}

function SDMChart({ data }) {
  const mapContainerRef = useRef(null);
  const mapInstanceRef = useRef(null);

  useEffect(() => {
    if (!data || !Array.isArray(data)) return;

    if (!mapInstanceRef.current) {
      // Create a new Leaflet map
      mapInstanceRef.current = L.map(mapContainerRef.current, {
        crs: L.CRS.EPSG4326,
        center: [36, -107], // Set the initial center of the map, you can adjust this
        zoom: 2, // Set the initial zoom level, adjust as needed
      });

      // Add a tile layer to the map (e.g., OpenStreetMap)
      L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        attribution: "&copy; OpenStreetMap contributors",
      }).addTo(mapInstanceRef.current);

      mapInstanceRef.current.invalidateSize();
    }

    // Define the bounds for your GeoTIFF data, adjust according to your data's extent
    var southWest = L.latLng(-0.25, -180);
    var northEast = L.latLng(72.25, -34);
    var bounds = L.latLngBounds(southWest, northEast);

    // Fit the map to the defined bounds
    mapInstanceRef.current.fitBounds(bounds);

    const georaster = {
      noDataValue: -9999,
      pixelHeight: 1,
      pixelWidth: 1,
      numberOfRasters: 1,
      projection: 4326,
      xmin: -180,
      xmax: 180,
      ymin: -90,
      ymax: 90,
      height: data.length,
      width: data[0].length,
      values: [data],
    };

    // Create a color scale using d3
    const colorScale = scaleSequential(interpolateViridis).domain([0, 1]);

    try {
      const geoRasterLayer = new GeoRasterLayer({
        georaster,
        opacity: 0.7,
        pixelValuesToColorFn: (values) => {
          const value = values[0];
          if (value <= 0) {
            return null; // Don't color pixels with no data value
          } else {
            return colorScale(value); // Apply color scale to pixel value
          }
        },
        resolution: 256, // optional
      });

      geoRasterLayer.addTo(mapInstanceRef.current);
    } catch (error) {
      console.error("Error creating GeoRasterLayer:", error);
    }
  }, [data]);

  return (
    <div
      id="map"
      ref={mapContainerRef}
      style={{ height: "500px", width: "100%" }}
    />
  );
}

SDMChart.propTypes = {
  data: PropTypes.arrayOf(PropTypes.arrayOf(PropTypes.number)).isRequired,
};

export default SDMChart;*/
