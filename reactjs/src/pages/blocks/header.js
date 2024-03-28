import React from "react";

export default function Header(props){
    return (
        <header className="col-12 sticky-top bg-dark flex-md-nowrap p-3">
            <h1 className="text-white">{props.sitename}</h1>
            <h4 className="text-white">{props.tagline}</h4>
        </header>
    )
}