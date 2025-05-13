import PropTypes from 'prop-types';
import { Outlet } from "react-router-dom";
import UnAuthedHeader from './blocks/unauthed_header';
import Footer from './blocks/footer';

export default function UnauthedLayout(props) {
  return (
    <>
      <UnAuthedHeader sitename={props.sitename} tagline={props.tagline} />
      <div className='container-fluid px-0 mx-0'>
        <main role='main' className='col-12'>
          <Outlet />
        </main>
        <Footer sitename={props.sitename} />
      </div>
    </>
  );
}

UnauthedLayout.propTypes = {
  sitename: PropTypes.string.isRequired,
  tagline: PropTypes.string,
};
