
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './LoginPage.css'
const BASE_URL = 'http://127.0.0.1:5000/api';
function LoginPage() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [rememberMe, setRememberMe] = useState(false);  // Track the state of the checkbox
    const [error, setError] = useState('');
    const navigate = useNavigate();

    const handleLogin = async (e) => {
        e.preventDefault();
        setError('');

        try {
            const response = await fetch(`${BASE_URL}/login`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                credentials: 'include',
                body: JSON.stringify({ email: email, password, remember_me: rememberMe }),  // Send remember_me in the body
            });

            const data = await response.json();
            if (response.ok) {
                localStorage.setItem('token', data.token);
                localStorage.setItem('username', data.username);
                navigate('/');
                window.location.reload() 
            } else {
                setError(data.error);
            }
        } catch (error) {
            setError('An error occurred. Please try again.');
        }
    };

    const navigateToRegister = () => {
        navigate('/register');
    };
    const navigateToComment = () => {
        navigate('/');
    };
    return (
        <div className="login-container">
            
            <div className="login-card">
            <button onClick={navigateToComment} className="register-btn">All Comment's</button>
                <header className="login-header">
                    <h2>Login</h2>
                </header>
                <br />
                <form onSubmit={handleLogin} className="login-form">
                    <input
                        type="email"
                        placeholder="Email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        required
                        className="input-field"
                    />
                    <input
                        type="password"
                        placeholder="Password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        required
                        className="input-field"
                    />
                    <label className="remember-me">
                        <input
                            type="checkbox"
                            checked={rememberMe}
                            onChange={(e) => setRememberMe(e.target.checked)}
                            className="checkbox"
                        />
                        Remember me
                    </label>
                    <button type="submit" className="login-btn">Login</button>
                    {error && <p className="error-message">{error}</p>}
                </form>
                <button onClick={navigateToRegister} className="register-btn">Register</button>
            </div>
        </div>
    );
}

export default LoginPage;