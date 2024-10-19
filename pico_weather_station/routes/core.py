from lightberry import Router, Response


core = Router("core")


@core.route("/")
async def healthcheck(request):
    return Response(payload="Hello World")
