import React, { useEffect, useRef } from "react";
import * as d3 from "d3";

// Inside the SDMChart component
function SDMChart({ data, prediction }) {
  return (
    <div>
      {prediction && (
        <div>
          <img
            className="SDMChart"
            src={
              prediction
                ? `data:image/png;base64, ${prediction}`
                : "publiclogo192.png"
            }
          />
        </div>
      )}
    </div>
  );
}

export default SDMChart;
