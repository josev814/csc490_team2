import React, { useState, useEffect } from "react";
import LoginForm from "./auth/LoginForm";
import RegisterForm from "./auth/RegisterForm";
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import Cookies from 'universal-cookie';

const cookies = new Cookies();

export function LoginRegister({ mode }) {
  const [formData, setFormData] = useState({
    email: "",
    password: ""
  });
  const [errorMessage, setErrorMessage] = useState(""); // State to manage error message
  const navigate = useNavigate(); // Access the history object for navigation

  const base_url = 'http://localhost:8889'; // Define your base URL here

  const handleSubmit = async (e, isLoginPage) => {
    e.preventDefault();
    try {
      let url = '';
      if (isLoginPage) {
        url = `${base_url}/auth/login/`;
      } else {
        url = `${base_url}/auth/register/`;
      }
      const response = await axios.post(url, formData);
      if (response.status === 200 || response.status === 201) {
        //Store return from response of the user into user cookie / expiration = 1 day
        const userData = response.data.user;
        const cookieExpiration = new Date();
        cookieExpiration.setDate(cookieExpiration.getDate() + 1);
        cookies.set('user', userData, { expires: cookieExpiration });
        //cookie(login status) / vailid: 30 minutes
          //status(onLogin | onRegistration) = true
        const loginStatusExpiration = new Date();
        loginStatusExpiration.setTime(loginStatusExpiration.getTime() + (0.5 * 60 * 60 * 1000));
        cookies.set('is_active', userData.is_active, { expires: loginStatusExpiration });
  
        //local storage: store access token and refresh token from response
        localStorage.setItem('accessToken', response.data.token);
        localStorage.setItem('refreshToken', response.data.refresh);
  
        navigate('/rules');
      } else {
        throw new Error('Failed to register user');
      }
    } 
    catch (error) {
      if (error.response && error.response.status === 409) {
        setErrorMessage("User already exists");
      } else {
        setErrorMessage("Invalid Credentials, Try again");
      }
    }
    
  };

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  return (
    <div className="container-fluid d-flex justify-content-center vh-100 align-items-center">
      <div className="col-12 col-md-4">
        {mode === "signin" ? (
          <LoginForm
            formData={formData}
            handleChange={handleChange}
            handleSubmit={(e) => handleSubmit(e, true)}
            errorMessage={errorMessage}
          />
        ) : (
          <RegisterForm
            formData={formData}
            handleChange={handleChange}
            handleSubmit={(e) => handleSubmit(e, false)}
            errorMessage={errorMessage}
          />
        )}
      </div>
    </div>
  );
}

export function Logout(){
  const navigate = useNavigate()

  useEffect(() => {
    const cookieNames = ['is_active', 'user']

    cookieNames.forEach(cookieName => {
      cookies.remove(cookieName)
      //console.log(cookies.remove({cookieName}))
    });
    // removes access and refresh tokens
    localStorage.clear()
    navigate('/login');
  }, [navigate])

  return null
}
