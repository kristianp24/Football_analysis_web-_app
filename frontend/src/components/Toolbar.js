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
import FullScreenDialog from './StatisticsDialog';
import { useNavigate } from 'react-router-dom';
import logout from '../requests/logoutRequest';
import getFullName from '../requests/getFullNameRequest';

export default function ButtonAppBar() {
    const [anchorEl, setAnchorEl] = React.useState(null);
    const [anchorEl2, setAnchorEl2] = React.useState(null); 
    const [open, setOpen] = React.useState(false);
    const [name, setName] = React.useState(null);
    const navigate = useNavigate();

    React.useEffect(() => {
      loadName();
  }, []);

    const loadName = async () => {
      const full_name = await getFullName()
          console.log(full_name)
          if (full_name !== null)
          {
            
            setName(String(full_name));
          }
          else{
            setName("No name found!")
          }
    }


    const handleLogOut = async () => {
          const token = localStorage.getItem('token');
          const response = await logout(token);
          if (response.status === 200){
            localStorage.removeItem('token');
            if (sessionStorage.getItem('prediction') !== null){
            sessionStorage.removeItem('prediction');
            }
            navigate('/')
          }
          else if (response.status === 500){
             console.log(response['response']['data']['error']);
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
            Welcome {name}
          </Typography>
          <Button color='inherit'>
                  Help
            <HelpRoundedIcon size='small' style={{marginLeft: '5px'}}/>
          </Button>
          <Button color="inherit" onClick={handleLogOut}>Log Out <LogoutRoundedIcon style={{marginLeft: '5px'}} /></Button>
        </Toolbar>
      </AppBar>
     
    </Box>
  );
}
