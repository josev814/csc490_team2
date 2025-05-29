import React from 'react';
import LinkedInIcon from '@mui/icons-material/LinkedIn';
import Spinner from 'react-bootstrap/Spinner';
import { Link, useParams } from 'react-router';

function withParams(Component){
  const ComponentWithParams = (props) => <Component {...props} params={useParams()} />;
  
    // Give the component a display name for better debugging
    const wrappedName = Component.displayName || Component.name || 'Component';
    ComponentWithParams.displayName = `withParams(${wrappedName})`;
  
    return ComponentWithParams;
}

class TeamCards extends React.Component {
  constructor(props){
    super(props);
    this.state = {
      user: [],
      loading: true
    };
  }

  componentDidMount() {
    this.setState({ user:this.props, loading: false }); // Set loading to false here
  }

  render(){
    return (
        <div className="col-md-2 card p-4 bg-white">
        {
            this.state.loading ? (
                <div className='card-img-top'>
                    <Spinner animation="border" variant="primary" />
                </div>
            ) : (
                <>
                <img className='card-img-top' alt={this.state.user.name} src={'/images/' + this.state.user.img} />
                <div className="card-body">
                    <h4 className="card-title">{this.state.user.name}</h4>
                </div>
                <div className="card-text">
                    {this.state.user.position}
                    <br />
                    <Link to={'https://www.linkedin.com/in/' + this.state.user.linkedin} target='_blank'>
                        <LinkedInIcon />
                    </Link>
                </div>
                </>
            )
        }
        </div>
    );
  }
}

export default withParams(TeamCards);
