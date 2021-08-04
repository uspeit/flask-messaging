from resources.auth import RegisterApi
from resources.messages import MessagesApi


def initialize_routes(api):
    api.add_resource(RegisterApi, '/register')
    api.add_resource(MessagesApi, '/messages')
