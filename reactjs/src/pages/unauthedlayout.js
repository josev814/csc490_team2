import { Outlet } from "react-router-dom";
import UnAuthedHeader from './blocks/unauthed_header';
import Footer from './blocks/footer';

export default function UnauthedLayout() {
  return (
    <>
      <UnAuthedHeader />
      <div className='container-fluid px-0 mx-0'>
        <main role='main' className='col-12'>
          <Outlet />
        </main>
        <Footer />
      </div>
    </>
  );
}
