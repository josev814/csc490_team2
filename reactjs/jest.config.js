module.exports = {
  preset: 'ts-jest',
    testEnvironment: 'jest-environment-jsdom',
    transform: {
      "^.+\\.tsx?$": "ts-jest" 
    // process `*.tsx` files with `ts-jest`
  },
  reporters: [
    ['jest-slow-test-reporter', {
      numTests: 8,
      warnOnSlowerThan: 300,
      color: true
    }]
  ],
  moduleNameMapper: {
    '^highcharts$': './__mocks__/highcharts.jsx',
    '^highcharts-react-official$': './__mocks__/highcharts-react-official.jsx'
  }
};
