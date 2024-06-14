import React from "react";
import { render, fireEvent, screen } from "@testing-library/react";
import PredictionControls from "./PredictionControls";

describe("PredictionControls Component", () => {
	test("updates CO2 emission scenario and calls onPredictionUpdated", async () => {
		const handlePredictionUpdated = jest.fn();
		render(<PredictionControls onPredictionUpdated={handlePredictionUpdated} />);

		// Use the correct name as displayed in the UI
		const initialButton = screen.getByRole("button", { name: "SSP1-2.6" });
		fireEvent.click(initialButton);
		expect(handlePredictionUpdated).toHaveBeenCalledWith(2021, "ssp126");
	});
});
