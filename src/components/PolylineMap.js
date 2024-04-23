import React, { useState, useEffect, useRef, useCallback } from "react";
import * as d3 from "d3";
import { feature } from "topojson-client";
import worldData from "world-atlas/countries-110m.json";
import axios from "axios";

function PolylineMap({ data }) {
  const svgRef = useRef(null);
  const birdName = "anser";
  const [trajectoryData, setTrajectoryData] = useState({});
  const [selectedBirdIDs, setSelectedBirdIDs] = useState([]);
  const [allBirdIDs, setAllBirdIDs] = useState([]);

  const fetchAllBirdIDs = useCallback(() => {
    const baseUrl = "http://localhost:5000";
    // Make an API call to fetch all available bird IDs
    axios
      .get(`${baseUrl}/get_bird_ids?bird=${birdName}`)
      .then((response) => {
        if (Array.isArray(response.data)) {
          setAllBirdIDs(response.data);
          setSelectedBirdIDs([response.data[0]]); // Initially select the first bird ID
        } else {
          console.error("Error: Response data is not an array", response.data);
          setAllBirdIDs([]);
        }
      })
      .catch((error) => {
        console.error("Error fetching bird IDs", error);
        setAllBirdIDs([]);
      });
  }, [birdName]);

  const handleDropdownChange = (event) => {
    // Update selected bird IDs state when dropdown selection changes
    setSelectedBirdIDs([event.target.value]);
  };

  useEffect(() => {
    // Fetch all available bird IDs and populate the dropdown options
    fetchAllBirdIDs();
  }, [fetchAllBirdIDs]);

  useEffect(() => {
    // Fetch trajectory data for the selected bird IDs
    const getTrajectoryData = () => {
      const baseUrl = "http://localhost:5000";
      const firstBirdID = selectedBirdIDs[0]; // Fetch trajectory data for the first selected bird ID
      // Make an API call to fetch trajectory data for the selected bird ID
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
    if (selectedBirdIDs.length > 0) {
      getTrajectoryData();
    }
  }, [selectedBirdIDs, birdName]);

  const renderPolyline = (svg, data, projection) => {
    // Filter out data points with invalid coordinates
    const validData = data.filter(
      (d) => !isNaN(d.LATITUDE) && !isNaN(d.LONGITUDE)
    );
    if (validData.length === 0) {
      console.error("No valid coordinates found in data.");
      return;
    }

    const line = d3
      .line()
      .x((d) => projection([parseFloat(d.LONGITUDE), parseFloat(d.LATITUDE)])[0])
      .y((d) => projection([parseFloat(d.LONGITUDE), parseFloat(d.LATITUDE)])[1]);

    svg
      .append("path")
      .datum(validData)
      .attr("fill", "none")
      .attr("stroke", "steelblue")
      .attr("stroke-width", 2)
      .attr("d", line);
  };

  useEffect(() => {
    if (!trajectoryData || Object.keys(trajectoryData).length === 0) return; // Return if data is not available

    const width = 800;
    const height = 600;

    const projection = d3
      .geoNaturalEarth1()
      .scale(150)
      .translate([width / 2, height / 2]);

    const path = d3.geoPath().projection(projection);

    const svg = d3.select(svgRef.current);
    svg.selectAll("*").remove(); // Clear previous drawings

    // Create a zoom behavior
    const zoom = (event) => d3.zoom()
      .scaleExtent([1, 8]) // Set the scale extent for zooming
      .on("zoom", () => {
        svg.selectAll(".country").attr("transform", event.transform);
      }); // Call zoomed function when zoom event occurs

    svg.call(zoom); // Apply zoom behavior to the SVG

    svg
      .selectAll(".country")
      .data(feature(worldData, worldData.objects.countries).features)
      .enter()
      .append("path")
      .attr("class", "country")
      .attr("d", path)
      .attr("fill", "lightgray")
      .attr("stroke", "white");

    // Render polylines only if trajectoryData is available
    renderPolyline(svg, trajectoryData, projection);
    console.log("Polyline rendered");
  }, [trajectoryData]);

  return (
    <div>
      <select onChange={handleDropdownChange} value={selectedBirdIDs[0]}>
        <option value="">Select bird ID</option>
        {allBirdIDs.map((birdID) => (
          <option key={birdID} value={birdID}>
            {birdID}
          </option>
        ))}
      </select>
      <svg ref={svgRef} width={800} height={600}></svg>
    </div>
  );
}

export default PolylineMap;
