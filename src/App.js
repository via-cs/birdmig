import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';
import BirdInfo from './components/BirdInfo';
import SDMChart from './components/SDMChart';
import MigrationMap from './components/MigrationMap';
import EnvironmentalControls from './components/EnvironmentalControls';

function App() {
  const [selectedBird, setSelectedBird] = useState(null);
  const [birdData, setBirdData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  
  useEffect(() => {
    selectBird('Bird 1');
  }, []);

  function selectBird(birdName) {
    setSelectedBird(birdName);
    getData(birdName);
  }

  function getData(birdName) {
    setLoading(true);
    setError(null);
    const baseUrl = 'http://localhost:5000'; 
  
    // Map the bird names to filenames
    const birdMap = {
      'Bird 1': 'blackpoll_warbler_kde_heatmap.html',
      'Bird 2': 'eagle_kde_heatmap.html',
      'Bird 3': 'geese_kde_heatmap.html',
      'Bird 4': 'long_billed_curlew_kde_heatmap.html',
      'Bird 5': 'whimbrel_kde_heatmap.html'
    };
    
    const birdFileName = birdMap[birdName];
  
    if (!birdFileName) {
      setError(`No map available for ${birdName}.`);
      setLoading(false);
      return;
    }
  
    const migrationMapUrl = `${baseUrl}/migration_images/${birdFileName}`;
  
    axios.get(`${baseUrl}/bird-data/${birdName}`)
      .then(response => {
        // Set the bird data along with the migrationMapUrl
        setBirdData({
          ...response.data,
          migrationMapUrl: migrationMapUrl // Add this new property
        });
        setLoading(false);
      })
      .catch(error => {
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
          {['Bird 1', 'Bird 2', 'Bird 3', 'Bird 4', 'Bird 5'].map((bird) => (
            <li key={bird} onClick={() => selectBird(bird)}>
              {bird}
            </li>
          ))}
        </ul>
      </nav>
      <main className="main-content">
        {loading && <p>Loading...</p>}
        {error && <p>Error: {error}</p>}
        {birdData ? (
          <>
            <div className="BirdInfo">
                <BirdInfo data={birdData} />
            </div>
            <div className="EnvironmentalControls">
                <EnvironmentalControls
                onTemperatureChange={(value) => { /* handle change */ }}
                onPrecipitationChange={(value) => { /* handle change */ }}
                />
            </div>
            <div className="MigrationMap">
                <MigrationMap url={birdData.migrationMapUrl} /> {/* Render MigrationMap with the URL */}
            </div>
            <div className="SDMChart">
                <SDMChart data={birdData.sdmData} />
            </div>
          </>
        ) : (
          <p>Select a bird to see its data.</p>
        )}
      </main>
    </div>
  );
}

export default App;
