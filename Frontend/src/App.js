import './App.css';
import React from 'react';
import LoggingScreen from "./LoggingScreen";
import MainScreen from "./MainScreen"

function App() {

  const [isLoggingScreen, toggleLoggingScreen] = React.useState(true);


  return (
    <div id='main'>
      <div id='logscreen'>
        {isLoggingScreen ? <LoggingScreen/> : <MainScreen/>}
      </div>
    </div>
  );
}

export default App;
