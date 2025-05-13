import PropTypes from "prop-types";

export default function Pagination(props) {
    // Function to handle clicking on the previous or next page button
    const handlePage = (direction, event) => {
        if (direction === 'next'){
            if (props.links.next != null) {
                props.onPageChange(props.links.next); // Go to the next page
            }
        } else { // previous
            if (props.links.previous != null) {
                props.onPageChange(props.links.previous); // Go to the previous page
            }
        }
        const target_element = document.getElementById(props.target_element);
        if (target_element) {
            target_element.scrollIntoView({ behavior: 'smooth' });
        }
        event.target.blur() // remove the focus of the button that was clicked
    }

    // Render pagination component
    return (
        <nav>
            <ul className="pagination">
                {/* Previous page button */}
                <li className={`page-item ${props.links.previous === null ? 'disabled' : ''}`}>
                    <button className="page-link" onClick={(event) => handlePage('previous', event)}>Previous</button>
                </li>
                {/* Next page button */}
                <li className={`page-item ${props.links.next === null ? 'disabled' : ''}`}>
                    <button className="page-link" onClick={(event) => handlePage('next', event)}>Next</button>
                </li>
            </ul>
        </nav>
    );
}



Pagination.propTypes = {
    links: PropTypes.object,
    onPageChange: PropTypes.func,
    target_element: PropTypes.string,
}