import * as React from 'react';
import Button from '@mui/material/Button';
import Dialog from '@mui/material/Dialog';
import ListItemText from '@mui/material/ListItemText';
import ListItemButton from '@mui/material/ListItemButton';
import List from '@mui/material/List';
import Divider from '@mui/material/Divider';
import AppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import IconButton from '@mui/material/IconButton';
import Typography from '@mui/material/Typography';
import CloseIcon from '@mui/icons-material/Close';
import Slide from '@mui/material/Slide';
import SaveIcon from '@mui/icons-material/Save';
import { Box, ListItem, OutlinedInput } from '@mui/material';
import {TextField} from '@mui/material';
import getFullName from '../requests/getFullNameRequest';
import getEmail from '../requests/getUserEmail';

const Transition = React.forwardRef(function Transition(props, ref) {
  return <Slide direction="up" ref={ref} {...props} />;
});

export default function FullScreenDialog({open,handleClose}) {
  const [name, setName] = React.useState(null);
  const [email, setEmail] = React.useState(null);
   
  React.useEffect(() => {
    getName();
    getUserEmail();
  }, [])


  const getUserEmail = () => {
      const email =  getEmail();
      console.log(email)
      if (email !== null){
        setEmail(email)
      }
      else{
        setName('No item found!')
      }
  }

  const getName = async () => {
    const fullName = await getFullName();
    if (fullName !== null){
      setName(fullName)
    }
    else{
      setName("Not found!")
    }
    
  }


  return (
    <React.Fragment>
      {/* <Button variant="outlined" onClick={handleClickOpen}>
        Open full-screen dialog
      </Button> */}
      <Dialog
        fullScreen
        open={open}
        onClose={handleClose}
        TransitionComponent={Transition}
    
      >
        <AppBar sx={{ position: 'relative' }}>
          <Toolbar>
            <IconButton
              edge="start"
              color="inherit"
              onClick={handleClose}
              aria-label="close"
            >
              <CloseIcon />
            </IconButton>
            <Typography sx={{ ml: 2, flex: 1 }} variant="h6" component="div">
              Profile
            </Typography>
            <Button autoFocus color="inherit" onClick={handleClose}>
              Save
            </Button>
          </Toolbar>
        </AppBar>
        <Box 
              sx={{ 
                display: 'flex', 
                alignItems: 'flex-start',
                pt: 2, 
                justifyContent: 'center', 
                height: '100vh' // Ensures full screen height
              }}
        >
          <Box sx={{ width: '300px', height: '100px', p:1, m: 2 , alignItems: 'center', justifyContent: 'center', display: 'flex', flexDirection: 'column', backgroundColor: '#BDBDBD', 
                     border: "2px solid black", borderRadius: "10px"
          }}>
            <Typography variant='h6' >Name: {name} </Typography>
            <Typography variant='h6' >Email: {email}</Typography>
            
            </Box>
          </Box>
          <div>
            
          </div>
      </Dialog>
    </React.Fragment>
  );
}
