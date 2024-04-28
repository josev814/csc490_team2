import React, {useState, useEffect} from "react";
import { useNavigate } from "react-router";
import axios from 'axios';
import Cookies from 'universal-cookie'
import { AsyncDropDown } from "../inputs/AsyncDropDown";
import Spinner from "react-bootstrap/Spinner";

function RemoveRow(props){
    if (props.event !== 1 ) {
        return (
            <button className="btn btn-danger" onClick={() => props.removeRowCondition({'event':props.event})}>
                Remove Condition
            </button>
        )
    }
    return null;
}

function AddRowCondition(props){
    const event_data = [
        {value:'price', label: 'Current Price'},
        {value:'open', label: 'Open Price'},
        {value:'high', label: 'High Price'},
        {value:'low', label: 'Low Price'},
        {value:'close', label: 'Close Price'}
    ]
    const event_operators = [
        {value:'gt', label: 'greater than'},
        {value:'gte', label: 'greater than or equal to'},
        {value:'lt', label: 'less than'},
        {value:'lte', label: 'less than or equal to'},
        {value:'eq', label: 'equal to'},
    ]
    console.log(props);
    return (
        <div className="row px-2 py-3" id={"condition_" + props.event}>
            <div className="col">
                <div className="row">
                    <span className="h5">{props.event === 1 ? 'IF' : 'AND'}:</span>
                    <input type='hidden' name={'event_condition_' + props.event} aria-hidden aria-readonly value={props.event === 1 ? 'if' : 'and'} />
                </div>
                <div className="row shadow py-3 px-2">
                    <div className="col-md-3">
                        <AsyncDropDown name={'event_symbol_' + props.event} handleChange={props.handleChange} django_url={props.django_url} value={props.condition.symbol} />
                    </div>
                    <div className="col-auto">
                        HAS 
                    </div>
                    <div className="col-auto">
                        <select required aria-required name={'event_data_' + props.event} className="form-select" onChange={props.handleChange} value={props.condition.data}>
                            <option value=''>---</option>
                            {event_data.map((item, index) =>
                                <option key={index} value={item.value}>{item.label}</option>
                            )}
                        </select>
                    </div>
                    <div className="col-auto">
                        <select required aria-required name={'event_operator_' + props.event} className="form-select" onChange={props.handleChange} value={props.condition.operator}> 
                            <option value=''>---</option>
                            {event_operators.map((item, index) =>
                                <option key={index} value={item.value}>{item.label}</option>
                            )}
                        </select>
                    </div>
                    <div className="col-auto">
                        <input 
                            required aria-required 
                            type="text" 
                            pattern='^\d+(\.\d{2})?$' 
                            name={'event_value_' + props.event} 
                            className="form-control" 
                            placeholder="Comparison Value $"  
                            onChange={props.handleChange} 
                            value={props.condition.value}
                        />
                    </div>
                    <div className="col-auto">
                        <RemoveRow event={props.event} removeRowCondition={props.removeRowCondition} />
                    </div>
                </div>
            </div>
        </div>
    )
}


