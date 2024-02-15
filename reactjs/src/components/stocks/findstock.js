import React from 'react';
import axios from 'axios';

class FindStock extends React.Component {
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

  render(){  
    return (
        <>
        {this.state.tickers.map(ticker => (
            <p key={ticker.symbol}>{ticker.symbol}: {ticker.longname}</p>
        ))}
        </>
    );
  }
}

export default FindStock;
