import { useEffect } from 'react';
import { RouterProvider } from 'react-router';
import { createBrowserRouter } from 'react-router-dom';
import { sitedetails, get_auth_header, get_user_from_cookie, refresh_session } from './utils/appContext';
import getRoutes from './Routes';


export default function App() {
  
  useEffect(() => {
    refresh_session();
  }, []);

  const router = createBrowserRouter(getRoutes({
    sitedetails,
    get_auth_header,
    get_user_from_cookie,
    refresh_session,
  }), {
    future: {
      v7_relativeSplatPath: true,
      v7_startTransition: true,
      v7_fetcherPersist: true,
      v7_normalizeFormMethod: true,
      v7_partialHydration: true,
    } as any,
  });
  
  return <RouterProvider router={router} />;
}