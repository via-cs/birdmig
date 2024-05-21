import React, { useState, useEffect } from "react";
import axios from "axios";
import "./App.css";
import { CookiesProvider, useCookies } from "react-cookie";
import { io } from "socket.io-client";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faBars } from "@fortawesome/free-solid-svg-icons";
//import WebSocketCall from ""
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
  const backendUrl = "http://localhost:5000";

  // Define birdMap and climateVariables
  const birdMap = {
    "Blackpoll Warbler": "warbler",
    "Bald Eagle": "eagle",
    "White Fronted Goose": "anser",
    "Long Billed Curlew": "curlew",
    Whimbrel: "whimbrel",
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
      .post(`${backendUrl}/prediction_input`, {
        bird: birdMap[inputBird],
        year: year,
        emissions: emissionRate,
      })
      .then((response) => {
        console.log(response.data.prediction);
        //setPredictionData(response.data.prediction);
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
  const [selectedMap, setSelectedMap] = useState("Polyline");
  const [predictionData, setPredictionData] = useState(null);
  const [isOpen, setIsOpen] = useState(true);
  const toggleSidebar = () => {
    setIsOpen(!isOpen);
  };

  axios.create({ withCredentials: true });
  axios.defaults.withCredentials = true;

  useEffect(() => {
    selectBird("Blackpoll Warbler");
  }, []);

  function selectBird(birdName) {
    setSelectedBird(birdName);
    fetchBirdInfo(birdName);
    fetchSDMData(birdName);
    updatePredictionVars(selectedYear, selectedEmissions, birdName);
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
    const socket = io(backendUrl, {
      transports: ["websocket"],
      cors: {
        origin: "http://localhost:3000",
      },
    });

    setSocketInstance(socket);
    socket.on("predictions", (data) => {
      setPredictionData(data.prediction);
    });
  }, [selectedBird, selectedYear, selectedEmissions]);

  return (
    <div className="App">
      <CookiesProvider>
        <div className="header">
          <button className="toggle-button" onClick={toggleSidebar}>
            <FontAwesomeIcon icon={faBars} />
          </button>
          <h1 className="header-title"> {selectedBird} </h1>
        </div>

        <div>
          {isOpen && (
            <nav className={"sidebar"}>
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
          )}
        </div>
        <main className="main-content">
          {loading && <p>Loading...</p>}
          {error && <p>Error: {error}</p>}
          {birdInfo && (
            <div className="BirdInfo">
              <BirdInfo data={birdInfo} />
            </div>
          )}
          <div className="TrajectoryContainer">
            <h2> Trajectory</h2>
            <div className="tabs">
              <button
                className="tab"
                onClick={() => setSelectedMap("Polyline")}
              >
                Show Individual Path
              </button>
              <button className="tab" onClick={() => setSelectedMap("Heatmap")}>
                Show Aggregated Path
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
          <div className="PredictionControlsContainer">
            <div className="PredictionControlsHeader">
              <h2> Prediction Controls</h2>
              <div className="PredictionControls">
                <PredictionControls
                  onPredictionUpdated={(year, emissions) => {
                    setObservedYear(year);
                    setEmissionRate(emissions);
                    updatePredictionVars(year, emissions, selectedBird);
                  }}
                />
              </div>
            </div>
            <div className="ChartsContainer">
              <div className="ClimateContainer">
                <h2> Climate </h2>
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
                {climateData && <ClimateChart data={climateData} />}
              </div>
              <div className="SDMContainer">
                <h2> Species Distribution</h2>
                <SDMChart data={sdmData} prediction={predictionData} />
              </div>
            </div>
          </div>
        </main>
      </CookiesProvider>
    </div>
  );
}

export default App;
