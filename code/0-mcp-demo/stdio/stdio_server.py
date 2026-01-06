
import os
import asyncio
from mcp.server.fastmcp import FastMCP, Context
import httpx


mcp = FastMCP(name="0-mcp-intro-weather")


@mcp.tool()
async def get_weather(city: str, ctx: Context):
    return 22

@mcp.resource(
    f"file:///{__file__.rsplit('/', 1)[0]}/test_json.md"
)
def get_file() -> dict:
    return "Content of the file"


@mcp.tool()
async def summarize(text_to_summarize: str, ctx: Context):
    # Mock summary for demo purposes (avoids requiring API key)
    summary = f"Summary: {text_to_summarize[:100]}{'...' if len(text_to_summarize) > 100 else ''}"
    return summary
    
    
@mcp.tool()
async def add(a: int, b: int, ctx: Context) -> int:
    await ctx.info("Preparing to add...")
    await ctx.report_progress(20, 100)

    await asyncio.sleep(10)

    await ctx.info("OK, adding...")
    await ctx.report_progress(80, 100)

    return a + b

@mcp.tool()
async def list_folders_under_roots(ctx: Context):
    """
    Lists all folders under the client roots (as specified by the MCP client).
    """
    roots = await ctx.session.list_roots()
    if not roots:
        return {"error": "No client roots available in context."}
    
    return {"roots": roots}


@mcp.tool()
async def download_webpage(url: str, ctx: Context) -> str:
    """
    Downloads the content of a web page as markdown using Jina reader.
    
    Args:
        url: The URL of the web page to download
        
    Returns:
        The markdown content of the web page
    """
    jina_url = f"https://r.jina.ai/{url}"
    
    async with httpx.AsyncClient() as client:
        response = await client.get(jina_url)
        response.raise_for_status()
        return response.text

if __name__ == "__main__":
    mcp.run(transport="stdio")
