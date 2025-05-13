import React from "react";
import PropTypes from "prop-types";

export default function Header(props){
    return (
        <header className="col-12 bg-dark flex-md-nowrap p-3">
            <h1 className="text-white">{props.sitename}</h1>
            <h4 className="text-white">{props.tagline}</h4>
        </header>
    )
}

Header.propTypes = {
    sitename: PropTypes.string.isRequired,
    tagline: PropTypes.string.isRequired,
};