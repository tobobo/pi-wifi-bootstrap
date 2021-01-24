import asyncio
from aiohttp import web


async def index(request):
    return web.FileResponse(path='public/index.html')


async def set_credentials(request):
    data = await request.post()
    asyncio.create_task(request.app['set_credentials_and_reboot'](data['ssid'], data['psk']))
    return web.Response(text="setting credentials and restarting...")


async def start_wifi_setup_server(set_credentials_and_reboot):
    app = web.Application()
    app['set_credentials_and_reboot'] = set_credentials_and_reboot
    app.add_routes(
        [web.get('/', index), web.post('/set_credentials', set_credentials), web.static('/', 'public')])
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 8080)
    await site.start()
    print("web server started on port {0}".format(8080))
    while 1:
        await asyncio.sleep(1)


if __name__ == "__main__":
    async def set_credentials_and_reboot(ssid, psk):
        print("doing some credential setting")
        await asyncio.sleep(5)
        print(ssid)
        print(psk)
        await asyncio.sleep(5)
        print("restarting")

    asyncio.run(start_wifi_setup_server(set_credentials_and_reboot))
