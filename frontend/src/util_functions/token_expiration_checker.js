import axios from 'axios';

async function check_and_refresh_token () {
  const token = localStorage.getItem('token');
  const refreshToken = localStorage.getItem('refresh_token');

  if (!token || !refreshToken) return true; 

  try {
    await axios.get('http://127.0.0.1:5000/auth/videoDownload', {
      headers: { Authorization: `Bearer ${token}` }
    });

    return false; 
  } catch (err) {
    if (err.response?.status === 401 && err.response?.data?.msg === "Token has expired") {
  
      try {
        const res = await axios.post('http://127.0.0.1:5000/auth/refresh', {}, {
          headers: { Authorization: `Bearer ${refreshToken}` }
        });

        const newAccessToken = res.data.access_token;
        localStorage.setItem('token', newAccessToken);
        return false; 
      } catch (refreshError) {
        console.error("Refresh failed:", refreshError);
        return true; 
      }
    }

    console.error("Token check error:", err);
    return false; 
  }
}

export default check_and_refresh_token;

