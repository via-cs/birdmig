import React, { useState, useEffect } from "react";
import axios from "axios";
import "./App.css";
import { CookiesProvider, useCookies } from "react-cookie";
import { io } from "socket.io-client";
//import WebSocketCall from ""
import BirdInfo from "./components/BirdInfo";
import SDMChart from "./components/SDMChart";
import PolylineMap from "./components/PolylineMap";
import Heatmap from "./components/HeatMap";
import GeneralMigrationMap from "./components/GeneralMigrationMap";
import PredictionControls from "./components/PredictionControls";
import ClimateChart from "./components/ClimateChart";

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

	// Define updatePredictionVars
	function updatePredictionVars(year, emissionRate) {
		setObservedYear(year);
		setEmissionRate(emissionRate);

		axios
			.post(`${backendUrl}/prediction_input`, {
                    year: year,
                    emissions: emissionRate })
			.then((response) => {
                console.log(response.data.prediction)
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
	const [selectedEmissions, setEmissionRate] = useState("SSP 245");
	const [climateData, setClimateData] = useState(null);
	const [selectedClimateVariable, setSelectedClimateVariable] = useState("");
	const [showPolylineMap, setShowPolylineMap] = useState(true);
	const [predictionData, setPredictionData] = useState(null);

	axios.create({ withCredentials: true });
	axios.defaults.withCredentials = true;

	useEffect(() => {
		selectBird("Blackpoll Warbler");
	}, []);

	function selectBird(birdName) {
		setSelectedBird(birdName);
		console.log(selectedBird);
		fetchBirdInfo(birdName);
		fetchSDMData(birdName);
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
                origin: "http://localhost:3000"
            }
        });
        
        setSocketInstance(socket)
        socket.on("predictions", (data) => {
            setPredictionData(data.prediction)
        })

	}, [selectedBird, selectedYear, selectedEmissions]);

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
					{birdInfo && (
						<div className="BirdInfo">
							<BirdInfo data={birdInfo} />
							<div className="PredictionControls">
								<PredictionControls
									onPredictionUpdated={(year, emissions) => {
										updatePredictionVars(year, emissions);
									}}
								/>
							</div>
						</div>
					)}
					<div className="MigrationMap">
						<button onClick={() => setShowPolylineMap(!showPolylineMap)}>
							{showPolylineMap ? "Show General Map" : "Show Polyline Map"}
						</button>
						{showPolylineMap ? (
							<PolylineMap data={birdMap[selectedBird]} />
						) : (
							<GeneralMigrationMap selectedBird={birdMap[selectedBird]} />
						)}
					</div>
					<p>Data: {predictionData ? predictionData : "Nothing"}</p>
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
