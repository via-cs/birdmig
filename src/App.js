import { useState, useEffect } from "react";
import axios from "axios";
import "./App.css";
import { CookiesProvider, useCookies } from "react-cookie"

import BirdInfo from './components/BirdInfo';
import SDMChart from './components/SDMChart';
import MigrationMap from './components/MigrationMap';
import EnvironmentalControls from './components/EnvironmentalControls';

function App() {
  
  /* Cookies are required for functionality with flask sessions. */
  axios.create({withCredentials:true});
  // override axios defaults to enable credentials for flask sessions.
  axios.defaults.withCredentials  = true

  // Allow the app to use cookies, for utility with backend request memory.
  const [cookies, setCookie] = useCookies(['user'])

  // Set cookies on request. TODO: find more graceful solution to set cookies.
  function onRequest() {
    setCookie('user', 1)
  }

  
  const [selectedBird, setSelectedBird] = useState(null);
  const [birdInfo, setBirdInfo] = useState(null);
  const [sdmData, setSdmData] = useState(null);
  const [migrationMapUrl, setMigrationMapUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  
  // Map the bird names to filenames for migration images
  const birdMap = {
    'Bird 1': 'blackpoll_warbler_kde_heatmap.html',
    'Bird 2': 'eagle_kde_heatmap.html',
    'Bird 3': 'geese_kde_heatmap.html',
    'Bird 4': 'long_billed_curlew_kde_heatmap.html',
    'Bird 5': 'whimbrel_kde_heatmap.html'
  };

  useEffect(() => {
    selectBird('Bird 1'); // Default bird selection on component mount
  }, []);

  function selectBird(birdName) {
    setSelectedBird(birdName);
    fetchBirdInfo(birdName);
    fetchSDMData(birdName);
    updateMigrationMapUrl(birdName);
  }

  function fetchBirdInfo(birdName) {
    setLoading(true);
    const baseUrl = 'http://localhost:5000'; 

    axios.get(`${baseUrl}/bird-info/${birdName}`)
      .then(response => {
        setBirdInfo(response.data);
        setLoading(false);
      })
      .catch(error => {
        console.error("Error fetching bird info", error);
        setError("Error fetching bird info");
        setBirdInfo(null);
        setLoading(false);
      });
  }

  function fetchSDMData(birdName) {
    setLoading(true);
    const baseUrl = 'http://localhost:5000';

    axios.get(`${baseUrl}/bird-sdm-data/${birdName}`)
      .then(response => {
        setSdmData(response.data.sdmData);
        setLoading(false);
      })
      .catch(error => {
        console.error("Error fetching SDM data", error);
        setError("Error fetching SDM data");
        setSdmData(null);
        setLoading(false);
      });
  }

  function updateMigrationMapUrl(birdName) {
    const baseUrl = 'http://localhost:5000';
    setMigrationMapUrl(`${baseUrl}/migration_images/${birdMap[birdName]}`);
  }

  return (
    <div className="App">
      <CookiesProvider>
        <nav className="sidebar">
          <ul>
            {Object.keys(birdMap).map((bird) => (
              <li key={bird} onClick={() => selectBird(bird)}>
                {bird}
              </li>
            ))}
          </ul>
        </nav>
        <main className="main-content">
          {loading && <p>Loading...</p>}
          {error && <p>Error: {error}</p>}
          {birdInfo && <div className="BirdInfo">
              <BirdInfo data={birdInfo} />
          </div>}
          {sdmData && <div className="SDMChart">
              <SDMChart data={sdmData} />
          </div>}
          <div className="MigrationMap">
              <MigrationMap url={migrationMapUrl} />
          </div>
          <div className="EnvironmentalControls">
              <EnvironmentalControls
                onTemperatureChange={(value) => { /* handle change */ }}
                onPrecipitationChange={(value) => { /* handle change */ }}
              />
          </div>
        </main>
      </CookiesProvider>
    </div>
  );
}

export default App;
