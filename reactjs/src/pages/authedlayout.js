import { Outlet, useNavigate } from "react-router-dom";
import { useEffect, useState, useMemo } from "react";
import axios from 'axios';
import Header from './blocks/header';
import Footer from './blocks/footer';
import LeftNav from './blocks/leftnav';
import Cookies from 'universal-cookie';


export default function AuthedLayout(props) {
    const cookies = useMemo(() => new Cookies(null, { path: '/' }), []);
    const navigate = useNavigate();

    const [userData, setUserData] = useState(undefined);
    useEffect(() => {
      function stillLoggedIn(){
        const active = cookies.get('is_active');
        if (!active) {
          console.log('Redirect to login');
          navigate('/login/');
        }
      }
  
      function getUserCookieData() {
          const user = cookies.get('user');
          setUserData(user);
          if (!user) {
              console.log('Redirect to login');
              navigate('/login/');
          }
      }
      getUserCookieData();
      stillLoggedIn();
      const interval = setInterval(() => {
        stillLoggedIn(); // Call every 5 minutes
      }, 5 * 60 * 1000); // 5 minutes in milliseconds

      return () => clearInterval(interval); // Cleanup function to clear interval
    }, [navigate, cookies]);

    function get_auth_header(){
      const token = localStorage.getItem('accessToken')
      const headers = {
          Authorization: `Bearer ${token}`,
      }
      return headers
  }

  function refresh_login_cookie() {
      // Calculate expiration time for the login status cookie (30 minutes)
      const loginStatusExpiration = new Date();
      loginStatusExpiration.setTime(loginStatusExpiration.getTime() + (0.5 * 60 * 60 * 1000));
      
      // Check if 'is_active' cookie exists
      const is_active = cookies.get('is_active');
      if (is_active) {
          // Log the current value of 'is_active' (optional for debugging)
          console.log("Current 'is_active' value:", is_active);
          
          // Update the expiration time of the 'is_active' cookie
          cookies.set('is_active', is_active, { expires: loginStatusExpiration });
      } else {
          console.error("User is not logged in.");
          navigate('/login')
      }
  }    

  async function refresh_token() {
      try {
          const refresh_url = `${props.django_url}/auth/refresh/`;
          const data = {'refresh': localStorage.getItem('refreshToken')};
          
          // Send POST request to refresh URL
          const response = await axios.post(refresh_url, data, { headers: get_auth_header() });
  
          // Check if response is successful
          if (response.status === 200) {
              // Update tokens in local storage
              localStorage.setItem('accessToken', response.data.access);
              localStorage.setItem('refreshToken', response.data.refresh);
              
              // Refresh login cookie
              refresh_login_cookie();
          } else {
              // Handle unexpected response status codes
              console.error('Unexpected response status:', response.status);
          }
      } catch (error) {
          // Handle network errors or other exceptions
          console.error('Error refreshing token:', error);
          // Optionally, navigate to login page or handle the error
      }
  }
  

  function get_user_from_cookie(){
      const userCookie = cookies.get('user');
      if (!userCookie || !userCookie.id) {
          console.error("User cookie or user ID not found.");
          return null; // or handle the error appropriately
      }
  
      // Construct user URL based on user ID
      const user_id = userCookie.id;
      const user_url = `${props.django_url}/users/${user_id}/`;
      return user_url;
  }
    
    return (
      <>
        <Header sitename={props.sitename} tagline={props.tagline} />
      <div id='toastContainer' className="position-fixed bottom-0 end-0 p-3" style={{ zIndex: 9999 }}>
      </div>
        <div className='container-fluid'>
            <div className='row'>
                <LeftNav />
                <main role='main' className='col-md-9 ml-sm-auto col-lg-10 pt-3 px-4'>
                    <div className="justify-content-end d-flex container-fluid">
               
                        User:
                        <a className="ps-1" href={userData ? '/users/' + userData.id + '/' : '#'}>
                            {userData ? userData.email : ''}
                        </a>
                    </div>
                    <Outlet 
                      get_auth_header = {get_auth_header}
                      refresh_token = {refresh_token}
                      get_user_from_cookie = {get_user_from_cookie}
                      django_url = {props.django_url}
                    />
                </main>
                <Footer sitename={props.sitename} />
            </div>
        </div>
      </>
    );
}
