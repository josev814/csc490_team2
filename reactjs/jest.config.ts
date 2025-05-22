import type { Config } from 'jest';

const config: Config = {
  preset: 'ts-jest',
  testEnvironment: 'jest-environment-jsdom',
  transform: {
    "^.+\\.[tj]sx?$": "ts-jest" 
    // process `*.tsx` files with `ts-jest`
  },
  moduleFileExtensions: ['ts', 'tsx', 'js', 'jsx'],
  testMatch: ['**/__tests__/**/*.test.(ts|tsx)', '**/?(*.)+(spec|test).(ts|tsx)'],
  collectCoverage: true,
  testTimeout: 30000,
  setupFilesAfterEnv: ['<rootDir>/src/setupTests.ts'],
  reporters: [
    'default',
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

export default config;