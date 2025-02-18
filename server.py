# server.py
from mcp.server.fastmcp import FastMCP
from databridge import DataBridge

# Create an MCP server
mcp = FastMCP("Demo")
db = DataBridge(is_local=True, timeout=300)

# Add an addition tool
@mcp.tool(
    name="ingest_user_observations",
    description="Ingest user observations, returns a list of documents that it has ingested - with id. Provide a list of observation, where each item has an observation field as well as a metadata field. The observation contains the actual observations, and the metadata field contains any additional information about the observation. The metadata field is a dictionary that can contain any information about the observation."
)
def ingest_user_observations(observations: list[dict]) -> int:
    """Ingest user observations, returns a list of documents that it has ingested - with id"""
    db_responses = []
    for observation in observations:
        response = db.ingest_text(observation["observation"], observation["metadata"])
        db_responses.append(response)
    return db_responses

@mcp.tool(
    name="retrieve_information",
    description="Retrieve information from the database. Provide a query, and the database will return a list of documents or chunks that match the query. Every time the the user speaks with you, call this tool with the user's query. this tool will return a list of documents or chunks that will help you answer the user's query."
)
def retrieve_information(query: str) -> list[dict]:
    """Retrieve information from the database"""
    chunks = [chunk.content for chunk in db.retrieve_chunks(query, k=10)]
    content = ""
    for i, chunk in enumerate(chunks, 1):
        content += f"Chunk {i}:\n{chunk}\n\n"
    return content


if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')
