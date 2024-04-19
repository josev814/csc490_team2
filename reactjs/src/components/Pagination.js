import React from 'react';

export default function Pagination({ currentPage, totalPages, onPageChange, itemsPerPage, totalItems }) {
    // Function to handle clicking on the previous page button
    const handlePreviousPage = () => {
        console.log("Previous button clicked");
        if (currentPage > 1) {
            onPageChange(currentPage - 1); // Go to the previous page
        }
    };

    // Function to handle clicking on the next page button
    const handleNextPage = () => {
        console.log("Next button clicked");
        if (currentPage < totalPages) {
            onPageChange(currentPage + 1); // Go to the next page
        }
    };

    // Calculate start and end indices of items to display on the current page
    const startIndex = (currentPage - 1) * itemsPerPage;
    const endIndex = Math.min(startIndex + itemsPerPage, totalItems);

    // Render pagination component
    return (
        <nav>
            <ul className="pagination">
                {/* Previous page button */}
                <li className={`page-item ${currentPage === 1 ? 'disabled' : ''}`}>
                    <button className="page-link" onClick={handlePreviousPage}>Previous</button>
                </li>
                {/* Next page button */}
                <li className={`page-item ${currentPage === totalPages || totalPages === 1 ? 'disabled' : ''}`}>
                    <button className="page-link" onClick={handleNextPage}>Next</button>
                </li>
            </ul>
            {/* Display current range of items */}
            <div>
                Showing items {startIndex + 1} to {endIndex} of {totalItems}
            </div>
        </nav>
    );
}


