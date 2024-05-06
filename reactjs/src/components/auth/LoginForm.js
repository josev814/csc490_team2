
import React from "react";
import { useNavigate } from 'react-router-dom';

export default function LoginForm({ formData, handleChange, handleSubmit, errorMessage }) {
  const navigate = useNavigate();

  const handleRegisterRedirect = () => {
    // Redirect to the registration page
    navigate('/register');
  };

  return (
    <form role="form" className="form shadow" onSubmit={handleSubmit}>
      <div className="card px-5 py-2 rounded border-2 border-light">
        <div className="card-body">
          <h3 className="card-title text-center">Account Login</h3>
          <div className="card-text text-center">
            <p>Not registered yet? <span role="link" className="link-primary" onClick={handleRegisterRedirect}>Register</span></p>
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
            <button role="button" type="submit" className="btn btn-primary">Login</button>
          </div>
          <p className="text-center mt-2">
            <a role="link" href="/forgot-password">Forgot password?</a>
          </p>
          {errorMessage && (
            <div className="alert alert-danger mt-3" role="alert">
              {errorMessage}
            </div>
          )}
        </div>
      </div>
    </form>
  );
}
