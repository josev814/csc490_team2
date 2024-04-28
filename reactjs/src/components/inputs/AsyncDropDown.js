import React, {useState} from "react";
import axios from "axios";
import AsyncSelect from 'react-select/async';

export function AsyncDropDown(props) {
    const [selectedOption, setSelectedOption] = useState(null);

    const loadOptions = async (inputValue, callback) => {
        //axios.get(`${django_url}/stocks/find_ticker?ticker=${inputValue}`)
        let records = {}
        await axios.get(
            `${props.django_url}/stocks/find_ticker/?ticker=${inputValue}`
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
         console.groupCollapsed('handleSelect')
         console.log(selectedOption)
         if (selectedOption && selectedOption !== null && props.handleChange){
            const event = {'target': {'value': selectedOption.value, 'name': props.name}}
            try {
                console.log('Handling change')
                props.handleChange(event)
                console.log('Done handling change')
            } catch (err) {
                console.log(err)
            }
            console.group('event')
            console.log(event)
            console.groupEnd()
         }
         console.groupEnd()
    };

    if (props.defaultValue !== undefined){
        setSelectedOption(props.defaultValue)
      }

    return(
        <>
            <AsyncSelect
                name={props.name}
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