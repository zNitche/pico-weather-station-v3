from lightberry import Router, Response, typing

if typing.TYPE_CHECKING:
    from lightberry import Request


core = Router("core")


@core.route("/")
async def home(request: Request):
    return Response(payload="hello world")
