import * as React from 'react';
import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';
import IconButton from '@mui/material/IconButton';
import MenuIcon from '@mui/icons-material/Menu';
import Menu from '@mui/material/Menu';
import { MenuItem } from '@mui/material';
import AccountCircleRoundedIcon from '@mui/icons-material/AccountCircleRounded';
import ManageAccountsRoundedIcon from '@mui/icons-material/ManageAccountsRounded';
import PasswordRoundedIcon from '@mui/icons-material/PasswordRounded';
import HelpRoundedIcon from '@mui/icons-material/HelpRounded';
import LogoutRoundedIcon from '@mui/icons-material/LogoutRounded';
import FullScreenDialog from './ProfileDialog';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

export default function ButtonAppBar() {
    const [anchorEl, setAnchorEl] = React.useState(null);
    const [anchorEl2, setAnchorEl2] = React.useState(null); 
    const [open, setOpen] = React.useState(false);
    const navigate = useNavigate();

    const handleLogOut = async () => {
        try{
          const token = localStorage.getItem('token');
          const response = await axios.post(
            'http://127.0.0.1:5000/auth/logout', 
            {},  // No body needed
            {
                headers: {
                    Authorization: `Bearer ${token}` // Add Authorization header
                }
            }
        );
        localStorage.removeItem('token');
        navigate('/')
        }
        catch (error) {
          console.log(error);
          
        }
    }

    const handleClick2 = (event) => {
        setAnchorEl2(event.currentTarget);
    }

    
    const handleClose2 = () => {
        setAnchorEl2(null);
      };

    const handleClick = (event) => {
        setAnchorEl(event.currentTarget);
    }

    const handleClose = () => {
        setAnchorEl(null);
      };
    
      const openDialog = () => {  
        setOpen(true);
      }

      const closeDialog = () => {
        setOpen(false);
      }
    
  return (
    <Box sx={{ flexGrow: 1 }}>
      <AppBar position="static">
        <Toolbar>
          <IconButton
            size="large"
            edge="start"
            color="inherit"
            aria-label="menu"
            sx={{ mr: 2 }}
            id='menu-icon'
            onClick={handleClick}
          >
            <MenuIcon />
          </IconButton>

          <Menu
            id="menu-appbar"
            anchorEl={anchorEl}
            open={Boolean(anchorEl)}
            onClose={handleClose}
          >
            <MenuItem onClick={openDialog} >Profile  <AccountCircleRoundedIcon style={{marginLeft: '5px'}}/> </MenuItem>
            <MenuItem onClick={handleClick2}>Settings <ManageAccountsRoundedIcon style={{marginLeft: '5px'}}/> </MenuItem>
            
          </Menu>

          <Menu
          id="menu-changedata"
          anchorEl={anchorEl2}
          open={Boolean(anchorEl2)}
          onClose={handleClose2}>
            <MenuItem >Change personal data <PasswordRoundedIcon style={{marginLeft: '5px'}}/></MenuItem>
          </Menu>

          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            Welcome Kristian
          </Typography>
          <Button color='inherit'>
                  Help
            <HelpRoundedIcon size='small' style={{marginLeft: '5px'}}/>
          </Button>
          <Button color="inherit" onClick={handleLogOut}>Log Out <LogoutRoundedIcon style={{marginLeft: '5px'}} /></Button>
        </Toolbar>
      </AppBar>
      <FullScreenDialog open={open} handleClose={closeDialog}/>
      
    </Box>
  );
}
