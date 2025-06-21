import * as React from 'react';
import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';
import ActionAreaCard from './HelpCard';
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
    const [name, setName] = React.useState(null);
    const [open, setOpen] = React.useState(false);
    const navigate = useNavigate();

    React.useEffect(() => {
      loadName();
  }, []);

   const onClickHelp = () => {
      setOpen(true);
    }

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

  return (
    <Box sx={{ flexGrow: 1 }}>
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6" sx={{ fontWeight: 'bold', flexGrow: 1 }}>
                  Welcome {name ? name : 'User'}
          </Typography>
          <Button color='inherit' onClick={onClickHelp}>
                  Help
            <HelpRoundedIcon size='small' style={{marginLeft: '5px'}} />
          </Button>
          <Button color="inherit" onClick={handleLogOut}>Log Out <LogoutRoundedIcon style={{marginLeft: '5px'}} /></Button>
        </Toolbar>
          </AppBar>
          <Box
        sx={{
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center', 
          mt: 2, 
        }}
      >
        <ActionAreaCard open={open} setOpen={setOpen} />
      </Box>
    </Box>
  );
}
