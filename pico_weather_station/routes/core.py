from lightberry import Router, Response, typing
from lightberry.shortcuts import jsonify

if typing.TYPE_CHECKING:
    from lightberry import Request


core = Router("core")


@core.route("/sensors")
async def sensors(request: Request):
    data = {"hello": "world"}

    return Response(payload=jsonify(data))
