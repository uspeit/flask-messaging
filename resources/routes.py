from resources.auth import RegisterApi
from resources.messages import MessageApi
from resources.messages import MessagesApi


def initialize_routes(api):
    api.add_resource(RegisterApi, '/register')

    api.add_resource(MessageApi, '/message',
                                 '/message/<message_id>')

    api.add_resource(MessagesApi, '/messages',
                                  '/messages/<all_or_unread>',
                                  '/messages/<all_or_unread>/<sent_or_received>')
