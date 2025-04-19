import TextField from '@mui/material/TextField';

const TextFieldTeamDialog = ({ name, id, label, color, value, onChange}) => {
   
    return(
    <TextField
                autoFocus
                required
                margin="dense"
                id={id}
                name={name}
                label= {label}
                type="text"
                fullWidth
                variant="standard"
                value={value}   
                onChange={onChange} 
                sx={{
                    '& .MuiInputBase-input': {
                      color: {color}, 
                    },
                    '& .MuiInputLabel-root': {
                      color: {color}, 
                    },
                    '& .MuiInput-underline:before': {
                      borderBottomColor: {color}, 
                    },
                    '& .MuiInput-underline:after': {
                      borderBottomColor: {color}, 
                    },
                    '& .MuiInput-underline:hover:before': {
                      borderBottomColor: {color}, 
                    },
                    '& .MuiInput-underline:hover:after': {
                      borderBottomColor: {color}, 
                    },}}
              />
    );
}

export default TextFieldTeamDialog;
