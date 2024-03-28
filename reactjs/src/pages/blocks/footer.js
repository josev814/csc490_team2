import React from "react";

export default function Footer(props){
    return (
        <footer className="col-12">
            &copy; 2024 - {props.sitename}
        </footer>
    )
}