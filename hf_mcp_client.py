import asyncio
import os

from dotenv import load_dotenv
from huggingface_hub import MCPClient

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")

if not HF_TOKEN:
    raise RuntimeError("HF_TOKEN is not set in .env")


async def main():
    client = MCPClient(
        model="Qwen/Qwen2.5-72B-Instruct",
        provider="hf-inference",
        api_key=HF_TOKEN,
    )

    await client.add_mcp_server(
        type="stdio",
        command=r"C:\Users\pavan\.local\bin\uv.exe",
        args=[
            "run",
            "--directory",
            r"C:\Users\pavan\Projects\story-mcp",
            "python",
            "main.py",
        ],
        allowed_tools=["save_story"],
    )

    messages = [
        {
            "role": "user",
            "content": (
                "Write a short creative story about a programmer "
                "who discovers a mysterious AI. "
                "Then save the complete story using the save_story "
                "MCP tool as ai_story.md."
            ),
        }
    ]

    async for chunk in client.process_single_turn_with_tools(messages):
        if hasattr(chunk, "choices"):
            delta = chunk.choices[0].delta

            if delta.content:
                print(delta.content, end="", flush=True)

        elif hasattr(chunk, "name"):
            print(f"\nTool called: {chunk.name}")
            print(f"Result: {chunk.content}")

    await client.cleanup()


if __name__ == "__main__":
    asyncio.run(main())