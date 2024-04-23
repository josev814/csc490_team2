import React, { useState } from 'react';
import axios from 'axios';
import Cookies from 'universal-cookie'
import Cookies from 'universal-cookie'
import { EditOutlined, ContentCopyOutlined, DeleteOutline, ArrowBackIosOutlined } from '@mui/icons-material';
import { useNavigate, useParams } from 'react-router-dom';
import Modal from 'react-bootstrap/Modal';
import ShowRuleTransactionChart from '../components/rules/rule_chart';
import CreateRuleForm from '../components/rules/CreateRule'

export function SHOW_RULE(props) {
    const {rule, rule_name} = useParams()
    const navigate = useNavigate()

    function get_auth_header(){
        const token = localStorage.getItem('accessToken')
        const headers = {
            Authorization: `Bearer ${token}`,
        }
        return headers
    }

    const [showModal, setShow] = useState(false);
    const handleClose = () => setShow(false);
    const handleShow = () => setShow(true);

    async function handleDelete() {
        const delete_url = `${props.sitedetails.django_url}/rules/delete/${rule}/`
        try {
            const response = await axios.delete(delete_url, { headers: get_auth_header() });
            switch (response.status) {
                case 204:
                    navigate('/rules/')
                    break;
                case 404:
                    showToastError('Record not found to delete')
                    break;
                default:
                    break;
            }
        } catch(error){
            showToastError(error)
        }
    }
    const toastContainer = document.getElementById('toastContainer')

    function showToastError(message) {    
        // Create the toast element
        const toastElement = document.createElement('div');
        toastElement.className = 'toast show'; // Set the class name
        toastElement.setAttribute('role', 'alert');
        toastElement.setAttribute('aria-live', 'assertive');
        toastElement.setAttribute('aria-atomic', 'true');
        toastElement.setAttribute('data-bs-autohide', 'true');
        toastElement.setAttribute('data-bs-delay', 5000);
    
        // Create the inner content of the toast element
        const toastContent = document.createElement('div');
        toastContent.className = 'toast-body bg-danger text-white';
        toastContent.textContent = message;
    
        // Construct the inner HTML content
        const toastHeader = `
            <div class="toast-header">
                <strong class="me-auto text-danger">Error</strong>
                <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Close"></button>
            </div>
        `;
    
        // Set the inner HTML content of the toast element
        toastElement.innerHTML = toastHeader;
        toastElement.appendChild(toastContent);
    
        // Append the toast element to the toast container
        toastContainer.appendChild(toastElement);
    }
    
    
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
        let value = undefined
        switch (operator.operator) {
            case 'gt':
                value = '>'
                break
            case 'gte':
                value = '>='
                break
            case 'lt':
                value = '<'
                break
            case 'lte':
                value = '<='
                break
            default:
                value = '='
                break
        }
        return value
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
                <Modal show={showModal} onHide={handleClose}>
                    <Modal.Header closeButton>
                        <Modal.Title>Delete Rule {rule_name} ({rule})</Modal.Title>
                    </Modal.Header>
                    <Modal.Body>
                        Are you sure you want to delete this rule?
                    </Modal.Body>
                    <Modal.Footer>
                    <button className='btn btn-secondary' onClick={handleClose}>
                        Cancel
                    </button>
                    <button className="btn btn-danger" onClick={handleDelete}>
                        Delete
                    </button>
                    </Modal.Footer>
                </Modal>
                <div className='row'>
                    <div className='col-1'>
                        <button className="btn btn-warning btn-md" onClick={() => navigate(-1)}>
                            <ArrowBackIosOutlined />
                        </button>
                    </div>
                    <div className='col-11'>
                        <h1>{rule_name}</h1>
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
                            <button className="btn btn-danger btn-md" onClick={handleShow}>
                                <DeleteOutline /> Remove
                            </button>
                        </div>
                    </div>
                </div>
                <div className="row border border-light border-2 shadow-sm mb-5">
                    <h2>Performance</h2>
                    <ShowRuleTransactionChart />
                    {/* ^ pass symbol and transactions that are loaded from request */}
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


export function CREATE_RULE(props){
    const navigate = useNavigate()
    const cookies = new Cookies(null, { path: '/' })

    function get_auth_header(){
        const token = localStorage.getItem('accessToken')
        const headers = {
            Authorization: `Bearer ${token}`,
        }
        return headers
    }

    function refresh_login_cookie() {
        // Calculate expiration time for the login status cookie (30 minutes)
        const loginStatusExpiration = new Date();
        loginStatusExpiration.setTime(loginStatusExpiration.getTime() + (0.5 * 60 * 60 * 1000));
        
        // Check if 'is_active' cookie exists
        const is_active = cookies.get('is_active');
        if (is_active) {
            // Log the current value of 'is_active' (optional for debugging)
            console.log("Current 'is_active' value:", is_active);
            
            // Update the expiration time of the 'is_active' cookie
            cookies.set('is_active', is_active, { expires: loginStatusExpiration });
        } else {
            console.error("User is not logged in.");
            navigate('/login')
        }
    }    

    async function refresh_token() {
        try {
            const refresh_url = `${props.django_url}/auth/refresh/`;
            const data = {'refresh': localStorage.getItem('refreshToken')};
            
            // Send POST request to refresh URL
            const response = await axios.post(refresh_url, data, { headers: get_auth_header() });
    
            // Check if response is successful
            if (response.status === 200) {
                // Update tokens in local storage
                localStorage.setItem('accessToken', response.data.access);
                localStorage.setItem('refreshToken', response.data.refresh);
                
                // Refresh login cookie
                refresh_login_cookie();
            } else {
                // Handle unexpected response status codes
                console.error('Unexpected response status:', response.status);
            }
        } catch (error) {
            // Handle network errors or other exceptions
            console.error('Error refreshing token:', error);
            // Optionally, navigate to login page or handle the error
        }
    }
    

    function get_user_from_cookie(){
        const userCookie = cookies.get('user');
        if (!userCookie || !userCookie.id) {
            console.error("User cookie or user ID not found.");
            return null; // or handle the error appropriately
        }
    
        // Construct user URL based on user ID
        const user_id = userCookie.id;
        const user_url = `${props.django_url}/users/${user_id}/`;
        return user_url;
    }

    const handleSubmit = async (e) => {
        e.preventDefault();
        const url = `${props.django_url}/rules/`
        await refresh_token()

        const updatedFormData = {
            ...formData,
            user: get_user_from_cookie(),
        };

        setFormData(updatedFormData);
        try {
            const headers = get_auth_header()
            const response = await axios.post(url, updatedFormData, {headers})
            console.log(response)
            if (response.status === 200 || response.status === 201) {
                const rule_id = response.data.id
                const rule_name = response.data.name
                navigate(`/rule/${rule_id}/${rule_name}/`);
            } else {
                console.log('Failed to create rule')
                throw new Error('Failed to create rule');
            }
        }
        catch (error) {
            if (error.response && error.response.status === 409) {
                setErrorMessage("Rule already exists");
                console.log(errorMessage);
            } else {
                setErrorMessage(`${error.response.status}: ${error}`);
                console.log(errorMessage);
            }
        }
    };

    const handleChange = (e) => {
        console.log(e.target.name)
        if (['name'].indexOf(e.target.name) !== -1 ){
            setFormData({ ...formData, [e.target.name]: e.target.value });
        } else if (['initial_investment'].indexOf(e.target.name) !== -1 ){
            setFormData({ ...formData, [e.target.name]: e.target.value + '.00' });
        } else {
            // parse the rule to a json rule

            //TODO: wire rule input into json object, that goes to rule state, commit  
        }
    };
    
    return (
        <CreateRuleForm 
            handleSubmit={(e) => handleSubmit(e)}
            handleChange={(e) => handleChange(e)}
            django_url={props.django_url}
        />
    )
}