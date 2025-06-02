import React from "react";
import PropTypes from 'prop-types';

export default function Footer(props){
    return (
        <footer data-testid="site-footer" className="col-12">
            &copy; 2024 - {new Date().getFullYear()} | {props.sitename}
        </footer>
    )
}

Footer.propTypes = {
    sitename: PropTypes.string,
}