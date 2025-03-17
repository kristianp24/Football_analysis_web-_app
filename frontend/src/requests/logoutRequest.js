import axios from "axios";

const logout = async (token) => {
    try{
        const response = await axios.post(
            'http://127.0.0.1:5000/auth/logout', 
            {}, 
            {
                headers: {
                    Authorization: `Bearer ${token}` 
                }
            }
        );
        return response;
    }
    catch (error){
        return error;
    }
}

export default logout;