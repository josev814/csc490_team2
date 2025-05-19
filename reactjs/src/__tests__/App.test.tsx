import '@testing-library/jest-dom';
import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import App from '../App';

describe("App", () => {
  test('renders home page when route is /', async () => {
    render(
      <App />
    );
    const elementsWithContent = await screen.findAllByText(/Create Test Trading strategies against the market/i);
    elementsWithContent.forEach(element => {
      expect(element).toBeInTheDocument();
    });
    const loginLink = screen.getByText(/Login/i);
    expect(loginLink).toBeInTheDocument();
  });

  test('renders login page when route is /login', async () => {
    render(
      <App />
    );
    const loginLink = screen.getByText(/Login/i);
    fireEvent.click(loginLink);
    expect(screen.getByText('Account Login')).toBeInTheDocument();
    
  });

  test('renders register page when route is /register', async () => {
    render(
      <App />
    );
    const links = await screen.findAllByRole('link')
    const registerLink = links.find((link) => {
      return link.textContent.match(/Register/i)
    })
    if(!registerLink){
      throw new Error('Registration link was not found')
    }

    fireEvent.click(registerLink);
    expect(screen.getByText('Account Registration')).toBeInTheDocument();
  });
});