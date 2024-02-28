import React from 'react';
import axios from 'axios';
import Spinner from 'react-bootstrap/Spinner'


class FindStock extends React.Component {
  state = {
    stocks: null,
    loading: false,
    value: ''
  };


  search = async val => {
    this.setState({ loading: true});
    axios.get(
      'http://localhost:8889/stocks/find_ticker/?ticker=' + val
    ).then(res => {
      this.setState({stocks: res.data['quotes'], loading: false})
    }).catch(error => {
      console.log('Error fetching data: ', error)
      this.setState({loading: false })
    })
  };

  onChangeHandler = async e => {
    this.setState({ loading: true});
    
    if (this.searchTimer) {
      clearTimeout(this.searchTimer);
    }

    this.setState({ value: e.target.value });
    if (e.target.value.length <= 1) {
      this.setState({ loading: false })
    }

    // Start a new timer to execute the search after 1 second
    this.searchTimer = setTimeout(() => {
      if (e.target.value.length > 1) {
        this.search(e.target.value);
      }
    }, 1000)
  };

  get renderStocks(){
    if (this.state.loading){
      return <Spinner animation="border" variant="primary" />;
    } else if (this.state.value.length > 1){
      let stocks = <h3> There are no stocks with the name {this.state.value}.</h3>
      if (this.state.stocks) {
        stocks = ( this.state.stocks.map(stocks => (
          <div className='row py-2' key={stocks.symbol}>
            <a href={'stocks/' + stocks.symbol}>{stocks.symbol}: {stocks.longname}</a>
          </div>
        )))
      }
      return stocks;
    }
    return '';
  }

  render(){  
    return (
        <>
        <div className="container-fluid">
          <div className="row mb-3">
            <input 
              className="form-control mr-sm-2"
              type="search"
              aria-label="Search"
              value={this.state.value}
              onChange={e => this.onChangeHandler(e)}
              placeholder="Type to search a stock ..."
            />
          </div>
        </div>
        <div className='container-fluid'>
          {this.renderStocks}
        </div>        
        </>
    );
  }
}

export default FindStock;
