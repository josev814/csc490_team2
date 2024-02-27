import './App.css';
import React from 'react';
import {BrowserRouter, Routes, Route} from 'react-router-dom';
import Find_stock from './pages/stocks';
import Layout from './pages/layout';
import Home from './pages/home';
import NoPage from './pages/nopage';
import Show_ticker_news from './pages/news';

import 'bootstrap/dist/css/bootstrap.min.css'
import './App.css'
import Auth from './components/Auth'



class App extends React.Component {
  render() {
    return (
      <BrowserRouter>
        <Routes>
        <Route path="/auth" element={<Auth />} />
          <Route path="/" element={<Layout />}>
            <Route index element={<Home />} />
            <Route path="stocks" element={<Find_stock />} />
            <Route path="stocks/:ticker/news" element={<Show_ticker_news />} />
            {/* <Route path="stocks/:ticker/news" element={<Show_ticker_news />} /> */}
            <Route path="*" element={<NoPage />} />
          </Route>
        </Routes>
      </BrowserRouter>
    );
  }
}

export default App;
