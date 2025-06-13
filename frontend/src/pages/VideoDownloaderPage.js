import React, { use, useEffect, useRef, useState } from "react";
import { Box, Typography } from "@mui/material";
import ButtonAppBar from "../components/Toolbar";
import backgroundImage from "../media/fundal.png";
import Button from "@mui/material/Button";
import AlertComponent from "../components/Alert";
import useAlertSetter from "../hooks/useAlertSetter";
import saveVideo from "../requests/saveVideoRequest";
import predictVideo from "../requests/predictVideoRequest";
import FormDialog from "../components/TeamColoursDialog";
import FullScreenDialog from "../components/StatisticsDialog";
import check_and_refresh_token from "../util_functions/token_expiration_checker";
import { useNavigate } from "react-router-dom";

const VideoDownloaderPage = () => {
     const [url, setUrl] = useState("");
     const [selectedFile, setSelectedFile] = useState(null);
     const filePickerRef = useRef(null);
     const videoRef = useRef(null);
     const { alert, showAlert } = useAlertSetter();
     const [open, setOpen] = useState(false);
     const [openTeamForm, setOpenTeamForm] = useState(false)
     const [hiddenStatisticsButton, setHidden] = useState(true);
     const [disableButton, setDisableButton] = useState(false);
     const navigate = useNavigate();
     

     useEffect(() => {
        const checkAndRedirect = async () => {
            const shouldRedirect = await check_and_refresh_token();
            if (shouldRedirect) {
            localStorage.clear();
            navigate('/');
            }
           
        };

        checkAndRedirect();
        const intervalId = setInterval(checkAndRedirect, 120000);
        return () => clearInterval(intervalId);
        }, [navigate]);

    
    
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
        if (!selectedFile) {
            showAlert('error', 'Please select a video file to upload!');
            return;
        }
        setDisableButton(true);
        // console.log(selectedFile);
        try {
            const response = await saveVideo(formData)
            console.log(response);
            if (response.status === 200) {
                showAlert('success', 'Video saved successfully! We will send you an email when the statistics are ready.');

                try {
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
                finally {
                    setDisableButton(false);
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
        <Box
        sx={{
            display: 'flex',
            justifyContent: 'center',
            alignItems: 'center',
            width: '30%',
            height: '50px',
            backgroundColor: '#0d47a1',
            borderRadius: '12px',
            boxShadow: '0px 4px 12px rgba(0,0,0,0.3)'
        }}
         >
        <Button
        disabled={disableButton}
        onClick={() => filePickerRef.current.click()}
        variant="contained"
        color="primary"
        sx={{ px: 4, py: 1.5, fontWeight: 600, borderRadius: 2 }}
        >                Upload Video
                <input accept="video/*" ref={filePickerRef} id="filepicker" type="file" placeholder="Enter URL" onChange={handleFileChange} hidden='true' />
            </Button>
        </Box>
        </div>

        <div style={{display: 'flex', justifyContent: 'center', marginTop: '10px'}}>
        <Box sx={{
            display: "inline-block",
            border: "2px solid black",
            borderRadius: "15px",
            mt: 2,
            backgroundColor: "#182950",
            alignItems: "center",
            justifyContent: "center",
          }}>
            
            <div>
        
                <video
                    ref={videoRef}
                    width="640"
                    height="360"
                    controls
                    style={{ borderRadius: '12px', backgroundColor: '#000' }}
                    />
            </div>
        </Box>
        </div>

        <div style={{display: 'flex', justifyContent: 'center', marginTop: '10px'}}>
       
           <Button
                disabled={disableButton}
                onClick={handleSaveVideo}
                variant="contained"
                color="secondary"
                sx={{ px: 4, py: 1.5, ml: 2, fontWeight: 600, borderRadius: 2 }}
                >
                Predict Video
                </Button>


           {!hiddenStatisticsButton && (
                <Button
                    onClick={handleStatistics}
                    disabled={disableButton}
                    variant="contained"
                    title="View statistics"
                    color="secondary"
                    sx={{ px: 4, py: 1.5, fontWeight: 600, borderRadius: 2, marginLeft: '20px' }}
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