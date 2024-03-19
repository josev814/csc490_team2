// import React, { useState } from "react";
// import axios from 'axios';

// export default function LoginRegister (props) {
//   //let [authMode, setAuthMode] = useState("signin")

//   const [authMode, setAuthMode] = useState("signin");
//   const [formData, setFormData] = useState({
//     email: "",
//     password: ""
//   });

//   const changeAuthMode = () => {
//     setAuthMode(authMode === "signin" ? "signup" : "signin")
//   }

//   if (authMode === "signin") {
//     return (
//       <div className="container-fluid d-flex justify-content-center vh-100 align-items-center">
//         <div className="col-12 col-md-3">
//           <form className="form shadow">
//             <div className="card px-5 py-2 rounded border-2 border-light">
//               <div className="card-body">
//                 <h3 className="card-title text-center">Account Login</h3>
//                 <div className="card-text text-center">
//                   Not registered yet?{" "}
//                   <span className="link-primary" onClick={changeAuthMode}>
//                     Register
//                   </span>
//                 </div>
//                 <div className="form-group mt-3">
//                   <label htmlFor='email_address' className='form-label'>Email address</label>
//                   <input
//                     id='email_address'
//                     type="email"
//                     className="form-control mt-1"
//                     placeholder="Enter email"
//                   />
//                 </div>
//                 <div className="form-group mt-3">
//                   <label htmlFor='password' className='form-label'>Password</label>
//                   <input
//                     id='password'
//                     type="password"
//                     className="form-control mt-1"
//                     placeholder="Enter password"
//                   />
//                 </div>
//                 <div className="d-grid mt-3">
//                   <button type="submit" className="btn btn-primary">
//                     Login
//                   </button>
//                 </div>
//                 <p className="text-center mt-2">
//                   <a href="/Logout">Forgot password?</a>
//                 </p>
//               </div>
//             </div>
//           </form>
//         </div>
//       </div>
//     )
//   }

//   return (
//     <div className="Auth-form-container d-flex justify-content-center vh-100 align-items-center">
//       <div className="col-12 col-md-3">
//         <form className="Auth-form shadow">
//           <div className="Auth-form-content card px-5 py-2 rounded border-2 border-light">
//             <div className="card-body">
//               <h3 className="Auth-form-title text-center">Account Registration</h3>
//               <div className="card-text text-center">
//                 Already registered?{" "}
//                 <span className="link-primary" onClick={changeAuthMode}>
//                   Log In
//                 </span>
//               </div>
//               <div className="form-group mt-3">
//                 <label htmlFor='email_address' className='form-label'>Email address</label>
//                 <input
//                   id='email_address'
//                   type="email"
//                   className="form-control mt-1"
//                   placeholder="Email Address"
//                 />
//               </div>
//               <div className="form-group mt-3">
//                 <label htmlFor='password' className='form-label'>Password</label>
//                 <input
//                   id='password'
//                   type="password"
//                   className="form-control mt-1"
//                   placeholder="Password"
//                 />
//               </div>
//               <div className="d-grid gap-2 mt-3">
//                 <button type="submit" className="btn btn-primary">
//                   Register
//                 </button>
//               </div>
//             </div>
//           </div>
//         </form>
//       </div>
//     </div>
//   )
// }

import React, { useState } from "react";
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

export default function LoginRegister(props) {
  const [authMode, setAuthMode] = useState("signin");
  const [formData, setFormData] = useState({
    email: "",
    password: ""
  });
  const navigate = useNavigate(); // Access the history object for navigation

  const base_url = 'http://localhost:8889'; // Define your base URL here

  const changeAuthMode = () => {
    setAuthMode(authMode === "signin" ? "signup" : "signin");
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
        navigate('/rules'); // Redirect to dashboard or any other desired route
      } else {
        // Handle authentication or registration failure
      }
    } catch (error) {
      console.error('Error:', error);
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
            </div>
          </div>
        </form>
      </div>
    </div>
  );
}
