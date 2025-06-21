import * as React from 'react';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import CardMedia from '@mui/material/CardMedia';
import Typography from '@mui/material/Typography';
import CardActionArea from '@mui/material/CardActionArea';
import { Button } from '@mui/material';

export default function ActionAreaCard({open, setOpen}) {
    if (!open) {
        return null;
    }
  return (
    <Card sx={{ maxWidth: 345 } }>
      <CardActionArea>
        <CardContent>
          <Typography gutterBottom variant="h5" component="div">
            How to use the app
          </Typography>
          <Typography variant="body2" sx={{ color: 'text.secondary' }}>
            1) Upload a '.mp4', '.avi', '.mov' video file.<br />
            2) Click on the "Predict" button to process the video.<br />
            3) Once the prediction is done you will recieve an email and the "View Statistics" button will appear.<br />
            4) After recieving the email, you can view the predictions by clicking "View Statistics" button.<br />
            5) Keep in mind, the longer the video, the longer it will take to process.<br />
            6) The app works best with the camera angle below: <br />
            <CardMedia
              component="img"
              height="140"
              src="/image.png"
              alt="help image"
            />
            <br />
            7) Enjoy it and stay tuned for more features!<br />
          </Typography>
        </CardContent>
        <Button
            variant="contained"
            color="primary"
            onClick={() => setOpen(false)}
            sx={{ margin: 2, marginLeft: 16 }}
        >
            Close 
        </Button>
      </CardActionArea>
    </Card>
  );
}
