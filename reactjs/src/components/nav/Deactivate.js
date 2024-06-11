import React from 'react';
import Modal from 'react-bootstrap/Modal';
import Button from 'react-bootstrap/Button';

const CustomModal = ({ show, handleClose }) => {
    return (
        <Modal show={show} onHide={handleClose}>
            <Modal.Header closeButton>
                <Modal.Title>Deactivate your account?</Modal.Title>
            </Modal.Header>
            <Modal.Body>Details about your account and password will be erased!</Modal.Body>
            <Modal.Footer>
                <Button variant="secondary" onClick={handleClose}>
                    No
                </Button>
                <Button variant="danger" onClick={handleClose}>
                    Yes, Deactivate
                </Button>
            </Modal.Footer>
        </Modal>
    );
};

export default CustomModal;
