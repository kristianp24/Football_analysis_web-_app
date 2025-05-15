import React from "react";
import { Box, Grid, Typography, TextField, InputAdornment, IconButton, OutlinedInput, InputLabel, FormControl, Button, Card } from "@mui/material";
import EmailIcon from '@mui/icons-material/Email';
import LockIcon from '@mui/icons-material/Lock';
import PersonIcon from '@mui/icons-material/Person';
import Visibility from '@mui/icons-material/Visibility';
import VisibilityOff from '@mui/icons-material/VisibilityOff';
import Utils from "../util_functions/Utils";
import useAlertSetter from "../hooks/useAlertSetter";
import AlertComponent from "../components/Alert";
import addUser from "../requests/register_request"

const RegisterForm = () => {
  const [showPassword, setShowPassword] = React.useState(false);
  const [showConfirm, setShowConfirm] = React.useState(false);
  const { alert, showAlert } = useAlertSetter();

  const handleClickShowPassword = () => setShowPassword((show) => !show);
  const handleClickShowConfirm = () => setShowConfirm((show) => !show);

  const registerData = async (email, password, name, surname) => {
    const response = await addUser(email, password, name, surname);
    if (response.status === 201) {
      showAlert("success", "Registration successful. Go back to login");
    } else if (response.status === 409 || response.status === 500) {
      showAlert("error", response['response']['data']['error']);
    }
  };

  const buttonClicked = async () => {
    const emailInput = document.getElementById("email");
    const passwordInput = document.getElementById("password");
    const confirmPasswordInput = document.getElementById("confirm_password");
    const nameInput = document.getElementById("first_name");
    const surnameInput = document.getElementById("last_name");

    const email = emailInput.value;
    const password = passwordInput.value;
    const confirmPassword = confirmPasswordInput.value;
    const name = nameInput.value;
    const surname = surnameInput.value;

    if (!Utils.checkEmptyField(name)) {
      showAlert("error", "Name is required");
    } else if (!Utils.checkEmptyField(surname)) {
      showAlert("error", "Last Name is required");
    } else if (!Utils.checkEmptyField(email)) {
      showAlert("error", "Email is required");
    } else if (!Utils.checkEmptyField(password)) {
      showAlert("error", "Password is required");
    } else if (!Utils.checkEmptyField(confirmPassword)) {
      showAlert("error", "Password Confirmation is required");
    } else if (Utils.checkforNumbers(name) || Utils.checkforNumbers(surname)) {
      showAlert("error", "Name and Surname cannot contain numbers");
      nameInput.value = "";
      surnameInput.value = "";
    } else if (!Utils.checkEmail(email)) {
      showAlert("error", "Invalid Email");
      emailInput.value = "";
      passwordInput.value = "";
      confirmPasswordInput.value = "";
    } else if (!Utils.checkPassword(password)) {
      showAlert("error", "Password must be at least 8 characters long");
      passwordInput.value = "";
      confirmPasswordInput.value = "";
    } else if (!Utils.checkConfirmPassword(password, confirmPassword)) {
      showAlert("error", "Passwords do not match");
      passwordInput.value = "";
      confirmPasswordInput.value = "";
    } else {
      registerData(email, password, name, surname);
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
            Create your account to get started.
          </Typography>
        </Grid>

        <Grid item xs={12} md={6} sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: '100vh' }}>
          <Card elevation={3} sx={{ p: 5, borderRadius: 3, minWidth: 350, backgroundColor: 'white', color: 'black' }}>
            <Typography variant="h5" fontWeight={600} gutterBottom>
              Register
            </Typography>

            {alert.visible && (
              <AlertComponent 
                severity={alert.severity} 
                message={alert.message} 
                style={{ width: '100%', boxSizing: 'border-box', mb: 2 }} 
              />
            )}

            <TextField required fullWidth label="First Name" id="first_name" margin="normal" InputProps={{ startAdornment: (<InputAdornment position="start"><PersonIcon /></InputAdornment>) }} />
            <TextField required fullWidth label="Last Name" id="last_name" margin="normal" InputProps={{ startAdornment: (<InputAdornment position="start"><PersonIcon /></InputAdornment>) }} />
            <TextField required fullWidth label="Email" id="email" margin="normal" InputProps={{ startAdornment: (<InputAdornment position="start"><EmailIcon /></InputAdornment>) }} />
            <FormControl fullWidth variant="outlined" margin="normal">
              <InputLabel htmlFor="password">Password</InputLabel>
              <OutlinedInput id="password" type={showPassword ? 'text' : 'password'} startAdornment={<InputAdornment position="start"><LockIcon /></InputAdornment>} endAdornment={<InputAdornment position="end"><IconButton onClick={handleClickShowPassword} edge="end">{showPassword ? <VisibilityOff /> : <Visibility />}</IconButton></InputAdornment>} label="Password" />
            </FormControl>
            <FormControl fullWidth variant="outlined" margin="normal">
              <InputLabel htmlFor="confirm_password">Confirm Password</InputLabel>
              <OutlinedInput id="confirm_password" type={showConfirm ? 'text' : 'password'} startAdornment={<InputAdornment position="start"><LockIcon /></InputAdornment>} endAdornment={<InputAdornment position="end"><IconButton onClick={handleClickShowConfirm} edge="end">{showConfirm ? <VisibilityOff /> : <Visibility />}</IconButton></InputAdornment>} label="Confirm Password" />
            </FormControl>

            <Button fullWidth variant="contained" color="primary" sx={{ mt: 3 }} onClick={buttonClicked}>
              Register
            </Button>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};

export default RegisterForm;