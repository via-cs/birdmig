// PredictionControls.test.js

import React from "react";
import { render, fireEvent, screen } from "@testing-library/react";
import PredictionControls from "./PredictionControls";

describe("PredictionControls Component", () => {
	test("updates CO2 emission scenario and calls onPredictionUpdated", () => {
		const handlePredictionUpdated = jest.fn();
		render(<PredictionControls onPredictionUpdated={handlePredictionUpdated} />);

		const initialButton = screen.getByRole("button", { name: "ssp126" });
		fireEvent.click(initialButton);
		expect(handlePredictionUpdated).toHaveBeenCalledWith(2021, "ssp126");
	});
});
