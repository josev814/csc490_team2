import logo from './logo.svg';
import './App.css';
import React from 'react';
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
    tickers: []
  };

  componentDidMount() {
    axios.get('http://stocks_backend:8889/stocks/find/amazon/')
      .then(res => {
        const tickers = res.data;
        this.setState({ tickers });
      });
  }

  render() {
    return (
      <div>
        {this.state.tickers.map(ticker => (
          <p key={ticker.symbol}>{ticker.longname}</p>
        ))}
      </div>
    );
  }
}

export default App;
