import { useState } from "react";
import axios from "axios";
import logo from "./logo.svg";
import "./App.css";

// DEBUG content
import distribution from "./DEBUG_dist.png";

function App() {

  const [profileData, setProfileData] = useState(null);

  // Read data from flask
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
          distribData: distribution
        });
      })
      .catch((error) => {
        if (error.response) {
          console.log(error.response);
          console.log(error.response.status);
          console.log(error.response.headers);
        }
        
        setProfileData({
            profile_name: "NULL Name",
            about_me: "Check to make sure the backend is working.",
            distribData: distribution
          });
      }
    );
  }

  // Export the main user interface for the application.
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <button onClick={getData}>Click me</button>
        {profileData && (
          <div>
            <p>Project name: {profileData.profile_name}</p>
            <p>Message: {profileData.about_me}</p>
            <img src={profileData.distribData} className="Distribution Data" alt="distribution" />
          </div>
        )}
      </header>
    </div>
  );
}

export default App;