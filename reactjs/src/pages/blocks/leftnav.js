import React from "react";
import { NavLink } from "react-router-dom";
import { useEffect, useState } from 'react';
import { useLocation } from 'react-router-dom';
import {CandlestickChartOutlined, RuleOutlined, SettingsOutlined, ExitToAppOutlined} from '@mui/icons-material';

export default function LeftNav() {
    const links = [
        {'pageName': 'Home', 'path': '/rules', 'icon': <RuleOutlined />},
        {'pageName': 'Stock Search', 'path': '/stocks', 'icon': <CandlestickChartOutlined />},
        // {'pageName': 'Settings', 'path': '/settings', 'icon': <SettingsOutlined />},
        {'pageName': 'Logout', 'path': '/logout', 'icon': <ExitToAppOutlined />}
    ]

    const location = useLocation();
    const [displayText, setDisplayText] = useState({});

    useEffect(() => {
        const url = location.pathname;
        if (url === '/rules') {
            setDisplayText(
                {
                    'header': 'This is the Rules Display Page',
                    'description': [
                        'Here you can:',
                        '1. View all previously created rule',
                        '2. Access individual rule information and performance by clicking the rule name',
                        '3. Go to Create Rule form to add new rules'
                    ]
                }
            );
        } else if (url === '/rule/create') {
            setDisplayText(
                {
                    'header': 'This is the Rule Creation Page',
                    'description': [
                        'Here you can:',
                        '1. Create new rules that impose conditions on a specific stock*',
                        '*Think of it as you telling the tool "If X happens for this stock (IF condition to be met), then I want you to do Y for the balance invested in this stock (THEN condition(s) you want to be fulfiled)"'
                    ]
                }
            );
        } else if (url === '/stocks') {
            setDisplayText(
                {
                    'header': 'This is the Stocks Search Page',
                    'description': [
                        'Here you can:',
                        '1. Search for stocks listed on the market',
                        '2. Monitor the performance of individual stocks by clicking on the stock itself',
                        '3. Discover recent news articles about individual stocks'
                    ]
                }
            );
        } else if (url === '/settings') {
            setDisplayText(
                {
                    'header': 'This is the User Settings Page',
                    'description': [
                        'Here you can:',
                        '1. View information about your account',
                        '2. Edit your personal information',
                        '3. Delete your account'
                    ]
                }
            );
        } else if (url.match('^/rule/[0-9]+/')) {
            setDisplayText(
                {
                    'header': 'This is the Individual Rule Page',
                    'description': [
                        'Here you can:',
                        '1. View information about your specific rule',
                        '2. Edit information and conditions regarding the rule',
                        '3. Delete your rule'
                    ]
                }
            );
        } else {
            setDisplayText(
                {
                    'header': [],
                    'description': []
                }
            )
        }
    }, [location]);

    return (
        <nav className="col-md-2 d-none d-md-block bg-light sidebar vh-100">
            <div className="sidebar-sticky d-flex">
                <ul className="nav flex-column pt-3">
                {links.map(link => (
                    <li key={link.pageName} className="d-flex align-items-center">
                        <NavLink to={link.path} className={"text-decoration-none"}>
                            {link.icon !== undefined && link.icon} {" "}
                            {link.pageName}
                        </NavLink>
                    </li>
                ))}
                </ul>
            </div>
            <div className="d-flex align-items-center h-100">
                <div>
                    <p>{displayText.header}</p>
                    {displayText.description && displayText.description.map((line, index) => (
                        <p key={index} className="fst-italic">{line}</p>
                    ))}
                </div>
            </div>
        </nav>
    )
}