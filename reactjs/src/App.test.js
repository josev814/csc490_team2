import { render, screen } from '@testing-library/react';
import App from './App';

test('renders home link', () => {
  render(<App />);
  const linkElement = screen.getByText(/stocks/i);
  expect(linkElement).toBeInTheDocument();
});
