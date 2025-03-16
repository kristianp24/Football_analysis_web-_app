import axios from "axios";
const addUser = async (email, password, name, surname) => { 
    try {
        const response = await axios.post('http://127.0.0.1:5000/auth/register',{
            email: email,
            password: password,
            full_name: name + " " + surname,
        })
        return response;
    }
    catch (error) {
        return error;
    }
}

export default addUser;