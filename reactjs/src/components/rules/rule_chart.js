import React from 'react';
import axios from 'axios';
import Spinner from 'react-bootstrap/Spinner';
import { useParams } from 'react-router-dom';
import Highcharts from 'highcharts'
import HighchartsReact from 'highcharts-react-official'

function withParams(Component){
  return props => <Component {...props} params={useParams()} />;
}

class ShowRuleTransactionChart extends React.Component {
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
    let { transactions } = this.props.params
    transactions = 'amzn'
    this.setState({symbol: transactions})
    let url = 'http://localhost:8889/stocks/get_ticker_metrics/?ticker=' + transactions

    //pass data from rule.js via getrule endpoint {{base_url}}/rules/1/
    //transactions from rule.js passed into here

    axios.get(url)
      .then(res => {
          //console.log(res.data); // Log the response data to understand its structure
          const results = res.data
          //const timestamps = results['timestamp'];
          const quotes = results['records']
          const xDates = [];
          const returned = [];
          quotes.forEach(record => {
            xDates.push(record.timestamp.substring(0, 10));
            returned.push(record.high);
          });
          this.setState({ chartSeries: [
            {name: 'Return', data: returned},
          ], chartXaxis: xDates,
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
    let options = {
        title: {
          text: ''
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
          <div className="row pb-3" id="chartContainer" style={{ height: "400px" }}>
          {this.renderGraph}
          </div>
        </div>
    );
  }
}

export default withParams(ShowRuleTransactionChart);
