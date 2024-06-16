import React from 'react';
import { render, screen } from '@testing-library/react';
import SDMChart from './SDMChart';

describe('SDMChart Component', () => {
  test('does not render an image if no prediction is provided', () => {
    render(<SDMChart />);
    const imgElements = screen.queryAllByRole('img');
    expect(imgElements.length).toBe(0); // No images should be present
  });

  test('renders an image with the correct src if a prediction is provided', () => {
    const base64String = 'iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w38GIAXDIBKE0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg==';
    render(<SDMChart prediction={base64String} />);
    const imgElements = screen.getAllByRole('img'); // Get all images
    expect(imgElements.length).toBe(2);
    expect(imgElements[0]).toHaveAttribute('src', `data:image/png;base64, ${base64String}`); // Check the src of the first image
    expect(imgElements[1]).toHaveAttribute('src', expect.stringContaining("legend.png")); // Check the src of the legend image
  });
});
