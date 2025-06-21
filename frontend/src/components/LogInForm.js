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
import { Button, Card, Grid, Typography, Link } from "@mui/material";
import EmailIcon from '@mui/icons-material/Email';
import LockIcon from '@mui/icons-material/Lock';
import { useNavigate } from 'react-router-dom';
import loginUser from "../requests/loginRequest";
import AlertComponent from "./Alert";
import useAlertSetter from "../hooks/useAlertSetter";

const LogInForm = () => {
  const navigate = useNavigate();
  const { alert, showAlert } = useAlertSetter();
  const [showPassword, setShowPassword] = React.useState(false);
  const [disableButton, setDisableButton] = React.useState(false);

  const handleClickShowPassword = () => setShowPassword((show) => !show);

  const sendData = async (e) => {
    e.preventDefault();
    const email = document.getElementById('email').value;
    const password = document.getElementById('outlined-adornment-password').value;
    setDisableButton(true);
    const response = await loginUser(email, password);

    if (response.status === 200 && response.data.token) {
      const token = response.data.token;
      const refreshToken = response.data.refresh_token;
      localStorage.setItem("token", token);
      localStorage.setItem("refresh_token", refreshToken);
      console.log("Login successful, refresh token:", refreshToken);
      showAlert('success', 'Login successful!');
      navigate('/VideoDownload', {replace : true});
    } else if (response.status === 401 || response.status === 409 || response.status === 500) {
      showAlert('error', response.response.data.error);
      setDisableButton(false);
    }
  };

  return (
    <Box sx={{ width: '100vw', height: '100vh', overflow: 'hidden', background: 'linear-gradient(135deg, #004d99, #007acc)', display: 'flex' }}>
      <Grid container sx={{ flexGrow: 1 }}>
        <Grid
          item
          xs={12}
          md={6}
          sx={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            color: 'white',
            flexDirection: 'column',
            p: 4,
            textAlign: 'center',
            position: 'relative',
            height: '100vh'
          }}
        >
          <Box
            component="img"
            src="/logo2.png"
            alt="football graphic"
            sx={{ width: '55%', maxWidth: 280, mb: 3, filter: 'drop-shadow(2px 4px 6px rgba(0,0,0,0.4))' }}
          />
          <Typography variant="h3" fontWeight={700} sx={{ mb: 1, textShadow: '1px 1px 2px rgba(0,0,0,0.5)' }}>
            Football Eye App
          </Typography>
          <Typography variant="h6" sx={{ textShadow: '1px 1px 2px rgba(0,0,0,0.3)' }}>
            Unlock Computer Vision benefits in football.
          </Typography>
        </Grid>

        <Grid item xs={12} md={6} sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: '100vh' }}>
          <Card elevation={3} sx={{ p: 5, borderRadius: 3, minWidth: 350, backgroundColor: 'white', color: 'black' }}>
            <Typography variant="h5" fontWeight={600} gutterBottom>
              Welcome Back
            </Typography>
            <Typography variant="body2" sx={{ mb: 3 }}>
              Log in to analyze, predict football videos and get an instant match report.
            </Typography>

            {alert.visible && (
              <AlertComponent 
                severity={alert.severity} 
                message={alert.message} 
                style={{ width: '100%', boxSizing: 'border-box', mb: 2 }} 
              />
            )}

            <TextField
              required
              fullWidth
              id="email"
              label="Email"
              variant="outlined"
              margin="normal"
              InputProps={{
                startAdornment: (
                  <InputAdornment position="start">
                    <EmailIcon />
                  </InputAdornment>
                )
              }}
            />

            <FormControl fullWidth variant="outlined" margin="normal">
              <InputLabel htmlFor="outlined-adornment-password">Password</InputLabel>
              <OutlinedInput
                id="outlined-adornment-password"
                type={showPassword ? 'text' : 'password'}
                endAdornment={
                  <InputAdornment position="end">
                    <IconButton
                      onClick={handleClickShowPassword}
                      edge="end"
                      aria-label={showPassword ? 'hide password' : 'show password'}
                    >
                      {showPassword ? <VisibilityOff /> : <Visibility />}
                    </IconButton>
                  </InputAdornment>
                }
                startAdornment={
                  <InputAdornment position="start">
                    <LockIcon />
                  </InputAdornment>
                }
                label="Password"
              />
            </FormControl>

    

            <Button
              fullWidth
              variant="contained"
              color="primary"
              sx={{ mt: 2, mb: 2 }}
              onClick={sendData}
              disabled={disableButton}
            >
              Log In
            </Button>

            <Grid container justifyContent="space-between">
              <Link
                disabled={disableButton}
                component="button"
                variant="body2"
                onClick={() => navigate('/Register')}
              >
                Sign up
              </Link>
            </Grid>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};

export default LogInForm;