export default function EditRuleForm(props) {
    const navigate = useNavigate();
    const cookies = new Cookies(null, { path: '/' })
    const [formData, setFormData] = useState({
        user: "",
        name: "",
        initial_investment: 0.0,
        rule: {},
        start_date: "",
        is_active: true
    });
    const [loading, setLoading] = useState(true)
    const [inputs, setInputs] = useState({})
    const [action, setAction] = useState({}); // State to manage the action
    const [conditions, setConditions] = useState([]); // State to manage rule conditions
    const [conditionCount, addConditionCount] = useState(1); // State to manage rule conditions
    const [trigger, setTrigger] = useState({}); // State to manage the action
    const [errorMessage, setErrorMessage] = useState(""); // State to manage error message
    
    const then_methods = [
        {value:'buy', label: 'Buy'},
        {value: 'sell', label: 'Sell'},
        // {value: 'notify', label: 'Notify'}
    ]
    const then_qty_types = [
        {value:'usd', label: 'USD'},
        {value: 'shares', label: 'Share(s)'},
    ]
    const exec_frequencies = [
        {value:'minutes', label: 'minutes(s)'},
        {value:'hours', label: 'Hour(s)'},
        {value:'days', label: 'Day(s)'}
    ]

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
        const url = `${props.django_url}/rules/update/${props.rule}`;
    
        const updatedFormData = {
            ...formData,
            user: get_user_from_cookie(),
        };
    
        setFormData(updatedFormData);
        try {
            const headers = props.get_auth_header();
            const response = await axios.put(url, updatedFormData, { headers });
            if (response.status === 200 || response.status === 201) {
                const rule_id = response.data.id;
                const rule_name = response.data.name;
                navigate(`/rule/${rule_id}/${rule_name}/`);
            } else {
                console.error('Failed to update rule');
                throw new Error('Failed to update rule');
            }
        } catch (error) {
            if (error.response && error.response.status === 409) {
                setErrorMessage("Rule already exists");
            } else {
                setErrorMessage(`${error.response.status}: ${error}`);
            }
            console.log(errorMessage);
        }
    };
    

    const addRowCondition = () => {
        addConditionCount(conditionCount + 1)
    }

    const removeRowCondition = (params) => {
        console.groupCollapsed('removeRow')
        console.log(params)
        console.log('condition_' + params.event)
        function remove_html_element(idx){
            const element = document.getElementById('condition_' + idx)
            console.log(element)
            if (element) {
                element.remove()
            }
        }
        function empty_condition(idx){
            let form_conditions = [...conditions]
            form_conditions[(idx - 1)] =  {}
            setConditions(form_conditions)
        }
        remove_html_element(params.event)
        empty_condition(params.event)
        console.groupEnd()
    }

    const parse_form_rule_action = (event) => {
        let field_prefix = 'then_'
        if (event.target.name.startsWith(field_prefix)){
            if (event.target.name.includes('symbol')){
                let symbol_info = event.target.value.split('|');
                let value = {'id': symbol_info[0], 'ticker': symbol_info[1]}
                setAction({...action, [event.target.name.replace(field_prefix, '')]: value})
            } else {
                setAction({...action, [event.target.name.replace(field_prefix, '')]: event.target.value})
            }
        }
    }

    const parse_form_rule_events = (event) => {
        const event_fields = ['condition', 'symbol', 'data', 'operator', 'value']
        
        // parse the rule to a json rule
        let form_conditions = [...conditions]

        let symbol_info = undefined
        let field_prefix = 'event_'
        let name_segments = event.target.name.split('_')
        let name_segments_size = name_segments.length
        let condition_index = name_segments[name_segments_size - 1] - 1
        let key = undefined
        let value = undefined
        
        if (event.target.name.startsWith(field_prefix)){
            event_fields.forEach(field => {
                if (event.target.name.indexOf(field) !== -1){
                    key = field
                    return // break out of for loop
                }
            });
            if (event.target.name.includes('symbol')){
                symbol_info = event.target.value.split('|');
                value = {'id': symbol_info[0], 'ticker': symbol_info[1]}
            } else {
                value = event.target.value
            }

            if (form_conditions.length > condition_index){
                let condition = {...form_conditions[condition_index], [key]: value}
                form_conditions[condition_index] = condition
            } else {
                let ifand = document.getElementsByName(
                    'event_condition_' + (condition_index + 1)
                )[0].value
                form_conditions.push({
                    [key]: value,
                    'condition': ifand
                })
            }
            setConditions(form_conditions)
        }
    }

    const parse_form_rule_interval = (event) => {
        let field_prefix = 'exec_'
        if (event.target.name.startsWith(field_prefix)){
            setTrigger({...trigger, [event.target.name.replace(field_prefix, '')]: event.target.value})
        }
    }
    
    const handleChange = (e) => {
        if (['name', 'start_date'].indexOf(e.target.name) !== -1 ){
            setInputs({...inputs, [e.target.name]: e.target.value})
            //setFormData({ ...formData, [e.target.name]: e.target.value });
        } else if ('initial_investment' === e.target.name ){
            setInputs({
                ...inputs,
                [e.target.name]: e.target.value + '.00',
                'balance': e.target.value + '.00'
            })
            //setFormData({ ...formData, [e.target.name]: e.target.value + '.00' });
        } else if (e.target.name.startsWith('then_')){
            parse_form_rule_action(e)
        } else if (e.target.name.startsWith('event_')){
            parse_form_rule_events(e)
        } else if (e.target.name.startsWith('exec_')){
            parse_form_rule_interval(e)
        } else {
            console.warn('Unknown field that needs handling: ' + e.target.name)
        }
    };

    // Build the formData when the states change
    useEffect(() => {
        if(!loading){
            const validConditions = conditions.filter(condition => Object.keys(condition).length > 4);
            const json_rule = {'conditions': validConditions, 'action': action, 'trigger': trigger};
            setFormData( prevFormData => ({ ...prevFormData, 'rule': json_rule, ...inputs }));
            console.groupEnd()
        }
        return () => {} // function cleanup
    }, [loading, conditions, action, trigger, inputs]);

    useEffect(() => {
        const recordInfo = JSON.parse(localStorage.getItem('user_rule')).record;
        const inputFields = ['name', 'start_date', 'initial_investment'];
    
        // Update input fields state
        const updatedInputs = {};
        inputFields.forEach(input => {
            updatedInputs[input] = recordInfo[input];
        });
        setInputs(updatedInputs);
    
        // Set action and conditions states
        setAction(recordInfo.rule.action);
        setConditions(recordInfo.rule.conditions);
        setTrigger(recordInfo.rule.trigger);
        console.log(recordInfo.rule.conditions);
        setLoading(false); // Set loading to false after retrieving and setting data
    }, []);

    if (loading){
        return (
            <div className="container-fluid">
                <Spinner animation="border" variant="primary" />
            </div>
        )
    }

    return (
        <div className="container-fluid">
            <h2 className="mb-4">Edit Rule</h2>
            <form className="form" onSubmit={handleSubmit}>
            <div className="row mb-3">
                <label htmlFor="name" className="form-label">Name:</label>
                <input 
                    type="text" 
                    className="form-control" 
                    name="name" 
                    id="name" 
                    placeholder="Enter rule name" 
                    value={inputs.name}  // Bind value to state variable
                    onChange={handleChange} 
                />
            </div>
            <div className="row mb-3">
                <label htmlFor="initial_investment" className="form-label">Initial Investment:</label>
                <div className="input-group">
                    <div className="input-group-prepend">
                        <span className='input-group-text'>$</span>
                    </div>
                    <input type="text" className="form-control" name="initial_investment" id="initial_investment" placeholder="Enter your initial investment" value={inputs.initial_investment}  readOnly  />
                    <div className="input-group-append">
                        <span className='input-group-text'>.00</span>
                    </div>
                </div>
            </div>
            <div className="row mb-3">
                <input 
                    label='Start Date' 
                    description='The date that the rule should start evaluating from' 
                    id='start_date' 
                    name='start_date' 
                    type='date'
                    handleChange={handleChange} 
                    defaultValue={inputs.start_date}  // Bind value to state variable
                />
            </div>
                <div className="conditions">
                    {Array.from({ length: conditionCount }).map((_, index) => (
                        <AddRowCondition 
                            key={index} 
                            event={index + 1} 
                            handleChange={handleChange} 
                            django_url={props.django_url} 
                            removeRowCondition={removeRowCondition} 
                            condition={conditions[index]}
                        />
                    ))}
                </div>
                <div className="row mb-3">
                    <button className="btn btn-success" onClick={() => addRowCondition()}>Add Another Condition</button>
                </div>
                <div className="row mb-3 px-2 py-3">
                    <div className="col">
                        <div className="row">
                            <span className="h5">THEN: <span className="lead">
                                    Perform the following action
                                </span>
                            </span>
                        </div>
                        <div className="row shadow px-2 py-3">
                            <div className="col-auto">
                                <select required aria-required name='then_method' className="form-select" onChange={handleChange} value={action.method}>
                                    <option value=''>---</option>
                                    {then_methods.map((item, index) =>
                                        <option key={index} value={item.value}>{item.label}</option>
                                    )}
                                </select>
                            </div>
                            <div className="col-auto">
                                <input type="text" name='then_quantity' className="form-control" placeholder="Quantity"  onChange={handleChange} value={action.quantity}/>
                            </div>
                            <div className="col-auto">
                                <select required aria-required name='then_quantity_type' className="form-select" onChange={handleChange} value={action.quantity_type}>
                                    <option value=''>---</option>
                                    {then_qty_types.map((item, index) =>
                                        <option key={index} value={item.value}>{item.label}</option>
                                    )}
                                </select>
                            </div>
                            <div className="col-auto">
                                OF
                            </div>
                            <div className="col-md-3">
                                <AsyncDropDown name='then_symbol' handleChange={handleChange}  django_url={props.django_url}/>
                            </div>
                        </div>
                    </div>
                </div>
                <div className="row px-2 py-3">
                    <div className="col">
                        <div className="row">
                            <span className="h5">
                                EXECUTION: <span className="lead">
                                    Execute the rule no more frequently than once every
                                </span>
                            </span>
                        </div>
                        <div className="row shadow px-2 py-3">
                            <div className="col-auto">
                                <label className="col-form-label">Interval Value</label>
                            </div>
                            <div className="col-auto">
                                <select required aria-required name='exec_interval' className="form-select" onChange={handleChange} value={trigger.interval}>
                                    <option value=''>---</option>
                                    {[...Array(60).keys()].map(index => (
                                        <option key={index + 1} value={index + 1}>{index + 1}</option>
                                    ))}
                                </select>
                            </div>
                            <div className="col-auto">
                                <label className="col-form-label">Frequency</label>
                            </div>
                            <div className="col-auto">
                                <select required aria-required name='exec_frequency' className="form-select" onChange={handleChange} value={trigger.frequency}>
                                    <option value=''>---</option>
                                    {exec_frequencies.map((item, index) =>
                                        <option key={index} value={item.value}>{item.label}</option>
                                    )}
                                </select>
                            </div>
                        </div>
                    </div>
                </div>
                <div className="row py-3">
                    <div className="col-md-1 px-0">
                        <button type="submit" className="btn btn-primary">Submit Changes</button>
                    </div>
                    <div className="col-md-2 px-0">
                        <button type="button" className="btn btn-warning" onClick={() => navigate(-1)}>Cancel</button>
                    </div>
                </div>
            </form>
            <div style={{display: 'None'}}>{JSON.stringify(formData)}</div>
        </div>
    )
}