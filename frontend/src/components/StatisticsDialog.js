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
import StatisticsDisplay from './StatisticsDisplay';
import downloadHeatmap from '../requests/getHeatmap';

const Transition = React.forwardRef(function Transition(props, ref) {
  return <Slide direction="up" ref={ref} {...props} />;
});

export default function FullScreenDialog({open,handleClose, predictionData}) {
  const [name, setName] = React.useState(null);
  const [email, setEmail] = React.useState(null);
  const [data, setData] = React.useState({'team_0': "NA", 'team_1':"NA"});
   
  React.useEffect(() => {
    getName();
    getUserEmail();
    const prediction = JSON.parse(sessionStorage.getItem('prediction'));
    console.log('Type of prediction!!!', typeof(prediction))
    if (prediction === null || prediction === typeof(undefined)){
       const pred = {'team_0': "NA", 'team_1':"NA"}
       setData(pred)
    }
    else{
       setData(prediction);
    }
   
  }, [open])

  const handleDownloadHeatmap = (team_name, team_cluster) => {
    if (sessionStorage.getItem('prediction') !== null){
       console.log('Team name:', team_name)
    console.log('Team cluster:', team_cluster)
    downloadHeatmap(team_name, team_cluster);
    }
    else{
       console.log('No prediction data found!')
       return;
    }
    
  }

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
              Match Statistics
            </Typography>
           
          </Toolbar>
        </AppBar>
        <Box 
              sx={{ 
                display: 'flex', 
                alignItems: 'center',
                justifyContent: 'center', 
                pt: 2, 
                mt: -12,
                flexDirection: 'column',
                justifyContent: 'center', 
                height: '100vh',
                gap: 2,
              }}
        >
          <Box sx={{ width: '300px', height: '100px', p:1, m: 2 , alignItems: 'center', justifyContent: 'center', display: 'flex', flexDirection: 'column', backgroundColor: '#BDBDBD', 
                     border: "2px solid black", borderRadius: "10px", 
          }}>
            <Typography variant='h6' >Name: {name} </Typography>
            <Typography variant='h6' >Email: {email}</Typography>
            
         
          </Box>
        
       <Box sx={{
        justifyContent: 'center',
        flexDirection: 'row',
        display: 'flex',
        flexWrap: 'nowrap', 
        width: '100%',
       }}>
          <Box sx={{ width: '400px', height: '250px', p:1, m: 2 , alignItems: 'center', justifyContent: 'center', display: 'flex', flexDirection: 'column', backgroundColor: '#BDBDBD',
                      border: "2px solid black", borderRadius: "10px", 
            }}>
               <StatisticsDisplay team_name= {data['team_0']['name']}
                                  passes= {data['team_0']['number_of_passes']} 
                                  possesion= {data['team_0']['possesion_count']}
                                  possesion_percentage={data['team_0']['percentage_possesion']}
               ></StatisticsDisplay>

               <Button variant="contained" startIcon={<SaveIcon />} sx={{ mt: 2 }} onClick={() => handleDownloadHeatmap(data['team_0']['name'], 0)}>
                Generate Team Heatmap
              </Button>
          </Box>

          <Box sx={{ width: '400px', height: '250px', p:1, m: 2 , alignItems: 'center', justifyContent: 'center', display: 'flex', flexDirection: 'column', backgroundColor: '#BDBDBD',
                      border: "2px solid black", borderRadius: "10px", 
            }}>
                 <StatisticsDisplay team_name= {data['team_1']['name']}
                                  passes= {data['team_1']['number_of_passes']} 
                                  possesion= {data['team_1']['possesion_count']}
                                  possesion_percentage={data['team_1']['percentage_possesion']}
               ></StatisticsDisplay>
               <Button variant="contained" startIcon={<SaveIcon />} sx={{ mt: 2 }} onClick={() => handleDownloadHeatmap(data['team_1']['name'], 1)}>
                Generate Team Heatmap
              </Button>
            </Box>
       </Box>
          
         
         </Box>

      </Dialog>
    </React.Fragment>
  );
}
