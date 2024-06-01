// components/BirdInfo.js
function BirdInfo({ data }) {
  return (
    <div>
      <h2> Scientific Name: {data.scientific_name} </h2>
      <b>Summary</b>
      <p>{data.general}</p>
      <b>Migration: </b> <p> {data.migration}</p>
    </div>
  );
}

export default BirdInfo;
