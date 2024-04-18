module.exports = {
    setupFilesAfterEnv: ['@testing-library/jest-dom'],
    testMatch: ['<rootDir>/src/**/?(*.)test.{js,jsx}'],
    coverageDirectory: '<rootDir>/coverage',
    collectCoverageFrom: [
      'src/**/*.{js,jsx}',
      '!src/index.js',
      '!src/reportWebVitals.js',
      '!src/setupTests.js',
    ],
  };
  