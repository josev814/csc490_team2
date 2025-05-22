// jest-dom adds custom jest matchers for asserting on DOM nodes.
// allows you to do things like:
// expect(element).toHaveTextContent(/react/i)
// learn more: https://github.com/testing-library/jest-dom
import '@testing-library/jest-dom';
import 'whatwg-fetch';

// suppressing v7 transition messages
beforeAll(() => {
  jest.spyOn(console, 'warn').mockImplementation((msg) => {
    if (
      typeof msg === 'string' &&
      msg.includes('React Router Future Flag Warning')
    ) return;
    console.warn(msg);
  });
  // Suppress ECONNREFUSED errors (e.g., API not running during tests)
  jest.spyOn(console, 'error').mockImplementation((msg) => {
    if (
      typeof msg === 'string' &&
      (
        msg.includes('connect ECONNREFUSED') || 
        msg.includes('getaddrinfo ENOTFOUND') // this happens when the backend container isn't up yet
      )
    ) return;
    // Otherwise, show error
    console.error(msg);
  });
});