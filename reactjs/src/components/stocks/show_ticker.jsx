import React from 'react';
import PropTypes from 'prop-types';
import axios from 'axios';
import Spinner from 'react-bootstrap/Spinner';
import { useParams } from 'react-router';
import Highcharts from 'highcharts'
import HighchartsReact from 'highcharts-react-official'

function withParams(Component){
  const ComponentWithParams = (props) => <Component {...props} params={useParams()} />;

  // Give the component a display name for better debugging
  const wrappedName = Component.displayName || Component.name || 'Component';
  ComponentWithParams.displayName = `withParams(${wrappedName})`;

  return ComponentWithParams;
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
    const { ticker } = this.props.params
    this.setState({symbol: ticker})
    const now = new Date()
    const current_time = (now.getTime() / 1000).toString().split('.')[0]
    const four_months_ago = (new Date(now.getFullYear(), now.getMonth() - 4, now.getDate()).getTime() / 1000).toString().split('.')[0]; // Date four months ago
    let url = 'http://localhost:8889/stocks/get_ticker_metrics/?ticker=' + ticker + '&interval=1d&starttime=' + four_months_ago + '&endtime=' + current_time
    //https://query1.finance.yahoo.com/v8/finance/chart/AMZN?interval=1d&includePrePost=True&period1=1704174096&period2=1714542096&lang=en-Us&region=US
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
          {/* <div className="row pb-3">
            <form>
              <label className="px-2">Granularity:</label>
              <select>
                <option>1d</option>
              </select>
            </form>
          </div> */}
          <div className="row pb-3" id="chartContainer" style={{ height: "600px" }}>
          {this.renderGraph}
          </div>
        </div>
    );
  }
}

export default withParams(ShowTickerChart);

ShowTickerChart.propTypes = {
  params: PropTypes.object,
}
