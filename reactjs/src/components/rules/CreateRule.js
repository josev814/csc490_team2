import React from "react";

export default function CreateRuleForm({handleSubmit, handleChange}) {
    return(
        <div className="container">
            <h2 className="mb-4">Add Rule</h2>
            <form className="form" onSubmit={handleSubmit}>
                <div className="row mb-3">
                    <label htmlFor="name" className="form-label">Name:</label>
                    <input type="text" className="form-control" name="name" id="name" placeholder="Enter rule name" onChange={handleChange} />
                </div>
                <div className="row mb-3">
                    <label htmlFor="investment" className="form-label">Initial Investment:</label>
                    <div className=" input-group">
                        <div className="input-group-prepend">
                            <span className='input-group-text'>$</span>
                        </div>
                        <input type="text" className="form-control" name="investment" id="investment" placeholder="Enter your initial investment" onChange={handleChange} />
                        <div className="input-group-append">
                            <span className='input-group-text'>.00</span>
                        </div>
                    </div>
                </div>
                <div className="row shadow px-2 py-3 mb-3">
                    <label className="col-md-1">
                        <select name="event_prefix[]" className="form-select" aria-readonly>
                            <option value='if' selected>IF</option>
                        </select> 
                    </label>
                    <div className="col-md-2">
                        <select name="event_symbol[]" className="form-select">
                            <option value='' selected>---</option>
                            <option value={'amzn'}>{'Amazon'}</option>
                        </select>
                    </div>
                    <div className="col-md-1">
                        HAS 
                    </div>
                    <div className="col-md-2">
                        <select name="event_comparison[]" className="form-select">
                            <option value='' selected>---</option>
                            <option value={'price'}>{'Price'}</option>
                            <option value={'open'}>{'Open'}</option>
                            <option value={'high'}>{'High'}</option>
                            <option value={'low'}>{'Low'}</option>
                            <option value={'close'}>{'Close'}</option>
                        </select>
                    </div>
                    <div className="col-md-1">
                        IS 
                    </div>
                    <div className="col-md-2">
                        <select name="event_operator[]" className="form-select">
                            <option value='gt' selected>greater than</option>
                            <option value='gte'>greater than or equal to</option>
                            <option value='lt'>less than</option>
                            <option value='lte'>less than or equal to</option>
                            <option value='eq'>equal to</option>
                        </select>
                    </div>
                    <div className="col-md-2">
                        <input type="text" name="event_value[]" className="form-control" placeholder="Comparison Value" />
                    </div>
                </div>
                <div className="row shadow px-2 py-3">
                    <div className="col-md-1">
                        <span className="h4">THEN:</span>
                    </div>
                    <div className="col-md-1">
                        <select name='then_clause' className="form-select">
                            <option value={'buy'}>Buy</option>
                            <option value={'sell'}>Sell</option>
                            <option value={'notify'}>Notify</option>
                        </select>
                    </div>
                    <div className="col-md-2">
                        <input type="text" name='then_value' className="form-control" placeholder="Quantity" />
                    </div>
                    <div className="col-md-2">
                        <select name='then_value2' className="form-select">
                            <option value={'usd'}>USD</option>
                            {/* <option value={'percentage'}>%</option> */}
                            <option value={'shares'}>Share(s)</option>
                        </select>
                    </div>
                    <div className="col-md-1">
                        OF
                    </div>
                    <div className="col-md-2">
                        <select name="then_symbol[]" className="form-select">
                            <option value='' selected>---</option>
                            <option value={'amzn'}>{'Amazon'}</option>
                        </select>
                    </div>
                </div>
                <div className="row py-3">
                    <div className="col-md-2 px-0">
                        <button type="submit" className="btn btn-primary">Add Rule</button>
                    </div>
                </div>
            </form>
        </div>
    )
}