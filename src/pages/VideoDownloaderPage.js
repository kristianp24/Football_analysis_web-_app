import React, { useEffect, useRef, useState } from "react";
import { Box, Typography } from "@mui/material";
import ButtonAppBar from "../components/Toolbar";

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
        <div>

        <ButtonAppBar />

      
        <div style={{display: 'flex', justifyContent: 'center', marginTop: '30px'}}>
        <input accept="video/*" ref={filePickerRef} id="filepicker" type="file" placeholder="Enter URL" onChange={handleFileChange} />
        </div>

        <div style={{display: 'flex', justifyContent: 'center', marginTop: '10px'}}>
        <Box sx={{
            display: "inline-block",
            border: "2px solid black",
            mt: 2,
            backgroundColor: "#f0f0f0",
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