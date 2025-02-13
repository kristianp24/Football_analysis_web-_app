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

const LogInForm = () => {
  const navigate = useNavigate();

  const [showPassword, setShowPassword] = React.useState(false);

  const handleClickShowPassword = () => setShowPassword((show) => !show);

  const handleMouseDownPassword = (event) => {
    event.preventDefault();
  };

  const handleMouseUpPassword = (event) => {
    event.preventDefault();
  };

  const onClickLogIn = () => {
      navigate('/VideoDownload');
  }

    return (
        <Box 
        component="form"
        sx={{ '& .MuiTextField-root': { m: 1, width: '25ch' } }}
        noValidate
        autoComplete="off"
        
           >
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
          onClick={onClickLogIn}
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
                        console.info("I'm a button.");
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