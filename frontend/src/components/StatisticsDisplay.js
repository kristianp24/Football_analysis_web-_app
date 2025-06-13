import { Typography } from "@mui/material";

const StatisticsDisplay = ({team_name, passes, possesion, possesion_percentage, km_runned, avg_speed_player}) => {
    return (
        <div>
             <Typography variant="h6"> Team: {team_name} </Typography>
             <Typography variant="h6">Possesion ball percentage: {possesion_percentage}% </Typography>
             <Typography variant="h6">Possesion ball count: {possesion}</Typography>
             <Typography variant="h6"> Number of passes: {passes}</Typography>
             <Typography variant="h6"> Estimated km runned: {km_runned} km</Typography>
             <Typography variant="h6"> Estimated Average speed of player: {avg_speed_player} km/h </Typography>
        </div>
       
    );
}

export default StatisticsDisplay;