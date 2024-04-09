import React from "react";
import { NavLink } from "react-router-dom";
import { useEffect, useState } from 'react';
import { useLocation } from 'react-router-dom';

export default function LeftNav() {
    const links = [
        {'pageName': 'Home', 'path': '/rules'},
        {'pageName': 'Stock Search', 'path': '/stocks'},
        {'pageName': 'Settings', 'path': '/settings'},
        {'pageName': 'Logout', 'path': '/logout'}
    ]

    const location = useLocation();
    const [displayText, setDisplayText] = useState('');

    useEffect(() => {
        const url = location.pathname;
        if (url === '/rules') {
            setDisplayText(
                <>
                <div>This is the Rules Display Page</div>
                <div>Here you can:</div>
                <div>1. View all previously created rule</div>
                <div>2. Access individual rule information and</div>
                <div>performance by clicking the rule name</div>
                <div>3. Go to Create Rule form to add new rules</div>
                </>
            );
        } else if (url === '/rule/create') {
            setDisplayText(
                <>
                <div>This is the Rule Creation Page</div>
                <div>Here you can:</div>
                <div>1. Create new rules that impose</div>
                <div>conditions* on a specific stock**</div>
                <div>*Think of it as you telling the</div>               
                <div>the tool "If X happens for Y </div>
                <div>stock, then I want you to do X</div>                
                <div>for Y stock." and then</div>
                <div>*Think of it as you telling the</div>

                </>
            );
        } else if (url === '/stocks') {
            setDisplayText(
                <>
                <div>This is the Stocks Search Page</div>
                <div>Here you can:</div>
                <div>1. Search for stocks listed on the market</div>
                <div>2. Monitor the performance of individual</div>
                <div>stocks by clicking on the stock itself</div>
                <div>3. Discover recent news articles about</div>
                <div>individual stocks</div>
                </>
            );
        } else if (url === '/settings') {
            setDisplayText(
                <>
                <div>This is the User Settings Page</div>
                <div>Here you can:</div>
                <div>1. View information about your account</div>
                <div>2. Edit your personal information</div>
                <div>3. Delete your account</div>
                </>
            );
        } else {
            setDisplayText('Default')
        }
    }, [location]);
    return (
        <nav className="col-md-2 d-none d-md-block bg-light sidebar">
            <div className="sidebar-sticky d-flex vh-100">
                <ul className="nav flex-column">
                {links.map(link => (
                    <li key={link.pageName}>
                        <NavLink to={link.path}>{link.pageName}</NavLink>
                    </li>
                ))}

                <div>
                    <div class="fst-italic">
                        {displayText}
                    </div>
                </div>

                </ul>
            </div>
        </nav>
    )
}