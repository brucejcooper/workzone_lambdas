import logging
import sys
from threading import Timer
import asyncio
from aiohttp import web, WSMsgType
import json
from datetime import datetime
import os

# Setup logging to stdout
logger = logging.getLogger(__name__)

async def websocket_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    async for msg in ws:
        if msg.type == WSMsgType.TEXT:
            if msg.data == 'close':
                await ws.close()
            else:
                await ws.send_str(msg.data + '/answer')
        elif msg.type == WSMsgType.ERROR:
            print('ws connection closed with exception %s' %
                  ws.exception())

    print('websocket connection closed')

    return ws



async def index(request):
    d = """
        <html>
        <head>
            <script type="text/javascript"
                src="http://code.jquery.com/jquery.min.js"></script>
            <script type="text/javascript">
            var ws = new WebSocket(`ws://${window.location.host}/ws`);

            ws.addEventListener('open', function(evt) {
                ws.send("blah");
            });

            ws.addEventListener('message', function(evt) {
                console.log('Message from server', evt.data);
            })
            </script>
        </head>
        <body style="border: 0;">
            <h1>Response from server:</h1>
            <pre id="response"></pre>

            <iframe src="http://localhost:3000/d/3mEuOwggk/farm-production?orgId=1&refresh=250ms&kiosk" onload="this.width=this.window.innerWidth;this.height=this.window.innerHeight-300;" frameborder="0" >
            No Iframes
            </iframe>

        </body>
    </html>
    """
    with open(os.path.join(os.path.dirname(__file__), "html", "index.html")) as f:
        d = f.read()
    return web.Response(text=d, content_type='text/html')

app = web.Application()
app.router.add_route('GET', '/ws', websocket_handler)
# app.router.add_route('GET', '/hello', hello)
app.router.add_route('GET', '/index', index)
web.run_app(app, host='127.0.0.1', port=8080)

def function_handler(event, context):
    return
