import React from "react";
import PropTypes from 'prop-types';

export default function Footer(props){
    return (
        <footer className="col-12">
            &copy; 2024 - {props.sitename}
        </footer>
    )
}

Footer.propTypes = {
    sitename: PropTypes.string,
}