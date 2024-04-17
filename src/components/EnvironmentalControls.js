// EnvironmentalControls.js

import React, { useState } from 'react';

function EnvironmentalControls(props) {
  // State hooks to keep track of the slider values
  const [temperature, setTemperature] = useState(50); // Example initial value
  const [precipitation, setPrecipitation] = useState(50); // Example initial value

  // Function to handle temperature change
  const handleTemperatureChange = (e) => {
    setTemperature(e.target.value);
    if (props.onTemperatureChange) {
      props.onTemperatureChange(e.target.value);
    }
  };

  // Function to handle precipitation change
  const handlePrecipitationChange = (e) => {
    setPrecipitation(e.target.value);
    if (props.onPrecipitationChange) {
      props.onPrecipitationChange(e.target.value);
    }
  };

  return (
    <div className="EnvironmentalControls">
      <div className="slider-container">
        <label htmlFor="temperature-slider" className="slider-label">Temperature:</label>
        <input
          id="temperature-slider"
          type="range"
          min="0"
          max="100"
          value={temperature}
          onChange={handleTemperatureChange}
        />
        <span>{temperature}°C</span>
      </div>
      <div className="slider-container">
        <label htmlFor="precipitation-slider" className="slider-label">Precipitation:</label>
        <input
          id="precipitation-slider"
          type="range"
          min="0"
          max="100"
          value={precipitation}
          onChange={handlePrecipitationChange}
        />
        <span>{precipitation}mm</span>
      </div>
    </div>
  );
}

export default EnvironmentalControls;
