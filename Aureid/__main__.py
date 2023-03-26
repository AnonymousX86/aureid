# -*- coding: utf-8
from datetime import datetime, timezone
from json import loads as json_loads
from logging import basicConfig, INFO, getLogger

from nextguild import Client, Events, Message, Embed
from requests import get as requests_get
from rich.logging import RichHandler

from Aureid.api_calls.members import get_member
from Aureid.api_calls.messages import get_message
from Aureid.config import BOT_TOKEN, PREFIX
from Aureid.logging import rich_log


def main():
    client = Client(BOT_TOKEN)
    events = Events(client)

    api_unavailable_embed = Embed(
        title='Oops!',
        description='API unavailable'
    )

    @events.on_ready
    async def on_ready():
        rich_log.info('Ready!')

    @events.on_message
    async def bot_command(message: Message):
        # Check if it's a command
        if not (cmd := message.content).startswith(PREFIX):
            return
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

        # "chuck" command
        if cmd.startswith('chuck'):
            req = requests_get('https://api.chucknorris.io/jokes/random')
            if not req.ok:
                client.send_message(
                    message.channelId,
                    embed=api_unavailable_embed
                )
                return
            res = json_loads(req.content)
            client.send_message(message.channelId, embed=Embed(
                description=res.get('value'),
                thumbnail=res.get('icon_url').replace(
                    'assets.chucknorris.host',
                    'api.chucknorris.io'
                )
            ))

        # "dadjoke" command
        if cmd.startswith('dadjoke'):
            req = requests_get(
                'https://reddit.com/r/dadjokes/random.json?limit=1&t=month',
                headers={
                    'User-Agent': 'Aureid'
                }
            )
            if not req.ok:
                client.send_message(
                    message.channelId,
                    embed=api_unavailable_embed
                )
                return
            res = json_loads(req.content)
            data = res[0]['data']['children'][0]['data']
            client.send_message(
                message.channelId,
                embed=Embed(
                    description='**{}**\n\n{}\n\n*{}*'.format(
                        data.get('title', '').replace('\n', ''),
                        data.get('selftext', '').replace('\n', ''),
                        '[Upvote]({})'.format(data.get('url'))
                    ),
                    thumbnail='https://www.redditstatic.com/desktop2x/img/'
                              'favicon/favicon-96x96.png'
                )
            )

        else:
            rich_log.info('But that command does not exists')

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
