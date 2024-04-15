import React, { useState, useEffect } from 'react';
import { AddCircleOutlineOutlined, NotificationsNoneOutlined } from '@mui/icons-material';
import { Link } from 'react-router-dom';
import Pagination from 'react-bootstrap/Pagination';
import Form from 'react-bootstrap/Form';
import axios from 'axios';


export default function LIST_RULES(props) {
    // update to pull rules from backend 
    // {{base_url}}/rules/list/
    // const rules = {
    //     'errors': null,
    //     'count': 2,
    //     'total': 2,
    //     'records':
    //     [
    //         {
    //             'id': 1,
    //             'name': 'Amazon Buy The Dips',
    //             'status': 0,
    //             'growth': 0.25,
    //             'return': 0.13
    //         },
    //         {
    //             'id': 2,
    //             'name': 'Apple Buy The Dips',
    //             'status': 1,
    //             'growth': 11.78,
    //             'return': 11.78
    //         }
    //     ]
    // }
    
    const [rules, setRules] = useState(null);

    useEffect(() => {
        async function fetchRules() {
            try {
                const headers = props.get_auth_header();
                const response = await axios.post(props.url, props.updatedFormData, { headers });
                
                // Check if response status is OK (200)
                if (response.status === 200) {
                    // Assuming the response data is an array of rules
                    setRules(response.data);
                } else {
                    console.error('Unexpected response status:', response.status);
                }
            } catch (error) {
                // Log and handle errors
                console.error('Error fetching rules:', error);
            }
        }
     
        fetchRules();
    }, [props]);
    
    function GetPagination(){
        let active = 2;
        let max_page = 5;
        let pagination_items = [];
        let first_pagination = false
        for (let number = 1; number <= 5; number++) {
            if (number !== 1 && first_pagination){
                pagination_items.push(
                    <React.Fragment key={number + "_first"}>
                        <Pagination.First key="first" />
                        <Pagination.Prev key="prev" />
                    </React.Fragment>
                )
                first_pagination = true
            }
            pagination_items.push(
                <Pagination.Item key={number} active={number === active}>
                    {number}
                </Pagination.Item>,
            );
        }
        if (active !== max_page){
            pagination_items.push(
                <React.Fragment key="next_last">
                    <Pagination.Next key="next" />
                    <Pagination.Last key="last" />
                </React.Fragment>
            )
            first_pagination = true
        }
    
        return (
            <div className='container-fluid'>
                <Pagination>
                    {pagination_items}
                </Pagination>
            </div>
        );
    }
    
    // function GetRuleLinkRoute(rule){
    //     let rule_route = '/rule/' + rule.rule.id + '/' + encodeURIComponent(rule.rule.name)
    //     return (
    //         <Link to={rule_route}>{rule.rule.name}</Link>
    //     )
    // }
    function GetRuleLinkRoute(rule) {
        let rule_route = `/rule/${rule.id}/${encodeURIComponent(rule.name)}`;
        return (
            <Link to={rule_route}>{rule.name}</Link>
        );
    }
    

    function DisplayRule(){

        if (!rules || !rules.records || rules.records.length === 0) {
            return <div>No rules found.</div>;
        }

        return (
            rules.records.map(rule => (
                <div className='row border border-light border-2 shadow-sm mb-5' key={rule.name}>
                    <div className='col-md-3'>
                        <h3>
                            <GetRuleLinkRoute rule={rule} />
                        </h3>
                    </div>
                    <div className='col-md-3'>
                        Status
                        <br />
                        <Form.Check disabled type='switch' checked={rule.status} />
                    </div>
                    <div className='col-md-3'>
                        Growth
                        <br />
                        {rule.growth}
                    </div>
                    <div className='col-md-3'>
                        Net Profit
                        <br />
                        ${rule.return}
                    </div>
                </div> 
            ))
        );
    }
    return (
        <>
            <div className="container-fluid">
                <div className="row mb-3">
                    <div className="col-md-8">
                        <h3>Total Balance:</h3>
                        <h4 className='text-success'>$0</h4>
                        <h4 className='text-danger'>-$20</h4>
                    </div>
                    <div className='col-md-4 d-flex justify-content-end'>
                        <div className='col-md-6 d-flex me-3 align-items-center justify-content-end'>
                            <button className="btn btn-outline-dark btn-lg">
                                <NotificationsNoneOutlined /> Notifications
                            </button>
                        </div>
                        <div className='col-md-6 d-flex align-items-center justify-content-end'>
                            <Link to='/rule/create'>
                                <button className="btn btn-info btn-lg">
                                    Create Rule <AddCircleOutlineOutlined />
                                </button>
                            </Link>
                        </div>
                    </div>
                </div>
                <div className='row mb-5'>
                    <div className='col-auto'>
                        <label htmlFor='filter' className='col-form-label fw-bold'>Filters:</label>
                    </div>
                    <div className='col-auto ps-0'>
                        <select className='form-select form-control' name='filter' id='filter' defaultValue='all'>
                            <option value='all'>All</option>
                            <option value='active'>Active</option>
                            <option value='inactive'>Paused</option>
                        </select>
                    </div>
                    <div className='col-auto'>
                        <label htmlFor='sort' className='col-form-label fw-bold'>Sort:</label>
                    </div>
                    <div className='col-auto ps-0'>
                        <select name='sort' className='form-select form-control' id='sort' defaultValue='created_asc'>
                            <option value='created_asc'>Created - &#9650;</option>
                            <option value='created_desc'>Created - &#9660;</option>
                            <option value='return_asc'>Return - &#9650;</option>
                            <option value='return_desc'>Return - &#9660;</option>
                            <option value='return_asc'>Growth - &#9650;</option>
                            <option value='growth_desc'>Growth - &#9660;</option>
                        </select>
                    </div>
                </div>
                <DisplayRule />
                <div className='row'>
                    <GetPagination />
                </div>
            </div>
        </>
    )
};