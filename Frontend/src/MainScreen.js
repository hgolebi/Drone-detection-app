import './MainScreen.css'

function MainScreen(props) {

    function pass(){;}
    return (
        <div id="main_screen">
            <div id="video">A</div>
            <div id="controls">
                <button id="slow" onClick={pass}>slow</button>
                <button id="fast" onClick={pass}>fast</button>
                <button id="flow" onClick={pass}>flow</button>
                <input type='range'></input>
                <button id="download">download</button>
            </div>
            <div id="thumbnail_list">C</div>
            
        </div>
    )
}

export default MainScreen