import React from 'react';
import { render, screen } from '@testing-library/react';
import MigrationMap from './MigrationMap';

describe('MigrationMap', () => {
  test('renders MigrationMap component with given URL', () => {
    const testUrl = 'https://example.com/migration-map';
    render(<MigrationMap url={testUrl} />);
    
    const migrationMapElement = screen.getByTitle('Migration Map');
    expect(migrationMapElement).toBeInTheDocument();
    expect(migrationMapElement).toHaveAttribute('src', testUrl);
    expect(migrationMapElement).toHaveStyle({ width: '100%', height: '400px' });
  });
});
