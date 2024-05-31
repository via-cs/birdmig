# Data format:
- ```info```: string
- ```sdmData```: x-y coordinate pair.
- ```timeSeriesData```: array of time-series values for climate variables
  - ```precipiation```
  - ```climate```
  - ```temperature```

# Running Tests:
Write all tests for the backend in the ```tests``` directory.

With pytest installed, you can run tests from the command line with the following command:

```pytest tests/```

And if you want to include coverage reports:
```pytest --cov=app/```

