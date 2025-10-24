# MCP servers
### This repo contains various custom mcp-servers

To create an mcp server follow the steps below:

1. Create a new directory and give it a name
2. Create and activate a virtual environment (i think this will create a pyproject.toml file)
    ```BASH
    uv venv
    source .venv/bin/activate
    ```
3. then run     
    ```BASH
    uv sync
    ```
    this should synchronize a uv.lock file with the .toml file.
4. uv add mcp[cli] and any other dependencies
5. Create a main.py and add your MCP code
6. If using Docker, create a Dockerfile. This describes how to create a docker vm to run your server
    ```Dockerfile
    # Use Python slim image
    FROM python:3.10-slim

    # Set working directory
    WORKDIR /app

    # Install uv (the package manager used in the tutorial)
    RUN pip install uv

    # Copy your project files
    COPY pyproject.toml .
    COPY weather.py .

    # Install dependencies using uv
    RUN uv sync

    # Set the entrypoint to run your server
    ENTRYPOINT ["uv", "run", "weather.py"]
    ```
7. Edit this ```~/.docker/mcp/catalogs/custom.yaml```
    ```yaml
    version: 2
    name: custom
    displayName: Custom MCP Servers
    registry:
    weather-mcp:
        description: "Weather forecast and alerts"
        title: "Weather Server"
        type: server
        dateAdded: "2025-01-01T00:00:00Z"
        image: weather-mcp-server:latest
        ref: ""
        tools:
        - name: get_alerts
        - name: get_forecast
    ```

8. Edit this ```~/.docker/mcp/custom-registry.yaml```
    ```yaml
    registry:
        weather-mcp:
            ref: ""
    ```
9. Then check the Claude config custom catalog and registry @ ```~/Library/Application Support/Claude/claude_desktop_config.json```
    ```json
    {
        "mcpServers":{
            "weather":{
                "command":"uv",
                "args":["--directory","/Users/benjamin/Code/mcp-servers/weather","run","weather.py"]
            },
                "MCP_DOCKER": {
                    "command": "docker",
                    "args": [
                        "run",
                        "-i",
                        "--rm",
                        "-v", "/var/run/docker.sock:/var/run/docker.sock",
                        "-v", "/Users/benjamin/.docker/mcp:/mcp",
                        "docker/mcp-gateway",
                        "--catalog=/mcp/catalogs/docker-mcp.yaml",
                        "--catalog=/mcp/catalogs/custom.yaml",
                        "--registry=/mcp/registry.yaml",
                        "--registry=/mcp/custom-registry.yaml",
                        "--transport=stdio"
        ]
                }
        }
    }
```