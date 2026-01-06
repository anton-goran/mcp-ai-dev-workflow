import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

current_path = __file__.rsplit("/", 1)[0]

server_params = StdioServerParameters(
    command="python",
    args=["-u", f"{current_path}/stdio_server.py"],
)


async def run():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            result = await session.call_tool(
                name="download_webpage",
                arguments={"url": "https://datatalks.club/"},
            )
            content = result.content[0].text  # Assuming the content is in text format
            word = "data"
            count = content.lower().count(word.lower())
            print(f"The word '{word}' appears {count} times on https://datatalks.club/")


if __name__ == "__main__":
    import asyncio

    asyncio.run(run())