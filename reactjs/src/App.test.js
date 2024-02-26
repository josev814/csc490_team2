import { render, screen } from '@testing-library/react';
import App from './App';

test('renders home link', () => {
  render(<App />);
  const elementsWithContent = screen.getByText(/Test trading/i);
  expect(elementsWithContent).toBeInTheDocument();
});
