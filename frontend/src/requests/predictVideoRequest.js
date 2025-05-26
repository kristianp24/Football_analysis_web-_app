import axios from "axios";

const predictVideo = async () => {
    const token = localStorage.getItem('token');
    try{
        const response = await axios.get('http://127.0.0.1:5000/predictVideo', {
            headers: {
                Authorization: `Bearer ${token}`
            }
        });
        return response;
    }
    catch(error){
        return error;
    }
}

export default predictVideo;