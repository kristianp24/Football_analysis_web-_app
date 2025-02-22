import React from 'react';
import Alert from '@mui/material/Alert';

const AlertComponent = ({ severity, message }) => {  
    return (
        <Alert severity={severity} variant='filled'>{message}</Alert>
    );
}

export default AlertComponent;