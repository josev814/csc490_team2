import React, {useState, useEffect} from "react";
import { useNavigate } from "react-router";
import axios from 'axios';
import Cookies from 'universal-cookie'
import { AsyncDropDown } from "../inputs/AsyncDropDown";
import { DateInput } from "../inputs/DateInput";

export default function CreateRuleForm(props) {
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
    const [action, setAction] = useState({}); // State to manage the action
    const [conditions, setConditions] = useState([]); // State to manage rule conditions
    const [errorMessage, setErrorMessage] = useState(""); // State to manage error message
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
    const then_methods = [
        {value:'buy', label: 'Buy'},
        {value: 'sell', label: 'Sell'},
        {value: 'notify', label: 'Notify'}
    ]
    const then_qty_types = [
        {value:'usd', label: 'USD'},
        {value: 'shares', label: 'Share(s)'},
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
        const url = `${props.django_url}/rules/`
        await props.refresh_token()

        const updatedFormData = {
            ...formData,
            user: get_user_from_cookie(),
        };

        setFormData(updatedFormData);
        try {
            const headers = props.get_auth_header()
            const response = await axios.post(url, updatedFormData, {headers})
            if (response.status === 200 || response.status === 201) {
                const rule_id = response.data.id
                const rule_name = response.data.name
                navigate(`/rule/${rule_id}/${rule_name}/`);
            } else {
                console.error('Failed to create rule')
                throw new Error('Failed to create rule');
            }
        }
        catch (error) {
            if (error.response && error.response.status === 409) {
                setErrorMessage("Rule already exists");
            } else {
                setErrorMessage(`${error.response.status}: ${error}`);
            }
            console.log(errorMessage)
        }
    };

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
                form_conditions.push({[key]: value})
            }
            setConditions(form_conditions)
        }
    }
    
    const handleChange = (e) => {
        if (['name', 'start_date'].indexOf(e.target.name) !== -1 ){
            setFormData({ ...formData, [e.target.name]: e.target.value });
        } else if ('initial_investment' === e.target.name ){
            setFormData({ ...formData, [e.target.name]: e.target.value + '.00' });
        } else if (e.target.name.startsWith('then_')){
            parse_form_rule_action(e)
        } else if (e.target.name.startsWith('event_')){
            parse_form_rule_events(e)
        } else {
            console.warn('Unknown field that needs handling: ' + e.target.name)
        }
    };
    
    useEffect(() => {
        const json_rule = {'conditions': conditions, 'action': action};
        setFormData( prevFormData => ({ ...prevFormData, 'rule': json_rule }));
    }, [conditions, action, setFormData]);

    return(
        <div className="container">
            <h2 className="mb-4">Add Rule</h2>
            <form className="form" onSubmit={handleSubmit}>
                <div className="row mb-3">
                    <label htmlFor="name" className="form-label">Name:</label>
                    <input type="text" className="form-control" name="name" id="name" placeholder="Enter rule name" onChange={handleChange} />
                </div>
                <div className="row mb-3">
                    <label htmlFor="initial_investment" className="form-label">Initial Investment:</label>
                    <div className="input-group">
                        <div className="input-group-prepend">
                            <span className='input-group-text'>$</span>
                        </div>
                        <input type="number" className="form-control" name="initial_investment" id="initial_investment" placeholder="Enter your initial investment" onChange={handleChange} />
                        <div className="input-group-append">
                            <span className='input-group-text'>.00</span>
                        </div>
                    </div>
                </div>
                <div className="row mb-3">
                    <DateInput label='Start Date' id='start_date' name='start_date' handleChange={handleChange} />
                </div>
                <div className="row shadow px-2 py-3 mb-3">
                    <label className="col-md-1">
                        <span className="h5">IF:</span>
                        <input type='hidden' name="event_condition_1" aria-hidden aria-readonly value='if' />
                    </label>
                    <div className="col-md-3">
                        <AsyncDropDown name='event_symbol_1' handleChange={handleChange} django_url={props.django_url} />
                    </div>
                    <div className="col-md-1">
                        HAS 
                    </div>
                    <div className="col-md-2">
                        <select required aria-required name="event_data_1" className="form-select" onChange={handleChange}>
                            <option value=''>---</option>
                            {event_data.map((item, index) =>
                                <option key={index} value={item.value}>{item.label}</option>
                            )}
                        </select>
                    </div>
                    <div className="col-md-3">
                        <select required aria-required name="event_operator_1" className="form-select" onChange={handleChange}>
                            <option value=''>---</option>
                            {event_operators.map((item, index) =>
                                <option key={index} value={item.value}>{item.label}</option>
                            )}
                        </select>
                    </div>
                    <div className="col-md-2">
                        <input required aria-required type="text" pattern='^\d+(\.\d{2})?$' name="event_value_1" className="form-control" placeholder="Comparison Value $"  onChange={handleChange} />
                    </div>
                </div>
                <div className="row shadow px-2 py-3">
                    <div className="col-md-1">
                        <span className="h5">THEN:</span>
                    </div>
                    <div className="col-md-1">
                        <select required aria-required name='then_method' className="form-select" onChange={handleChange}>
                            <option value=''>---</option>
                            {then_methods.map((item, index) =>
                                <option key={index} value={item.value}>{item.label}</option>
                            )}
                        </select>
                    </div>
                    <div className="col-md-2">
                        <input type="text" name='then_quantity' className="form-control" placeholder="Quantity"  onChange={handleChange} />
                    </div>
                    <div className="col-md-2">
                        <select required aria-required name='then_quantity_type' className="form-select" onChange={handleChange}>
                            <option value=''>---</option>
                            {then_qty_types.map((item, index) =>
                                <option key={index} value={item.value}>{item.label}</option>
                            )}
                        </select>
                    </div>
                    <div className="col-md-1">
                        OF
                    </div>
                    <div className="col-md-3">
                        <AsyncDropDown name='then_symbol' handleChange={handleChange}  django_url={props.django_url}/>
                    </div>
                </div>
                <div className="row py-3">
                    <div className="col-md-1 px-0">
                        <button type="submit" className="btn btn-primary">Add Rule</button>
                    </div>
                    <div className="col-md-2 px-0">
                        <button type="button" className="btn btn-warning" onClick={() => navigate(-1)}>Cancel</button>
                    </div>
                </div>
            </form>
        </div>
    )
}