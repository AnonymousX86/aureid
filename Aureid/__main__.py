# -*- coding: utf-8
from datetime import datetime, timezone
from logging import basicConfig, INFO, getLogger

from nextguild import Client, Events, Message, Embed
from rich.logging import RichHandler

from Aureid.api_calls.members import get_member
from Aureid.api_calls.messages import get_message
from Aureid.config import BOT_TOKEN, PREFIX
from Aureid.logging import rich_log


def main():
    client = Client(BOT_TOKEN)
    events = Events(client)

    @events.on_ready
    async def on_ready():
        rich_log.info('Ready!')

    @events.on_message
    async def bot_command(message: Message):
        # Check if it's a command
        if (cmd := message.content).startswith(PREFIX):
            cmd = cmd[len(PREFIX)::]
            author = get_member(message.guildId, message.authorId)
            rich_log.info('"{}" issued "{}" command'.format(
                author['user']['name'], cmd)
            )

            # "ping" command
            if cmd.startswith('ping'):
                og_message = get_message(message.channelId, message.messageId)
                msg_timedelta = \
                    datetime.now(tz=timezone.utc) \
                    - datetime.fromisoformat(og_message['createdAt'])
                client.send_message(
                    message.channelId,
                    embed=Embed(
                        title=':table_tennis_paddle_and_ball: Pong!',
                        description=f'Response took '
                                    f'{msg_timedelta.microseconds // 1000}ms'
                    )
                )

    events.run()


if __name__ == '__main__':
    basicConfig(
        level=INFO,
        format='%(message)s',
        datefmt='[%x]',
        handlers=[RichHandler(rich_tracebacks=True)]
    )
    requests_log = getLogger('urllib3')
    requests_log.setLevel(INFO)
    requests_log.propagate = True
    websockets_log_client = getLogger('websockets.client')
    websockets_log_client.setLevel(INFO)
    websockets_log_client.propagate = True
    websockets_log_server = getLogger('websockets.server')
    websockets_log_server.setLevel(INFO)
    websockets_log_server.propagate = True
    try:
        main()
    except KeyboardInterrupt:
        rich_log.info('Goodbye!')
