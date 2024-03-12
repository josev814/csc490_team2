
import React from 'react';

export default function Settings() {
    return (
        <div className="container mt-5">
            <div className="card">
                <h4 className="card-header">Account settings</h4>
                <div className="card-body">
                    <div className="form-group row">
                        <label htmlFor="firstname" className="col-md-3 col-form-label">First Name</label>
                        <div className="col-md-9">
                            <input type="text" className="form-control" id="firstname" placeholder="Enter First name.." />
                        </div>
                    </div>
                    <div className="form-group row">
                        <label htmlFor="lastname" className="col-md-3 col-form-label">Last Name</label>
                        <div className="col-md-9">
                            <input type="text" className="form-control" id="lastname" placeholder="Enter Last Name..." />
                        </div>
                    </div>
                    <div className="form-group row">
                        <label htmlFor="email" className="col-md-3 col-form-label">Email Address</label>
                        <div className="col-md-9">
                            <input type="email" className="form-control" id="email" placeholder="Enter Email Address..." />
                        </div>
                    </div>
                    <div className="form-group row">
                        <label htmlFor="phone" className="col-md-3 col-form-label">Phone Number</label>
                        <div className="col-md-9">
                            <input type="tel" className="form-control" id="phone" placeholder="Enter Phone Number..." />
                        </div>
                    </div>
                    <div className="form-group row">
                        <div className="col-md-9 offset-md-3">
                            <button className="btn btn-primary mr-3">Save Changes</button>
                            <button className="btn btn-secondary">Cancel</button>
                        </div>
                    </div>
                    <div className="form-group row">
                        <div className="col-md-9 offset-md-3">
                            <div>
                                <b>Deactivate your account</b>
                                <p>Details about your account and password will be erased!</p>
                            </div>
                            <button className="btn btn-danger">Deactivate</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}
