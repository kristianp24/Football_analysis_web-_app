import React, { useState } from "react";
import Utils from "../util_functions/Utils";
import RegisterForm from "../components/RegisterForm";
import AlertComponent from "../components/Alert";
import useAlertSetter from "../hooks/useAlertSetter";
import Button from "@mui/material/Button";
import axios from "axios";


const Register = () => {
    const { alert, showAlert } = useAlertSetter();
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

        

        if (Utils.checkEmptyField(name) === false) {
           showAlert("error", "Name is required");
           
        }
        
        else if (Utils.checkEmptyField(surname) === false){
            showAlert("error", "Last Name is required");
        }
        
        else if (Utils.checkEmptyField(email) === false){
            showAlert("error", "Email is required");
        }
        
        else if (Utils.checkEmptyField(password) === false){
            showAlert("error", "Password is required");
        }
        
        else if (Utils.checkEmptyField(confirmPassword) === false){
          showAlert("error", "Password Confirmation is required");
        }
        
        else if(Utils.checkforNumbers(name) === true || Utils.checkforNumbers(surname) === true) {
            showAlert("error", "Name and Surname cannot contain numbers");
            nameInput.value = "";
            surnameInput.value = "";

        }
        else if(Utils.checkEmail(email) === false) {
            showAlert("error", "Invalid Email");
            emailInput.value = "";
            passwordInput.value = "";
            confirmPasswordInput.value = "";
        }
        else if(Utils.checkPassword(password) === false) {
            showAlert("error", "Password must be at least 8 characters long");
           passwordInput.error = true;
           passwordInput.helperText = "Parola trebuie sa aiba minim 8 caractere";
            passwordInput.value = "";
            confirmPasswordInput.value = "";
        }
        else if(Utils.checkConfirmPassword(password, confirmPassword) === false) {
           showAlert("error", "Passwords do not match");
            passwordInput.value = "";
            confirmPasswordInput.value = "";
            
        }
       
       else{
        registerData(email, password, name, surname);
       }
    }

    const registerData = async (email, password, name, surname) => {
        try{
            const response = await axios.post('http://127.0.0.1:5000/auth/register',{
                email: email,
                password: password,
                full_name: name + " " + surname,
            })
        
            if (response.status === 201) {
                showAlert("success", "Registration successful go back to login");
            }
        }
        catch (error) {
            console.log(error);
            if (error.response.status === 409) {
                showAlert("error", "User with this email already exists");
            }
           else if (error.response.status === 500) {
                showAlert("error", "Server Error");
            }
        }
    }

    return (
        <div className="Register" style={{alignContent: "center", textAlign: "center", marginTop:'70px'}} >
          
        <div style={{ width: '400px', margin: '0 auto', textAlign: "center" }}>

               
                {alert.visible && 
                    <AlertComponent 
                        severity={alert.severity} 
                        message={alert.message} 
                        style={{ width: '100%', boxSizing: 'border-box' }} 
                    />
                }

                <h1>Register</h1>

                <RegisterForm />

                <div>
                    <Button 
                        label="Register" 
                        id="registerBtn"  
                        onClick={buttonClicked}  
                        type="submit"  
                        variant="contained" 
                        color="primary"
                        style={{ marginTop: '20px' }} 
                    >
                        Register
                    </Button>
                </div>

                </div> {/* End of Centered Container */}
                            
        </div>
    );
}

export default Register;