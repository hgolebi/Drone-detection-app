import './MainScreen.css'
import React from 'react'

const API_URL = 'http://localhost:5000/'
function pass(){;}

class MainScreen extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            videos: [],
            vid_group: 'video/',
            vid_name: null,
        }
    }

    componentDidMount() {
        this.getVideos();
        return;
    }

    getVideos()  {
        fetch(API_URL+'video/').then(response => response.json())
        .then(json => {
            this.setState({videos: json});
            this.setState({vid_name: json[0]})
        })
    }

    sendVideo(video) {
        const videoData = new FormData();
        videoData.append('file', video, video.name);
        fetch(API_URL+'upload/', {
          method: 'POST',
          body: videoData
        })
          .then(response => console.log(response))
          .then(() => this.getVideos())
          .catch(error => console.error(error))
    }

    addVideoEventHandler = (event) => {
        const file = event.target.files[0];
        if (file == undefined) {
            return;
        }
        this.sendVideo(file);
    }

    train = () => {
        this.setState({vid_group: 'tracking/'});
    }

    render(){
        const thumbnail_list = this.state.videos.map((video, index) => (
            <div className='tn_card' key={index}>
                <img
                    className='tn'
                    src={API_URL+'thumbnail/'+video}
                    key={index}>
                    </img>
            </div>
        ))
        return (
            <div id="main_screen">
                <div id="video_container">
                    <video id='video' controls
                        src={API_URL+this.state.vid_group+this.state.vid_name} type='video/mp4'>
                    </video>
                </div>
                <div id="buttons_container">
                    <button id="train" onClick={this.train}>train</button>
                    <input type='range'></input>
                    <button id="download" onClick>download</button>
                </div>
                <div id="thumbnails_container">
                    <input
                        type="file"
                        accept="video/mp4, video/mov"
                        onChange={this.addVideoEventHandler}>
                    </input>
                    <ul id='tn_list'>
                        {thumbnail_list}
                    </ul>
                </div>
            </div>
        )
    }
}

export default MainScreen