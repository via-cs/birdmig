// components/SDMChart.js
function SDMChart({ data }) {
    return (
      <div>
        <h2>SDM Data</h2>
        <ul>
          {data.map((item, index) => (
            <li key={index}>{`x: ${item.x}, y: ${item.y}`}</li>
          ))}
        </ul>
      </div>
    );
  }
  
  export default SDMChart;
  