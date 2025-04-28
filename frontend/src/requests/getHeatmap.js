import axios from 'axios';
const downloadHeatmap = async (team_name, team_cluster) => {
    try{
        const response = await axios.post('http://127.0.0.1:5000/createHeatmap', 
            {
                team_cluster: team_cluster,
                team_name: team_name
            }, 
            {
                headers: {
                    'Content-Type': 'application/json'
                },
                responseType: 'blob'  
            }
        );

        const url = window.URL.createObjectURL(response.data);
        const a = document.createElement('a');
        a.href = url;

        a.download = `${team_name}_heatmap.png`; 
        document.body.appendChild(a);
        a.click(); 
        a.remove(); 
        console.log('Heatmap downloaded successfully!');
    }
    catch (error) {
        console.error('Error downloading heatmap:', error);
    }

}

export default downloadHeatmap;
