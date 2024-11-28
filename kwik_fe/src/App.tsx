import './App.css';
import {HashRouter as R, Route, Routes} from 'react-router-dom'
import Nav from './components/Navigators/Nav';
import MobileNav from './components/Navigators/MobileNav';
import Home from './views/Home';
import About from './views/About';
import Login from './views/Login';
import AddCase from "./views/AddCase";
import Track from "./views/Track";
import Cases from "./views/Cases";

function App() {
  return (
      // wrap around navigation

        <R>
          <div className="App">
            <Nav/>
            <div className='rom-app'>
              <Routes>
                  <Route element={<Home/>} path='/' />
                  <Route element={<About/>} path='/about' />
                  <Route element={<Login/>} path='/alogin' />
                  <Route element={<AddCase/>} path='/add-case' />
                  <Route element={<Track/>} path='/track/:cid' />
                  <Route element={<Cases/>} path='/cases/' />

              </Routes>
            </div>
            <MobileNav/>
          </div>
        </R>
  );
}

export default App;
