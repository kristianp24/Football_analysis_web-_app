import axios from 'axios';

async function check_token_expiration () {
    const token = localStorage.getItem('token');
    try
    {
         const response = await axios.get('http://127.0.0.1:5000/auth/protected', {
            headers: {
                Authorization: `Bearer ${token}`
            }
        });
        if (response.status === 404) {
            return true;
        }
        else{
            return false;
        }
    }
    catch(err){
        console.log(err);
        return false;
    }
   
    

}
export default check_token_expiration;