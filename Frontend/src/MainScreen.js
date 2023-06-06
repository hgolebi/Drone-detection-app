import './MainScreen.css'
import React from 'react'

var API_URL = 'http://192.168.1.27:5000/'
// var API_URL = 'http://172.20.0.2:5000/'


class MainScreen extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            videos: [],
            vid_group: 'videos/',
            vid_name: undefined,

            last_generated: undefined,
            is_gen_vid_displayed: false,
            method: 'deepsort',
            precision: 0.3,
            generating: false,
            gen_videos: [],
            isListVisible: false,
        }
    }

    componentDidMount() {
        this.getVideos();

        // this.updateGeneratedVideo();
        return;
    }

    componentDidUpdate(prevProps, prevState) {
        // if (prevState.vid_name !== this.state.vid_name ||
        // prevState.method != this.state.method) {
        //     this.updateGeneratedVideo();
        // }
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

    getGeneratedVideos(vid_name) {
        fetch(API_URL + 'list_tracked_videos/' + vid_name, {
            credentials: 'include',
        })
        .then(response => response.json())
        .then(json => {
            const keys = Object.keys(json);
            const lastKey = keys[keys.length - 1];
            const lastValue = json[lastKey];
            const attributes = this.processVideoName(lastValue);
            const video_name = attributes[0];
            const precision = parseInt(attributes[1]) / 10000;
            const method = attributes[2];
            const gen_vid_name = video_name + '.mp4?treshold=' + precision + '&tracker=' + method;
            this.setState({
                gen_videos: json,
                last_generated: gen_vid_name,
            });
        })
        .catch(error => console.error(error))
    }

    changeVideo(name) {
        this.setState({
            vid_name: name,
            vid_group: 'videos/',
            is_gen_vid_displayed: false,
        })
        this.getGeneratedVideos(name);
    }

    processVideoName(filename) {
        const regex = /^(.*)-(\d+)-(.*).mp4$/;
        const matches = filename.match(regex);

        if (matches && matches.length === 4) {
            const name = matches[1]
            const precision = matches[2];
            const method = matches[3];
            return [name, precision, method]
        }
    }

    listElemOnClickHandle(event) {

    }

    createListElement(name) {
        const attributes = this.processVideoName(name)
        const video_name = attributes[0]
        const precision = parseInt(attributes[1]) / 10000
        const method = attributes[2]
        const gen_vid_name = video_name + '.mp4?treshold=' + precision + '&tracker=' + method
        return (
            <div className='list_elem'>
                <div className='gen_vid_card gvt' value={gen_vid_name} onClick={this.listElemOnClickHandle}>
                    <video className='gen_vid' src={API_URL + 'tracked_videos/' + gen_vid_name} name={gen_vid_name} type='video/mp4'></video>
                    <img src='play.png' className='icon play'></img>
                </div>
                <div className='attributes'>
                    <p>Method</p>
                    <b className='attr meth'>{method}</b>
                    <p>Precision</p>
                    <b className='attr prec'>{precision}</b>
                </div>
            </div>
        )
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
        fetch(API_URL + 'tracked_videos/'+ this.state.vid_name, {
            credentials: 'include',
        })
        .then(() => this.setState({vid_group: 'tracked_videos/'}));
    }

    showGeneratedVideo() {
        this.setState({
            vid_group: 'tracked_videos/',
            is_gen_vid_displayed: true,
        });
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
        const value = event.target.value / 100
        this.setState({precision: value});
    }

    handleMethodChange = (event) => {
        this.setState({method: event.target.value});

    }

    handleGenerateButton = () => {
        this.setState({generating: true})
        this.generateVideo()
    }

    generateVideo() {
        this.setState({generating: true})
        const vid_name = this.state.vid_name
        const method = this.state.method
        const precision = this.state.precision
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
        .then(() => {
            this.setState({generating: false})
            this.getGeneratedVideos(vid_name)
        })
    }

    downloadVideo() {
        fetch(API_URL + 'tracked_videos/' + this.state.last_generated + '&as_attachment=True', {
            credentials: 'include',
            headers: {
                'Accept': 'video/*'
            }
        })
        .then(response => response.blob())
        .then(blob => {
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'tracked_' + this.state.vid_name;
            a.click();
        });
    }

    downloadAddnotations() {
        fetch(API_URL + 'adnotations/' + this.state.last_generated, {
            credentials: 'include',
        })
        .then(response => response.blob())
        .then(blob => {
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'annotations.txt';
            a.click();
        });
    }

    updateGeneratedVideo() {
        const vid_name = this.state.vid_name
        const treshold = this.state.precision
        const tracker = this.state.method
        const gen_vid =  vid_name + "?treshold=" + treshold + '&tracker=' + tracker
        this.setState({last_generated: gen_vid})
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
                        <input type='radio' value='deepsort' checked={this.state.method === 'deepsort'} name='method' onChange={this.handleMethodChange}></input>
                        <span>deepsort</span>

                    </label>
                    <label className='radio'>
                        <input type='radio' value='sort' checked={this.state.method === 'sort'} name='method' onChange={this.handleMethodChange}></input>
                        <span>sort</span>
                    </label>
                    <label className='radio'>
                        <input type='radio' value='medianflow' checked={this.state.method === 'medianflow'} name='method' onChange={this.handleMethodChange}></input>
                        <span>medianflow</span>
                    </label>
                </div>
                <div className='method_btns'>
                    <label className='radio'>
                        <input type='radio' value='kcf' checked={this.state.method === 'kcf'} name='method' onChange={this.handleMethodChange}></input>
                        <span>kcf</span>

                    </label>
                    <label className='radio'>
                        <input type='radio' value='csrt' checked={this.state.method === 'csrt'} name='method' onChange={this.handleMethodChange}></input>
                        <span>csrt</span>
                    </label>
                    <label className='radio'>
                        <input type='radio' value='opticalflow' checked={this.state.method === 'opticalflow'} name='method' onChange={this.handleMethodChange}></input>
                        <span>opticalflow</span>
                    </label>
                </div>
                <b>CHOOSE PRECISION</b>
                <div className="slidercontainer">
                    <label>0.01</label>
                    <input type="range" min="1" max="50" value={this.state.precision * 100} className="slider" id="myRange" onChange={this.handleSliderChange}></input>
                    <label>0.5</label>
                </div>
                <button className='btn generate' onClick={this.handleGenerateButton}>Generate</button>
            </div>
            <div className='gen_vid_panel'>
                <b>LAST GENERATED VIDEO</b>
                <div className='gen_vid_card' onClick={this.state.generating ? () => {} : () => this.showGeneratedVideo()}>
                    {
                        this.state.generating ?
                        <div class="lds-ring"><div></div><div></div><div></div><div></div></div> :
                        <img src='play.png' className='icon play'></img>
                    }
                    <video className='gen_vid' src={API_URL + 'tracked_videos/' + this.state.last_generated} type='video/mp4'></video>
                </div>
            </div>
            <div className='see_more_panel' onClick={() => {this.setState({isListVisible: true})}}>
                <b>SEE FULL LIST</b>
                <img className='icon' src='list.png'></img>
            </div>
        </div>
        const gen_vid_controls =
        <div className='gen_vid_controls'>
            <div className='button_card' onClick={() => this.goBack()}>
                <b>GO BACK</b>
                <img src='arrow_back.png' className='icon back'></img>
            </div>
            <div className='button_card' onClick={() => this.downloadVideo()}>
                <b className='button_label'>DOWNLOAD VIDEO</b>
                <img src='download_film.png' className='icon down_vid' ></img>
            </div>
            <div className='button_card' onClick={() => this.downloadAddnotations()}>
                <b className='button_label'>DOWNLOAD ANNOTATIONS</b>
                <img src='download_file.png' className='icon down_addn'></img>
            </div>
        </div>
        const video_url = API_URL + this.state.vid_group + this.state.vid_name
        const list_elements = this.state.gen_videos.map((name, index) => (
        <div className='le' key={'elem' + index}>
            {this.createListElement(name)}
        </div>
        ))
        const listPanel =
        <div className='list_div' onClick={() => {this.setState({isListVisible: false})}}>
            <div className='list'>
                {list_elements}
            </div>
        </div>
        return (
            <div id="main_screen">
                {this.state.isListVisible ? listPanel : ()=>{}}
                <div id="video_container">
                    <video id='video' controls
                        src={this.state.is_gen_vid_displayed ? API_URL + 'tracked_videos/' + this.state.last_generated : video_url} type='video/mp4'>
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