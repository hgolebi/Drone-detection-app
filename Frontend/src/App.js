import './App.css';
import React from 'react';
import LoggingScreen from "./LoggingScreen";
import MainScreen from "./MainScreen"

function App() {
  const [isLoggingScreen, setLoggingScreen] = React.useState(true);
  return (
    <div id='app'>
      <div id='logscreen'>
        {isLoggingScreen ? <LoggingScreen switchScene = {setLoggingScreen}/> : <MainScreen/>}
      </div>
    </div>
  );
}

export default App;
