import PropTypes from "prop-types";
import { NavLink } from "react-router-dom";

export default function UnAuthedHeader(props){
    return (
        <header className="col-12 bg-dark flex-md-nowrap p-3">
            <div className="row">
                <div className="col-md-6">
                    <h1>
                    <NavLink to='/' className={"text-decoration-none text-white"}>
                        {props.sitename}
                    </NavLink>
                    </h1>
                    <h4 className="text-white">{props.tagline}</h4>
                </div>
                <div className="col-md-6 d-flex justify-content-end align-items-center">
                    <NavLink role="link" to="/login" className="pe-3">
                        <button className="bg-warning btn btn-lg">Login</button>
                    </NavLink>
                    <NavLink role="link" to="/register">
                        <button className="bg-warning btn btn-lg">Register</button>
                    </NavLink>
                </div>
            </div>
        </header>
    )
}

UnAuthedHeader.propTypes = {
    sitename: PropTypes.string,
    tagline: PropTypes.string,
}