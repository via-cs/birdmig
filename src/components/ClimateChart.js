import React, { useState, useEffect } from "react";
import { Line } from "react-chartjs-2";
import "chart.js/auto";
import "reactjs-popup/dist/index.css";
import "../App.css";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faInfo } from "@fortawesome/free-solid-svg-icons";
import Popup from "reactjs-popup";

const ClimateChart = ({ selectedYear }) => {
  const [activeTab, setActiveTab] = useState("temperature");
  const [chartData, setChartData] = useState({
    labels: [],
    datasets: [
      {
        label: "Average Data by Month",
        data: [],
        borderColor: "rgba(75, 192, 192, 1)",
        backgroundColor: "rgba(75, 192, 192, 0.2)",
      },
    ],
  });

  useEffect(() => {
    const endpoint =
      activeTab === "temperature" ? "temperature" : "precipitation";
    fetch(`http://localhost:8000/${endpoint}/${selectedYear}`)
      .then((response) => response.json())
      .then((jsonData) => {
        const labels = jsonData.map((item) => item.month);
        const data = jsonData.map((item) => item.avgt || item.pcpn);

        setChartData({
          labels: labels,
          datasets: [
            {
              label:
                activeTab === "temperature"
                  ? "Average Temperature (°F)"
                  : "Average Precipitation (inches)",
              data: data,
              borderColor: "rgba(75, 192, 192, 1)",
              backgroundColor: "rgba(75, 192, 192, 0.2)",
            },
          ],
        });
      })
      .catch((error) => console.error("Error fetching data:", error));
  }, [selectedYear, activeTab]); 

  return (
    <div className="ClimateChart">
      <h2>
        Monthly Average{" "}
        {activeTab === "temperature" ? "Temperature" : "Precipitation"} in CA
        for Year {selectedYear}
        <Popup
          trigger={
            <button className="ButtonInfo">
              <FontAwesomeIcon icon={faInfo} />
            </button>
          }
          modal
          nested
        >
          {(close) => (
            <div className="PredictionControlModal">
              <button className="ButtonExit" onClick={() => close()}>
                X
              </button>
              <h2>How to Read This Chart</h2>
              <p>
                This chart visualizes average monthly climate data—either
                temperature or precipitation—based on which tab you select. The
                chart then displays either historical or projected climate
                trends for the year selected by the slider above.
              </p>

              <h2>Where is this data from?</h2>
              <p>
                The data is from the National Oceanic and Atmospheric
                Administration (NOAA). The underlying climate data is derived
                using the LOCA (Localized Constructed Analogs) methodology based
                on the ssp585 climate scenario. LOCA enhances the resolution of
                climate scenarios by matching daily model outputs with
                historical data to predict future conditions. This methodology
                and the data can be explored further via the websites for
                <a
                  href="https://www.rcc-acis.org/"
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  {" "}
                  RCC-ACIS
                </a>{" "}
                and the
                <a
                  href="https://crt-climate-explorer.nemac.org/"
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  {" "}
                  CRT Climate Explorer
                </a>
                .
              </p>
            </div>
          )}
        </Popup>
      </h2>

      <div>
        <button onClick={() => setActiveTab("temperature")}>Temperature</button>
        <button onClick={() => setActiveTab("precipitation")}>
          Precipitation
        </button>
      </div>
      <Line data={chartData} />
    </div>
  );
};

export default ClimateChart;
