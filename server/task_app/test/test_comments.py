import unittest
import json
from task_app.models import User, Comment, Reply
from flask import current_app
import os, sys

# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
from task_app import create_app, db

class FlaskTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

    # def tearDown(self):
    #     with self.app.app_context():
    #         db.session.remove()
    #         db.drop_all()   

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()  


    # def test_registration(self):
    #     data = {
    #         "username": "testuser1",
    #         "email": "testuser1@example.com",
    #         "password": "Password@123"
    #     }

    #     response = self.client.post('/api/register', json=data)
    #     json_data = json.loads(response.data)
    #     print('json_data : ',json_data)
    #     self.assertEqual(json_data['message'], "Registration successful!")

    # def test_registration_invalid_data(self):
    #     data = {
    #         "username": "testuser",
    #         "email": "invalidemail",
    #         "password": "12"
    #     }

    #     response = self.client.post('/api/register', json=data)
    #     json_data = json.loads(response.data)
    #     print("json_data :",json_data)
    #     print("response.status_code :",response.status_code)
    #     self.assertEqual(response.status_code, 400)

    def test_login(self):

        data = {
            "email": "testuser@example.com",
            "password": "Password@123" 
        }

        # Send a POST request to the login API
        response = self.client.post('/api/login', json=data)
        print("response : ",response)
        json_data = json.loads(response.data)

        # Debug print statements
        print("json_data :", json_data)
        print("json_data['username'] :", json_data['username'])
        print("response.status_code :", response.status_code)

        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', json_data)
        self.assertEqual(json_data['username'], "testuser")

    # def test_invalid_login(self):
    #     data = {
    #         "email": "nonexistent@example.com",
    #         "password_hash": "wrongpassword"
    #     }

    #     response = self.client.post('/api/login', json=data)
    #     json_data = json.loads(response.data)
    #     self.assertEqual(response.status_code, 401)
    #     self.assertEqual(json_data['error'], "Invalid credentials.")

    # def test_logout(self):
    #     response = self.client.post('/api/logout')
    #     json_data = json.loads(response.data)
    #     print('json_data ; ',json_data)
    #     print('json_response.status_codedata ; ',response.status_code)
    #     print('json_data[message] ; ',json_data['message'])
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(json_data['message'], "Logged out successfully.")

    # def test_create_comment(self):
    #     self.token = 'your_valid_jwt_token_here'
    #     headers = {'Authorization': f'Bearer {self.token}'}  # Adjust as per your auth scheme
    #     print("headers : ",headers)
    #     response = self.client.post('/api/comments', json={"content": "Test comment"}, headers=headers)
    #     print("response : ",response)
    #     self.assertEqual(response.status_code, 201)
    
    def test_create_comment(self):

        data = {
            "content": "This is a test comment."
        }
        # Assuming the user is logged in, we pass a valid JWT token
        token = "valid-jwt-token"  # Mock the token for testing
        response = self.client.post('/api/comments', json=data, headers={'Authorization': f'Bearer {token}'})
        json_data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(json_data['message'], "Comment added successfully!")

    # def test_create_reply(self):
    #     # Test reply creation
    #     user = User(username="testuser", email="testuser@example.com", password_hash="password123")
    #     db.session.add(user)
    #     db.session.commit()

    #     comment = Comment(user_id=user.id, content="This is a comment.")
    #     db.session.add(comment)
    #     db.session.commit()

    #     data = {
    #         "parent_id": comment.id,
    #         "content": "This is a test reply."
    #     }
    #     # Assuming the user is logged in, we pass a valid JWT token
    #     token = "valid-jwt-token"  # Mock the token for testing

    #     response = self.client.post('/api/reply', json=data, headers={'Authorization': f'Bearer {token}'})
    #     json_data = json.loads(response.data)
    #     self.assertEqual(response.status_code, 201)
    #     self.assertEqual(json_data['message'], "Reply added successfully!")

    # def test_get_comments(self):
    #     # Test retrieving comments and replies
    #     user = User(username="testuser", email="testuser@example.com", password_hash="password123")
    #     db.session.add(user)
    #     db.session.commit()

    #     comment = Comment(user_id=user.id, content="This is a comment.")
    #     db.session.add(comment)
    #     db.session.commit()

    #     data = {
    #         "content": "This is a test reply."
    #     }
    #     # Create a reply to the comment
    #     reply = Reply(user_id=user.id, comment_id=comment.id, reply_content="This is a reply.")
    #     db.session.add(reply)
    #     db.session.commit()

    #     response = self.client.get('/api/comments')
    #     json_data = json.loads(response.data)

    #     self.assertEqual(response.status_code, 200)
    #     self.assertIn("comments", json_data)
    #     self.assertIn("replies", json_data['comments'][0])

    # def test_invalid_reply(self):
    #     # Test invalid reply to non-existent comment
    #     data = {
    #         "parent_id": 9999,  # Non-existent comment
    #         "content": "This is a test reply."
    #     }
    #     token = "valid-jwt-token"  # Mock the token for testing

    #     response = self.client.post('/api/reply', json=data, headers={'Authorization': f'Bearer {token}'})
    #     json_data = json.loads(response.data)
    #     self.assertEqual(response.status_code, 404)
    #     self.assertEqual(json_data['error'], "Parent comment or reply not found.")
