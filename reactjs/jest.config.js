module.exports = {
    transform: {
      '^.+\\.js$': 'babel-jest',
    },
    reporters: [
      ['jest-slow-test-reporter', {"numTests": 8, "warnOnSlowerThan": 300, "color": true}]
    ]
  };
  