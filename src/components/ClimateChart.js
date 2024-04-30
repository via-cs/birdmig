import React, { Component } from 'react';
import * as d3 from 'd3';

class ClimateChart extends Component {
    constructor(props) {
        super(props);
        this.d3Container = React.createRef();
    }

    componentDidMount() {
        this.drawChart();
    }

    componentDidUpdate() {
        this.drawChart();
    }

    normalizeData(data) {
        const minValue = d3.min(data, d => d.Mean_Value);
        const maxValue = d3.max(data, d => d.Mean_Value);
        return data.map(d => ({
            Month: d.Month,
            Mean_Value: minValue + (d.Mean_Value - minValue) / (maxValue - minValue) // Normalized
        }));
    }

    drawChart() {
        if (this.props.data && this.d3Container.current) {
            const svg = d3.select(this.d3Container.current);
            svg.selectAll("*").remove(); // Clear the SVG to prevent duplication

            const margin = { top: 40, right: 20, bottom: 70, left: 60 }; // Adjusted for label spacing
            const width = 800 - margin.left - margin.right;
            const height = 500 - margin.top - margin.bottom;

            const normalizedData = this.normalizeData(this.props.data); // Normalize the data

            const chart = svg.append('g')
                             .attr('transform', `translate(${margin.left},${margin.top})`);

            // Parse months as date for better handling in D3
            const parseMonth = d3.timeParse("%m");
            const data = normalizedData.map(d => ({
                date: parseMonth(d.Month.toString()),
                value: d.Mean_Value
            }));

            // Scales
            const x = d3.scaleTime()
                        .domain(d3.extent(data, d => d.date))
                        .range([0, width]);
            const y = d3.scaleLinear()
                        .domain([0, 1]) // Normalized scale
                        .range([height, 0]);

            // Axes
            const xAxis = d3.axisBottom(x).tickFormat(d3.timeFormat("%B"))
                           .ticks(data.length);
            const yAxis = d3.axisLeft(y);

            chart.append('g')
                 .attr('transform', `translate(0,${height})`)
                 .call(xAxis)
                 .selectAll("text")
                 .style("text-anchor", "end")
                 .attr("dx", "-.8em")
                 .attr("dy", ".15em")
                 .attr("transform", "rotate(-65)");

            chart.append('g').call(yAxis);

            // Line generator
            const line = d3.line()
                          .x(d => x(d.date))
                          .y(d => y(d.value));

            // Drawing the line
            chart.append('path')
                 .datum(data)
                 .attr('fill', 'none')
                 .attr('stroke', 'steelblue')
                 .attr('stroke-width', 2)
                 .attr('d', line);

            // Adding labels
            svg.append("text")
               .attr("transform", "translate(" + (width/2 + margin.left) + " ," + (height + margin.top + 50) + ")")
               .style("text-anchor", "middle")
               .text("Month");

            svg.append("text")
               .attr("transform", "rotate(-90)")
               .attr("y", 0 - margin.left + 20)
               .attr("x",0 - (height / 2))
               .attr("dy", "1em")
               .style("text-anchor", "middle")
               .text("Normalized Mean Value");
        }
    }

    render() {
        return (
            <div className="ClimateChart">
                <h2>Monthly Climate Data</h2>
                <svg ref={this.d3Container} width="900" height="600"></svg>
            </div>
        );
    }
}

export default ClimateChart;
