// components/BirdInfo.js
function BirdInfo({ data }) {
    return (
      <div>
        <h2>Bird Information</h2>
        <p>{data.info}</p>
      </div>
    );
  }
  
  export default BirdInfo;
  