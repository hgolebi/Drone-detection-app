import './LoggingScreen.css'
import React from 'react';
import './App'

var API_URL = 'http://192.168.1.27:5000/'
// var API_URL = 'http://172.20.0.2:5000/'


class LoggingScreen extends React.Component {
    constructor(props) {
        super(props);
        this.props = props;
        this.state = {
            username: '',
            password: '',
            message: '',
        };
    }

    switchScene = () => {
        this.props.switchScene(false);
    }

    logIn() {
        this.setState({message: ''});
        const username = this.state.username
        const password = this.state.password
        if (!username) {
            this.setState({message: 'Missing username'})
            return
        }
        if (!password) {
            this.setState({message: 'Missing password'})
            return
        }
        const form = {
            username: this.state.username,
            password: this.state.password,
        }
        fetch(API_URL + 'login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            credentials: 'include',
            body: JSON.stringify(form)
        })
        .then(response => {
            if (response.ok) {
                this.switchScene()
            }
            else if (response.status === 404) {
                response.json().then(json => {
                    this.setState({
                        message: json.message
                    })
                })
            }
        })
        .catch(error => {
            this.setState({message: 'Something went wrong.'})
        })
    }

    register() {
        this.setState({message: ''});
        const username = this.state.username
        const password = this.state.password
        if (!username) {
            this.setState({message: 'Missing username'})
            return
        }
        if (!password) {
            this.setState({message: 'Missing password'})
            return
        }
        const form = {
            username: username,
            password: password,
        }
        fetch(API_URL + 'register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            credentials: 'include',
            body: JSON.stringify(form)
        })
        .then(response => {
            if (response.ok) {
                this.logIn();
                alert('Succesfully registered!');
            }
            else if (response.status === 400) {
                response.json().then(json => {
                    this.setState({
                        message: json.message
                    })
                })
            }
        })
        .catch(error => {
            this.setState({message: 'Something went wrong.'})
        })
    }

    handleLoginChange = event => {
        this.setState({username: event.target.value})
    }
    handlePasswordChange = event => {
        this.setState({password: event.target.value})
    }

    render () {
        return (
            <div className="logging_screen">
                <div className='logging_panel'>
                    <header className='log_head'>LOG IN</header>
                    <label className="label" >username:</label>
                    <input type='text' className='input' onChange={this.handleLoginChange}></input>
                    <label className="label" >password:</label>
                    <input type='password' className='input' onChange={this.handlePasswordChange}></input>
                    <div className="log_buttons">
                        <button className='button' onClick={() => this.logIn()}>Log in</button>
                        <button className='button' onClick={() => this.register()}>Register</button>
                    </div>
                </div>
                <div className='info'>
                    <p>{this.state.message}</p>
                </div>
            </div>
        )
    }
}

export default LoggingScreen