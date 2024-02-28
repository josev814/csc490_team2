import React from 'react';
import axios from 'axios';
import Spinner from 'react-bootstrap/Spinner';
import { useParams } from 'react-router-dom';
import Highcharts from 'highcharts'
import HighchartsReact from 'highcharts-react-official'

function withParams(Component){
  return props => <Component {...props} params={useParams()} />;
}

class ShowTickerChart extends React.Component {
  constructor(props){
    super(props);
    this.state = {
      symbol: null,
      chartData: [1,2,3],
      loading: true
    };
  }

  componentDidMount() {
    let { ticker } = this.props.params
    this.setState({symbol: ticker})
    let url = 'http://localhost:8889/stocks/get_ticker/?ticker=' + ticker    
    axios.get(url)
      .then(res => {
          //console.log(res.data); // Log the response data to understand its structure
          const results = res.data['chart']['result'][0];
          const timestamps = results['timestamp'];
          const quotes = results['indicators']['quote'][0]
          const high = quotes['high'];
          const low = quotes['low'];
          const open = quotes['open'];
          const close = quotes['close'];
          const volume = quotes['volume'];
          this.setState({ chartData: high, loading: false }); // Set loading to false here
        })
      .catch(error => {
          console.error('Error fetching data:', error);
          this.setState({ loading: false }); // Ensure loading is set to false on error
      });
  }

  get renderGraph(){
    if (this.state.loading){
      return <Spinner animation="border" variant="primary" />;
    } else {
      let chartTitle = this.state.symbol + ' Chart'
      let options = {
          title: {
            text: chartTitle
          },
          series: [{ data: this.state.chartData }]
      }
      return <HighchartsReact
        highcharts = {Highcharts}
        options = {options}
      />
    }
    return ''
  }

  render(){  
    return (
        <div className="container-fluid">
          <div className="row pb-3">
          {this.renderGraph}
          </div>
        </div>
    );
  }
}

export default withParams(ShowTickerChart);
