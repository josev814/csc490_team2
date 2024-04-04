import { Outlet } from "react-router-dom";
import Header from './blocks/header';
import Footer from './blocks/footer';
import LeftNav from './blocks/leftnav';
import Cookies from 'universal-cookie';

export default function AuthedLayout(props) {
    const cookies = new Cookies(null, { path: '/' });
    const userData = cookies.get('user');

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
                <a className="ps-1" href={'/users/' + userData.id + '/'}>
                  {userData.email}
                </a>
              </div>
              <Outlet />
          </main>
        <Footer sitename={props.sitename} />
        </div>
      </div>
      </>
    )
  };