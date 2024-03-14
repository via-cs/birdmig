/** > > > IMPORTANT: < < <
 * 
 * THIS IS A DUMMIED-OUT APP.JS SOLELY FOR DEBUGGING SESSIONS.
 * THIS SHOULD NEVER REPLACE ACTUAL WORK DONE FOR THE FRONT END.
*/

import { useState, useEffect } from "react";
import axios from "axios";
import "./App.css";
import BirdInfo from "./components/BirdInfo";
import SDMChart from "./components/SDMChart";
import TimeSeries from "./components/TimeSeries";

function App() {

  const [io_result, setResult] = useState(null);
  const baseUrl = 'http://localhost:5000';
  
  function getData() {
    setLoading(true);
    setError(null);
  
    axios.get(`${baseUrl}/model-input`)
      .then(response => {
        setResult(response.msg);
      })
      .catch(error => {
        console.error("Error fetching bird data", error);
        setResult(null);
      });
  }

  return (
    <div className="App">
      <button/>
      <button/>
    </div>
  );
}

export default App;
