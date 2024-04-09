import React from "react";
import { NavLink } from "react-router-dom";
import { useEffect, useState } from 'react';
import { useLocation } from 'react-router-dom';
import {CandlestickChartOutlined, RuleOutlined, SettingsOutlined, ExitToAppOutlined} from '@mui/icons-material';

export default function LeftNav() {
    const links = [
        {'pageName': 'Home', 'path': '/rules', 'icon': <RuleOutlined />},
        {'pageName': 'Stock Search', 'path': '/stocks', 'icon': <CandlestickChartOutlined />},
        {'pageName': 'Settings', 'path': '/settings', 'icon': <SettingsOutlined />},
        {'pageName': 'Logout', 'path': '/logout', 'icon': <ExitToAppOutlined />}
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

                <div style={{ position: 'relative', width: '600px', height: '800px' }}>    
                    <div style={{ position: 'absolute', bottom: '33%', fontStyle: 'italic' }}>
                        <div>{displayText}</div>
                    </div>
                </div>

                </ul>
            </div>
        </nav>
    )
}