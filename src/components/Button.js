import React from 'react';
import ButtonUI from '@mui/material/Button';

const Button = ({ id,label, onclick, style }) => {
    return (
        <ButtonUI size="medium" id={id} onClick={onclick} style={style} variant="contained">{label}</ButtonUI>
    );
}

export default Button;