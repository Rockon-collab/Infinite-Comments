
from flask import Blueprint
from .views import RegistrationAPI, LoginAPI, LogoutAPI, CommentAPI, ReplyAPI
routes = Blueprint('routes', __name__)

# Register the views
routes.add_url_rule('/api/register', view_func=RegistrationAPI.as_view('register_api'))
routes.add_url_rule('/api/login', view_func=LoginAPI.as_view('login_api'))
routes.add_url_rule('/api/logout', view_func=LogoutAPI.as_view('logout_api'))
routes.add_url_rule('/api/comments', view_func=CommentAPI.as_view('comment_api'))
routes.add_url_rule('/api/reply', view_func=ReplyAPI.as_view('reply_api'))



