from pathlib import Path
from mcp.server.mcpserver import MCPServer

mcp = MCPServer("Creative Story MCP")

OUTPUT_DIR = Path.home() / "mcp-stories"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


@mcp.tool()
def save_story(filename: str, story: str) -> str:
    """Save an AI-generated creative story as a Markdown file."""

    safe_filename = Path(filename).name

    if not safe_filename:
        raise ValueError("Invalid filename.")

    if not safe_filename.endswith(".md"):
        safe_filename += ".md"

    file_path = OUTPUT_DIR / safe_filename
    file_path.write_text(story, encoding="utf-8")

    return f"Story saved successfully to: {file_path}"


if __name__ == "__main__":
    mcp.run()