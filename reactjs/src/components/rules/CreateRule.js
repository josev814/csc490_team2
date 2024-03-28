import React from "react";

export default function CreateRule() {
    return(
        <div className="container mt-5">
            <h2 className="mb-4">Add Rule</h2>
            <form>
                <div className="mb-3">
                    <label htmlFor="ruleName" className="form-label">Rule Name</label>
                    <input type="text" className="form-control" id="ruleName" placeholder="Enter rule name" />
                </div>
                <div className="mb-3">
                    <label htmlFor="trigger" className="form-label">Trigger</label>
                    <input type="text" className="form-control" id="trigger" placeholder="Enter trigger condition" />
                </div>
                <div className="mb-3">
                    <label htmlFor="action" className="form-label">Action</label>
                    <input type="text" className="form-control" id="action" placeholder="Enter action to perform" />
                </div>
                <div className="mb-3">
                    <label htmlFor="condition" className="form-label">Condition</label>
                    <input type="text" className="form-control" id="condition" placeholder="Enter additional condition" />
                </div>
                <button type="submit" className="btn btn-primary">Add Rule</button>
            </form>
        </div>
    )
}