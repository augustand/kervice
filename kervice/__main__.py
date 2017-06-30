import asyncio
import sys
from os.path import abspath as ap, dirname as dn

sys.path.append(dn(dn(ap(__file__))))

from kervice.utils import pp
from kervice.utils.colors import yellow

import click

click.disable_unicode_literals_warning = True


@click.command()
@click.option('--env', '-e', default='local', help=u'开发环境设置', show_default=True)
@click.option('--port', '-p', default=80, help=u'端口', show_default=True)
@click.option('--name', '-n', default="test", help=u'服务名称', show_default=True)
def main(env, port, name):
    """启动服务"""

    from kervice.utils.app import Application
    app = Application.instance()
    app.env = env

    from kervice.utils.net_tool import get_open_port
    from kervice.utils import when

    app.port = when(port == 80, get_open_port(), port)
    if name == "test":
        pp(yellow,print)("service name: test is default")
    app.name = name
    app.debug = when(env == 'pro', False, True)

    from kervice.app.main import init_app
    asyncio.ensure_future(init_app())
    asyncio.ensure_future(app.create_server(host="0.0.0.0", port=app.port, debug=app.debug))
    asyncio.get_event_loop().run_forever()


if __name__ == "__main__":
    main()