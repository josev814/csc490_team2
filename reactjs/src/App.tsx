import { useEffect } from 'react';
import { RouterProvider, createBrowserRouter } from 'react-router-dom';
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
    },
  });
  
  return <RouterProvider router={router} />;
}