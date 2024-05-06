import React from "react";
import { Link } from "react-router-dom";

export default function UnAuthedHeader(props){
    return (
        <header className="col-12 bg-dark flex-md-nowrap p-3">
            <div className="row">
                <div className="col-md-6">
                    <h1 className="text-white">{props.sitename}</h1>
                    <h4 className="text-white">{props.tagline}</h4>
                </div>
                <div className="col-md-6 d-flex justify-content-end align-items-center">
                    <Link role="link" to='/login' className="pe-3">
                        <button role="button" className='bg-warning btn btn-lg'>Login</button>
                    </Link>
                    <Link role="link" to='/register'>
                        <button role="button" className='bg-warning btn btn-lg'>Register</button>
                    </Link>
                </div>
            </div>
        </header>
    )
}