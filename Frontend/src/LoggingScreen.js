import './LoggingScreen.css'
import React from 'react';
import './App'

var API_URL = 'http://192.168.1.27:5000/'
// var API_URL = 'http://localhost:9001/'


class LoggingScreen extends React.Component {
    constructor(props) {
        super(props);
        this.props = props;
        this.state = {
            username: '',
            password: '',
        };
    }

    switchScene = () => {
        this.props.switchScene(false);
    }

    logIn() {
        const form = this.state
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
        })
    }

    register() {
        const form = this.state
        fetch(API_URL + 'register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(form)
        })
        .then(response => {
            if (response.ok) {
                this.logIn()
            }
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
            <div id="logging_screen">
                <header id='log_head'>LOG IN</header>
                <label id="username_label" >username:</label>
                <input type='text' id='username_input' onChange={this.handleLoginChange}></input>
                <label id="pass_label" >password:</label>
                <input type='password' id='pass_input' onChange={this.handlePasswordChange}></input>
                <div id="log_buttons">
                    <button id='username_button' onClick={() => this.logIn()}>Log in</button>
                    <button id='register_button' onClick={() => this.register()}>Register</button>
                </div>
            </div>
        )
    }
}

export default LoggingScreen