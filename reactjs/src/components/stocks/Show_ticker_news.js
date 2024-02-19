import React from 'react';
import axios from 'axios';
import { useParams } from 'react-router-dom';

function withParams(Component){
  return props => <Component {...props} params={useParams()} />;
}
class ShowTickerNews extends React.Component {
  state = {
    symbol: null,
    news: [],
    loading: false
  };

  componentDidMount() {
    this.setState({loading: true});
    let { ticker } = this.props.params
    this.setState({symbol: ticker})
    let url = 'http://localhost:8889/stocks/ticker/' + ticker + '/news/'
    console.log(url)
    axios.get(url)
      .then(res => {
          console.log(res.data); // Log the response data to understand its structure

  //       const tickers = res.data['news'];
  //       this.setState({ tickers });
  //     })
  //     .then(this.setState({loading: false}));
  // }
          const news = res.data['news'];
          this.setState({ news: news, loading: false }); // Set loading to false here
        })
      .catch(error => {
          console.error('Error fetching data:', error);
          this.setState({ loading: false }); // Ensure loading is set to false on error
      });
  }

  render(){  
    return (
        <div class="container-fluid">
          <div className="row py-3">
            <h3>News for {this.state.symbol}</h3>
          </div>
        {this.state.news.map(news => (
          <div class="row py-3">
            <a href={news.link} target="_blank">
              <h4 key={news.uuid}>{news.title}</h4>
            </a>
          </div>
        ))}
        </div>
    );
  }
}

export default withParams(ShowTickerNews);
