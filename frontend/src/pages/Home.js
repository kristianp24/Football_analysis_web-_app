import LogInForm from '../components/LogInForm';
import logo from '../icon_football.png';
import { Button } from '@mui/material';

const Home = () => {    
    return (
        <div className="Home">    
              <header className="Home-header">
                {/* <img src={logo} className="Home-logo" alt="logo" /> */}
                 
                  <div style={{display: 'flex', justifyContent: 'center'}}>
                <LogInForm />
          
                  </div>
                 
              </header>
            
            
            </div>
    );
}

export default Home;