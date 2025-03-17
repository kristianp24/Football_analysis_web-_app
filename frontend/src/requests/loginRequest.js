import axios from "axios"

const loginUser = async (email, password) => {
    try
    {
        const response = await axios.post('http://127.0.0.1:5000/auth/login', {
          email: email,
          password: password
      });
     
       return response;
    }
    catch (error) 
    {
        return error;
    }
}

export default loginUser;