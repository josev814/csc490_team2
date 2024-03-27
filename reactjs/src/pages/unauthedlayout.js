import { Outlet } from "react-router-dom";
import Header from './blocks/header';
import Footer from './blocks/footer';

export default function UnauthedLayout() {
    return (
      <>
      <Header />
      <div className='container-fluid px-0 mx-0'>
        <main role='main' className='col-12'>
            <Outlet />
        </main>
        <Footer />
      </div>
      </>
    )
  };