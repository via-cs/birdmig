// components/MigrationMap.js

import React from 'react';

const MigrationMap = ({ url }) => {
  return (
    <div className="migration-map">
      <h2>Migration Map</h2>
      {/* Using an iframe to embed your HTML heatmap */}
      <iframe src={url} title="Migration Map" style={{ width: '100%', height: '400px' }} />
    </div>
  );
};

export default MigrationMap;
