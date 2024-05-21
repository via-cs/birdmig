// components/BirdInfo.js
function BirdInfo({ data }) {
  return (
    <div>
      <h2>Summary</h2>
      <p>{data.general}</p>
      <b>Migration: </b> <p> {data.migration}</p>
    </div>
  );
}

export default BirdInfo;
