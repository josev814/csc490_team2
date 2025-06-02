import { screen, fireEvent, waitFor } from '@testing-library/react';
import { renderWithRoute } from './utils/testRouter';

test('base', () => {
  expect(true).toBeTruthy();
})

describe("App", () => {
  test("website initial load", async () => {
    await renderWithRoute('/');
    expect(true).toBeTruthy();
  });

  test('load home page when route is /', async () => {
    await renderWithRoute('/');
    const elementsWithContent = await screen.findAllByText(/Create Test Trading strategies against the market/i);
    elementsWithContent.forEach(element => {
      expect(element).toBeInTheDocument();
    });
    const loginLink = screen.getByText(/Login/i);
    expect(loginLink).toBeInTheDocument();
  });

  test('navigate to login page from home', async () => {
    await renderWithRoute('/');
    const loginLink = screen.getByText(/Login/i);
    fireEvent.click(loginLink);
    await waitFor(() => {
      expect(screen.getByText('Account Login')).toBeInTheDocument()
    }, { timeout: 3000 });
  });

  test('navigate to register page from home', async () => {
    await renderWithRoute('/');
    const links = await screen.findAllByRole('link')
    const registerLink = links.find((link) => {
      if (link && link.textContent){ 
        return link.textContent.match(/Register/i);
      }
    })
    if(!registerLink){
      throw new Error('Registration link was not found')
    }
    fireEvent.click(registerLink);
    await waitFor(() => {
      expect(screen.getByText('Account Registration')).toBeInTheDocument()
    }, { timeout: 3000 });
  });
});