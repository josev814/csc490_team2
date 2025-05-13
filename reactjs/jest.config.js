module.exports = {
    transform: {
      '^.+\\.js$': 'babel-jest',
    },
    reporters: [
      ['jest-slow-test-reporter', {"numTests": 8, "warnOnSlowerThan": 300, "color": true}]
    ],
    "moduleNameMapper": {
      "^highcharts$": "./__mocks__/highcharts.js",
      "^highcharts-react-official$": "./__mocks__/highcharts-react-official.js"
    }
  };
  