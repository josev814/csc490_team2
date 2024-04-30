import React, { useState, useEffect, useCallback } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';
import { Form, Spinner } from 'react-bootstrap';
import { AddCircleOutlineOutlined } from '@mui/icons-material';
import Pagination from '../components/Pagination'; // Import the Pagination component

export default function LIST_RULES(props) {
    const { get_auth_header, django_url } = props;

    // State variables
    const [rules, setRules] = useState(null); // State for storing rules data
    const [links, setLinks] = useState(null); // Sets the prev/next links
    const [loading, setLoading] = useState(true); // State for loading status
    const [error, setError] = useState(null); // State for error handling
    const [totalBalance, setTotalBalance] = useState(null);
    const [totalUserProfit, setTotalUserProfit] = useState(null);

    // Function to fetch rules data
    const fetchRules = useCallback(async (link) => {
        try {
            if (link === undefined){
                link = `${django_url}/rules/list/`
            }
            const headers = get_auth_header();
            // Fetch rules data from the server based on current page
            const response = await axios.get(link, { headers });

            // Check response status
            if (response.status === 200) {
                setRules(response.data.records); // Set rules data
                setLinks(response.data.links);
            } else {
                setError('Unexpected response status'); // Handle unexpected response status
            }
        } catch (error) {
            let errorMessage = 'An error occurred, try again later'; // Default error message
        
            if (error.response && error.response.data && error.response.data.errors && error.response.data.errors.length > 0) {
                // Use the first error message from the response
                errorMessage = error.response.data.errors[0];
            }
        
            setError(errorMessage); // Set error message
        } finally {
            setLoading(false); // Update loading status
        }               
    }, [get_auth_header, django_url]);

    // Effect to fetch rules data when currentPage changes
    useEffect(() => {
        if (django_url === undefined){
            setLoading(true);
        } else {
            fetchRules();
        }
    }, [fetchRules, django_url]);


    // Function to handle page change
    const handlePageChange = (link) => {
        fetchRules(link); // Update currentPage
    };

    // Component to render individual rule
    function GetRuleLinkRoute(props) {
        // Construct the route for each rule
        let rule_route = `/rule/${props.rule.id}/${encodeURIComponent(props.rule.name)}`;
        return (
            <Link to={rule_route}>{props.rule.name}</Link>
        );
    }

    // Component to display rules
    function DisplayRules({ rules }) {
        // Check if rules exist or empty
        if (!rules || rules.length === 0) return <div>No rules found.</div>;

        return (
            <>
                {rules.map(rule => (
                    <div className='row border border-light border-2 shadow-sm mb-5' key={rule.id}>
                        <div className='col-md-3'>
                            <h3>
                                <GetRuleLinkRoute rule={rule} />
                            </h3>
                        </div>
                        <div className='col-md-3'>
                            Status
                            <br />
                            {/* Display status switch */}
                            {rule.status ? (
                                <Form.Check disabled type='switch' checked={rule.status} />
                            ) : (
                                <Form.Check disabled type='switch' /> 
                            )}
                        </div>
                        <div className='col-md-3'>
                            Growth
                            <br />
                            {/* Display growth percentage */}
                            {rule.growth}%
                        </div>
                        <div className='col-md-3'>
                            Net Profit
                            <br />
                            {/* Display net profit */}
                            $ {rule.profit}
                        </div>
                    </div> 
                ))}
            </>
        );
    }

    //function to fetch total balance of rules
    const fetchBalance = useCallback(async (balanceLink) => {
        try {
            if (balanceLink === undefined){
                balanceLink = `${django_url}/users/get_profit_loss/`
            }
            const headers = get_auth_header();
            // Fetch rules data from the server based on current page
            const res = await axios.get(balanceLink, { headers });

            // Check response status
            if (res.status === 200) {
                setTotalBalance(res.data.record.total_balance)
                setTotalUserProfit(res.data.record.total_profit)

                console.log(res.data.record)
            } else {
                setError('Unexpected response status'); // Handle unexpected response status
            }
        } catch (error) {
            let errorMessage = 'An error occurred, try again later'; // Default error message
        
            if (error.response && error.response.data && error.response.data.errors && error.response.data.errors.length > 0) {
                // Use the first error message from the response
                errorMessage = error.response.data.errors[0];
            }
        
            setError(errorMessage); // Set error message
        }            
    }, [get_auth_header, django_url]);

    useEffect(() => {
        if (django_url === undefined){
            setLoading(true);
        } else {
            fetchBalance();
        }
    }, [fetchBalance, django_url]);

    function DisplayBalCreate() {
        
        return (
            <div className="row mb-3">
                <div className="col-md-8">
                    <h3>Total Balance:</h3>
                    {/* Display total balance */}
                    <h4 className='text-success'>${totalBalance}</h4>
                    <h3 className='fs-5'>Total User Profit:</h3>
                    <h4 className='text-success fs-5'>${totalUserProfit}</h4>
                </div>
                <div className='col-md-4 d-flex justify-content-end'>
                    <div className='col-md-6 d-flex align-items-center justify-content-end'>
                        {/* Link to create new rule */}
                        <Link to='/rule/create'>
                            <button className="btn btn-info btn-lg">
                                Create Rule <AddCircleOutlineOutlined />
                            </button>
                        </Link>
                    </div>
                </div>
            </div>
        );
    }

    if (loading) {
        return (
          <div className="container-fluid">
            <DisplayBalCreate />
            <div>
              <Spinner animation="border" variant="primary" />
            </div>
          </div>
        )
      }

    // Component to render error state
    if (error) {
        return (
          <div className="container-fluid">
            <DisplayBalCreate />
            <div>{error}</div>
          </div>
        )
    }

    // Render component
    return (
        <>
            <div className="container-fluid">
                <DisplayBalCreate />
                <div id='displayRules'>
                    <DisplayRules rules={rules} />
                    <Pagination
                        onPageChange={handlePageChange} // Pass the handlePageChange function as prop
                        links={links}
                        target_element='displayRules'
                    />
                </div>
            </div>
        </>
    );
}