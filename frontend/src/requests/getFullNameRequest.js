import axios from "axios";

const getFullName = async () => {
    try{
        const token = localStorage.getItem('token')
        console.log('token from request getName:  ', token)
        const response = await axios.get('http://127.0.0.1:5000/user/fullName',
            {
                headers: {
                    Authorization: `Bearer ${token}` 
                }
            }
        );
        console.log(response)
        if (response.status === 200){
            const userFullName = response['data']['full_name'];
            return userFullName;
        }
    }
    catch (error){
        return null;
    }
}

export default getFullName;