import './App.css';
import React from 'react';
import {BrowserRouter, Routes, Route} from 'react-router-dom';
import AuthedLayout from './pages/authedlayout';
import UnauthedLayout from './pages/unauthedlayout';
import NoPage from './pages/nopage';
import Home from './pages/home';
import FIND_STOCK from './pages/stocks';
import SHOW_TICKER from './pages/show_ticker';
//import Dashboard from './pages/dashboard';
import SHOW_TICKER_NEWS from './pages/news';
import LIST_RULES from './pages/rules';
import SHOW_RULE from './pages/rule';


class App extends React.Component {
  constructor(props){
    super(props);
    this.state = {
      sitedetails: {},
    };
  }

  componentDidMount() {
    this.setState({
      sitedetails:{
        'sitename': 'Stock Strategies',
        'tagline': 'Test Trading Strategies'
      }
    });
  }

  render() {
    return (
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<UnauthedLayout sitename={this.state.sitedetails.sitename} tagline={this.state.sitedetails.tagline} />}>
            <Route index element={<Home />} />
            <Route path="login" element={<></>} />
            <Route path="logout" element={<></>} />
          </Route>
          <Route path="/user/" element={<AuthedLayout sitename={this.state.sitedetails.sitename} tagline={this.state.sitedetails.tagline} />}>
            <Route path=":user_id/profile" element={<></>} />
          </Route>
          <Route path="/stocks/" element={<AuthedLayout sitename={this.state.sitedetails.sitename} tagline={this.state.sitedetails.tagline} />}>
            <Route index element={<FIND_STOCK />} />
            <Route path=":ticker" element={<SHOW_TICKER />} />
            <Route path=":ticker/news" element={<SHOW_TICKER_NEWS />} />
          </Route>
          <Route path="/rules/" element={<AuthedLayout sitename={this.state.sitedetails.sitename} tagline={this.state.sitedetails.tagline} />}>
            <Route index element={<LIST_RULES />} />
          </Route>
          <Route path="/rule/" element={<AuthedLayout sitename={this.state.sitedetails.sitename} tagline={this.state.sitedetails.tagline} />}>
            <Route path=":rule" element={<SHOW_RULE />} />
          </Route>
          <Route path="*" element={<UnauthedLayout sitename={this.state.sitedetails.sitename} tagline={this.state.sitedetails.tagline} />}>
            <Route index element={<NoPage />} />
          </Route>
        </Routes>
      </BrowserRouter>
    );
  }
}

export default App;
