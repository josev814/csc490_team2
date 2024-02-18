import './App.css';
import React from 'react';
import {BrowserRouter, Routes, Route, NavLink} from 'react-router-dom';
import Find_stock from './pages/stocks';
import Layout from './pages/layout';
import Home from './pages/home';
import NoPage from './pages/nopage';

class App extends React.Component {
  render() {
    return (
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Layout />}>
            <Route index element={<Home />} />
            <Route path="stocks" element={<Find_stock />} />
            <Route path="*" element={<NoPage />} />
          </Route>
        </Routes>
      </BrowserRouter>
    );
  }
}

export default App;
