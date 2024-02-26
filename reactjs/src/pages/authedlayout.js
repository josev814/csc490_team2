import { Outlet } from "react-router-dom";
import Header from './blocks/header';
import Footer from './blocks/footer';
import LeftNav from './blocks/leftnav';

export default function AuthedLayout() {
    return (
      <>
      <Header />
      <div className='container-fluid'>
        <div className='row'>
          <LeftNav />
          <main role='main' className='col-md-9 ml-sm-auto col-lg-10 pt-3 px-4'>
              <Outlet />
          </main>
        <Footer />
        </div>
      </div>
      </>
    )
  };