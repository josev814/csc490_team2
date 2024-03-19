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
      chartSeries: [],
      chartXaxis: [],
      loading: true
    };
  }

  componentDidMount() {
    let { ticker } = this.props.params
    this.setState({symbol: ticker})
    let url = 'http://localhost:8889/stocks/get_ticker_metrics/?ticker=' + ticker    
    axios.get(url)
      .then(res => {
          //console.log(res.data); // Log the response data to understand its structure
          const results = res.data
          //const timestamps = results['timestamp'];
          const quotes = results['records']
          const timestamps = [];
          const shigh = [];
          const slow = [];
          const sopen = [];
          const sclose = [];
          quotes.forEach(record => {
            timestamps.push(record.timestamp);
            shigh.push(record.high);
            slow.push(record.low);
            sopen.push(record.open);
            sclose.push(record.close);
          });
          this.setState({ chartSeries: [
            {name: 'High', data: shigh},
            {name: 'Low', data: slow},
            {name: 'Market Open', data: sopen},
            {name: 'Market Close', data: sclose},
          ], chartXaxis: timestamps,
          loading: false }); // Set loading to false here
        })
      .catch(error => {
          console.error('Error fetching data:', error);
          this.setState({ loading: false }); // Ensure loading is set to false on error
      });
  }

  get renderGraph(){
    if (this.state.loading){
      return <Spinner animation="border" variant="primary" />;
    } 
    let chartTitle = this.state.symbol + ' Chart'
    let options = {
        title: {
          text: chartTitle
        },
        yAxis: {
          title: {
            text: 'Value'
          }
        },
        xAxis: {
          categories: this.state.chartXaxis
        },
        series: this.state.chartSeries
    }
    return <HighchartsReact
      highcharts = {Highcharts}
      options = {options}
    />
  }

  render(){
    return (
        <div className="container-fluid">
          <div className="row pb-3">
            <form>
              <label className="px-2">Granularity:</label>
              <select>
                <option>1d</option>
              </select>
            </form>
          </div>
          <div className="row pb-3" id="chartContainer" style={{ height: "600px" }}>
          {this.renderGraph}
          </div>
        </div>
    );
  }
}

export default withParams(ShowTickerChart);
