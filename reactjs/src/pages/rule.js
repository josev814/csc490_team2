import React from 'react';
import { EditOutlined, ContentCopyOutlined, DeleteOutline, ArrowBackIosOutlined } from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import ShowRuleTransactionChart from '../components/rules/rule_chart';

export default function SHOW_RULE() {
    const navigate = useNavigate()
    
    const return_data = {
        'errors': null,
        'rule':
            {
                'id': 1,
                'created_date': '2024-03-22 08:40:23.1123',
                'name': 'Amazon Buy The Dips',
                'status': 0,
                'initial_investment': 20,
                'growth': 0.25,
                'return': -20.13,
                'rule': {
                    'checks': [{
                        'conditions': 
                        [
                            {
                                'condition': 'if',
                                'symbol': {'id':1,'ticker':'amzn'},
                                'data': 'price',
                                'operator': 'gt',
                                'value': 10
                            },
                            {
                                'condition': 'and',
                                'symbol': {'id':1,'ticker':'amzn'},
                                'data': 'open',
                                'operator': 'lte',
                                'value': 6
                            }
                        ],
                        'action': {
                            'method': 'buy',
                            'quantity': 5,
                            'symbol': {'id':1,'ticker':'amzn'},
                            'order_type': 'limit'
                        }
                    }]
                },
                'transactions': {
                    'count': 5,
                    'columns': ['id', 'action','datetime','quantity', 'price'],
                    'records':[
                        [ 1, 'sell', '2024-03-22 08:40:23.1123', 5, 10 ],
                        [ 2, 'sell', '2024-03-22 08:40:23.1123', 5, 11 ],
                        [ 3, 'sell', '2024-03-22 08:40:23.1123', 5, 14 ],
                        [ 4, 'sell', '2024-03-22 08:40:23.1123', 5, 8 ],
                        [ 5, 'sell', '2024-03-22 08:40:23.1123', 5, 6 ]
                    ]
                }
            }
    }

    function GetOperator(operator){
        switch (operator.operator) {
            case 'gt':
                return ('>')
            case 'gte':
                return ('>=')
            case 'lt':
                return ('<')
            case 'lte':
                return ('<=')
            default:
                break;
        }
    }

    function DisplayCondition(content){
        let data = content.content
        return (
            <span>
                <b className='text-info'>{data.condition.toUpperCase()}</b>{' '}
                <b>{data.symbol.ticker.toUpperCase()}</b>{' has '}
                <b>{data.data.toUpperCase()}</b>{' '}
                <b><GetOperator operator={data.operator} /></b>{' '}
                <b>{data.value}</b>
            </span>
        )
    }

    function DisplayAction(content){
        let data = content.content
        return (
            <span>
                <b className='text-danger'>THEN </b>
                <b className='text-primary'>{data.method.toUpperCase()}</b>{' '}
                <b>{data.quantity}</b>{' of '}
                <b>{data.symbol.ticker.toUpperCase()}</b>{' as '}
                <b>{data.order_type}</b>{' order '}
            </span>
        )
    }

    function DisplaySequence(){
        if(return_data.rule.rule.checks.length > 0){
            return (
                <>
                {return_data.rule.rule.checks[0].conditions.map(condition => (
                    <div className='row' key={condition.condition}>
                        <DisplayCondition content={condition} />
                    </div>
                ))}
                <DisplayAction content={return_data.rule.rule.checks[0].action} />
                </>
            )
        } else if (return_data.errors) {
            <div className='row'>
                {return_data.errors.map(error => (
                    error
                ))}
            </div>
        } else {
            return (
                <div className='row'>
                    No Items Found
                </div>
            );
        }
    }

    function DisplayTransactionColumns(){
        // Check if rule.rule.transactions[0] exists and is an object
        if (return_data.rule.transactions.columns) {
            return (
                <div className='row border border-light border-2'>
                    {return_data.rule.transactions.columns.map(column => (
                        <div className='col-md-2' key={column}>
                            <b>{column.toUpperCase()}</b>
                        </div>
                    ))}
                </div>
            );
        } else {
            return null; // Handle case when rule.rule.transactions[0] is not an object
        }
    }

    function DisplayTransactions(){
        if (return_data.rule.transactions.count > 0) {
            return (
                return_data.rule.transactions.records.map(transaction => (
                    <div className='row border border-light border-1' key={transaction[0]}>
                        <div className='col-md-2'>
                            {transaction[0]}
                        </div>
                        <div className='col-md-2'>
                            {transaction[1]}
                        </div>
                        <div className='col-md-2'>
                            {transaction[2]}
                        </div>
                        <div className='col-md-2'>
                            {transaction[3]}
                        </div>
                        <div className='col-md-2'>
                            {transaction[4]}
                        </div>
                    </div> 
                ))
            );
        } else {
            return (
                <div className='row'>
                    <h4>No transactions found</h4>
                </div>
            );
        }
    }

    function DisplayBalance(){
        let balance = return_data.rule.initial_investment + return_data.rule.return
        let className = 'text-success'
        if (balance < 0){
            className = 'text-danger'
        }
        return (
            <h4 className={className}>${balance.toFixed(2)}</h4>
        )
    }

    function DisplayStatus(data){
        let status = data.status
        if (status === 0){
            return (
                <span className='text-danger'>Disabled</span>
            )
        }
        return (
            <span className='text-success'>Enabled</span>
        )
    }


    return (
        <>
            <div className="container-fluid">
                <div className='row'>
                    <div className='col-1'>
                        <button className="btn btn-warning btn-md" onClick={() => navigate(-1)}>
                            <ArrowBackIosOutlined />
                        </button>
                    </div>
                    <div className='col-11'>
                        <h1>{return_data.rule.name}</h1>
                    </div>
                </div>
                <div className="row mb-3">
                    <div className="col-md-8">
                        <h3>Total Balance:</h3>
                        <DisplayBalance />
                    </div>
                    <div className='col-md-4 d-flex justify-content-end'>
                        <div className='col-md-4 d-flex me-3 align-items-center justify-content-end'>
                            <button className="btn btn-warning btn-md">
                                <EditOutlined /> Edit
                            </button>
                        </div>
                        <div className='col-md-4 d-flex me-3 align-items-center justify-content-end'>
                            <button className="btn btn-warning btn-md">
                                <ContentCopyOutlined /> Duplicate
                            </button>
                        </div>
                        <div className='col-md-4 d-flex align-items-center justify-content-end'>
                            <button className="btn btn-danger btn-md">
                                <DeleteOutline /> Remove
                            </button>
                        </div>
                    </div>
                </div>
                <div className="row border border-light border-2 shadow-sm mb-5">
                    <h2>Performance</h2>
                    <ShowRuleTransactionChart />
                </div>
                <div className="row border border-light border-2 shadow-sm mb-5">
                    <div className='col-md-6'>
                        <h4>Rule Information</h4>
                        <div><b>Start:</b> {return_data.rule.created_date}</div>
                        <div><b>Transactions:</b> {return_data.rule.transactions.count}</div>
                        <div><b>Growth:</b> {return_data.rule.growth}</div>
                        <div><b>Return:</b> ${return_data.rule.growth}</div>
                        <div><b>Status:</b> <DisplayStatus data={return_data.rule.status} /></div>
                    </div>
                    <div className='col-md-6'>
                        <h4>Sequence</h4>
                        <DisplaySequence />
                    </div>
                </div>
                <div className="row border border-light border-2 shadow-sm mb-5">
                    <div className='container-fluid'>
                        <h2>Transactions</h2>
                        <DisplayTransactionColumns />
                        <DisplayTransactions />
                    </div>
                </div>
            </div>
      </>
    )
  };