import React from "react";
import Box from '@mui/material/Box';
import TextField from '@mui/material/TextField';  
import IconButton from '@mui/material/IconButton';
import OutlinedInput from '@mui/material/OutlinedInput';
import InputLabel from '@mui/material/InputLabel';
import InputAdornment from '@mui/material/InputAdornment';
import FormControl from '@mui/material/FormControl';
import Visibility from '@mui/icons-material/Visibility';
import VisibilityOff from '@mui/icons-material/VisibilityOff';
import { Button } from "@mui/material";
import Typography from "@mui/material/Typography";
import Link from "@mui/material/Link";
import {useNavigate} from 'react-router-dom';
import RegisterForm from "./RegisterForm";
import axios from 'axios';
import AlertComponent from "./Alert";
import useAlertSetter from "../hooks/useAlertSetter";

const LogInForm = () => {
  const navigate = useNavigate();
  const { alert, showAlert } = useAlertSetter();

  const [email, setEmail] = React.useState('');
  const [password, setPassword] = React.useState('');

  const [showPassword, setShowPassword] = React.useState(false);

  const handleClickShowPassword = () => setShowPassword((show) => !show);

  const handleMouseDownPassword = (event) => {
    event.preventDefault();
  };

  const handleMouseUpPassword = (event) => {
    event.preventDefault();
  };

  const onClickLogIn = () => {
      //navigate('/VideoDownload');
     const email = document.getElementById('email').value;
     const password = document.getElementById('outlined-adornment-password').value;
     setEmail(email);
     setPassword(password);
     sendData();
  }


  const sendData = async (e) => {
    e.preventDefault();
    try{
       const response = await axios.post('http://127.0.0.1:5000/auth/login', {
        email: document.getElementById('email').value,
        password: document.getElementById('outlined-adornment-password').value
    });
    console.log(response);
    localStorage.setItem('token', response['data']['token']);
    navigate('/VideoDownload');
    }
    catch (error) {
      if (error.response.status === 401) {
        showAlert('error', 'Invalid email or password');
      }
      if (error.response.status === 409) {
        showAlert('error', 'You are already logged in!');
      }
      else if (error.response.status === 500) {
        showAlert('error', 'Server error');
      }
    }
   

  }

    return (
        <Box 
        component="form"
        sx={{ '& .MuiTextField-root': { m: 1, width: '25ch' } }}
        noValidate
        autoComplete="off"
        
           >
            <div>
            {alert.visible && 
                    <AlertComponent 
                        severity={alert.severity} 
                        message={alert.message} 
                        style={{ width: '100%', boxSizing: 'border-box' }} 
                    />
                }

            </div>
            <div>
            
                <TextField
                    required
                    id="email"
                    label="Email"
                    defaultValue=""
                    type="text"
                    variant="outlined"
                    size="medium"/>
                </div>
                <div>
                {/* <TextField
                    required
                    id="password"
                    label="Parola"
                    defaultValue=""
                    variant="outlined"
                    type="password"
                    size="small"
                    /> */}
                    <FormControl sx={{ m: 1, width: '25ch' }} variant="outlined">
          <InputLabel htmlFor="outlined-adornment-password" required>Password</InputLabel>
          <OutlinedInput
            id="outlined-adornment-password"
            type={showPassword ? 'text' : 'password'}
            endAdornment={
              <InputAdornment position="end">
                <IconButton
                  aria-label={
                    showPassword ? 'hide the password' : 'display the password'
                  }
                  onClick={handleClickShowPassword}
                  onMouseDown={handleMouseDownPassword}
                  onMouseUp={handleMouseUpPassword}
                  edge="end"
                >
                  {showPassword ? <VisibilityOff /> : <Visibility />}
                </IconButton>
              </InputAdornment>
            }
            label="Password"
          />
        </FormControl>
            </div>
            <div>
            <Button
          fullWidth
          variant="contained"
          color="primary"
          style={{ marginTop: '16px' }}
          onClick={sendData}
        >
                 Log In
        </Button>            
        </div>

        <div>
            <Typography variant="body2" color="textSecondary" align="center" style={{ marginTop: '16px' }}>
            {"Forgot your password?   " }
            <Link
                    component="button"
                    variant="body2"
                    onClick={() => {
                        console.info("I'm a button.");
                    }}
                    style={{ cursor: 'pointer', marginLeft: '4px', marginBottom: '3px' }}    
                    >
                   Reset Password
                   </Link>
                 </Typography>
                 
        </div>

        <div>
            <Typography variant="body2" color="textSecondary" align="center" style={{ marginTop: '16px' }}>
            {"Here for the first time?   " }
            <Link
                    component="button"
                    variant="body2"
                    onClick={() => {
                         navigate('/Register');
                    }}
                    style={{ cursor: 'pointer', marginLeft: '4px', marginBottom: '3px' }}    
                    >
                   Sign Up
                   </Link>
                 </Typography>
        </div>

            </Box>
    );
}

export default LogInForm;