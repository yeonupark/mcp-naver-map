# MCP-NAVER-Map
**MCP-NAVER-Location** is an MCP server that integrates with Naver Cloud's **Geolocation API** and **Directions15 API** to provide IP-based location lookup and route finding capabilities.

---

## ✨ Features

### 📍 IP-Based Location Lookup
Retrieve an approximate location by providing an IP address.

> "Where am I right now (IP: xxx.xxx.xxx.xxx)?"  
> → 📍 Returns latitude and longitude based on the provided IP

- Powered by NCP Geolocation API
- Manual IP input required
    

         
### 🛣️ Route Finding
Get optimal driving directions between two specified points.

> "How do I get from City Hall to Seoul Station?"  
> → 🛣️ Returns route directions

- Powered by NCP Directions15 API


---

## 🚀 Quick Start

### Prerequisites
- Python 3.12+
- `uv` package manager
- Naver Cloud Platform account and API services activated:
  - Geolocation API
  - Directions15 API
- MCP-compatible client (e.g., Claude for Desktop)

---

### 1. Clone and Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/mcp-naver-location.git
cd mcp-naver-map

# Install dependencies
uv sync
```
Create a .env file with your credentials:
```
NAVER_ACCESS_KEY_ID=your_access_key
NAVER_SECRET_KEY=your_secret_key
MAP_CLIENT_ID=your_map_client_id
MAP_CLIENT_SECRET=your_map_client_secret
```
### 2. Configure MCP Client
Register this server in your MCP client (e.g., Claude for Desktop).

Edit ~/Library/Application Support/Claude/claude_desktop_config.json:
```
{
  "mcpServers": {
    "mcp-naver-location": {
      "command": "uv",
      "args": [
        "--directory",
        "/ABSOLUTE/PATH/TO/PARENT/FOLDER/mcp-naver-location",
        "run",
        "server"
      ]
    }
  }
}
```
### 3. Launch Claude

⚠️ Important: Claude must be launched from the terminal to establish a proper connection to the MCP server.

  ```
# macOS:
/Applications/Claude.app/Contents/MacOS/Claude


# Windows:
"C:\Program Files\Claude\Claude.exe"
```
---
## 📝 License
This project is licensed under the [MIT License](LICENSE). See the LICENSE file for details.
