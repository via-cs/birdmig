// components/TimeSeries.js
function TimeSeries({ data }) {
    return (
      <div>
        <h2>Time Series Data</h2>
        <h3>Precipitation</h3>
        <ul>
          {data.precipitation.map((item, index) => (
            <li key={index}>{item}</li>
          ))}
        </ul>
        <h3>Climate</h3>
        <ul>
          {data.climate.map((item, index) => (
            <li key={index}>{item}</li>
          ))}
        </ul>
        <h3>Temperature</h3>
        <ul>
          {data.temperature.map((item, index) => (
            <li key={index}>{item}</li>
          ))}
        </ul>
      </div>
    );
  }
  
  export default TimeSeries;
  