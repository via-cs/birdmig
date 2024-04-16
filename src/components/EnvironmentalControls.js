import React from 'react';

const EnvironmentalControls = ({ onTemperatureChange, onPrecipitationChange }) => {
  return (
    <div className="environmental-controls">
      <div className="slider-container">
        <label>Temperature:</label>
        <input
          type="range"
          min="0"
          max="100"
          onChange={e => onTemperatureChange(e.target.value)}
        />
      </div>
      <div className="slider-container">
        <label>Precipitation:</label>
        <input
          type="range"
          min="0"
          max="100"
          onChange={e => onPrecipitationChange(e.target.value)}
        />
      </div>
    </div>
  );
};

export default EnvironmentalControls;
