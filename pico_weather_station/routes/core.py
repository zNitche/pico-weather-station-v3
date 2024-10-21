from lightberry import Router, Response


core = Router("core")


@core.catch_all()
async def home(request):
    return Response(payload="Hello World")
