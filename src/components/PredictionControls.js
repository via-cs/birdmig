// PredictionControls.js

import React, { useState } from 'react';

function PredictionControls(props) {
  const [year, setYear] = useState(2021) //2021 by default
  const [co2, setEmission] = useState('ssp245') // SSP 245 by default.

  // TODO: perhaps rename these to something more meaningful for a general audience?
  const CO2_Futures = [
    'ssp126',
    'ssp245',
    'ssp370',
    'ssp585'
  ]

  const handleYearChange = (e) => {
    setYear(e.target.value);
    if (props.onPredictionUpdated) {
      props.onPredictionUpdated(e.target.value, co2);
    }
  }

  function handleCO2Change (emission_type) {
    setEmission(emission_type);
    if(props.onPredictionUpdated) {
      props.onPredictionUpdated(year, emission_type);
    }
  }

  return (
    <div className="PredictionControls">
      <div className="slider-container">
        <label htmlFor="time-slider" className="slider-label">Year: {year}</label>
        <input
          id="time-slider"
          type="range"
          min="2021"
          max="2100"
          value={year}
          onChange={handleYearChange}
        />
      </div>
      <ul>
        {CO2_Futures.map((emission_type) => (
            <button
              disabled = {co2 === emission_type}
              onClick={()=>handleCO2Change(emission_type)}>
              {emission_type}
            </button>
        ))}
      </ul>
    </div>

  );
}

export default PredictionControls;