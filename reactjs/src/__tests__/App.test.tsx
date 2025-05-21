import '@testing-library/jest-dom';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { createMemoryRouter, RouterProvider } from 'react-router-dom';
import getRoutes from '../Routes';
import { sitedetails, get_auth_header, get_user_from_cookie, refresh_session } from '../utils/appContext';

const renderWithRoute = async (route: string) => {
  const testRouter = createMemoryRouter(
    getRoutes({
      sitedetails,
      get_auth_header,
      get_user_from_cookie,
      refresh_session,
    }), {
    initialEntries: [route],
    future: {
      v7_relativeSplatPath: true,
      v7_startTransition: true,
    },
  })
  render(
    <RouterProvider router={testRouter} />
  );
  await waitFor(() => {
    expect(screen.getByTestId('site-footer')).toBeInTheDocument();
  });
};

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
    expect(screen.getByText('Account Login')).toBeInTheDocument();
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
    expect(screen.getByText('Account Registration')).toBeInTheDocument();
  });
});