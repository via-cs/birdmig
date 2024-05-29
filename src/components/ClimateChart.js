import React, { useState, useEffect } from 'react';
import { Line } from 'react-chartjs-2';
import 'chart.js/auto';
import Popup from 'reactjs-popup';
import 'reactjs-popup/dist/index.css';

const ClimateChart = ({ selectedYear }) => {

    const [activeTab, setActiveTab] = useState('temperature');
    const [chartData, setChartData] = useState({
        labels: [],
        datasets: [
            {
                label: 'Average Data by Month',
                data: [],
                borderColor: 'rgba(75, 192, 192, 1)',
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
            },
        ],
    });

    useEffect(() => {
        const endpoint = activeTab === 'temperature' ? 'temperature' : 'precipitation';

        fetch(`http://localhost:8000/${endpoint}/${selectedYear}`)
            .then(response => response.json())
            .then(jsonData => {
                const labels = jsonData.map(item => item.month);
                const data = jsonData.map(item => item.avgt || item.pcpn);

                setChartData({
                    labels: labels,
                    datasets: [{
                        label: activeTab === 'temperature' ? 'Average Temperature (°F)' : 'Average Precipitation (inches)',
                        data: data,
                        borderColor: 'rgba(75, 192, 192, 1)',
                        backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    }]
                });
            })
            .catch(error => console.error('Error fetching data:', error));
    }, [selectedYear, activeTab]); // Depend on activeTab as well

    return (
        <div>
            <h2>Monthly Average {activeTab === 'temperature' ? 'Temperature' : 'Precipitation'} in CA for year {selectedYear}</h2>
            <div>
                <button onClick={() => setActiveTab('temperature')}>Temperature</button>
                <button onClick={() => setActiveTab('precipitation')}>Precipitation</button>
            </div>
            <Line data={chartData} />
        </div>
    );
};

export default ClimateChart;
