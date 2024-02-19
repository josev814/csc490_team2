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
      this.setState({stocks: res.data['quotes']})
    }).then(
      this.setState({ loading: false })
    ).catch(error => {
      console.log('Error fetching data: ', error)
      this.setState({loading: false })
    })
  };

  onChangeHandler = async e => {
    if (e.target.value.length > 1) {
      this.search(e.target.value);
    }
    this.setState({ value: e.target.value});
  };

  get renderStocks(){
    if (this.state.value.length > 1){
    let stocks = <h3> There are no stocks with the name {this.state.value}.</h3>
    if (this.state.stocks) {
      stocks = ( this.state.stocks.map(stocks => (
        <div className='row py-2'>
          <a href='stocks/:stocks.symbol/news' key={stocks.symbol}>{stocks.symbol}: {stocks.longname}</a>
        </div>
      )))
    }
    return stocks;
  }
  }

  render(){  
    return (
        <>
        <div className="input-wrapper">
          <input 
            value={this.state.value}
            onChange={e => this.onChangeHandler(e)}
            placeholder="Type to search a stock ..."/>
        </div>
        <div className='container'>
          {this.renderStocks}
        </div>        
        </>
    );
  }
}

export default FindStock;
