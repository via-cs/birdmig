import React, { useEffect, useRef } from 'react';
import * as d3 from 'd3';

// Inside the SDMChart component
function SDMChart({ data, prediction }) {
    return (
        <div>
            {prediction && (
                <div>
                    <h3>Prediction:</h3>
                    <p>{prediction}</p>
                </div>
            )}
        </div>
    );
}

export default SDMChart;
