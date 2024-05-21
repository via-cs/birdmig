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
    
        // Avoid division by zero if all values are the same
        if (minValue === maxValue) {
            return data.map(d => ({
                Month: d.Month,
                Mean_Value: 0.5 // or any fixed middle value
            }));
        }
    
        return data.map(d => ({
            Month: d.Month,
            Mean_Value: (d.Mean_Value - minValue) / (maxValue - minValue)
        }));
    }
    

    drawChart() {
        if (this.props.data && this.d3Container.current) {
            const svg = d3.select(this.d3Container.current);
            svg.selectAll("*").remove(); // Clear the SVG to prevent duplication
    
            const margin = { top: 40, right: 20, bottom: 70, left: 60 };
            const width = this.d3Container.current.clientWidth - margin.left - margin.right; // Adjusted for margins
            const height = this.d3Container.current.clientHeight - margin.top - margin.bottom; // Adjusted for margins
    
            const normalizedData = this.normalizeData(this.props.data);
    
            const chart = svg.append('g')
                             .attr('transform', `translate(${margin.left},${margin.top})`);
    
            // Setup the x-axis as a band scale
            const x = d3.scaleBand()
                        .domain(normalizedData.map(d => d.Month))
                        .range([0, width])
                        .padding(0.1);

            // Setup the y-axis as a linear scale
            const y = d3.scaleLinear()
                        .domain([0, 1]) // Normalized scale
                        .range([height, 0]);

            // Add axes to the chart
            const xAxis = d3.axisBottom(x).tickFormat(d3.format("d"));
            const yAxis = d3.axisLeft(y);

            chart.append('g')
                 .attr('transform', `translate(0,${height})`)
                 .call(xAxis);

            chart.append('g')
                 .call(yAxis);

            // Define the line generator
            const line = d3.line()
                          .x(d => x(d.Month) + x.bandwidth() / 2) // Center the line in the band
                          .y(d => y(d.Mean_Value));

            // Draw the line
            chart.append('path')
                 .datum(normalizedData)
                 .attr('fill', 'none')
                 .attr('stroke', 'steelblue')
                 .attr('stroke-width', 2)
                 .attr('d', line);

            // Add axis labels
            svg.append("text")
               .attr("transform", "translate(" + (width/2 + margin.left) + " ," + (height + margin.top + 50) + ")")
               .style("text-anchor", "middle")
               .text("Month");

            svg.append("text")
               .attr("transform", "rotate(-90)")
               .attr("y", 0 - margin.left + 20)
               .attr("x", 0 - (height / 2))
               .attr("dy", "-1.2em")
               .style("text-anchor", "middle")
               .text("Normalized Mean Value");
        }
    }

    render() {
        return (
            <div className="ClimateChart">
                <svg ref={this.d3Container}></svg>
            </div>
        );
    }
}

export default ClimateChart;
