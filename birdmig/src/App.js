import { useState } from 'react'
import axios from "axios";
import logo from './logo.svg';
import './App.css';

function App() {

  const [profileData, setProfileData] = useState(null)

  function getData() {
    axios({
      method: "GET",
      url:"/profile",
    })
    .then((response) => {
      const res =response.data
      setProfileData(({
        profile_name: res.name,
        about_me: res.about}))
    }).catch((error) => {
      if (error.response) {
        console.log(error.response)
        console.log(error.response.status)
        console.log(error.response.headers)
        }
    })}

  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />

        <button onClick={getData}>Click me</button>
        {profileData && <div>
              <p>Project name: {profileData.profile_name}</p>
              <p>Message: {profileData.about_me}</p>
            </div>
        }
      </header>
    </div>
  );
}

export default App;