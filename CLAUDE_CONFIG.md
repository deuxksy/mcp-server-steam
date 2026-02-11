# Claude Desktop MCP 설정 방법

## 1. Steam API 키 발급

https://steamcommunity.com/dev/apikey 에 접속하여 API 키를 발급받으세요.

## 2. Claude Desktop 설정

### macOS

```bash
# Claude Desktop 설정 디렉토리로 이동
cd ~/Library/Application\ Support/Claude

# 또는 설정 파일 직접 편집
code ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

### Windows

```
%APPDATA%\Claude\claude_desktop_config.json
```

### Linux

```
~/.config/Claude/claude_desktop_config.json
```

## 3. 설정 파일에 mcp-server-steam 추가

```json
{
  "mcpServers": {
    "steam": {
      "command": "uv",
      "args": [
        "run",
        "python",
        "/Users/crong/git/mcp-server-steam/main/server.py"
      ],
      "env": {
        "STEAM_API_KEY": "your_steam_api_key_here"
      }
    }
  }
}
```

## 4. 환경 변수로 API 키 설정 (권장)

API 키를 직접 파일에 입력하는 대신 환경 변수를 사용하는 것을 권장합니다.

### macOS (zsh)
```bash
# ~/.zshrc 또는 ~/.zprofile에 추가
export STEAM_API_KEY="your_steam_api_key_here"

# 재시작 후 Claude Desktop 재시작
```

### 설정 파일에서 환경 변수 사용
```json
{
  "mcpServers": {
    "steam": {
      "command": "uv",
      "args": ["run", "python", "/path/to/server.py"],
      "env": {
        "STEAM_API_KEY": "${STEAM_API_KEY}"
      }
    }
  }
}
```

## 5. Claude Desktop 재시작

설정을 적용하려면 Claude Desktop을 완전히 종료했다가 다시 시작하세요.

## 6. 동작 확인

Claude Desktop에서 다음과 같이 테스트할 수 있습니다:

```
내 Steam 프로필을 조회해줘. Steam ID는 76561198000000000이야.
```

또는:

```
최근 플레이한 게임 목록을 보여줘.
```

## 사용 가능한 도구

### 프로필 도구
- `get_user_profile` - Steam 사용자 프로필 조회
- `get_friends_list` - 친구 목록
- `get_owned_games` - 소유 게임 목록
- `get_recently_played_games` - 최근 플레이한 게임
- `get_steam_level` - Steam 레벨
- `get_player_achievements` - 업적 진행상황

### 게임 도구
- `get_game_details` - 게임 상세 정보
- `get_game_news` - 게임 뉴스
- `get_global_achievement_percentages` - 전역 업적 통계
- `search_games` - 게임 검색
- `get_game_schema` - 게임 스키마

### 커뮤니티 도구
- `get_workshop_items` - 워크샵 아이템
- `get_workshop_item_details` - 워크샵 상세
- `get_user_reviews` - 사용자 리뷰
- `get_player_bans` - VAC/게임 밴 상태

### 유틸리티
- `resolve_vanity_url` - 커스텀 URL → Steam ID 변환

## 문제 해결

### 서버가 시작되지 않음
1. `uv sync`로 의존성이 설치되었는지 확인
2. `.env` 파일에 `STEAM_API_KEY`가 있는지 확인
3. Python 3.10+가 설치되었는지 확인

### 도구가 나타나지 않음
1. Claude Desktop이 완전히 재시작되었는지 확인
2. 설정 파일 JSON 형식이 올바른지 확인
3. 서버 파일 경로가 올바른지 확인

### API 인증 오류
1. Steam API 키가 올바른지 확인
2. API 키 도메인 제한이 있는지 확인 (localhost 사용 권장)

## 추가 리소스

- [Steam Web API 문서](https://steamapi.xpaw.me/)
- [FastMCP 문서](https://gofastmcp.com/)
- [Claude MCP 설정 가이드](https://github.com/anthropics/claude-desktop)
