import React, { useState, useEffect } from "react";
import axios from "axios";
import "./App.css";
import { CookiesProvider, useCookies } from "react-cookie";
import BirdInfo from "./components/BirdInfo";
import SDMChart from "./components/SDMChart";
import PolylineMap from "./components/PolylineMap";
import Heatmap from "./components/HeatMap";
import GeneralMigrationMap from "./components/GeneralMigrationMap";
import PredictionControls from "./components/PredictionControls";
import ClimateChart from "./components/ClimateChart";
import { image } from "d3";

function App() {
    const [socketInstance, setSocketInstance] = useState("");
	const [cookies, setCookie] = useCookies(["user"]);
	const backendUrl = "http://localhost:8000";

  // Define birdMap and climateVariables
  const birdMap = {
    "Blackpoll Warbler": "warbler",
    "Bald Eagle": "eagle",
    "White Fronted Goose": "anser",
    "Long Billed Curlew": "curlew",
    "Whimbrel": "whimbrel",
  };

  const climateVariables = {
    prec: "prec.json",
    tmax: "tmax.json",
    srad: "srad.json",
    tmin: "tmin.json",
    vapr: "vapr.json",
    wind: "wind.json",
    tavg: "tavg.json",
  };

  const images = require.context("./images", true);
  const imageList = images.keys().map((image) => images(image));
  const orderedImageList = Object.keys(birdMap).map((bird) => {
    const index = Object.keys(birdMap).indexOf(bird);
    return imageList.find((image) => image.includes(`/${bird}.`));
  });


  function updatePredictionVars(year, emissionRate, inputBird) {
		axios
			.put(`${backendUrl}/prediction`, {
                    bird: birdMap[inputBird],
                    year: year,
                    emissions: emissionRate },
                    {
                      headers: {
                        'Content-Type': 'application/json'
                      }
                  })
			.then((response) => {
        console.log(response.data.prediction)
				setPredictionData(response.data.prediction);
			})
			.catch((error) => {
				console.error("Error sending prediction variables:", error);
			});
	}

  const [selectedBird, setSelectedBird] = useState(null);
  const [birdInfo, setBirdInfo] = useState(null);
  const [sdmData, setSdmData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [selectedYear, setObservedYear] = useState(2021);
  const [selectedEmissions, setEmissionRate] = useState("ssp245");
  const [climateData, setClimateData] = useState(null);
  const [selectedClimateVariable, setSelectedClimateVariable] = useState("");
  /* const [showPolylineMap, setShowPolylineMap] = useState(true);
  const [showHeatMap, setShowHeatMap] = useState(false);
  const [showSDM, setShowSDM] = useState(false);*/
  const [selectedMap, setSelectedMap] = useState("Polyline");
  const [predictionData, setPredictionData] = useState(null);

  axios.create({ withCredentials: true });
  axios.defaults.withCredentials = true;

  useEffect(() => {
    selectBird("Blackpoll Warbler");
  }, []);

  function selectBird(birdName) {
    setSelectedBird(birdName);
    fetchBirdInfo(birdName);
    fetchSDMData(birdName);
    updatePredictionVars(selectedYear, selectedEmissions, birdName)
  }

  function fetchBirdInfo(birdName) {
    setLoading(true);
    axios
      .get(`${backendUrl}/bird-info/${birdName}`)
      .then((response) => {
        setBirdInfo(response.data);
        setLoading(false);
      })
      .catch((error) => {
        console.error("Error fetching bird info", error);
        setError("Error fetching bird info");
        setBirdInfo(null);
        setLoading(false);
      });
  }

  function fetchSDMData(birdName) {
    setLoading(true);
    axios
      .get(`${backendUrl}/bird-sdm-data/${birdName}`)
      .then((response) => {
        setSdmData(response.data.sdmData);
        setLoading(false);
      })
      .catch((error) => {
        console.error("Error fetching SDM data", error);
        setError("Error fetching SDM data");
        setSdmData(null);
        setLoading(false);
      });
  }

  useEffect(() => {
    if (selectedClimateVariable) {
      fetchClimateData(selectedClimateVariable);
    }
  }, [selectedClimateVariable]);

  function fetchClimateData(variable) {
    setLoading(true);
    axios
      .get(`${backendUrl}/json/${climateVariables[variable]}`)
      .then((response) => {
        setClimateData(response.data);
        setLoading(false);
      })
      .catch((error) => {
        console.error("Error fetching climate data", error);
        setError("Failed to fetch climate data");
        setLoading(false);
      });
  }

  function handleClimateVariableChange(variable) {
    setSelectedClimateVariable(variable);
  }

	useEffect(() => {

	}, [selectedBird, selectedYear, selectedEmissions]);

  return (
    <div className="App">
      <CookiesProvider>
        <div className="header">
          <h1> {selectedBird} </h1>
        </div>
        
        <nav className="sidebar">
          <ul>
            {Object.keys(birdMap).map((bird, index) => (
              <li key={bird} onClick={() => selectBird(bird)}>
                {bird}
                {orderedImageList[index] && (
                  <img
                    className="image"
                    src={orderedImageList[index]}
                    alt={`${index}`}
                  />
                )}
              </li>
            ))}
          </ul>
        </nav>
        <main className="main-content">
          {loading && <p>Loading...</p>}
          {error && <p>Error: {error}</p>}
          {birdInfo && (
            <div className="BirdInfo">
              <BirdInfo data={birdInfo} />
              <div className="PredictionControls">
                <PredictionControls
                  onPredictionUpdated = {(year, emissions) => {
                    setObservedYear(year)
                    setEmissionRate(emissions)
                    updatePredictionVars(year, emissions, selectedBird)
                  }}
                />
              </div>
            </div>
          )}
          <div className="MigrationMap">
            <div className="tabs">
              <button
                className="tab"
                onClick={() => setSelectedMap("Polyline")}
              >
                Show Single Bird Trajectory
              </button>
              <button className="tab" onClick={() => setSelectedMap("Heatmap")}>
                Show General Bird Trajectory
              </button>
              <button className="tab" onClick={() => setSelectedMap("SDM")}>
                Show Species Distribution Map
              </button>
            </div>
            <div>
              {selectedMap === "Polyline" && (
                <PolylineMap selectedBird={birdMap[selectedBird]} />
              )}
              {selectedMap === "Heatmap" && (
                <Heatmap data={birdMap[selectedBird]} />
              )}
            </div>
          </div>
          {sdmData && (
            <div className="SDMChart">
              <SDMChart data={sdmData} prediction={predictionData} />
            </div>
          )}
          <div className="ClimateDataContainer">
            <div className="ClimateData">
              <strong>Climate Data</strong>
              <div className="tabs">
                {Object.keys(climateVariables).map((variable) => (
                  <button
                    key={variable}
                    className={`tab ${
                      selectedClimateVariable === variable ? "active" : ""
                    }`}
                    onClick={() => handleClimateVariableChange(variable)}
                  >
                    {variable.toUpperCase()}
                  </button>
                ))}
              </div>
            </div>
            {climateData && <ClimateChart data={climateData} />}
          </div>
        </main>
      </CookiesProvider>
    </div>
  );
}

export default App;
