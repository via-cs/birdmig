import { useState, useEffect } from "react";
import axios from "axios";
import logo from "./logo.svg";
import "./App.css";



function App() {

  const [profileData, setProfileData] = useState(null);

  function sendData() {
    // VVV WTF is up with the full call to port 5000
    // Ideally, this auto-concatenates to the directory of the backend.
    axios.post('http://127.0.0.1:5000/choose_bird', {data: "TEST_POST"})
    .then(({data}) => {
      setProfileData({
        profile_name: data.name,
        about_me: data.about,
        distribData: data.output
      })
    })
    .catch((error) => {
      if(error.response) {
        console.log(error.response);
      }
    });
  }

  useEffect(() => {
    axios({
      method: "GET",
      url: "/profile",
    })
      .then((response) => {
        const res = response.data;
        setProfileData({
          profile_name: res.name,
          about_me: res.about,
          distribData: res.output
        });
      })
      .catch((error) => {
        if (error.response) {
          console.log(error.response);
          console.log(error.response.status);
          console.log(error.response.headers);
        }
      });
  }, []);

  
  return (
    <div className="App">
      <header className="App-header">

        {profileData && (
        <div>
          <p>Project name: {profileData.profile_name}</p>
          <p>Message: {profileData.about_me}</p>
          <p>Data: {profileData.distribData}</p>
        </div>
        )}

        <button onClick = {sendData}>TEST Post</button>
      </header>
    </div>
  );
}

export default App;

/*<p>Project name: {profileData.profile_name}</p>
        <p>Message: {profileData.about_me}</p>
        <p>Data: {profileData.distribData}</p> */