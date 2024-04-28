import React, { useState, useEffect } from "react";
import axios from "axios";
import "./App.css";
import BirdInfo from "./components/BirdInfo";
import SDMChart from "./components/SDMChart";
import TimeSeries from "./components/TimeSeries";
import PolylineMap from "./components/PolylineMap";
import GeneralMigrationMap from "./components/KDEHeatmap";

function App() {
  const [selectedBird, setSelectedBird] = useState(null);
  const [birdData, setBirdData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    selectBird("Bird 1");
  }, []);

  function selectBird(birdName) {
    setSelectedBird(birdName);
    getData(birdName);
  }

  function getData(birdName) {
    setLoading(true);
    setError(null);
    const baseUrl = "http://localhost:5000";

    // Fetch bird data
    axios
      .get(`${baseUrl}/bird-data/${birdName}`)
      .then((response) => {
        setBirdData(response.data);
        setLoading(false);
      })
      .catch((error) => {
        console.error("Error fetching bird data", error);
        setError("Error fetching bird data");
        setBirdData(null);
        setLoading(false);
      });
  }

  return (
    <div className="App">
      <nav className="sidebar">
        <ul>
          {["Bird 1", "Bird 2", "Bird 3", "Bird 4", "Bird 5"].map((bird) => (
            <li key={bird} onClick={() => selectBird(bird)}>
              {bird}
            </li>
          ))}
        </ul>
      </nav>
      <main className="main-content">
        {birdData ? (
          <>
            <BirdInfo data={birdData} />
            <SDMChart data={birdData.sdmData} />
            <TimeSeries data={birdData.timeSeriesData} />
            
            <GeneralMigrationMap data={selectedBird} />
          </>
        ) : (
          <p>Select a bird to see its data.</p>
        )}
      </main>
    </div>
  );
}

export default App;
