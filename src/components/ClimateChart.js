import React, { useState, useEffect } from 'react';
import { Line } from 'react-chartjs-2';
import 'chart.js/auto'; 

const ClimateChart = ({ selectedYear, setObservedYear }) => {
    const [chartData, setChartData] = useState({
      labels: [],
      datasets: [
        {
          label: 'Average Temperature by Month',
          data: [],
          borderColor: 'rgba(75, 192, 192, 1)',
          backgroundColor: 'rgba(75, 192, 192, 0.2)',
        },
      ],
    });
  
    useEffect(() => {
        fetch(`http://127.0.0.1:5000/temperature/${selectedYear}`)
          .then(response => response.json())
          .then(jsonData => {
            const labels = jsonData.map(item => item.month);
            const data = jsonData.map(item => item.avgt);
      
            setChartData({
              labels: labels,
              datasets: [{
                label: 'Average Temperature (°F)',
                data: data,
                borderColor: 'rgba(75, 192, 192, 1)',
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
              }]
            });
          })
        .catch(error => console.error('Error fetching data:', error));
    }, [selectedYear]);
      
  
    return (
      <div>
        <h2>Monthly Average Temperature in CA for year {selectedYear}</h2>
        <Line data={chartData} />
      </div>
    );
  };
  
  export default ClimateChart;
  