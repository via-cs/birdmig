import { render, fireEvent, screen } from '@testing-library/react';
import '@testing-library/jest-dom'; // Ensure this is imported
import EnvironmentalControls from './EnvironmentalControls';

describe('EnvironmentalControls', () => {
  test('renders temperature and precipitation sliders', () => {
    render(<EnvironmentalControls />);
    expect(screen.getByLabelText('Temperature:')).toBeInTheDocument();
    expect(screen.getByLabelText('Precipitation:')).toBeInTheDocument();
  });

  test('allows user to change temperature and precipitation', () => {
    const handleTemperatureChange = jest.fn();
    const handlePrecipitationChange = jest.fn();

    render(
      <EnvironmentalControls
        onTemperatureChange={handleTemperatureChange}
        onPrecipitationChange={handlePrecipitationChange}
      />
    );

    // Correct expectation to string for both temperature and precipitation
    fireEvent.change(screen.getByLabelText('Temperature:'), { target: { value: '70' } });
    expect(handleTemperatureChange).toHaveBeenCalledWith('70');
    expect(screen.getByLabelText('Temperature:')).toHaveValue('70');

    fireEvent.change(screen.getByLabelText('Precipitation:'), { target: { value: '30' } });
    expect(handlePrecipitationChange).toHaveBeenCalledWith('30');
    expect(screen.getByLabelText('Precipitation:')).toHaveValue('30');
  });
});
