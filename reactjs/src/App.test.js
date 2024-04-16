import { render, screen } from '@testing-library/react';
import App from './App';

test('renders home link', async () => {
  render(<App />);
  const elementsWithContent = await screen.findAllByText(/Test Trading/i);
  elementsWithContent.forEach(element => {
    expect(element).toBeInTheDocument();
  });
  const loginLink = screen.getByText(/Login/i);
  expect(loginLink).toBeInTheDocument();
});
