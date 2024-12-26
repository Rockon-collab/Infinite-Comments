from flask import request, jsonify, session, g
from flask.views import MethodView
from . import db, bcrypt, app
from .models import User, Comment, Reply
from datetime import  timedelta
from .authentication import login_required, create_jwt_token, get_user_from_token
from .forms import RegistrationForm


class RegistrationAPI(MethodView):
    def post(self):
        form = RegistrationForm(data=request.json)

        if not form.validate():
            return jsonify({"errors": form.errors}), 400

        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        new_user = User(
            username=form.username.data,
            email=form.email.data,
            password_hash=hashed_password
        )
        db.session.add(new_user)
        db.session.commit()

        return jsonify({"message": "Registration successful!"}), 201

@app.before_request
def load_user():
    user_id = session.get('user_id')
    username = session.get('username')
        
    if user_id and username:
        g.user = {"user_id": user_id, "username": username}
    else:
        g.user = None
        
            
class LoginAPI(MethodView):
    def post(self):
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        remember_me = data.get('remember_me', False)

        user = self.login_user(email, password)

        if user:
            session['user_id'] = user.id
            session['username'] = user.username
            g.user = user.username
            g.id = user.id
            g.user = {'user_id': user.id, 'username': user.username}

            if remember_me:
                session.permanent = True  
                app.permanent_session_lifetime = timedelta(days=30)  
            else:
                session.permanent = False  
            token = create_jwt_token(user.id, user.username, remember_me)
            username = user.username
            return jsonify({"message": "Login successful!","token": token, "username":username}), 200

        return jsonify({"error": "Invalid credentials."}), 401

    @staticmethod
    def login_user( email, password):
        user = User.query.filter_by(email = email).first()

        if user and bcrypt.check_password_hash(user.password_hash, password):
            return user
        return None


class LogoutAPI(MethodView):
    def post(self):
        session.clear()
        g.user = None
        return jsonify({"message": "Logged out successfully."}), 200


class CommentAPI(MethodView):

    
    def comment_tree(self, comments, replies):

        comment_map = {c.id: {
            "id": c.id,
            "user_id": c.user_id,
            "content": c.content,
            "created_at": c.created_at,
            "timestamp": c.timestamp,
            "username": c.user.username,
            "replies": []
        } for c in comments}

        # Create a dictionary to map reply IDs to their data
        reply_map = {r.id: {
            "id": r.id,
            "user_id": r.user_id,
            "reply_content": r.reply_content,
            "created_at": r.created_at,
            "comment_id": r.comment_id,
            "username": r.user.username,
        } for r in replies}

        root_comments = []

        for comment in comments:
            for reply in replies:
                if reply.comment_id == comment.id:
                    comment_map[comment.id]["replies"].append(reply_map[reply.id])

            if not comment.parent_id:
                root_comments.append(comment_map[comment.id])

        return root_comments

    def get(self):
        comments = Comment.query.order_by(Comment.timestamp.desc()).all()
        replies = Reply.query.all()

        comment_data = self.comment_tree(comments, replies)
        print("Session data:", session)
        user_data = {
        "user_id": g.user['user_id'] if g.user else None,
        "username": g.user['username'] if g.user else None,
    }
        return jsonify({"comments": comment_data, "current_user": user_data}), 200



    @login_required
    def post(self):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({"error": "Authorization token missing."}), 401
        token = auth_header.split(" ")[1]        
        user_id = get_user_from_token(token)
        if not user_id:
            return jsonify({"error": "Invalid or expired token."}), 401
        data = request.get_json()
        content = data.get('content', '').strip()

        if not (3 <= len(content) <= 200):
            return jsonify({"error": "Comment must be between 3 and 200 characters."}), 400

        new_comment = self.create_comment(user_id, data)
        return jsonify({"message": "Comment added successfully!"}), 201

    @staticmethod
    def create_comment(user_id, data):
        content = data.get('content', '').strip()
        
        new_comment = Comment(user_id=user_id, content=content)
        db.session.add(new_comment)
        db.session.commit()
        return new_comment




class ReplyAPI(MethodView): 
    @login_required
    def post(self):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({"error": "Authorization token missing."}), 401
        token = auth_header.split(" ")[1]        
        user_id = get_user_from_token(token)
        if not user_id:
            return jsonify({"error": "Invalid or expired token."}), 401
        
        data = request.get_json()
        parent_id = data.get('parent_id')  # Parent can be a comment or another reply
        reply_content = data.get('content', '').strip()

        if not (3 <= len(reply_content) <= 200):
            return jsonify({"error": "Reply must be between 3 and 200 characters."}), 400

        parent_comment = None
        parent_reply = None

        if parent_id:
            parent_comment = Comment.query.get(parent_id)  
            parent_reply = Reply.query.get(parent_id)  
            

        if not parent_comment and not parent_reply:
            return jsonify({"error": "Parent comment or reply not found."}), 404

        if parent_comment: 
            new_reply = Reply(
                user_id=user_id,
                comment_id=parent_comment.id,
                reply_content=reply_content
            )
        elif parent_reply:  
            new_reply = Reply(
                user_id=user_id,
                comment_id=parent_reply.comment_id,  
                parent_id=parent_reply.id, 
                reply_content=reply_content
            )

        db.session.add(new_reply)
        db.session.commit()

        return jsonify({
            "message": "Reply added successfully!",
            "reply": new_reply.to_dict()  
        }), 201

