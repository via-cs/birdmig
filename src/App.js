import { useState, useEffect } from "react";
import axios from "axios";
import "./App.css";
import { CookiesProvider, useCookies } from "react-cookie"

function App() {

  axios.create({withCredentials:true});
  // override axios defaults to enable credentials for flask sessions.
  axios.defaults.withCredentials  = true

  // Allow the app to use cookies, for utility with backend request memory.
  const [cookies, setCookie] = useCookies(['user'])

  // Set cookies on request. TODO: find more graceful solution to set cookies.
  function onRequest() {
    setCookie('user', 1)
  }

  const [io_result, setResult] = useState(null);
  const baseUrl = 'http://localhost:5000';

  useEffect(() => {
    setResult("Test");
  }, []);

  // Generic, quick and dirty function for getting data.
  function getData() {
    axios.get(`${baseUrl}/model-output`)
      .then(response => {
        setResult(response.msg);
      })
      .catch(error => {
        console.error("Error fetching bird data", error);
        setResult(null);
      });
  }

  // Generic, quick and dirty function for sending data.
  function sendData(birdName) {
    axios.post(`${baseUrl}/model-input/${birdName}`, birdName)
    .then(({data}) => {
      setResult(data.msg)
    })
    .catch((error) => {
      if(error.response) {
        console.log(error.response);
      }
    });
  }
  
  return (
    <div className="App">
      <CookiesProvider>
        <button onClick={()=>getData()}>GET Data</button>
        <button onClick={()=>sendData('Bird 1')}>SEND Bird 1</button>
        <button onClick={()=>sendData('Bird 2')}>SEND Bird 2</button>

        { io_result ? (
          <p>Response: {io_result.msg}</p>
        ) : (
          <p>Try to select a bird!</p>
        )}
      </CookiesProvider>
    </div>
  );
}

export default App;
