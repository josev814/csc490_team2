import React, {useState} from "react";
import axios from "axios";
import AsyncSelect from 'react-select/async';

export function AsyncDropDown(props) {
    const [selectedOption, setSelectedOption] = useState(null);

    const loadOptions = async (inputValue, callback) => {
        const django_url = 'http://localhost:8889'
        //axios.get(`${django_url}/stocks/find_ticker?ticker=${inputValue}`)
        let records = {}
        await axios.get(
            django_url + '/stocks/find_ticker/?ticker=' + inputValue
        ).then(res => {
            records = res.data['records']
        }).catch(error => {
            console.log('Error fetching data: ', error)
        })
        callback(records.map(i => ({ 
            label: i.ticker + ' - ' + i.name, 
            value: i.url.split('/')[4] + '|' + i.ticker
        })))
    };
    
    const handleSelect = (selectedOption) => {
         setSelectedOption(selectedOption);
         console.log(selectedOption)
         if (selectedOption && selectedOption !== null && props.handleChange){
            console.log('selectedOption: ' + selectedOption)
             props.handleChange({'target': {'value': selectedOption.value, 'name': props.name}} )
         }
    };

    return(
        <>
            <AsyncSelect
                name={props.name}
                cacheOptions
                value={selectedOption}
                onChange={handleSelect}
                loadOptions={loadOptions}
                isClearable
                placeholder="Type to find a symbol..."
                required
            />
        </>
    )
}