from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("robot")


@mcp.tool()
async def start_robot() -> None:
    """Starts the robot.

    Args:
        None

    Returns:
        None
    """
