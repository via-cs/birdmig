import React from "react";
import { render, waitFor, screen } from "@testing-library/react";
import { act } from 'react-dom/test-utils'; 
import axios from "axios";
import GeneralMigrationMap from "./GeneralMigrationMap"; 

// Mock axios
jest.mock('axios');

describe('GeneralMigrationMap', () => {
  it('should display loading initially', () => {
    axios.get.mockResolvedValueOnce({ data: { segmented_polylines: [] } });
    render(<GeneralMigrationMap selectedBird="Eagle" />);
    expect(screen.getByText('Loading...')).toBeInTheDocument();
  });

  it('should display an error message if the API call fails', async () => {
    axios.get.mockRejectedValueOnce(new Error('Failed to fetch'));

    render(<GeneralMigrationMap selectedBird="Eagle" />);
    await waitFor(() => expect(screen.queryByText('Loading...')).toBeNull());
    expect(screen.getByText(/An error occurred while fetching migration patterns:/)).toBeInTheDocument();
  });
});
