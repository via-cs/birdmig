import React, { useEffect, useRef } from 'react';
import * as d3 from 'd3';

function TimeSeries({ data }) {
  const precipitationRef = useRef(null);
  const climateRef = useRef(null);
  const temperatureRef = useRef(null);

  const drawChart = (ref, dataset, color, title) => {
    if (dataset && ref.current) {
      const margin = { top: 30, right: 20, bottom: 30, left: 40 },
            width = 460 - margin.left - margin.right,
            height = 300 - margin.top - margin.bottom;

      d3.select(ref.current).select("svg").remove(); // Clear previous SVG

      const svg = d3.select(ref.current)
        .append("svg")
          .attr("width", width + margin.left + margin.right)
          .attr("height", height + margin.top + margin.bottom)
        .append("g")
          .attr("transform", `translate(${margin.left},${margin.top})`);

      // X axis: scale and draw
      const x = d3.scaleLinear()
        .domain([0, dataset.length - 1])
        .range([0, width]);

      svg.append("g")
        .attr("transform", `translate(0,${height})`)
        .call(d3.axisBottom(x));

      // Y axis: scale and draw
      const y = d3.scaleLinear()
        .domain([0, d3.max(dataset)])
        .range([height, 0]);

      svg.append("g")
        .call(d3.axisLeft(y));

      // Draw the line
      const line = d3.line()
        .x((d, i) => x(i))
        .y(d => y(d));

      svg.append("path")
        .datum(dataset)
        .attr("fill", "none")
        .attr("stroke", color)
        .attr("stroke-width", 1.5)
        .attr("d", line);

      // Title
      svg.append("text")
        .attr("x", (width / 2))
        .attr("y", 0 - (margin.top / 2))
        .attr("text-anchor", "middle")
        .style("font-size", "16px")
        .style("text-decoration", "underline")
        .text(title);
    }
  };

  useEffect(() => {
    drawChart(precipitationRef, data.precipitation, "steelblue", "Precipitation");
    drawChart(climateRef, data.climate, "red", "Climate");
    drawChart(temperatureRef, data.temperature, "green", "Temperature");
  }, [data]); // Redraw charts if data changes

  return (
    <div>
      <h2>Time Series Data</h2>
      <div ref={precipitationRef}></div>
      <div ref={climateRef}></div>
      <div ref={temperatureRef}></div>
    </div>
  );
}

export default TimeSeries;
