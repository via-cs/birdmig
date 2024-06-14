import React from 'react';
import { render, screen } from '@testing-library/react';
import BirdInfo from './BirdInfo';

describe('BirdInfo Component', () => {
  it('renders Scientific Name heading', () => {
    const mockData = { scientific_name: 'Test Bird' };
    render(<BirdInfo data={mockData} />);
    
    const headingElement = screen.getByRole('heading', { name: /Scientific Name:/ });
    expect(headingElement).toBeInTheDocument();
  });

  it('renders the general information passed to it', () => {
    const mockData = { general: 'This is a test bird' };
    render(<BirdInfo data={mockData} />);
    
    const infoParagraph = screen.getByText('This is a test bird');
    expect(infoParagraph).toBeInTheDocument();
  });

  it('renders the migration information passed to it', () => {
    const mockData = { migration: 'Migrates North in Spring' };
    render(<BirdInfo data={mockData} />);
    
    const migrationParagraph = screen.getByText('Migrates North in Spring');
    expect(migrationParagraph).toBeInTheDocument();
  });
});
