import { useState } from "react";
import axios from "axios";
//import logo from "./logo.svg";
import "./App.css";



function App() {

  const [profileData, setProfileData] = useState(null);

  // Generic, quick and dirty function to get data.
  function getData() {
    axios({
      method: "GET",
      url: "/profile",
    })
      .then((response) => {
        const res = response.data;
        setProfileData({
          profile_name: res.name,
          about_me: res.about,
          data: res.output,
          format: res.resFormat
        });
      })
      .catch((error) => {
        if (error.response) {
          console.log(error.response);
          console.log(error.response.status);
          console.log(error.response.headers);
        }
      });
  }

  // Generic, quick and dirty function for sending data.
  function sendData() {
    // VVV WTF is up with the full call to port 5000
    // Ideally, this auto-concatenates to the directory of the backend.
    axios.post('http://127.0.0.1:5000/model_input', {data: "bird_2"})
    .then(({data}) => {
      setProfileData({
        profile_name: data.name,
        about_me: data.about,
        data: data.output
      })
    })
    .catch((error) => {
      if(error.response) {
        console.log(error.response);
      }
    });
  }
  
  return (
    <div className="App">
      <header className="App-header">

        <button onClick = {sendData}>Test Posting Data</button>
        <button onClick={getData}>Test Getting Data</button>
        
        {profileData && (
          <div>
            <p>Project name: {profileData.profile_name}</p>
            <p>Message: {profileData.about_me}</p>
            <img src={`data:image/${profileData.format};base64,${profileData.data}`} alt="DEBUG images" />
          </div>
        )}
      </header>
    </div>
  );
}

export default App;