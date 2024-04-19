import React, { useState, useEffect, useCallback } from 'react';
import { AddCircleOutlineOutlined } from '@mui/icons-material';
import { Link } from 'react-router-dom';
import axios from 'axios';
import { Form } from 'react-bootstrap';
import Pagination from '../components/Pagination'; // Import the Pagination component

export default function LIST_RULES(props) {
    const { get_auth_header, django_url = 'http://localhost:8889' } = props;

    // State variables
    const [rules, setRules] = useState(null); // State for storing rules data
    const [loading, setLoading] = useState(true); // State for loading status
    const [error, setError] = useState(null); // State for error handling
    const [currentPage, setCurrentPage] = useState(1); // State for current page number
    const [totalPages, setTotalPages] = useState(1); // State for total number of pages

    // Function to fetch rules data
    const fetchRules = useCallback(async () => {
        try {
            const headers = get_auth_header();
            // Fetch rules data from the server based on current page
            const response = await axios.get(`${django_url}/rules/list/?page=${currentPage}`, { headers });

            // Check response status
            if (response.status === 200) {
                setRules(response.data.records); // Set rules data
                setTotalPages(response.data.total_pages); // Set total number of pages
            } else {
                setError('Unexpected response status'); // Handle unexpected response status
            }
        } catch (error) {
            setError('Error fetching rules'); // Handle error while fetching rules
        } finally {
            setLoading(false); // Update loading status
        }
    }, [get_auth_header, django_url, currentPage]);

    // Effect to fetch rules data when currentPage changes
    useEffect(() => {
        fetchRules();
    }, [fetchRules, currentPage]);

    // Function to handle page change
    const handlePageChange = (page) => {
        setCurrentPage(page); // Update currentPage
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
    function DisplayRule({ rules }) {
        // Check if rules exist or empty
        if (!rules || rules.length === 0) return <div>No rules found.</div>;

        return (
            <div>
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
            </div>
        );
    }    

    // Slice rules based on currentPage
    const slicedRules = rules ? rules.slice((currentPage - 1) * 8, currentPage * 8) : null;

    // Render component
    return (
        <>
            <div className="container-fluid">
                <div className="row mb-3">
                    <div className="col-md-8">
                        <h3>Total Balance:</h3>
                        {/* Display total balance */}
                        <h4 className='text-success'>$0</h4>
                        <h4 className='text-danger'>-$20</h4>
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
                {/* Display sliced rules */}
                <DisplayRule rules={slicedRules} />
                <Pagination
                    currentPage={currentPage}
                    totalPages={totalPages}
                    onPageChange={handlePageChange} // Pass the handlePageChange function as prop
                />
            </div>
        </>
    );
}