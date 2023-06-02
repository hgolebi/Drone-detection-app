import './MainScreen.css'
import React from 'react'

var API_URL = 'http://192.168.1.27:5000/'

class MainScreen extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            videos: [],
            vid_group: 'videos/',
            vid_name: undefined,
            generated_vid: undefined,
            is_gen_vid_displayed: false,
            method: undefined,
            precision: 40
        }
    }

    componentDidMount() {
        this.getVideos();
        return;
    }

    getVideos() {
        fetch(API_URL + 'videos', {
            credentials: 'include',
        })
        .then(response => response.json())
        .then(json => {
            this.setState({ videos: json });
            this.changeVideo(json[0])
        })
    }

    changeVideo(name) {
        this.setState({
            vid_name: name,
            vid_group: 'videos/',
            is_gen_vid_displayed: false,
        })
    }

    sendVideo(video) {
        const videoData = new FormData();
        videoData.append('file', video, video.name);
        fetch(API_URL + 'videos', {
            method: 'POST',
            body: videoData,
            credentials: 'include',
        })
        .then(response => console.log(response))
        .then(() => this.getVideos())
        .catch(error => console.error(error))
    }

    addVideoEventHandler = (event) => {
        const file = event.target.files[0];
        if (file === undefined) {
            return;
        }
        this.sendVideo(file);
    }

    train = () => {
        fetch(API_URL + 'tracked/'+ this.state.vid_name, {
            credentials: 'include',
        })
        .then(() => this.setState({vid_group: 'tracked/'}));
    }

    showGeneratedVideo() {
        this.setState({
            vid_group: 'tracked/',
            is_gen_vid_displayed: true,
        });
        // this.setState({is_gen_vid_displayed: true});
    }

    goBack() {
        this.setState({
            vid_group: 'videos/',
            is_gen_vid_displayed: false,
        });
    }

    deleteVideo(name) {
        return;
    }

    handleSliderChange = (event) => {
        this.setState({precision: event.target.value});
    }

    handleMethodChange = (event) => {
        this.setState({method: event.target.value});
    }

    getGeneratedVideo() {

    }

    generateVideo() {
        const vid_name = this.state.vid_name
        const method = this.state.method
        const precision = this.state.precision / 100
        const form = {
            tracker: method,
            treshold: precision,
        }
        fetch(API_URL + 'tracking/' + vid_name, {
            method: 'POST',
            headers: {
                'Content-type': 'application/json'
            },
            credentials: 'include',
            body: JSON.stringify(form),
        })
        .then(response => {
            if (response.ok) {
                this.setState({
                    generated_vid: 'tracked/' + vid_name + '?treshold=' + precision + '&tracker=' + method,
                })
            }
        })
    }

    render() {
        const thumbnail_list = this.state.videos.map((name, index) => (
            <div className='tn_card' key={index} name={name} onClick={() => this.changeVideo(name)}>
                <img className='tn' src={API_URL+'thumbnails/'+name} key={'tn' + index}></img>
                <img key={'del' + index} className='delete' onClick={() => this.deleteVideo(name)} src='delete.png'></img>
            </div>
        ))
        const main_vid_controls =
        <div className='main_vid_controls'>
            <div className='generate_btns'>
                <b className='btn_label'>CHOOSE METHOD</b>
                <div className='method_btns'>
                    <label className='radio'>
                        <input type='radio' value='deepsort' name='method' onChange={this.handleMethodChange}></input>
                        <span>deepsort</span>

                    </label>
                    <label className='radio'>
                        <input type='radio' value='sort' name='method' onChange={this.handleMethodChange}></input>
                        <span>sort</span>
                    </label>
                    <label className='radio'>
                        <input type='radio' value='medianflow' name='method' onChange={this.handleMethodChange}></input>
                        <span>medianflow</span>
                    </label>
                </div>
                <div className='method_btns'>
                    <label className='radio'>
                        <input type='radio' value='kcf' name='method' onChange={this.handleMethodChange}></input>
                        <span>kcf</span>

                    </label>
                    <label className='radio'>
                        <input type='radio' value='csrt' name='method' onChange={this.handleMethodChange}></input>
                        <span>csrt</span>
                    </label>
                    <label className='radio'>
                        <input type='radio' value='opticalflow' name='method' onChange={this.handleMethodChange}></input>
                        <span>opticalflow</span>
                    </label>
                </div>
                <b>CHOOSE PRECISION</b>
                <div className="slidecontainer">
                    <input type="range" min="0" max="100" value={this.state.precision} class="slider" id="myRange" onChange={this.handleSliderChange}></input>
                </div>
                <button className='btn generate' onClick={() => this.generateVideo()}>Generate</button>
            </div>
            <div className='gen_vid_panel'>
                <b>GENERATED VIDEO</b>
                <div className='gen_vid_card' onClick={() => this.showGeneratedVideo()}>
                    <img src='play.png' className='icon play'></img>
                    <video className='gen_vid' src={API_URL + this.state.generated_vid} type='video/mp4'></video>
                </div>
            </div>
        </div>
        const gen_vid_controls =
        <div className='gen_vid_controls'>
            <div className='button_card' onClick={() => this.goBack()}>
                <b>GO BACK</b>
                <img src='arrow_back.png' className='icon back'></img>
            </div>
            <div className='button_card'>
                <b className='button_label'>DOWNLOAD VIDEO</b>
                <img src='download_film.png' className='icon down_vid'></img>
            </div>
            <div className='button_card'>
                <b className='button_label'>DOWNLOAD ADDNOTATIONS</b>
                <img src='download_file.png' className='icon down_addn'></img>
        </div>

    </div>
        return (
            <div id="main_screen">
                <div id="video_container">
                    <video id='video' controls
                        src={API_URL + this.state.vid_group + this.state.vid_name} type='video/mp4'>
                    </video>
                </div>
                <div id="buttons_container">
                    {this.state.is_gen_vid_displayed ? gen_vid_controls : main_vid_controls }
                </div>
                <div id="thumbnails_container">
                    <input
                        id='add_file'
                        type="file"
                        accept="video/mp4, video/mov"
                        onChange={this.addVideoEventHandler}
                        className='add_file_input'>

                    </input>
                    <label htmlFor='add_file' className='add_file_label'>
                        <img className='icon upload' src='upload.png'></img>
                        Add file
                    </label>
                    <ul id='tn_list'>
                        {thumbnail_list}
                    </ul>
                </div>
            </div>
        )
    }
}

export default MainScreen