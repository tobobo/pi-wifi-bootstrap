from aiohttp import web

print("stdout?")

async def hello(request):
    return web.Response(text="Hello, world")
    
app = web.Application()
app.add_routes([web.get('/', hello)])

web.run_app(app)
