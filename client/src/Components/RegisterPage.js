import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './RegisterPage.css'


const BASE_URL = 'http://127.0.0.1:5000/api';
function RegisterPage() {
    const [username, setUsername] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const navigate = useNavigate();

    const handleRegister = async (e) => {
        e.preventDefault();
        setError('');

        try {
            const response = await fetch(`${BASE_URL}/register`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, email, password }),
            });

            const data = await response.json();
            if (response.ok) {
                setUsername('');
                setEmail('');
                setPassword('');
                navigate('/login');
            } else {
                setError(data.errors || 'Registration failed.');
            }
        } catch (error) {
            setError('An error occurred. Please try again.');
        }
    };
    const navigateToRegister = () => {
        navigate('/login');
    };

    return (
        <div className="register-container">
            <header className="register-header">
                <h2>Register</h2>
                
            </header>
            <br></br>
            <form onSubmit={handleRegister} className="register-form">
                <input
                    type="text"
                    placeholder="Username"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    required
                    className="input-field"
                />
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
                <button type="submit" className="register-btn">Register</button>

                {error && <p className="error-message">{error}</p>}
            </form>
            <button onClick={navigateToRegister} className="register-btn">Login</button>
        </div>
    );
}

export default RegisterPage;