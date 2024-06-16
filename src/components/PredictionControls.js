import React, { useState } from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faInfo } from "@fortawesome/free-solid-svg-icons";
import Popup from "reactjs-popup";

function PredictionControls(props) {
  const [year, setYear] = useState(2021); //2021 by default
  const [co2, setEmission] = useState("ssp245"); // SSP 245 by default.

  const CO2_Futures = ["ssp126", "ssp245", "ssp370", "ssp585"];
  const CO2_Display = {
    ssp126: "SSP1-2.6",
    ssp245: "SSP2-4.5",
    ssp370: "SSP3-7.0",
    ssp585: "SSP5-8.5",
  };
  function handleYearChange() {
    if (year >= 2021 && year <= 2100 && props.onPredictionUpdated) {
      props.onPredictionUpdated(year, co2);
    }
  }

  function handleCO2Change(emission_type) {
    setEmission(emission_type);
    if (props.onPredictionUpdated) {
      props.onPredictionUpdated(year, emission_type);
    }
  }

  return (
    <div className="PredictionControls">
      <div className="slider-container">
        <label htmlFor="time-slider" className="slider-label">
          Year:
        </label>
        <input
          id="year_input"
          type="number"
          value={year}
          placeholder="Enter a year between 2021 and 2100"
          min={2021}
          max={2100}
          maxLength={4}
          minLength={4}
          onKeyDown={(event) => {
            if (event.key === "Enter") {
              handleYearChange();
            }
          }}
          onChange={(e) => {
            setYear(e.target.value);
          }}
          className="year_input"
        />
        <input
          id="time-slider"
          type="range"
          min="2021"
          max="2100"
          value={year}
          onChange={(e) => {
            setYear(e.target.value);
          }}
          onMouseUp={(e) => {
            handleYearChange();
          }}
        />
      </div>
      <ul>
        {CO2_Futures.map((emission_type) => (
          <button
            disabled={co2 === emission_type}
            onClick={() => handleCO2Change(emission_type)}
            style={
              emission_type === co2
                ? { backgroundColor: "#2574a8" }
                : { backgroundColor: "#3498db" }
            }
          >
            {CO2_Display[emission_type]}
          </button>
        ))}
      </ul>
      <Popup
        trigger={
          <button className="ButtonInfo">
            <FontAwesomeIcon icon={faInfo} />
          </button>
        }
        modal
        nested
      >
        {(close) => (
          <div className="PredictionControlModal">
            <button className="ButtonExit" onClick={() => close()}>
              X
            </button>
            <p>
              Shared Socioeconomic Pathways (SSPs) are climate change scenarios
              of projected socioeconomic global changes up to 2100. They are
              used to derive greenhouse gas emissions scenarios with different
              climate policies. There are 4 types of SSPs:
            </p>
            <ul>
              <li>
                <strong>SSP1:</strong> Sustainability ("Taking the Green Road")
                shows increased sustainability and reduced emissions.
              </li>
              <li>
                <strong>SSP2:</strong> "Middle of the Road" shows the continued
                path we are currently heading.
              </li>
              <li>
                <strong>SSP3:</strong> Regional Rivalry ("A Rocky Road")
                prioritizes national security and competition in the
                international market.
              </li>
              <li>
                <strong>SSP5:</strong> Fossil-fueled Development ("Taking the
                Highway") increases fossil fuel consumption and promotes free
                market policies.
              </li>
            </ul>
            <p>
              The first number on our buttons indicates what type of SSP is
              being shown. The second two numbers indicate the degree of climate
              change created by man-made greenhouse gas effects. The last two
              numbers show the intensity of the additional radiative forcing by
              the year 2100 in units of tenths of watts. For example, SSP126 is
              a scenario with 2.6 W/m² by the year 2100, which is a remake of
              the optimistic scenario RCP2.6 and was designed to simulate a
              development that is compatible with the 2°C target. This scenario
              assumes climate protection measures are being taken.
            </p>
          </div>
        )}
      </Popup>
    </div>
  );
}

export default PredictionControls;
