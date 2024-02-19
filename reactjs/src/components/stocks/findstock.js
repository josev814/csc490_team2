import React from 'react';
import axios from 'axios';
import './searchBar.css';



class FindStock extends React.Component {
  
  // state = {
  //   tickers: [],
  //   loading: false
  // };

  // componentDidMount() {
  //   this.setState({loading: true});
  //   axios.get('http://localhost:8889/stocks/ticker/find/amazon/')
  //     .then(res => {
  //       const tickers = res.data['quotes'];
  //       this.setState({ tickers });
  //     })
  //     .then(this.setState({loading: false}));
  // }

  state = {
    stocks: null,
    loading: false,
    value: ''
  };


  search = async val => {
    this.setState({ loading: true});
    axios.get(
      'http://localhost:8889/stocks/ticker/find/' + val + '/'
    ).then(res => {
      //const stocks = res.data['quotes'];
      this.setState({stocks: res.data['quotes']})
    }).then(
      this.setState({ loading: false })
    )
  };

  onChangeHandler = async e => {
    if (e.target.value.length > 1) {
      this.search(e.target.value);
    }
    this.setState({ value: e.target.value});
  };

  // get renderStocks(){
  //   let stocks = <h1> There's no stocks by this name. </h1>
  //   if (this.state.stocks) {
  //     stocks = <Stock list={this.state.stocks} /> // 
  //   }

  //   return stocks;
  // }

  render(){  
    return (
      
        <>
        <div className="input-wrapper">
          <input 
            value={this.state.value}
            onChange={e => this.onChangeHandler(e)}
            placeholder="Type to search a stock ..."/>
            {/* {this.renderStocks} */}
        </div>
        {/* {this.state.tickers.map(ticker => (
            <p key={ticker.symbol}>{ticker.symbol}: {ticker.longname}</p>
        ))} */}
        
        </>
    );
  }
}

export default FindStock;
