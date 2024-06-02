import React, { useState, useEffect } from "react";
import axios from "axios";
import "./App.css";
import { CookiesProvider, useCookies } from "react-cookie";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faBars, faInfo } from "@fortawesome/free-solid-svg-icons";
//import WebSocketCall from ""
import BirdInfo from "./components/BirdInfo";
import SDMChart from "./components/SDMChart";
import PolylineMap from "./components/PolylineMap";
import Heatmap from "./components/HeatMap";
import PredictionControls from "./components/PredictionControls";
import ClimateChart from "./components/ClimateChart";
import Popup from "reactjs-popup";

function App() {
  const backendUrl = "http://localhost:8000";

  // Define birdMap and climateVariables
  const birdMap = {
    "Blackpoll Warbler": "warbler",
    "Bald Eagle": "eagle",
    "White Fronted Goose": "anser",
    "Long Billed Curlew": "curlew",
    Whimbrel: "whimbrel",
  };

  const climateVariables = ["temperature", "precipitation"];

  const images = require.context("./images", true);
  const imageList = images.keys().map((image) => images(image));
  const orderedImageList = Object.keys(birdMap).map((bird) => {
    const index = Object.keys(birdMap).indexOf(bird);
    return imageList.find((image) => image.includes(`/${bird}.`));
  });

  function updatePredictionVars(year, emissionRate, inputBird) {
    axios
      .put(
        `${backendUrl}/prediction`,
        {
          bird: birdMap[inputBird],
          year: year,
          emissions: emissionRate,
        },
        {
          headers: {
            "Content-Type": "application/json",
          },
        }
      )
      .then((response) => {
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
  const [selectedMap, setSelectedMap] = useState("Polyline");
  const [predictionData, setPredictionData] = useState(null);
  const [isOpen, setIsOpen] = useState(true);
  const [showChart, setShowChart] = useState(true);

  const toggleSidebar = () => {
    setIsOpen(!isOpen);
  };
  const toggleEmissionsChart = () => {
    setShowChart(!showChart);
  };

  axios.create({ withCredentials: true });
  axios.defaults.withCredentials = true;

  useEffect(() => {
    selectBird("Blackpoll Warbler");
  }, []);

  function selectBird(birdName) {
    setSelectedBird(birdName);
    fetchBirdInfo(birdName);
    //fetchSDMData(birdName);
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

  useEffect(() => {}, [selectedBird, selectedYear, selectedEmissions]);

  return (
    <div className="App">
      <CookiesProvider>
        <div className="header">
          <button className="toggle-button" onClick={toggleSidebar}>
            <FontAwesomeIcon icon={faBars} />
          </button>
          <h1 className="header-title"> {selectedBird} </h1>
        </div>

        <div className="sidebardiv">
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
            <div className="TrajectoryHeader">
              <h2> Trajectory</h2>
              <div className="tabs">
                <button
                  className="tab"
                  onClick={() => setSelectedMap("Polyline")}
                  style={{
                    backgroundColor:
                      selectedMap === "Polyline" ? "#2574a8" : "#3498db",
                  }}
                >
                  Show Individual Path
                </button>
                <button
                  className="tab"
                  onClick={() => setSelectedMap("Heatmap")}
                  style={{
                    backgroundColor:
                      selectedMap === "Heatmap" ? "#2574a8" : "#3498db",
                  }}
                >
                  Show Aggregated Path
                </button>
              </div>
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
            <div className="PredictionControlsBody">
              <div className="SDMContainer">
                <h2>
                  {" "}
                  Species Distribution
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
                        <p>
                          <strong>Dark green</strong> indicates a high
                          probability that an individual bird will be there.
                          <br />
                          <strong>Lighter shades</strong> indicate less
                          probability.
                        </p>
                      </div>
                    )}
                  </Popup>
                </h2>
                <SDMChart prediction={predictionData} />
              </div>
              <div className="ChartsContainer">
                <div className="ClimateDataContainer">
                  <ClimateChart selectedYear={selectedYear} />
                </div>
                <div className="emissionsChart">
                  <div className="emissionsChart-iframe">
                    <iframe
                      src="https://cbhighcharts2019.s3.eu-west-2.amazonaws.com/CMIP6/emissions+cmip6.html"
                      width="100%"
                      height="400px"
                      title="Emissions Chart"
                    ></iframe>
                    <span className="emissionsChart-logoContainer">
                      <a href="https://www.carbonbrief.org">
                        <img
                          src="https://s3.eu-west-2.amazonaws.com/cbhighcharts2019/cb-logo-highcharts.svg"
                          className="emissionsChart-logo"
                          alt="Carbon Brief Logo"
                        />
                      </a>
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </main>
      </CookiesProvider>
    </div>
  );
}

export default App;
