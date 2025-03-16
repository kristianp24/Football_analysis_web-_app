import axios from "axios";

const saveVideo = async (formData) => {
    try{
        const response = await axios.post(
        'http://127.0.0.1:5000/saveVideo',
        formData,
        {
            headers: {
                'Content-Type': 'multipart/form-data'
            }
        }

    );
        return response;
    }
    catch (error){
        return error;
    }
    
}

export default saveVideo;