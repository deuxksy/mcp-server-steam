# mcp-server-steam

A comprehensive Model Context Protocol (MCP) server for Steam Web API integration using FastMCP 3.0 beta2.

## Features

- **User Profiles & Stats**
  - Profile information (persona, avatar, account details)
  - Friend lists
  - Owned games library
  - Playtime data
  - Recently played games
  - Steam level
  - Achievement progress

- **Game Info & Store**
  - Game details and metadata
  - Store prices and discounts
  - News and updates
  - Game search
  - Achievement data for specific games

- **Community Features**
  - Steam Workshop items
  - User reviews
  - VAC and game ban status

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd mcp-server-steam/main
```

2. Install dependencies with uv:
```bash
uv sync
```

3. Get a Steam Web API key:
   - Visit https://steamcommunity.com/dev/apikey
   - Log in with your Steam account
   - Register your domain and copy the API key

4. Configure environment:
```bash
cp .env.example .env
# Edit .env and add your STEAM_API_KEY
```

## Usage

### Running the Server

```bash
uv run python server.py
```

The server will start with STDIO transport, suitable for MCP clients like Claude Desktop.

### Claude Desktop Configuration

📖 **자세한 설정 가이드**: [CLAUDE_CONFIG.md](./CLAUDE_CONFIG.md)

#### macOS

Claude Desktop 설정 파일 (`~/Library/Application Support/Claude/claude_desktop_config.json`)에 추가:

```json
{
  "mcpServers": {
    "steam": {
      "command": "uv",
      "args": ["run", "python", "/Users/crong/git/mcp-server-steam/main/server.py"],
      "env": {
        "STEAM_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

#### 환경 변수 사용 (권장)

API 키를 직접 입력하는 대신 환경 변수를 사용하세요:

```bash
# ~/.zshrc 또는 ~/.zprofile에 추가
export STEAM_API_KEY="your_steam_api_key_here"
```

설정에서는:
```json
"env": {
  "STEAM_API_KEY": "${STEAM_API_KEY}"
}
```

#### Claude Desktop 재시작

설정을 적용하려면 Claude Desktop을 완전히 종료했다가 다시 시작하세요.

### MCP Client Configuration

Add to your MCP client configuration:

```json
{
  "mcpServers": {
    "steam": {
      "command": "uv",
      "args": ["run", "python", "/path/to/mcp-server-steam/main/server.py"],
      "env": {
        "STEAM_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

### Testing with FastMCP CLI

```bash
# List available tools
fastmcp list server.py

# Call a tool
fastmcp call server.py get_user_profile steam_id=76561198000000000
```

## Available Tools

### Profile Tools
- `get_user_profile` - Get Steam user profile
- `get_friends_list` - Get user's friend list
- `get_owned_games` - Get all owned games
- `get_recently_played_games` - Get recently played games
- `get_steam_level` - Get user's Steam level
- `get_player_achievements` - Get achievement progress for a game

### Game Tools
- `get_game_details` - Get game information from store
- `get_game_news` - Get news and updates for games
- `get_global_achievement_percentages` - Get global achievement stats
- `search_games` - Search for games on Steam
- `get_game_schema` - Get achievement and stats schema

### Community Tools
- `get_workshop_items` - Get Steam Workshop items
- `get_workshop_item_details` - Get workshop item details
- `get_user_reviews` - Get user reviews for games
- `get_player_bans` - Get VAC and game ban status

### Utility Tools
- `resolve_vanity_url` - Convert vanity URL to Steam ID

## Resources

- `steam://config` - Server configuration
- `steam://supported-games` - Common game App IDs

## Steam IDs vs App IDs

- **Steam ID (SteamID)**: 64-bit user account ID (e.g., 76561198000000000)
- **App ID (AppID)**: Game identifier on Steam store (e.g., 730 for CS2)

Use `resolve_vanity_url` to convert a custom profile URL to a Steam ID.

## Rate Limiting

The server implements rate limiting to respect Steam API limits:
- 100 requests per minute
- Automatic exponential backoff on errors
- Proper error handling for rate limit responses

## Project Structure

```
mcp-server-steam/
├── server.py              # Main entry point
├── steam_client.py         # Steam API client
├── config.py              # Configuration
├── requirements.txt        # Dependencies
├── README.md              # This file
├── .env                   # API key (not in git)
├── .env.example           # Environment template
└── tools/                 # Tool modules
    ├── __init__.py
    ├── profile.py          # User profile tools
    ├── games.py            # Game info tools
    └── community.py       # Community tools
```

## Error Handling

The server provides clear error messages for:
- Invalid Steam IDs or App IDs
- Missing API keys
- Rate limit exceeded
- Network errors
- Steam API errors

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## License

MIT License - See LICENSE file for details

## Resources

- [Steam Web API Documentation](https://steamapi.xpaw.me/)
- [FastMCP Documentation](https://gofastmcp.com/)
- [Steam Community Developer Portal](https://steamcommunity.com/dev)

## Acknowledgments

Built with [FastMCP 3.0](https://github.com/jlowin/fastmcp) and [Steam Web API](https://steamcommunity.com/dev).
