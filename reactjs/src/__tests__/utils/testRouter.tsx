import { render, screen, waitFor } from '@testing-library/react';
import { RouterProvider } from 'react-router';
import { createMemoryRouter } from 'react-router-dom';
import getRoutes from '../../Routes';
import { sitedetails, get_auth_header, get_user_from_cookie, refresh_session } from '../../utils/appContext';

sitedetails.django_url = 'http://backend:80';

export const createTestRouter = (route: string) =>
    createMemoryRouter(
        getRoutes({
        sitedetails,
        get_auth_header,
        get_user_from_cookie,
        refresh_session,
        }),
        {
            initialEntries: [route],
            future: {
                v7_relativeSplatPath: true,
            }
        }
    );

export const renderWithRoute = async (route: string) => {
  const testRouter = createTestRouter(route);
  render(
    <RouterProvider router={testRouter} />
  );
  await waitFor(() => {
    expect(screen.getByTestId('site-footer')).toBeInTheDocument();
  }, { timeout: 5000 });

  return testRouter;
};