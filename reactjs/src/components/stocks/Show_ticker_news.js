import React from 'react';
import axios from 'axios';

class ShowTickerNews extends React.Component {
  state = {
    tickers: [],
    loading: false
  };

  componentDidMount() {
    this.setState({loading: true});
    console.log('https://query1.finance.yahoo.com/v1/finance/search?q=amazon&lang=en-US&region=US&quotesCount=0&newsCount=10&listsCount=0')
    axios.get('https://query1.finance.yahoo.com/v1/finance/search?q=amazon&lang=en-US&region=US&quotesCount=0&newsCount=10&listsCount=0')
      .then(res => {
          console.log(res.data); // Log the response data to understand its structure

  //       const tickers = res.data['news'];
  //       this.setState({ tickers });
  //     })
  //     .then(this.setState({loading: false}));
  // }
          const tickers = res.data['news'];
          this.setState({ tickers, loading: false }); // Set loading to false here
        })
      .catch(error => {
          console.error('Error fetching data:', error);
          this.setState({ loading: false }); // Ensure loading is set to false on error
      });
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

export default ShowTickerNews;
