import './App.css';
import React from 'react';
import {BrowserRouter, Routes, Route} from 'react-router-dom';
import FIND_STOCK from './pages/stocks';
import AuthedLayout from './pages/authedlayout';
import UnauthedLayout from './pages/unauthedlayout';
//import Dashboard from './pages/dashboard';
import NoPage from './pages/nopage';
import SHOW_TICKER_NEWS from './pages/news';

import 'bootstrap/dist/css/bootstrap.min.css'
import './App.css'
import Auth from './components/Auth'



class App extends React.Component {
  render() {
    return (
      <BrowserRouter>
        <Routes>
        <Route path="/auth" element={<Auth />} />
          <Route path="/" element={<UnauthedLayout />}>
            <Route index element={<></>} />
            <Route path="login" element={<></>} />
            <Route path="*" element={<NoPage />} />
          </Route>
          <Route path="/user/" element={<AuthedLayout />}>
            <Route path=":user_id/profile" element={<></>} />
            <Route path="logout" element={<></>} />
            <Route path="*" element={<NoPage />} />
          </Route>
          <Route path="/stocks/" element={<AuthedLayout />}>
            <Route index element={<FIND_STOCK />} />
            <Route path=":ticker/news" element={<SHOW_TICKER_NEWS />} />
            <Route path="logout" element={<></>} />
            <Route path="*" element={<NoPage />} />
          </Route>
          <Route path="/rules/" element={<AuthedLayout />}>
            <Route index element={<FIND_STOCK />} />
            <Route path=":ticker/news" element={<SHOW_TICKER_NEWS />} />
            <Route path="logout" element={<></>} />
            <Route path="*" element={<NoPage />} />
          </Route>
        </Routes>
      </BrowserRouter>
    );
  }
}

export default App;
