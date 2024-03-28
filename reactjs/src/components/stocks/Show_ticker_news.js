import React from 'react';
import axios from 'axios';
import Spinner from 'react-bootstrap/Spinner';
import { useParams } from 'react-router-dom';

function withParams(Component){
  return props => <Component {...props} params={useParams()} />;
}
class ShowTickerNews extends React.Component {
  constructor(props){
    super(props);
    this.state = {
      symbol: null,
      news: [],
      loading: true
    };
  }

  componentDidMount() {
    let { ticker } = this.props.params
    this.setState({symbol: ticker})
    let url = 'http://localhost:8889/stocks/get_ticker_news/?ticker=' + ticker    
    axios.get(url)
      .then(res => {
          //console.log(res.data); // Log the response data to understand its structure
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
        <div className="container-fluid">
          <div className="row py-3">
            <h3>News for {this.state.symbol}</h3>
          </div>
        {
          this.state.loading ? (
            <Spinner animation="border" variant="primary" />
          ) : (
          this.state.news.map(news => (
            <div className="row py-3" key={news.uuid}>
              <a href={news.link} target="_blank" rel='noreferrer'>
                <h4>{news.title}</h4>
              </a>
            </div>
          )))
        }
        </div>
    );
  }
}

export default withParams(ShowTickerNews);
