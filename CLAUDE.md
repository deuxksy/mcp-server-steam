# Claude Desktop 설정

## MCP 서버 설정

### 일반 사용자 (PyPI에서 설치)

```json
{
  "mcpServers": {
    "steam": {
      "command": "uvx",
      "args": ["mcp-server-steam"],
      "env": {
        "STEAM_API_KEY": "${STEAM_API_KEY}",
        "STEAM_USER_ID": "${STEAM_USER_ID}"
      }
    }
  }
}
```

또는 `pip`으로 설치한 경우:

```json
{
  "mcpServers": {
    "steam": {
      "command": "mcp-server-steam",
      "env": {
        "STEAM_API_KEY": "${STEAM_API_KEY}",
        "STEAM_USER_ID": "${STEAM_USER_ID}"
      }
    }
  }
}
```

### 개발자 (로컬 개발 환경)

```json
{
  "mcpServers": {
    "steam": {
      "command": "uv",
      "args": [
        "run",
        "python",
        "-m",
        "mcp_server_steam"
      ],
      "cwd": "/path/to/mcp-server-steam",
      "env": {
        "STEAM_API_KEY": "${STEAM_API_KEY}",
        "STEAM_USER_ID": "${STEAM_USER_ID}"
      }
    }
  }
}
```

## AI 성격 설정

```json
{
  "temperature": 0.7,
  "maxTokens": 8192,
  "customInstructions": "너는 Steam 게임 전문가 AI 어시스턴트입니다. 사용자의 Steam 계정과 게임 라이브러리를 분석하고, 게임 관련 정보를 제공할 때 전문 용어를 사용하고, 한국어로 친절하게 설명해주세요. 플레이타임, 업적 달성률, 게임 통계 등의 수치 데이터는 정확하게 계산해서 보여주세요."
}
```

## 언어 설정

```json
{
  "locale": "ko-KR"
}
```
