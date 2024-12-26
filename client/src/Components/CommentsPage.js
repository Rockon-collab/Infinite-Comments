
import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import './CommentsPage.css'

// Retrieve the token (assumes it's stored in localStorage)
const token = localStorage.getItem('token');
const username = localStorage.getItem('username');
const BASE_URL = 'http://127.0.0.1:5000/api';
const isLoggedIn = !!token;


function CommentsPage() {
    const [comments, setComments] = useState([]);
    const [newComment, setNewComment] = useState('');
    const [replyContent, setReplyContent] = useState('');
    const [error, setError] = useState('');
    const [successMessage, setSuccessMessage] = useState('');
    const [replyingTo, setReplyingTo] = useState(null);
    const navigate = useNavigate();

    
    useEffect(() => {
        fetchComments();
    }, []);


    // Fetch all comments from the backend
    const fetchComments = async () => {
        try {
            const response = await fetch(`${BASE_URL}/comments`, {
                headers: {
                    'Authorization': `Bearer ${token}`,
                },
            });
            const data = await response.json();
            if (response.ok) {
                setComments(data.comments || []);
            } else {
                setError('Failed to fetch comments.');
            }
        } catch (error) {
            setError('An error occurred while fetching comments.');
        }
    };

    // Post a new comment
    const handleNewComment = async (e) => {
        e.preventDefault();
        setError('');
        setSuccessMessage('');

        try {
            const response = await fetch(`${BASE_URL}/comments`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`,
                },
                body: JSON.stringify({ content: newComment }),
            });

            if (response.ok) {
                setNewComment('');
                setSuccessMessage('Comment added successfully!');
                fetchComments();
            } else {
                const data = await response.json();
                setError(data.error || 'Failed to post comment.');
            }
        } catch (error) {
            setError('An error occurred while posting the comment.');
        }
    };

    // Post a reply to a comment
    const handleReply = async (e) => {
        e.preventDefault();
        setError('');
        setSuccessMessage('');
        try {
            const response = await fetch(`${BASE_URL}/reply`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`,
                },
                body: JSON.stringify({
                    parent_id: replyingTo,
                    content: replyContent,
                }),
            });

            if (response.ok) {
                setReplyContent('');
                setReplyingTo(null);
                setSuccessMessage('Reply added successfully!');
                fetchComments();
            } else {
                const data = await response.json();
                setError(data.error || 'Failed to post reply.');
            }
        } catch (error) {
            setError('An error occurred while posting the reply.');
        }
    };

    const handleLogout = async () => {
        try {
            const response = await fetch(`${BASE_URL}/logout`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`,
                },
            });
            if (response.ok) {

                // Clear token and redirect to login page after successful logout
                localStorage.clear();
                navigate('/login');
            } else {
                setError('Failed to logout.');
            }
        } catch (error) {
            setError('An error occurred while logging out.');
        }
    };
    
return (
    <div className="comments-container">
        <header className="header">
            <h3>Welcome {username}</h3>
            <button className="logout-btn" onClick={handleLogout}>Logout</button>
        </header>

        <h2>Comments</h2>

        {error && <p className="error-message">{error}</p>}
        {successMessage && <p className="success-message">{successMessage}</p>}

        <form onSubmit={handleNewComment} className="comment-form">
            <input
                type="text"
                placeholder="Write a comment"
                value={newComment}
                onChange={(e) => setNewComment(e.target.value)}
                required
                className="input-field"
            style={{ width: '45%', padding: '5px', fontSize: '14px' }}
            />
            <button className="submit-btn" type="submit">
                Add Comment
            </button>
        </form>

        <ul className="comments-list">
            {Array.isArray(comments) && comments.length > 0 ? (
                comments.map((comment) => (
                    <li key={comment.id} className="comment-item">
                        <div className="comment-header">
                            <strong>User : {comment.username}</strong>
                            <p className='created-at-time'>{comment.created_at}</p>
                            <p>{comment.content}</p>
                        </div>

                        <button 
                            className="reply-btn"
                            onClick={() => {
                                if (!isLoggedIn) {
                                    navigate('/login');
                                    return;
                                }
                                setReplyingTo(comment.id);
                            }}
                        >
                            Reply
                        </button>

                        {/* Reply form for each comment */}
                        {replyingTo === comment.id && (
                            <form onSubmit={handleReply} className="reply-form">
                                <h4>Replying to {comment.username}</h4>
                                <input
                                    type="text"
                                    placeholder="Write a reply"
                                    value={replyContent}
                                    onChange={(e) => setReplyContent(e.target.value)}
                                    required
                                    className="input-field"
                                />
                                <div className="reply-buttons">
                                    <button className="submit-btn" type="submit">Submit Reply</button>
                                    <button className="cancel-btn" onClick={() => setReplyingTo(null)}>Cancel</button>
                                </div>
                            </form>
                        )}

                        <ul className="replies-list">
                            {comment.replies?.map((reply) => (
                                <li key={reply.id} className="reply-item">
                                    <strong>User : {reply.username}</strong><p className='created-at-time'>{reply.created_at}</p>
                                    <p> {reply.reply_content}</p>
                                    
                                </li>
                            ))}
                        </ul>
                    </li>
                ))
            ) : (
                <p>No comments available</p>
            )}
        </ul>
    </div>
);
}

export default CommentsPage;