import { useState, useEffect } from "react";
import axios from "axios";
import "./App.css";
import { CookiesProvider, useCookies } from "react-cookie";
import BirdInfo from "./components/BirdInfo";
import SDMChart from "./components/SDMChart";
import MigrationMap from "./components/MigrationMap";
import PredictionControls from "./components/PredictionControls";
import ClimateChart from "./components/ClimateChart";

function App() {
	axios.create({ withCredentials: true });
	axios.defaults.withCredentials = true;

	const [cookies, setCookie] = useCookies(["user"]);
	function onRequest() {
		setCookie("user", 1);
	}

	const backendUrl = "http://localhost:5000";
	const [selectedBird, setSelectedBird] = useState(null);
	const [birdInfo, setBirdInfo] = useState(null);
	const [sdmData, setSdmData] = useState(null);
	const [migrationMapUrl, setMigrationMapUrl] = useState("");
	const [loading, setLoading] = useState(false);
	const [error, setError] = useState(null);
	const [selectedYear, setObservedYear] = useState(2021);
	const [selectedEmissions, setEmissionRate] = useState("SSP 245");
	const [climateData, setClimateData] = useState(null);
	const [selectedClimateVariable, setSelectedClimateVariable] = useState("");

	const birdMap = {
		"Blackpoll Warbler": "blackpoll_warbler_kde_heatmap.html",
		"Bald Eagle": "eagle_kde_heatmap.html",
		"White Fronted Goose": "geese_kde_heatmap.html",
		"Long Billed Curlew": "long_billed_curlew_kde_heatmap.html",
		Whimbrel: "whimbrel_kde_heatmap.html",
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

	function updatePredictionVars(year, emissionRate) {
		setObservedYear(year);
		setEmissionRate(emissionRate);
		axios
			.post(`${backendUrl}/prediction_input`, {
				year: year,
				emissions: emissionRate,
			})
			.then(({ data }) => {})
			.catch((error) => {
				if (error.response) {
					console.log(error.response);
				}
			});
	}

	useEffect(() => {
		selectBird("Blackpoll Warbler");
	}, []);

	function selectBird(birdName) {
		setSelectedBird(birdName);
		fetchBirdInfo(birdName);
		fetchSDMData(birdName);
		updateMigrationMapUrl(birdName);
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

	function updateMigrationMapUrl(birdName) {
		// Access files directly from the public folder
		setMigrationMapUrl(
			`${process.env.PUBLIC_URL}/migration_images/${birdMap[birdName]}`
		);
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
                                    onYearChanged={(value) => {
                                        updatePredictionVars(value, selectedEmissions);
                                    }}
                                    onEmissionChanged={(value) => {
                                        updatePredictionVars(selectedYear, value);
                                    }}
                                />
                            </div>
                        </div>
                    )}
                    <div className="MigrationMap">
                        <MigrationMap url={migrationMapUrl} />
                    </div>
                    {sdmData && (
                        <div className="SDMChart">
                            <SDMChart data={sdmData} />
                        </div>
                    )}
                    <div className="ClimateDataContainer">
                        <div className="ClimateData">
                            <strong>Climate Data</strong>
                            <div className="tabs">
                                {Object.keys(climateVariables).map((variable) => (
                                    <button
                                        key={variable}
                                        className={`tab ${selectedClimateVariable === variable ? 'active' : ''}`}
                                        onClick={() => handleClimateVariableChange(variable)}
                                    >
                                        {variable.toUpperCase()}
                                    </button>
                                ))}
                            </div>
                        </div>
                        {climateData && (
                            <ClimateChart data={climateData} />
                        )}
                    </div>
                </main>
            </CookiesProvider>
        </div>
    );
}
    
export default App;