import { Typography } from "@mui/material";

const StatisticsDisplay = ({team_name, passes, possesion, possesion_percentage}) => {
    return (
        <div>
             <Typography variant="h6"> Team: {team_name} </Typography>
             <Typography variant="h6">Possesion ball percentage: {possesion_percentage}% </Typography>
             <Typography variant="h6">Possesion ball count: {possesion}</Typography>
             <Typography variant="h6"> Number of passes: {passes}</Typography>
        </div>
       
    );
}

export default StatisticsDisplay;