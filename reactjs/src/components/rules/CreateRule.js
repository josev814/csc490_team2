import React from "react";
import { useNavigate } from "react-router";
import { AsyncDropDown } from "../inputs/AsyncDropDown";
import { DateInput } from "../inputs/DateInput";

export default function CreateRuleForm(props) {
    const navigate = useNavigate();
    const event_data = [
        {value:'price', label: 'Current Price'},
        {value:'open', label: 'Open Price'},
        {value:'high', label: 'High Price'},
        {value:'low', label: 'Low Price'},
        {value:'close', label: 'Close Price'}
    ]
    const event_operators = [
        {value:'gt', label: 'greater than'},
        {value:'gte', label: 'greater than or equal to'},
        {value:'lt', label: 'less than'},
        {value:'lte', label: 'less than or equal to'},
        {value:'eq', label: 'equal to'},
    ]
    const then_methods = [
        {value:'buy', label: 'Buy'},
        {value: 'sell', label: 'Sell'},
        {value: 'notify', label: 'Notify'}
    ]
    const then_qty_types = [
        {value:'usd', label: 'USD'},
        {value: 'shares', label: 'Share(s)'},
    ]

    return(
        <div className="container">
            <h2 className="mb-4">Add Rule</h2>
            <form className="form" onSubmit={props.handleSubmit}>
                <div className="row mb-3">
                    <label htmlFor="name" className="form-label">Name:</label>
                    <input type="text" className="form-control" name="name" id="name" placeholder="Enter rule name" onChange={props.handleChange} />
                </div>
                <div className="row mb-3">
                    <label htmlFor="initial_investment" className="form-label">Initial Investment:</label>
                    <div className="input-group">
                        <div className="input-group-prepend">
                            <span className='input-group-text'>$</span>
                        </div>
                        <input type="number" className="form-control" name="initial_investment" id="initial_investment" placeholder="Enter your initial investment" onChange={props.handleChange} />
                        <div className="input-group-append">
                            <span className='input-group-text'>.00</span>
                        </div>
                    </div>
                </div>
                <div className="row mb-3">
                    <DateInput label='Start Date' id='start_date' name='start_date' handleChange={props.handleChange} />
                </div>
                <div className="row shadow px-2 py-3 mb-3">
                    <label className="col-md-1">
                        <span className="h5">IF:</span>
                        <input type='hidden' name="event_condition_1" aria-hidden aria-readonly value='if' />
                    </label>
                    <div className="col-md-3">
                        <AsyncDropDown name='event_symbol_1' handleChange={props.handleChange} />
                    </div>
                    <div className="col-md-1">
                        HAS 
                    </div>
                    <div className="col-md-2">
                        <select required aria-required name="event_data_1" className="form-select" onChange={props.handleChange}>
                            <option value=''>---</option>
                            {event_data.map((item, index) =>
                                <option key={index} value={item.value}>{item.label}</option>
                            )}
                        </select>
                    </div>
                    <div className="col-md-3">
                        <select required aria-required name="event_operator_1" className="form-select" onChange={props.handleChange}>
                            <option value=''>---</option>
                            {event_operators.map((item, index) =>
                                <option key={index} value={item.value}>{item.label}</option>
                            )}
                        </select>
                    </div>
                    <div className="col-md-2">
                        <input required aria-required type="text" pattern='^\d+(\.\d{2})?$' name="event_value_1" className="form-control" placeholder="Comparison Value $"  onChange={props.handleChange} />
                    </div>
                </div>
                <div className="row shadow px-2 py-3">
                    <div className="col-md-1">
                        <span className="h5">THEN:</span>
                    </div>
                    <div className="col-md-1">
                        <select required aria-required name='then_method' className="form-select" onChange={props.handleChange}>
                            <option value=''>---</option>
                            {then_methods.map((item, index) =>
                                <option key={index} value={item.value}>{item.label}</option>
                            )}
                        </select>
                    </div>
                    <div className="col-md-2">
                        <input type="text" name='then_quantity' className="form-control" placeholder="Quantity"  onChange={props.handleChange} />
                    </div>
                    <div className="col-md-2">
                        <select required aria-required name='then_quantity_type' className="form-select" onChange={props.handleChange}>
                            <option value=''>---</option>
                            {then_qty_types.map((item, index) =>
                                <option key={index} value={item.value}>{item.label}</option>
                            )}
                        </select>
                    </div>
                    <div className="col-md-1">
                        OF
                    </div>
                    <div className="col-md-3">
                        <AsyncDropDown name='then_symbol' handleChange={props.handleChange} />
                    </div>
                </div>
                <div className="row py-3">
                    <div className="col-md-1 px-0">
                        <button type="submit" className="btn btn-primary">Add Rule</button>
                    </div>
                    <div className="col-md-2 px-0">
                        <button type="button" className="btn btn-warning" onClick={() => navigate(-1)}>Cancel</button>
                    </div>
                </div>
            </form>
        </div>
    )
}