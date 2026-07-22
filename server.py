from fastmcp import FastMCP
from fastmcp_credentials import CredentialMiddleware, HeaderCredentialBackend

from cal_mcp.cli import parse_args
from cal_mcp.tools import register_tools

backend = HeaderCredentialBackend()

mcp = FastMCP(
    "MewCP Cal MCP Server", middleware=[CredentialMiddleware(backend, "static")]
)

register_tools(mcp)

app = mcp.http_app(path="/mcp", transport="streamable-http", stateless_http=True)

if __name__ == "__main__":
    args = parse_args()

    run_kwargs = {}

    if args.transport:
        run_kwargs["transport"] = args.transport

    if args.host:
        run_kwargs["host"] = args.host

    if args.port:
        run_kwargs["port"] = args.port

    try:
        mcp.run(**run_kwargs)

    except Exception as e:
        print(f"Failed to start server: {e}")
        raise
