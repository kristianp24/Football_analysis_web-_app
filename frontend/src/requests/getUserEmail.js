import axios from "axios";

const getEmail = async () => {
    const token = localStorage.getItem('token')
    console.log('Token from getEmail:' ,token)
    try{
        const response = await axios.get('http://127.0.0.1:5000/user/email',
            {
                headers:{
                    Authorization: `Bearer ${token}`
                }
            }
        );
        console.log('Response from getEmail  ', response)
        if (response.status === 200){
            const email = response['data']['email'];
            return email;
        }
        else{
            return 'No email found';
        }
            
    }
    catch(error){
       return error;
    }
}

export default getEmail;