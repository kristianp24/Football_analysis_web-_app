import './App.css';
import Home from './pages/Home';
import VideoDownload from './pages/VideoDownloaderPage';
import { BrowserRouter as Router, Route, Switch, Routes } from 'react-router-dom';




function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/VideoDownload" element={<VideoDownload />} />  
      </Routes>
        
      </Router>
  );
}

export default App;
