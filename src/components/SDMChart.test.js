import React from 'react';
import { render, screen } from '@testing-library/react';
import SDMChart from './SDMChart';

describe('SDMChart Component', () => {
  test('does not render an image if no prediction is provided', () => {
    render(<SDMChart data={[]} />);
    const imgElement = screen.queryByRole('img');
    expect(imgElement).not.toBeInTheDocument();
  });

  test('renders an image with the correct src if a prediction is provided', () => {
    const base64String = 'iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w38GIAXDIBKE0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg==';
    render(<SDMChart data={[]} prediction={base64String} />);
    const imgElement = screen.getByRole('img');
    expect(imgElement).toBeInTheDocument();
    expect(imgElement).toHaveAttribute('src', `data:image/png;base64, ${base64String}`);
  });
});
