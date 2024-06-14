import React from "react";
import legend from "../assets/legend.png";
function SDMChart({ prediction }) {
  console.log(prediction);
  return (
    <div>
      {prediction && (
        <div className="SDM">
          <img
            className="SDMChart"
            src={
              prediction
                ? `data:image/png;base64, ${prediction}`
                : "publiclogo192.png"
            }
            alt="Species Distribution Model"
          />
          <img className="legend" src={legend} alt="Legend" />
        </div>
      )}
    </div>
  );
}

export default SDMChart;
