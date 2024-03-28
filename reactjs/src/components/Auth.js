import React, { useState } from "react";
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

export default function LoginRegister(props) {
  const [authMode, setAuthMode] = useState("signin");
  const [formData, setFormData] = useState({
    email: "",
    password: ""
  });
  const [errorMessage, setErrorMessage] = useState(""); // State to manage error message
  const navigate = useNavigate(); // Access the history object for navigation

  const base_url = 'http://localhost:8889'; // Define your base URL here

  const changeAuthMode = () => {
    setAuthMode(authMode === "signin" ? "signup" : "signin");
    // Clear the error message when switching authentication mode
    setErrorMessage("");
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      let url = '';
      if (authMode === 'signin') {
        url = `${base_url}/users/login_user/`;
      } else {
        url = `${base_url}/auth/register/`;
      }
      const response = await axios.post(url, formData);
      if (response.status === 200 || response.status === 201) {
        // Handle successful authentication or registration
        document.cookie = `user=${formData.email}`; // Save user email as a cookie
        navigate('/rules'); // Redirect to dashboard or any other desired route
      } 
    } 
    catch {
      setErrorMessage("Please use valid login.");
    }
  };

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  return (
    <div className="container-fluid d-flex justify-content-center vh-100 align-items-center">
      <div className="col-12 col-md-3">
        <form className="form shadow" onSubmit={handleSubmit}>
          <div className="card px-5 py-2 rounded border-2 border-light">
            <div className="card-body">
              <h3 className="card-title text-center">{authMode === 'signin' ? 'Account Login' : 'Account Registration'}</h3>
              <div className="card-text text-center">
                {authMode === 'signin' ? (
                  <p>Not registered yet? <span className="link-primary" onClick={changeAuthMode}>Register</span></p>
                ) : (
                  <p>Already registered? <span className="link-primary" onClick={changeAuthMode}>Log In</span></p>
                )}
              </div>
              <div className="form-group mt-3">
                <label htmlFor="email" className="form-label">Email address</label>
                <input
                  id="email"
                  type="email"
                  name="email"
                  className="form-control mt-1"
                  placeholder="Enter email"
                  value={formData.email}
                  onChange={handleChange}
                />
              </div>
              <div className="form-group mt-3">
                <label htmlFor="password" className="form-label">Password</label>
                <input
                  id="password"
                  type="password"
                  name="password"
                  className="form-control mt-1"
                  placeholder="Enter password"
                  minLength={8}
                  value={formData.password}
                  onChange={handleChange}
                />
              </div>
              <div className="d-grid mt-3">
                <button type="submit" className="btn btn-primary">
                  {authMode === 'signin' ? 'Login' : 'Register'}
                </button>
              </div>
              {authMode === 'signin' && (
                <p className="text-center mt-2">
                  <a href="/forgot-password">Forgot password?</a>
                </p>
              )}
              {errorMessage && (
                <div className="alert alert-danger mt-3" role="alert">
                  {errorMessage}
                </div>
              )}
            </div>
          </div>
        </form>
      </div>
    </div>
  );
}
