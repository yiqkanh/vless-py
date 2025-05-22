import asyncio
# import importlib
import struct
# import sys
import os
import socket
import uuid
# import subprocess

import aiohttp
from aiohttp import web

# def ensure_module(name, silent=False):
#     try:
#         importlib.import_module(name)
#     except ImportError:
#         if not silent:
#             print(f"Module '{name}' not found. Installing...")
#         subprocess.check_call(
#             [sys.executable, "-m", "pip", "install", name],
#             stdout=subprocess.DEVNULL if silent else None
#         )

NEZHA_SERVER = os.getenv('NEZHA_SERVER', '')
NEZHA_PORT = os.getenv('NEZHA_PORT', '')
NEZHA_KEY = os.getenv('NEZHA_KEY', '')
NAME = os.getenv('NAME', socket.gethostname())

print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
print("0.5.20 测试beta3版")
print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

UUID = os.getenv('UUID', '')
print("你的UUID：", UUID)

WEB_PATH = os.getenv('WEB_PATH', '/')
print("你的WEBPATH：", WEB_PATH)

PORT = int(os.getenv('PORT', 8080))
print("你的端口：", PORT)

DOMAIN = os.getenv('DOMAIN', '')
print("你的域名：", DOMAIN)

async def handle_root(request: web.Request) -> web.Response:
    return web.Response(text="Hello, World!", headers={"Content-Type": "text/plain"})

async def handle_config(request: web.Request) -> web.Response:
    if "server" in NAME.lower() or "hostypanel" in NAME.lower():
        ipv4_addresses = [
            "104.16.0.0", "104.17.0.0", "104.18.0.0", "104.19.0.0",
            "104.20.0.0", "104.21.0.0", "104.22.0.0", "104.24.0.0",
            "104.25.0.0", "104.26.0.0", "104.27.0.0"
        ]
        ipv6_addresses = [
            "[2606:4700::]", "[2400:cb00:2049::]"
        ]
        
        urls = []

        for ip in ipv4_addresses:
            urls.append(
                f"vless://{UUID}@{ip}:443?encryption=none&security=tls&sni={DOMAIN}&fp=chrome&"
                f"type=ws&host={DOMAIN}&path=%2F#Vl-ws-tls-{NAME}"
            )
        
        for ip in ipv6_addresses:
            urls.append(
                f"vless://{UUID}@{ip}:443?encryption=none&security=tls&sni={DOMAIN}&fp=chrome&"
                f"type=ws&host={DOMAIN}&path=%2F#Vl-ws-tls-{NAME}"
            )
        
        vlessURL = "\n".join(urls)
    else:
        vlessURL = f"vless://{UUID}@{DOMAIN}:443?encryption=none&security=tls&sni={DOMAIN}&fp=chrome&type=ws&host={DOMAIN}&path=%2F#Vl-ws-tls-{NAME}"
    
    return web.Response(text=vlessURL, headers={"Content-Type": "text/plain"})

async def start_server():
    httpServer = web.Application()
    @web.middleware
    async def websocket_check(request, handler):

        if request.headers.get('Upgrade', '').lower() == 'websocket' and request.headers.get('Connection', '').lower() == 'upgrade' :
        #if request.headers.get('Upgrade', '').lower() == 'websocket':
            return await handle_websocket(request)
        return await handler(request)

    # 先添加中间件
    httpServer.middlewares.append(websocket_check)
        


    async def handle_websocket(request: web.Request):
        ws = web.WebSocketResponse()
        await ws.prepare(request)

        if(request.path == WEB_PATH):
            msg = await ws.receive()
            
            if msg.type == aiohttp.WSMsgType.binary:
                data = msg.data
                # 尝试处理 vless 协议
                VERSION = data[0]
                id_bytes = data[1:17]
                if id_bytes != uuid.UUID(UUID).bytes:
                    return None
                
                i = data[17] + 19
                port = struct.unpack('>H', data[i:i+2])[0]
                i += 2
                ATYP = data[i]
                i += 1
                
                if ATYP == 1:  # IPv4
                    host = '.'.join(str(b) for b in data[i:i+4])
                    i += 4
                elif ATYP == 2:  # Domain
                    domain_len = data[i]
                    host = data[i+1:i+1+domain_len].decode('ascii')
                    i += 1 + domain_len
                elif ATYP == 3:  # IPv6
                    host = ':'.join(f'{x:02x}' for x in data[i:i+16])
                    i += 16
                else:
                    host = ''
                
                await ws.send_bytes(bytes([VERSION,0]))
                # 完成首次协议，开始创建双向通道
                reader, writer = await asyncio.open_connection(host, port)
                writer.write(data[i:])
                await writer.drain()  # 确保数据已发送

                # 2. 创建双向管道
                async def ws_to_tcp():
                    try:
                        async for msg in ws:
                            if msg.type == aiohttp.WSMsgType.BINARY:
                                writer.write(msg.data)
                                await writer.drain()
                            elif msg.type == aiohttp.WSMsgType.ERROR:
                                break
                    finally:
                        writer.close()
                        await writer.wait_closed()

                async def tcp_to_ws():
                    try:
                        while True:
                            data = await reader.read(4096)
                            if not data:
                                await ws.close()
                                break
                            await ws.send_bytes(data)
                    except Exception:
                        await ws.close()

                # 3. 并行运行两个方向的管道
                await asyncio.gather(
                    ws_to_tcp(),
                    tcp_to_ws(),
                    return_exceptions=True
                )


         
    
    httpServer.add_routes([
        web.get('/', handle_root),
        web.get(f'/{UUID}', handle_config)
        ])
    # web.run_app(httpServer, port=PORT)

    runner = web.AppRunner(httpServer)
    await runner.setup()
    
    site = web.TCPSite(runner, '0.0.0.0', PORT)
    await site.start()
        
    print(f"服务器已启动，监听端口 {PORT}")
    while True:
        await asyncio.sleep(3600)

if __name__ == '__main__':
    asyncio.run(start_server())