import React, { use, useEffect, useRef, useState } from "react";
import { Box, Typography } from "@mui/material";
import ButtonAppBar from "../components/Toolbar";
import backgroundImage from "../media/poza2.jpeg";
import Button from "@mui/material/Button";
import AlertComponent from "../components/Alert";
import useAlertSetter from "../hooks/useAlertSetter";
import axios from "axios";
import saveVideo from "../requests/saveVideoRequest";
import predictVideo from "../requests/predictVideoRequest";
import FormDialog from "../components/TeamColoursDialog";
import FullScreenDialog from "../components/StatisticsDialog";


const VideoDownloaderPage = () => {
     const [url, setUrl] = useState("");
     const [selectedFile, setSelectedFile] = useState(null);
     const filePickerRef = useRef(null);
     const videoRef = useRef(null);
     const { alert, showAlert } = useAlertSetter();
     const [open, setOpen] = useState(false);
     const [openTeamForm, setOpenTeamForm] = useState(false)
     const [hiddenStatisticsButton, setHidden] = useState(true);
     
    //  useEffect(() => {
    //     const checkAndRedirect = async  () => {    
    //         const isExpired = await check_token_expiration();
    //         if (isExpired){
    //             localStorage.removeItem('token');
    //             try{
    //                 const response = await axios.post(
    //                 'http://127.0.0.1:5000/auth/logout', 
    //                 {},  
    //                 {
    //                     headers: {
    //                         Authorization: `Bearer ${tokenRef.current}` 
    //                     }
    //                 }
    //                );
    //                navigate('/');
    //             }
    //             catch (error) {
    //                 console.log(error);
    //             }
                
                
    //         }
    //     }

    //     checkAndRedirect();

    //    const intervalId = setInterval(checkAndRedirect, 120000);
    //    return () => clearInterval(intervalId);
        
    //  }
    //     ,[navigate]);
    
    
    const closeDialog = () => {
        setOpen(false);
    }
    // const openDialog = () => {
    //     setOpen(true);
    // }


     const handleFileChange = (e) => {  
        const file = filePickerRef.current.files[0];
        setSelectedFile(file);
        const reader = new FileReader();
        
        reader.addEventListener("load", () => { 
            const videoSrc = reader.result;
            console.log(videoSrc);
      
            setUrl(videoSrc); 
            videoRef.current.src = videoSrc; 
            videoRef.current.load(); 
        })

        reader.readAsDataURL(file);
     }

     const handleSaveVideo = async () => {
        const formData = new FormData();
        formData.append("video", selectedFile);
        // console.log(selectedFile);
        try {
            const response = await saveVideo(formData)
            console.log(response);
            if (response.status === 200) {
                showAlert('success', 'Video saved successfully! Wait for the prediction!');
                try{
                    const prediction = await predictVideo();
                    console.log(prediction);
                    if (prediction.status === 200) {
                        showAlert('success', 'Prediction completed successfully!'); 
                        sessionStorage.setItem('prediction', JSON.stringify(prediction.data.data));
                        setHidden(false);
                        console.log(prediction.data.data);
                       
                    }
                }
                catch (error) {
                    console.log('Error in prediction');
                    console.log(error);
                }
             }
         }
         catch (error) {
             console.log(error);
         }
    }

    const handleStatistics = () => {
       
        if (sessionStorage.getItem('prediction') == null) {
            showAlert('warning', 'Please upload a video and wait for the prediction!');     
            return;
        }
        const prediction = JSON.parse(sessionStorage.getItem('prediction'));
        if (prediction['team_0']['name'] !== 'NA'){
            setOpen(true);
        }
        else{
            setOpenTeamForm(true);
        }
        
  
    }



    return (
        <div id="videoDownloadPage" style={{backgroundImage: `url(${backgroundImage})`,  backgroundSize: 'cover',
            backgroundPosition: 'center',
            backgroundRepeat: 'no-repeat',
            backgroundAttachment: 'fixed',
             minHeight: '100vh',  
             width: '100%',
           }}>

        <ButtonAppBar />

        <div style={{display: 'flex', justifyContent: 'center', marginTop: '30px'}}>
            {alert.visible && 
                                <AlertComponent 
                                    severity={alert.severity} 
                                    message={alert.message} 
                                    style={{ width: '100%', boxSizing: 'border-box' }} 
                                />
                            }
            
            </div>

      
        <div style={{display: 'flex', justifyContent: 'center', marginTop: '30px'}}>
        <Box sx={{display: 'flex', justifyContent: 'center', alignItems: 'center', width: '25%', height: '50px', backgroundColor: '#182950', borderRadius: '13px'}}>
            <Button onClick={() => filePickerRef.current.click()} style={{color: 'white'}} variant="contained" title="Upload Video">
                Upload Video
                <input accept="video/*" ref={filePickerRef} id="filepicker" type="file" placeholder="Enter URL" onChange={handleFileChange} hidden='true' />
            </Button>
        </Box>
        </div>

        <div style={{display: 'flex', justifyContent: 'center', marginTop: '10px'}}>
        <Box sx={{
            display: "inline-block",
            border: "2px solid black",
            borderRadius: "10px",
            mt: 2,
            backgroundColor: "#182950",
            alignItems: "center",
            justifyContent: "center",
          }}>
            
            <div>
        
                <video ref={videoRef} width="600" height="400" controls muted={false}/>
            </div>
        </Box>
        </div>

        <div style={{display: 'flex', justifyContent: 'center', marginTop: '10px'}}>
       
            <Button onClick={handleSaveVideo} style={{color: 'white', marginTop: '10px', marginRight: '5px'}} variant="contained" title="Download Video">
                Predict Video
            </Button>

           {!hiddenStatisticsButton && (
                <Button
                    onClick={handleStatistics}
                    style={{ color: 'white', marginTop: '10px', marginLeft: '5px' }}
                    variant="contained"
                    title="View statistics"
                >
                    View Statistics
                </Button>
                )}

       
        </div>
          
          <FormDialog openForm={openTeamForm}  onClose={() => setOpenTeamForm(false)} openDialog={() => setOpen(true)}/>
            <FullScreenDialog open={open}  handleClose={closeDialog}  />
    </div>
    );

}

export default VideoDownloaderPage;