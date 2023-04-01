import './LoggingScreen.css'

function LoggingScreen(props) {
    return (
        <div id="log_main">
            <header id='log_head'>LOG IN</header>
            <label id="login_label">login:</label>
            <input type='text' id='login_input'></input>
            <label id="pass_label">password:</label>
            <input type='password' id='pass_input'></input>
            <div id="log_buttons">
                <button id='login_button' onClick={}>Log in</button>
                <button id='signin_button'>Sign in</button>
            </div>
        </div>
    )
}

export default LoggingScreen