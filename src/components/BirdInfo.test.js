import React from 'react';
import { render, screen } from '@testing-library/react';
import BirdInfo from './BirdInfo';

describe('BirdInfo', () => {
  test('renders information about the bird', () => {
    const testData = {
      info: 'Blackpoll Warbler is a small songbird of the New World warbler family.'
    };
    
    render(<BirdInfo data={testData} />);
    
    const infoElement = screen.getByText(testData.info);
    expect(infoElement).toBeInTheDocument();
    expect(infoElement.tagName).toBe('P');  // Ensures that the information is displayed in a paragraph element
  });
});
