// PredictionControls.test.js

import React from 'react';
import { render, fireEvent, screen } from '@testing-library/react';
import PredictionControls from './PredictionControls';

describe('PredictionControls Component', () => {
  test('updates year through slider and calls onPredictionUpdated', () => {
    const handlePredictionUpdated = jest.fn();
    render(<PredictionControls onPredictionUpdated={handlePredictionUpdated} />);
    
    const slider = screen.getByLabelText(/year/i);
    fireEvent.change(slider, { target: { value: 2050 } });
    expect(slider.value).toBe('2050');
    expect(handlePredictionUpdated).toHaveBeenCalledWith('2050', 'SSP 245');
  });

  test('updates CO2 emission scenario and calls onPredictionUpdated', () => {
    const handlePredictionUpdated = jest.fn();
    render(<PredictionControls onPredictionUpdated={handlePredictionUpdated} />);
    
    const initialButton = screen.getByRole('button', { name: 'ssp126' });
    fireEvent.click(initialButton);
    expect(handlePredictionUpdated).toHaveBeenCalledWith(2021, 'ssp126');
  });
});

