import React, { useEffect, useRef, useState } from "react";
import { Box, Typography } from "@mui/material";
import ButtonAppBar from "../components/Toolbar";
import backgroundImage from "../media/poza2.jpeg";
import Button from "@mui/material/Button";

const VideoDownloaderPage = () => {
     const [url, setUrl] = useState("");
     const filePickerRef = useRef(null);
     const videoRef = useRef(null);

     const handleFileChange = (e) => {  
        // console.log(filePickerRef.current.value);
        // console.log(filePickerRef.current.files);
        const file = filePickerRef.current.files[0];
        const reader = new FileReader();
        
        reader.addEventListener("load", () => { 
            const videoSrc = reader.result;
            console.log(videoSrc);
      
            setUrl(videoSrc); // Store URL in state
            videoRef.current.src = videoSrc; // Directly set video source
            videoRef.current.load(); 
        })

        reader.readAsDataURL(file);
     }

     


    return (
        <div style={{backgroundImage: `url(${backgroundImage})`, height: '100vh',  backgroundSize: 'cover',
            backgroundPosition: 'center',
            backgroundRepeat: 'no-repeat',
            height: '100vh'}}>

        <ButtonAppBar />

      
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
        </div>
    );

}

export default VideoDownloaderPage;