import './App.css';
import React from 'react';
import { LoginRegister, Logout } from './components/Auth';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import AuthedLayout from './pages/authedlayout';
import UnauthedLayout from './pages/unauthedlayout';
import NoPage from './pages/nopage';
import Home from './pages/home';
import FIND_STOCK from './pages/stocks';
import SHOW_TICKER from './pages/show_ticker';
import SHOW_TICKER_NEWS from './pages/news';
import LIST_RULES from './pages/rules';
import { SHOW_RULE, CREATE_RULE } from './pages/rule';
import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css';
import Cookies from 'universal-cookie';
import axios from 'axios';

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      sitedetails: {},
    };
    this.cookies = new Cookies(null, { path: '/' });
  }

  componentDidMount() {
    this.setState({
      sitedetails: {
        sitename: 'Stock Strategies',
        tagline: 'Test Trading Strategies',
        django_url: 'http://localhost:8889'
      },
    });
    this.refresh_session()
  }

  componentDidUpdate() {
    this.refresh_session()
  }

  get_auth_header() {
    const token = localStorage.getItem('accessToken');
    const headers = {
      Authorization: `Bearer ${token}`,
    };
    return headers;
  }

  refresh_login_cookie() {
    // Calculate expiration time for the login status cookie (30 minutes)
    const loginStatusExpiration = new Date();
    loginStatusExpiration.setTime(loginStatusExpiration.getTime() + (0.5 * 60 * 60 * 1000));

    // Check if 'is_active' cookie exists
    const is_active = this.cookies.get('is_active');
    if (is_active) {
      // Log the current value of 'is_active' (optional for debugging)
      console.log("Current 'is_active' value:", is_active);

      // Update the expiration time of the 'is_active' cookie
      console.log('Login Expiration: ', loginStatusExpiration)
      this.cookies.set('is_active', is_active, { expires: loginStatusExpiration });
    } else {
      console.error("User is not logged in.");
      this.props.history.push('/login'); // Navigate to the login page
    }
  }

  async refresh_token() {
    const refresh_url = `${this.state.sitedetails.django_url}/auth/refresh/`;
    const data = {'refresh': localStorage.getItem('refreshToken')};
    if (this.state.sitedetails.django_url === undefined){
      return
    }
    try {
      if(data['refresh'] === undefined){
        throw new Error('Refresh token is undefined')
      }
      // Send POST request to refresh URL
      const response = await axios.post(refresh_url, data, { headers: this.get_auth_header() });

      // Check if response is successful
      if (response.status === 200) {
        // Update tokens in local storage
        localStorage.setItem('accessToken', response.data.access);
        localStorage.setItem('refreshToken', response.data.refresh);
      } else {
        // Handle unexpected response status codes
        // TODO: toastify this
        console.error('Error refreshing token')
        console.error('Unexpected response status:', response.status);
      }
    } catch (error) {
      // Handle network errors or other exceptions
      // TODO: toastify this
      console.error('Error refreshing token:', error);
      // Optionally, navigate to login page or handle the error
    }
  }

  async refresh_session(){
    console.groupCollapsed('refresh_session')
    let user_url = this.get_user_from_cookie()
    console.log(user_url)
    if(user_url !== undefined){
      this.refresh_token()
      this.refresh_login_cookie()
    }
    console.groupEnd()
  }

  get_user_from_cookie() {
    const userCookie = this.cookies.get('user');
    if (!userCookie || !userCookie.id) {
      console.error("User cookie or user ID not found.");
      return null; // or handle the error appropriately
    }

    // Construct user URL based on user ID
    const user_id = userCookie.id;
    const user_url = `${this.state.sitedetails.django_url}/users/${user_id}/`;
    return user_url;
  }

  render(){
    return (
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<UnauthedLayout sitename={this.state.sitedetails.sitename} tagline={this.state.sitedetails.tagline} />} >
            <Route index element={<Home />} />
            <Route path="login" element={<LoginRegister mode="signin" />} />
            <Route path="register" element={<LoginRegister mode="signup" />} />
            <Route path="logout" element={<Logout />} />
            <Route path="login" element={<LoginRegister mode="signin" />} />
            <Route path="register" element={<LoginRegister mode="signup" />} />
            <Route path="logout" element={<Logout />} />
          </Route>

          <Route path="/user/" element={<AuthedLayout sitename={this.state.sitedetails.sitename} tagline={this.state.sitedetails.tagline} refresh_session={this.refresh_session} />} >
            <Route path=":user_id/profile" element={<></>} />
          </Route>

          <Route path="/stocks/" element={<AuthedLayout sitename={this.state.sitedetails.sitename} tagline={this.state.sitedetails.tagline} />} >
            <Route index element={<FIND_STOCK />} />
            <Route path=":ticker" element={<SHOW_TICKER />} />
            <Route path=":ticker/news" element={<SHOW_TICKER_NEWS />} />
          </Route>

          <Route path="/rules/" element={<AuthedLayout sitename={this.state.sitedetails.sitename} tagline={this.state.sitedetails.tagline} django_url={this.state.sitedetails.django_url} />} >
            <Route index element={<LIST_RULES get_auth_header={this.get_auth_header} django_url={this.state.sitedetails.django_url} />} />
            
          </Route>

          <Route path="/rule/" element={<AuthedLayout sitename={this.state.sitedetails.sitename} tagline={this.state.sitedetails.tagline} />}>
            <Route path="create" element={
                <CREATE_RULE 
                  django_url={this.state.sitedetails.django_url}
                  get_auth_header={this.get_auth_header}
                  get_user_from_cookie={this.get_user_from_cookie}
                />
              }
            />
            <Route path=":rule/:rule_name" element={<SHOW_RULE sitedetails={this.state.sitedetails} />} />
          </Route>

          <Route path="*" element={<UnauthedLayout sitename={this.state.sitedetails.sitename} tagline={this.state.sitedetails.tagline} />} >
            <Route index element={<NoPage />} />
            <Route path='*' element={<NoPage />} />
          </Route>

        </Routes>
      </BrowserRouter>
    );
  }
}

export default App;