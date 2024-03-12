import React from 'react';
import { useState } from 'react';
import Button from 'react-bootstrap/Button';
import CustomModal from './Deactivate';

export default function Settings() {
    const [showModal, setShowModal] = useState(false);

    const handleCloseModal = () => setShowModal(false);
    const handleShowModal = () => setShowModal(true);

    return (
        <div className="container-fluid mt-1.5">
            <div className="card">
                <h4 className="card-header">Account settings</h4>
                <div className="card-body">
                    <div className="form-group row">
                        <label htmlFor="firstname" >First Name</label>
                        <br />
                        <input type="text" className="form-control" id="firstname" placeholder="Enter First name.." />
                    </div>
                    <div className="form-group row">
                        <label htmlFor="lastname" >Last Name</label>
                        <br />
                        <input type="text" className="form-control" id="lastname" placeholder="Enter Last Name..." />
                    </div>
                    <div className="form-group row">
                        <label htmlFor="email" >Email Address</label>
                        <br />
                        <input type="email" className="form-control" id="email" placeholder="Enter Email Address..." />
                    </div>
                    <div className="form-group row">
                        <label htmlFor="phone" >Phone Number</label>
                        <br />
                        <input type="tel" className="form-control" id="phone" placeholder="Enter Phone Number..." />
                    </div>
                    <div className="form-group row mt-2">
                        <div className="col-md-9 md-3">
                            <button className="btn btn-primary me-3">Save Changes</button>
                            <button className="btn btn-secondary me-3">Cancel</button>

                            {/* Your existing form elements */}
                            <Button variant="danger" onClick={handleShowModal}>
                                Deactivate
                            </Button>
                            {/* Use the ModalComponent here */}
                            <CustomModal show={showModal} handleClose={handleCloseModal} />
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}
