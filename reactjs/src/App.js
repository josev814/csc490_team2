import logo from './logo.svg';
import './App.css';
import React from 'react';
import {BrowserRouter, Route, NavLink} from 'react-router-dom';
import axios from 'axios';

// function App() {
//   return (
//     <div className="App">
//       <header className="App-header">
//         <img src={logo} className="App-logo" alt="logo" />
//         <p>
//           Hello World !!
//         </p>
//       </header>
//     </div>
//   );
// }

class App extends React.Component {
  state = {
    tickers: [],
    loading: false
  };

  componentDidMount() {
    this.setState({loading: true});
    axios.get('http://localhost:8889/stocks/ticker/find/amazon/')
      .then(res => {
        const tickers = res.data['quotes'];
        this.setState({ tickers });
      })
      .then(this.setState({loading: false}));
  }

  render() {
    return (
      <div>
        {this.state.tickers.map(ticker => (
          <p key={ticker.symbol}>{ticker.symbol}: {ticker.longname}</p>
        ))}
      </div>
    );
  }
}

export default App;
