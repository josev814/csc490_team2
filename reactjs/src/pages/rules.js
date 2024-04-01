import React from 'react';
import { AddCircleOutlineOutlined, NotificationsNoneOutlined } from '@mui/icons-material';
import { Link } from 'react-router-dom';
import Pagination from 'react-bootstrap/Pagination';
import Form from 'react-bootstrap/Form';

export default function LIST_RULES() {
    
    const rules = {
        'errors': null,
        'count': 2,
        'total': 2,
        'records':
        [
            {
                'id': 1,
                'name': 'Amazon Buy The Dips',
                'status': 0,
                'growth': 0.25,
                'return': 0.13
            },
            {
                'id': 2,
                'name': 'Apple Buy The Dips',
                'status': 1,
                'growth': 11.78,
                'return': 11.78
            }
        ]
    }

    function GetPagination(){
        let active = 2;
        let max_page = 5;
        let pagination_items = [];
        let first_pagination = false
        for (let number = 1; number <= 5; number++) {
            if (number !== 1 && first_pagination){
                pagination_items.push(
                    <>
                    <Pagination.First />
                    <Pagination.Prev />
                    </>
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
                <>
                <Pagination.Next />
                <Pagination.Last />
                </>
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

    function GetRuleLinkRoute(rule){
        let rule_route = '/rule/' + rule.rule.id + '/' + encodeURIComponent(rule.rule.name)
        return (
            <Link to={rule_route}>{rule.rule.name}</Link>
        )
    }

    function DisplayRule(){
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
                        ${rule.name}
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
                            <button className="btn btn-info btn-lg">
                                Create Rule <AddCircleOutlineOutlined />
                            </button>
                        </div>
                    </div>
                </div>
                <div className='row mb-5'>
                    <div className='col-auto'>
                        <label for='filter' className='col-form-label fw-bold'>Filters:</label>
                    </div>
                    <div className='col-auto ps-0'>
                        <select className='form-select form-control' name='filter' id='filter'>
                            <option selected value='all'>All</option>
                            <option value='active'>Active</option>
                            <option value='inactive'>Paused</option>
                        </select>
                    </div>
                    <div className='col-auto'>
                        <label for='sort' className='col-form-label fw-bold'>Sort:</label>
                    </div>
                    <div className='col-auto ps-0'>
                        <select name='sort' className='form-select form-control' id='sort'>
                            <option value={'created_asc'} selected>Created - &#9650;</option>
                            <option value={'created_desc'}>Created - &#9660;</option>
                            <option value={'return_asc'}>Return - &#9650;</option>
                            <option value={'return_desc'}>Return - &#9660;</option>
                            <option value={'return_asc'}>Growth - &#9650;</option>
                            <option value={'growth_desc'}>Growth - &#9660;</option>
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