import PropTypes from 'prop-types';
import { Outlet, useNavigate, Link } from "react-router";
import { useEffect, useState } from "react";
import Header from './blocks/header';
import Footer from './blocks/footer';
import LeftNav from './blocks/leftnav';
import Cookies from 'universal-cookie';

export default function AuthedLayout(props) {
    const navigate = useNavigate();
    const [userData, setUserData] = useState(undefined);
    useEffect(() => {
        const cookies = new Cookies(null, { path: '/' })

        function stillLoggedIn() {
            const active = cookies.get('is_active');
            if (!active) {
                console.log('Redirect to login');
                navigate('/login/');
            }
        }

        function getUserCookieData() {
            const user = cookies.get('user');
            setUserData(user);
            if (!user) {
                console.log('Redirect to login');
                navigate('/login/');
            }
        }
        getUserCookieData();
        stillLoggedIn();
        const interval = setInterval(() => {
            stillLoggedIn(); // Call every 5 minutes
        }, 5 * 60 * 1000); // 5 minutes in milliseconds

        return () => clearInterval(interval); // Cleanup function to clear interval
    }, [navigate]);

    return (
        <>
            <Header sitename={props.sitename} tagline={props.tagline} />
            <div id='toastContainer' className="position-fixed bottom-0 end-0 p-3" style={{ zIndex: 9999 }}>
            </div>
            <div className='container-fluid'>
                <div className='row'>
                    <LeftNav />
                    <main role='main' className='col-md-9 ml-sm-auto col-lg-10 pt-3 px-4'>
                        <div className="justify-content-end d-flex container-fluid">
                            User:
                            <Link className="ps-1" to={userData ? '/users/' + userData.id + '/' : '#'}>
                                {userData ? userData.email : ''}
                            </Link>
                        </div>
                        <Outlet />
                    </main>
                    <Footer sitename={props.sitename} />
                </div>
            </div>
        </>
    );
}

AuthedLayout.propTypes = {
    sitename: PropTypes.string,
    tagline: PropTypes.string,
}