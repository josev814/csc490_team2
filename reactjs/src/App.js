import './App.css';
import React from 'react';
import {BrowserRouter, Routes, Route} from 'react-router-dom';
import AuthedLayout from './pages/authedlayout';
import UnauthedLayout from './pages/unauthedlayout';
import NoPage from './pages/nopage';
import FIND_STOCK from './pages/stocks';
import SHOW_TICKER from './pages/show_ticker';
//import Dashboard from './pages/dashboard';
import SHOW_TICKER_NEWS from './pages/news';
import LIST_RULES from './pages/rules';


class App extends React.Component {
  render() {
    return (
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<UnauthedLayout />}>
            <Route index element={<></>} />
            <Route path="login" element={<></>} />
            <Route path="logout" element={<></>} />
          </Route>
          <Route path="/user/" element={<AuthedLayout />}>
            <Route path=":user_id/profile" element={<></>} />
          </Route>
          <Route path="/stocks/" element={<AuthedLayout />}>
            <Route index element={<FIND_STOCK />} />
            <Route path=":ticker" element={<SHOW_TICKER />} />
            <Route path=":ticker/news" element={<SHOW_TICKER_NEWS />} />
          </Route>
          <Route path="/rules/" element={<AuthedLayout />}>
            <Route index element={<LIST_RULES />} />
            {/* <Route path="rules/:rule_id" element={<SHOW_RULE />} /> */}
          </Route>
          <Route path="*" element={<UnauthedLayout />}>
            <Route index element={<NoPage />} />
          </Route>
        </Routes>
      </BrowserRouter>
    );
  }
}

export default App;
