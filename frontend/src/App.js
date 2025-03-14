import './App.css';
import Home from './pages/Home';
import VideoDownload from './pages/VideoDownloaderPage';
import Register from './pages/Register';
import { BrowserRouter as Router, Route, Switch, Routes } from 'react-router-dom';
import ProtectedRoute from './components/Protected';



function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path='/VideoDownload' element={<ProtectedRoute element={VideoDownload} />} />
       
        <Route path='/Register' element={<Register />} /> 
      </Routes>
        
      </Router>
  );
}

export default App;
