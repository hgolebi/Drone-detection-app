import './MainScreen.css'

function MainScreen(props) {

    function loadVideos() {
        fetch("http://localhost:5000/video/")
        .then(response => response.json())
        .then(json => console.log)
        return
    }

    function pass(){;}
    return (
        <div id="main_screen">
            <div id="video_container">
                <video id='video' controls
                    src='./videos/vid.mp4' type='video/mp4'>
                </video>
            </div>
            <div id="buttons_container">
                <button id="slow" onClick={loadVideos}>slow</button>
                <button id="fast" onClick={pass}>fast</button>
                <button id="flow" onClick={pass}>flow</button>
                <input type='range'></input>
                <button id="download" onClick>download</button>
            </div>
            <div id="thumbnails_container">
                
            </div>
            
        </div>
    )
}

export default MainScreen