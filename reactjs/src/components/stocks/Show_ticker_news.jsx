import React from 'react';
import PropTypes from 'prop-types';
import axios from 'axios';
import Spinner from 'react-bootstrap/Spinner';
import { useParams, Link } from 'react-router';
import { sitedetails } from '../../utils/appContext';

function withParams(Component){
  const ComponentWithParams = (props) => <Component {...props} params={useParams()} />;
  
    // Give the component a display name for better debugging
    const wrappedName = Component.displayName || Component.name || 'Component';
    ComponentWithParams.displayName = `withParams(${wrappedName})`;
  
    return ComponentWithParams;
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
    let url = sitedetails.django_url + '/stocks/get_ticker_news/?ticker=' + ticker    
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
              <Link to={news.link} target='_blank' rel='noreferrer'>
                <h4>{news.title}</h4>
              </Link>
            </div>
          )))
        }
        </div>
    );
  }
}

export default withParams(ShowTickerNews);

ShowTickerNews.propTypes = {
  params: PropTypes.object,
}