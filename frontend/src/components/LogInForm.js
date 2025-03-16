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
import loginUser from "../requests/loginRequest";
import axios from 'axios';
import AlertComponent from "./Alert";
import useAlertSetter from "../hooks/useAlertSetter";

const LogInForm = () => {
  const navigate = useNavigate();
  const { alert, showAlert } = useAlertSetter();

  const [showPassword, setShowPassword] = React.useState(false);

  const handleClickShowPassword = () => setShowPassword((show) => !show);

  const handleMouseDownPassword = (event) => {
    event.preventDefault();
  };

  const handleMouseUpPassword = (event) => {
    event.preventDefault();
  };

  const sendData = async (e) => {
      e.preventDefault();
      
      const email =  document.getElementById('email').value;
      const password = document.getElementById('outlined-adornment-password').value;
      const response = await loginUser(email, password);
      console.log(response);
          if (response.status === 200) {
            localStorage.setItem('token', response['data']['token']);
            navigate('/VideoDownload');
          }
          else if (response.status === 401 || response.status === 409 || response.status === 500) {
            showAlert('error', response['response']['data']['error']);
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