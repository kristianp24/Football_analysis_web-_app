import LogInForm from '../components/LogInForm';
import logo from '../icon_football.png';

const Home = () => {    
    return (
        <div className="Home">    
              <header className="Home-header">
                {/* <img src={logo} className="Home-logo" alt="logo" /> */}
                  <p id='welcome-txt'>
                    Welcome to Football Analysys App
                  </p>
                  <div style={{display: 'flex', justifyContent: 'center'}}>
                <LogInForm />
                  </div>
                 
              </header>
            
            
            </div>
    );
}

export default Home;