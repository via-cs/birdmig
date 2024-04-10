// components/BirdInfo.test.js
import React from 'react';
import { render, screen } from '@testing-library/react';
import BirdInfo from './BirdInfo';

describe('BirdInfo Component', () => {
  it('renders Bird Information heading', () => {
    const mockData = { info: 'This is a test bird' };
    render(<BirdInfo data={mockData} />);
    
    const headingElement = screen.getByRole('heading', { name: 'Bird Information' });
    expect(headingElement).toBeInTheDocument();
  });

  it('renders the information passed to it', () => {
    const mockData = { info: 'This is a test bird' };
    render(<BirdInfo data={mockData} />);
    
    const infoParagraph = screen.getByText('This is a test bird');
    expect(infoParagraph).toBeInTheDocument();
  });
});
