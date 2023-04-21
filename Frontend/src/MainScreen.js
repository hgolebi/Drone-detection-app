import './MainScreen.css'
import React from 'react'

const API_URL = 'http://localhost:5000/'
function pass(){const elo = 'elo';}

class MainScreen extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            videos: [],
        }
    }

    loadVideos() {
        fetch("http://localhost:5000/video/")
        .then(response => response.json())
        .then(json => console.log(json))
        return
    }

    sendVideo = (video) => {
        const videoData = new FormData();
        videoData.append('file', video, video.name);
        fetch(API_URL+'upload/', {
          method: 'POST',
          body: videoData
        })
          .then(response => console.log(response))
        //   .then(() => this.getPhotos())
          .catch(error => console.error(error))
      }

    addVideoEventHandler = (event) => {
        const file = event.target.files[0];
        if (file == undefined) {
            return;
        }
        this.sendVideo(file);
    }


    render(){
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
                    <button id="download" onClick>download</button>
                </div>
                <div id="thumbnails_container">
                <input
                    type="file"
                    accept="video/mp4, video/mov"
                    onChange={this.addVideoEventHandler}>
                </input>
                </div>

            </div>
        )
    }
}

export default MainScreen