import React from 'react';
import PropTypes from "prop-types";
import axios from 'axios';
import Spinner from 'react-bootstrap/Spinner';
import { useParams } from 'react-router-dom';
import Highcharts from 'highcharts'
import HighchartsReact from 'highcharts-react-official'

function withParams(Component){
  const ComponentWithParams = (props) => <Component {...props} params={useParams()} />;
  
    // Give the component a display name for better debugging
    const wrappedName = Component.displayName || Component.name || 'Component';
    ComponentWithParams.displayName = `withParams(${wrappedName})`;
  
    return ComponentWithParams;
}

class ShowRuleTransactionChart extends React.Component {
  constructor(props){
    super(props);
    this.state = {
      symbol: null,
      chartSeries: [],
      chartXaxis: [],
      loading: true,
      processing: false,
    };
  }

  get_strdate_to_date_obj(str_date){
    const dateParts = str_date.split("-");
    const year = parseInt(dateParts[0]);
    const month = parseInt(dateParts[1]) - 1; // Month is zero-based in JavaScript Date object
    const day = parseInt(dateParts[2]);

    // Create a Date object with the current date
    return new Date(year, month, day);
  }

  get_next_date(current_date) {
    const currentDate = this.get_strdate_to_date_obj(current_date)
    // Get the next day by adding 1 to the current day
    currentDate.setDate(currentDate.getDate() + 1);

    // Format the next day in the desired format (YYYY-MM-DD)
    return currentDate.toISOString().substring(0, 10);
  }

  componentDidMount() {
    if(this.state.processing === true){
      return;
    }
    this.setState( prevState => ({...prevState, 'processing':true }))
    console.log('props: ', this.props)
    let rule_id = this.props.params.rule
    let url = `${global.config.sitedetails.django_url}/transactions/rule/${rule_id}/?limit=50&ordering=pk`
    console.log(url)

    axios.get(url, {headers: this.props.get_auth_header()})
      .then(res => {
          const results = res.data
          const quotes = results['results'].reverse()
          let xDates = [];
          let purchased = [];
          let sold = [];
          let profit = [];
          let last_datetime=undefined
          let day_purchased_qty = 0
          let day_sold_qty = 0
          let next_day = undefined
          quotes.forEach(record => {
            let entry_date = record.timestamp.substring(0, 10)
            let entry_date_obj = this.get_strdate_to_date_obj(entry_date)
            if (next_day !== undefined){ // handles dates where no trx were performed
              while(entry_date_obj > this.get_strdate_to_date_obj(next_day)){
                day_purchased_qty = 0
                day_sold_qty = 0
                console.log(`Current Day ${entry_date} adding missing date ${next_day}`)
                xDates.push(next_day);
                sold.push(day_sold_qty)
                purchased.push(day_purchased_qty)
                next_day = this.get_next_date(next_day)
              }
            }
            if (last_datetime === undefined){
              if (record.action === 'buy'){
                day_purchased_qty += record.quantity
              } else if (record.action === 'sold'){
                day_sold_qty += record.quantity
              }
            } else if (last_datetime !== undefined){
              // Start add to qty if current date
              if (entry_date === last_datetime){
                if (record.action === 'buy'){
                  day_purchased_qty += record.quantity
                } else if (record.action === 'sold'){
                  day_sold_qty += record.quantity
                }
                // End add to qty if current date
              } else {
                xDates.push(last_datetime);
                sold.push(day_sold_qty)
                purchased.push(day_purchased_qty)
                //reset after push
                day_purchased_qty = 0
                day_sold_qty = 0
              }
            }
            last_datetime = entry_date
            next_day = this.get_next_date(entry_date)
          });
          this.setState({ chartSeries: [
            {name: 'Return', data: profit},
            {name: 'Purchased', data: purchased},
            {name: 'Sold', data: sold},
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
          {/* <div className="row pb-3">
            <form>
              <label className="px-2">Granularity:</label>
              <select>
                <option>1d</option>
              </select>
            </form>
          </div> */}
          <div className="row pb-3" id="chartContainer" style={{ height: "400px" }}>
          {this.renderGraph}
          </div>
        </div>
    );
  }
}

export default withParams(ShowRuleTransactionChart);

ShowRuleTransactionChart.propTypes = {
  params: PropTypes.object,
  get_auth_header: PropTypes.func,
}