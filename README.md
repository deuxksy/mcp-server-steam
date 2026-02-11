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

## AI 사용 예시

### 예시 1: 사용자 프로필 조회

```
사용자: "내 Steam 프로필 조회해줘"
AI: resolve_vanity_url을 호출하여 vanity URL을 Steam ID로 변환
AI: get_user_profile을 호출하여 프로필 정보 조회
```

### 예시 2: 게임 라이브러리 분석

```
사용자: "내 게임 목록 보여줘"
AI: get_user_profile로 Steam ID 획득
AI: get_owned_games로 소유 게임 목록 조회
AI: 플레이타임 기준으로 정렬하고 상위 게임 요약
```

### 예시 3: 게임 검색 및 상세 정보

```
사용자: "엘든 링 GO 정보 알려줘"
AI: search_games로 "ELDEN RING" 검색
AI: get_game_details로 상세 정보, 가격, 장르 조회
```

### 예시 4: 업적 확인

```
사용자: "내 염완의 왕 게임 업적이 어떻게 돼?"
AI: get_owned_games로 게임 목록 확인
AI: get_player_achievements로 염완의 왕 업적 조회
AI: get_global_achievement_percentages로 전체 플레이어 대비 비교
```

### 예시 5: 워크샵 모드 찾기

```
사용자: "스카이림 모드 추천해줘"
AI: search_games로 스타필드 스카이림(Skyrim, App ID: 72850) 검색
AI: get_workshop_items로 인기 모드 목록 조회
AI: get_workshop_item_details로 특정 모드 상세 정보 확인
```

### AI를 위한 팁

1. **도구 사용 순서**: `resolve_vanity_url` → `get_user_profile` → 다른 도구들
2. **데이터 효율성**: `include_app_info=True`로 한 번에 게임 정보까지 가져오기
3. **오류 처리**: Steam ID가 유효하지 않으면 vanity URL 변환 먼저 시도
4. **언어 설정**: 한국 사용자를 위한 `language="korean"` 또는 `language="english"` 파라미터 활용

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
