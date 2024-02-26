import './App.css';
import React from 'react';
import {BrowserRouter, Routes, Route} from 'react-router-dom';
import Find_Stock from './pages/stocks';
import AuthedLayout from './pages/authedlayout';
import UnauthedLayout from './pages/unauthedlayout';
//import Dashboard from './pages/dashboard';
import NoPage from './pages/nopage';
import Show_Ticker_News from './pages/news';

class App extends React.Component {
  render() {
    return (
      <BrowserRouter>
        <Routes>
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
            <Route index element={<Find_Stock />} />
            <Route path=":ticker/news" element={<Show_Ticker_News />} />
            <Route path="logout" element={<></>} />
            <Route path="*" element={<NoPage />} />
          </Route>
          <Route path="/rules/" element={<AuthedLayout />}>
            <Route index element={<Find_Stock />} />
            <Route path=":ticker/news" element={<Show_Ticker_News />} />
            <Route path="logout" element={<></>} />
            <Route path="*" element={<NoPage />} />
          </Route>
        </Routes>
      </BrowserRouter>
    );
  }
}

export default App;
