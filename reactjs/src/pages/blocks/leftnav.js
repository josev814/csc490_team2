import React from "react";
import { NavLink } from "react-router-dom";

export default function LeftNav() {
    const links = [
        {'pageName': 'Home', 'path': '/rules'},
        {'pageName': 'Stocks', 'path': '/stocks'},
        {'pageName': 'Settings', 'path': '/settings'},
        {'pageName': 'Logout', 'path': '/logout'}
    ]
    return (
        <nav className="col-md-2 d-none d-md-block bg-light sidebar">
            <div className="sidebar-sticky">
                <ul className="nav flex-column">
                {links.map(link => (
                    <li key={link.pageName}>
                        <NavLink to={link.path}>{link.pageName}</NavLink>
                    </li>
                ))}
                </ul>
            </div>
        </nav>
    )
}