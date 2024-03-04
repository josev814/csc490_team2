import React, { useState } from "react"

export default function LoginRegister (props) {
  let [authMode, setAuthMode] = useState("signin")

  const changeAuthMode = () => {
    setAuthMode(authMode === "signin" ? "signup" : "signin")
  }

  if (authMode === "signin") {
    return (
      <div className="container-fluid d-flex justify-content-center vh-100 align-items-center">
        <div className="col-12 col-md-3">
          <form className="form shadow">
            <div className="card px-5 py-2 rounded border-2 border-light">
              <div className="card-body">
                <h3 className="card-title text-center">Account Login</h3>
                <div className="card-text text-center">
                  Not registered yet?{" "}
                  <span className="link-primary" onClick={changeAuthMode}>
                    Register
                  </span>
                </div>
                <div className="form-group mt-3">
                  <label htmlFor='email_address' className='form-label'>Email address</label>
                  <input
                    id='email_address'
                    type="email"
                    className="form-control mt-1"
                    placeholder="Enter email"
                  />
                </div>
                <div className="form-group mt-3">
                  <label htmlFor='password' className='form-label'>Password</label>
                  <input
                    id='password'
                    type="password"
                    className="form-control mt-1"
                    placeholder="Enter password"
                  />
                </div>
                <div className="d-grid mt-3">
                  <button type="submit" className="btn btn-primary">
                    Login
                  </button>
                </div>
                <p className="text-center mt-2">
                  <a href="/Logout">Forgot password?</a>
                </p>
              </div>
            </div>
          </form>
        </div>
      </div>
    )
  }

  return (
    <div className="Auth-form-container d-flex justify-content-center vh-100 align-items-center">
      <div className="col-12 col-md-3">
        <form className="Auth-form shadow">
          <div className="Auth-form-content card px-5 py-2 rounded border-2 border-light">
            <div className="card-body">
              <h3 className="Auth-form-title text-center">Account Registration</h3>
              <div className="card-text text-center">
                Already registered?{" "}
                <span className="link-primary" onClick={changeAuthMode}>
                  Log In
                </span>
              </div>
              <div className="form-group mt-3">
                <label htmlFor='email_address' className='form-label'>Email address</label>
                <input
                  id='email_address'
                  type="email"
                  className="form-control mt-1"
                  placeholder="Email Address"
                />
              </div>
              <div className="form-group mt-3">
                <label htmlFor='password' className='form-label'>Password</label>
                <input
                  id='password'
                  type="password"
                  className="form-control mt-1"
                  placeholder="Password"
                />
              </div>
              <div className="d-grid gap-2 mt-3">
                <button type="submit" className="btn btn-primary">
                  Register
                </button>
              </div>
            </div>
          </div>
        </form>
      </div>
    </div>
  )
}