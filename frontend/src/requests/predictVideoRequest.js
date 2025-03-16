import axios from "axios";

const predictVideo = async () => {
    try{
        const response = await axios.get('http://127.0.0.1:5000/predictVideo');
        return response;
    }
    catch(error){
        return error;
    }
}

export default predictVideo;