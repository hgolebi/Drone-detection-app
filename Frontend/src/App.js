import './App.css';
import React from 'react';
import LoggingScreen from "./LoggingScreen";
import MainScreen from "./MainScreen"


function App() {
  const [isLoggingScreen, setLoggingScreen] = React.useState(true);
  return (
    <div id='app'>
      {isLoggingScreen ? <LoggingScreen switchScene = {setLoggingScreen}/> : <MainScreen/>}
    </div>
  );
}

export default App;
