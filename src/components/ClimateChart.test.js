import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import ClimateChart from './ClimateChart';

describe('ClimateChart Component', () => {
  test('switches tabs when buttons are clicked', () => {
    render(<ClimateChart selectedYear={2022} />);
    fireEvent.click(screen.getByRole('button', { name: /Precipitation/i }));
    expect(screen.getByText(/Monthly Average Precipitation in CA for year 2022/i)).toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: /Temperature/i }));
    expect(screen.getByText(/Monthly Average Temperature in CA for year 2022/i)).toBeInTheDocument();
  });
});
