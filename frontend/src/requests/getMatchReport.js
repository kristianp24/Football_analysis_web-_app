import axios from "axios"


const getMatchReport = async (data) => {
    try{
        const response = await axios.post('http://127.0.0.1:5000/createPDF', 
                    {
                        report: data
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
        a.download = `match_report.pdf`;
        document.body.appendChild(a);
        a.click();
        a.remove();
        console.log('Match report downloaded successfully!');
    }
    catch (error) {
        console.error('Error downloading match report:', error);
    }

}

export default getMatchReport;  