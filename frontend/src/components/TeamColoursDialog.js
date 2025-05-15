import * as React from 'react';
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import DialogContentText from '@mui/material/DialogContentText';
import DialogTitle from '@mui/material/DialogTitle';
import TextFieldTeamDialog from './TextFieldTeamDialog';

export default function FormDialog({openForm, onClose, openDialog}) {
  const [open, setOpen] = React.useState(false);
  const [color1, setColor1] = React.useState('rgb(122, 168, 37)');
  const [color2, setColor2] = React.useState('rgb(199, 134, 60)');
  
  React.useEffect(() => {
    setOpen(openForm);
    const prediction = JSON.parse(sessionStorage.getItem('prediction'));
    if (prediction !== null) {
       const [r, g, b] = prediction.team_0.colour;
      setColor1(`rgb(${r}, ${g}, ${b})`);
      const [r2, g2, b2] = prediction.team_1.colour;
      setColor2(`rgb(${r2}, ${g2}, ${b2})`);
    }
   
  }, [openForm])
 
  
  const onSubmit = (e) => {
    const team1 = document.getElementById('team1').value;
    const team2 = document.getElementById('team2').value;

    if (team1 === '' || team2 === ''){
      return;
    }

    
    const prediction = JSON.parse(sessionStorage.getItem('prediction'));
    console.log(prediction);
    prediction['team_0']['name'] = team1;
    prediction['team_1']['name'] = team2;
    
    
    sessionStorage.setItem('prediction', JSON.stringify(prediction));
    
    setOpen(false);
    onClose();
    openDialog();

  }

  return (
    <React.Fragment>
     
      
      <Dialog
        open={open}
       
      >
        <DialogTitle>Put team colours</DialogTitle>
        <DialogContent>
          <DialogContentText>
           We detected 2 team colors in this video. Please enter the team names for each colour 
           for better visualization. Write each team name in the corresponding text colour.
          </DialogContentText>
            <TextFieldTeamDialog name="team1Input" id="team1" label="Team 1 name" color={color1} />
            <TextFieldTeamDialog name="team2Input" id="team2" label="Team 2 name" color={color2} />
        </DialogContent>
        <DialogActions>
          
          <Button type="submit" onClick={onSubmit}>Done</Button>
        </DialogActions>
      </Dialog>
    </React.Fragment>
  );
}
