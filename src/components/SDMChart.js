import React, { useEffect, useRef } from 'react';
import * as d3 from 'd3';

function SDMChart({ data }) {
  const d3Container = useRef(null);

  useEffect(() => {
    if (data && d3Container.current) {
      // Set dimensions and margins for the graph
      const margin = { top: 30, right: 20, bottom: 30, left: 40 },
        width = 400 - margin.left - margin.right,
        height = 300 - margin.top - margin.bottom;

      // Append the svg object to the div and use viewBox for responsiveness
      const svg = d3.select(d3Container.current)
        .html("") // Clear svg content before redrawing
        .append("svg")
          .attr("viewBox", `0 0 ${width + margin.left + margin.right} ${height + margin.top + margin.bottom}`)
          .attr("preserveAspectRatio", "xMidYMid meet") // This preserves the aspect ratio
          .style("width", "100%") // Make svg width responsive
          .style("height", "auto") // Height can be auto (or you might want to specify a fixed height or use 100%)
        .append("g")
          .attr("transform", `translate(${margin.left},${margin.top})`);

      // Add X axis
      const x = d3.scaleLinear()
        .domain([0, d3.max(data, d => d.x)])
        .range([0, width]);
      svg.append("g")
        .attr("transform", `translate(0,${height})`)
        .call(d3.axisBottom(x));

      // Add Y axis
      const y = d3.scaleLinear()
        .domain([0, d3.max(data, d => d.y)])
        .range([height, 0]);
      svg.append("g")
        .call(d3.axisLeft(y));

      // Add dots
      svg.append('g')
        .selectAll("dot")
        .data(data)
        .join("circle")
          .attr("cx", d => x(d.x))
          .attr("cy", d => y(d.y))
          .attr("r", 5)
          .style("fill", "#69b3a2");
    }
  }, [data]); // Redraw chart if data changes

  return (
    <div>
      <h2>SDM Data</h2>
      <div ref={d3Container}></div>
    </div>
  );
}

export default SDMChart;
