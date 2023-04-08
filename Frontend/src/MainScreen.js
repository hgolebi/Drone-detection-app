import './MainScreen.css'

function MainScreen(props) {

    function pass(){;}
    return (
        <div id="main_screen">
            <div id="video_container">
                <video id='video' controls
                    src='./videos/vid.mp4' type='video/mp4'>
                </video>
            </div>
            <div id="buttons_container">
                <button id="slow" onClick={pass}>slow</button>
                <button id="fast" onClick={pass}>fast</button>
                <button id="flow" onClick={pass}>flow</button>
                <input type='range'></input>
                <button id="download">download</button>
            </div>
            <div id="thumbnails_container">C</div>
            
        </div>
    )
}

export default MainScreen