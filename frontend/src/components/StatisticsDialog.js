import * as React from 'react';
import Button from '@mui/material/Button';
import Dialog from '@mui/material/Dialog';
import AppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import IconButton from '@mui/material/IconButton';
import Typography from '@mui/material/Typography';
import CloseIcon from '@mui/icons-material/Close';
import Slide from '@mui/material/Slide';
import SaveIcon from '@mui/icons-material/Save';
import PercentIcon from '@mui/icons-material/Percent';
import SportsSoccerIcon from '@mui/icons-material/SportsSoccer';
import SpeedIcon from '@mui/icons-material/Speed';
import DirectionsRunIcon from '@mui/icons-material/DirectionsRun';
import TimelineIcon from '@mui/icons-material/Timeline';
import { Box, Card, Avatar, Grid, Stack } from '@mui/material';
import getFullName from '../requests/getFullNameRequest';
import getEmail from '../requests/getUserEmail';
import downloadHeatmap from '../requests/getHeatmap';
import getMatchReport from '../requests/getMatchReport';
import CountUp from 'react-countup';

const Transition = React.forwardRef(function Transition(props, ref) {
  return <Slide direction="up" ref={ref} {...props} />;
});

const StatRow = ({ icon, label, value, highlight, isNegative }) => (
  <Stack direction="row" alignItems="center" spacing={2} sx={{ mb: 1 }}>
    <Box>{icon}</Box>
    <Typography variant="body2" sx={{ flex: 1 }}>{label}</Typography>
    <Box
      sx={{
        px: 1.5,
        py: 0.5,
        borderRadius: 2,
        fontWeight: 500,
        color: 'white',
        bgcolor: highlight ? 'green' : isNegative ? 'red' : 'grey.400',
        minWidth: '60px',
        textAlign: 'center'
      }}
    >
      {value}
    </Box>
  </Stack>
);

export default function FullScreenDialog({ open, handleClose }) {
  const [name, setName] = React.useState(null);
  const [email, setEmail] = React.useState(null);
  const [data, setData] = React.useState({ 'team_0': {}, 'team_1': {} });

  React.useEffect(() => {
    getFullName().then(setName);
    const userEmail = getEmail();
    if (userEmail) setEmail(userEmail);
    const prediction = JSON.parse(sessionStorage.getItem('prediction'));
    if (prediction) setData(prediction);
  }, [open]);

  const handleDownloadHeatmap = (teamName, teamCluster) => {
    if (sessionStorage.getItem('prediction')) {
      downloadHeatmap(teamName, teamCluster);
    } else {
      console.log('No prediction data found!');
    }
  };

  const downloadReport = () => {
    const prediction = sessionStorage.getItem('prediction');
    if (prediction) {
      getMatchReport(JSON.parse(prediction));
    } else {
      console.log('No prediction data found!');
    }
  };

  const team0 = data.team_0 || {};
  const team1 = data.team_1 || {};

  const getHighlightFlags = (key) => {
    const a = team0[key] || 0;
    const b = team1[key] || 0;
    return [a > b, b > a];
  };

  const formatCountUp = (val, suffix = '', decimals = 3) =>
    val !== undefined && !isNaN(val) ? <CountUp end={val} decimals={decimals} suffix={suffix} duration={1.5} /> : 'N/A';

  const renderTeamCard = (team, clusterIndex, isTeam0) => {
    const [pos0, pos1] = getHighlightFlags('percentage_possesion');
    const [count0, count1] = getHighlightFlags('possesion_count');
    const [pass0, pass1] = getHighlightFlags('number_of_passes');
    const [run0, run1] = getHighlightFlags('km_runned');
    const [spd0, spd1] = getHighlightFlags('avg_speed_player');

    return (
      <Grid item xs={12} md={5} key={team.name}>
        <Card sx={{ p: 3, borderRadius: 3 }}>
          <Typography variant="h6" gutterBottom>{team.name}</Typography>
          <StatRow icon={<PercentIcon />} label="Possession" value={formatCountUp(team.percentage_possesion, '%', 0)} highlight={isTeam0 ? pos0 : pos1} isNegative={isTeam0 ? pos1 : pos0} />
          <StatRow icon={<SportsSoccerIcon />} label="Ball Count" value={formatCountUp(team.possesion_count, '', 0)} highlight={isTeam0 ? count0 : count1} isNegative={isTeam0 ? count1 : count0} />
          <StatRow icon={<TimelineIcon />} label="Passes" value={formatCountUp(team.number_of_passes, '', 0)} highlight={isTeam0 ? pass0 : pass1} isNegative={isTeam0 ? pass1 : pass0} />
          <StatRow icon={<DirectionsRunIcon />} label="Km Run" value={formatCountUp(team.km_runned, ' km')} highlight={isTeam0 ? run0 : run1} isNegative={isTeam0 ? run1 : run0} />
          <StatRow icon={<SpeedIcon />} label="Speed" value={formatCountUp(team.avg_speed_player, ' m/s')} highlight={isTeam0 ? spd0 : spd1} isNegative={isTeam0 ? spd1 : spd0} />
          <Box sx={{ mt: 3 }}>
            <Button variant="contained" startIcon={<SaveIcon />} fullWidth onClick={() => handleDownloadHeatmap(team.name, clusterIndex)}>
              Generate Team Heatmap
            </Button>
          </Box>
        </Card>
      </Grid>
    );
  };

  return (
    <Dialog fullScreen open={open} onClose={handleClose} TransitionComponent={Transition}>
      <AppBar sx={{ position: 'relative' }}>
        <Toolbar>
          <IconButton edge="start" color="inherit" onClick={handleClose} aria-label="close">
            <CloseIcon />
          </IconButton>
          <Typography sx={{ ml: 2, flex: 1 }} variant="h6" component="div">
            Match Statistics
          </Typography>
          <Button autoFocus color="inherit" onClick={downloadReport}>Download as PDF</Button>
        </Toolbar>
      </AppBar>

      <Box sx={{ p: 4 }}>
        <Box sx={{ display: 'flex', justifyContent: 'center', mb: 4 }}>
          <Card sx={{ px: 4, py: 2, borderRadius: 3, display: 'flex', alignItems: 'center', gap: 2 }}>
            <Avatar />
            <Box>
              <Typography variant="h6">{name}</Typography>
              <Typography variant="body2" color="text.secondary">{email}</Typography>
            </Box>
          </Card>
        </Box>

        <Grid container spacing={3} justifyContent="center">
          {renderTeamCard(team0, 0, true)}
          {renderTeamCard(team1, 1, false)}
        </Grid>
      </Box>
    </Dialog>
  );
}
