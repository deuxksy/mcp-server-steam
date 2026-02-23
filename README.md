# mcp-server-steam

> **AI** 를 활용해 생성된 프로젝트입니다.

FastMCP를 사용하여 Steam Web API와 통합하는 종합 MCP(Model Context Protocol) 서버입니다.

## 주요 기능

- **사용자 프로필 및 통계**
  - 프로필 정보 (닉네임, 아바타, 계정 상세)
  - 친구 목록
  - 소유 게임 라이브러리
  - 플레이시간 데이터
  - 최근 플레이한 게임
  - Steam 레벨
  - 업적 진행상황

- **게임 정보 및 스토어**
  - 게임 상세 정보 및 메타데이터
  - 스토어 가격 및 할인 정보
  - 뉴스 및 업데이트
  - 게임 검색
  - 특정 게임의 업적 데이터

- **커뮤니티 기능**
  - Steam 워크샵 아이템
  - 사용자 리뷰
  - VAC 및 게임 밴 상태

## PyPI에서 설치

PyPI에 게시된 후 다음과 같이 설치할 수 있습니다:

```bash
pip install mcp-server-steam
```

설치 후 다음과 같이 실행합니다:

```bash
mcp-server-steam
```

## 소스에서 설치

또는 소스 코드에서 직접 설치합니다:

1. 저장소 클론:
```bash
git clone <repository-url>
cd mcp-server-steam
```

2. uv로 의존성 설치:
```bash
uv sync
```

3. 패키지 설치:
```bash
uv pip install -e .
```

4. Steam Web API 키 발급:
   - https://steamcommunity.com/dev/apikey 방문
   - Steam 계정으로 로그인
   - 도메인 등록 후 API 키 복사

4. 환경 설정:

**중요**: `.env` 파일에 API 키를 설정해야 합니다.

```bash
# .env.example을 복사해서 .env 파일 생성
cp .env.example .env

# .env 파일을 텍스트 편집기로 열어서 STEAM_API_KEY 추가
# 예: STEAM_API_KEY=YOUR_API_KEY_HERE

# (선택사항) Steam ID를 기본값으로 설정하려면:
# STEAM_USER_ID=76561198XXXXXXXXXXX
```

**API 키 발급**: https://steamcommunity.com/dev/apikey

## 사용 방법

### 서버 실행

```bash
# PyPI에서 설치한 경우
mcp-server-steam

# 소스에서 개발 중인 경우
uv run python -m mcp_server_steam
```

서버가 STDIO 전송 방식으로 시작되며, Claude Desktop 같은 MCP 클라이언트에서 사용할 수 있습니다.

### Claude Desktop Configuration

📖 **자세한 설정 가이드**: [CLAUDE_CONFIG.md](./CLAUDE_CONFIG.md)

#### PyPI에서 설치한 경우 (권장)

Claude Desktop 설정 파일에 추가:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%/Claude/claude_desktop_config.json`
**Linux**: `~/.config/Claude/claude_desktop_config.json`

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

#### 소스에서 개발하는 경우

```json
{
  "mcpServers": {
    "steam": {
      "command": "uv",
      "args": ["run", "python", "-m", "mcp_server_steam"],
      "cwd": "/path/to/mcp-server-steam",
      "env": {
        "STEAM_API_KEY": "${STEAM_API_KEY}",
        "STEAM_USER_ID": "${STEAM_USER_ID}"
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

### MCP 클라이언트 설정

일반적으로는 PyPI 버전을 사용하는 것이 좋습니다:

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

### FastMCP CLI로 테스트

```bash
# 사용 가능한 도구 목록 보기
uv run fastmcp list src/mcp_server_steam/server.py

# 도구 호출 테스트
uv run fastmcp call src/mcp_server_steam/server.py get_user_profile steam_id=76561198000000000
```

## 사용 가능한 도구

### 프로필 도구
- `get_user_profile` - Steam 사용자 프로필 조회
- `get_friends_list` - 친구 목록 조회
- `get_owned_games` - 소유한 모든 게임 조회
- `get_recently_played_games` - 최근 플레이한 게임 조회
- `get_steam_level` - Steam 레벨 조회
- `get_player_achievements` - 특정 게임의 업적 진행상황 조회

### 게임 도구
- `get_game_details` - 스토어에서 게임 정보 조회
- `get_game_news` - 게임 뉴스 및 업데이트 조회
- `get_global_achievement_percentages` - 전체 업적 통계 조회
- `search_games` - Steam에서 게임 검색
- `get_game_schema` - 업적 및 통계 스키마 조회

### 커뮤니티 도구
- `get_workshop_items` - Steam 워크샵 아이템 조회
- `get_workshop_item_details` - 워크샵 아이템 상세 정보
- `get_user_reviews` - 게임 사용자 리뷰 조회
- `get_player_bans` - VAC 및 게임 밴 상태 조회

### 유틸리티 도구
- `resolve_vanity_url` - Vanity URL을 Steam ID로 변환

## 리소스

- `steam://config` - 서버 설정
- `steam://supported-games` - 일반적인 게임 App ID 목록

## Steam ID vs App ID

- **Steam ID (SteamID)**: 64비트 사용자 계정 ID (예: 76561198000000000)
- **App ID (AppID)**: Steam 스토어에서의 게임 식별자 (예: CS2의 경우 730)

커스텀 프로필 URL을 Steam ID로 변환하려면 `resolve_vanity_url`을 사용하세요.

## 속도 제한 (Rate Limiting)

서버는 Steam API 제한을 준수하기 위해 속도 제한을 구현합니다:
- 분당 100회 요청
- 오류 발생 시 자동 지수 백오프
- 속도 제한 응답에 대한 적절한 에러 처리

## 프로젝트 구조

```
mcp-server-steam/
├── src/
│   └── mcp_server_steam/
│       ├── __init__.py
│       ├── __main__.py        # 메인 진입점
│       ├── server.py          # MCP 서버
│       ├── steam_client.py    # Steam API 클라이언트
│       ├── config.py          # 설정
│       └── tools/             # 도구 모듈
│           ├── __init__.py
│           ├── profile.py     # 사용자 프로필 도구
│           ├── games.py       # 게임 정보 도구
│           └── community.py   # 커뮤니티 도구
├── pyproject.toml             # 프로젝트 설정 및 의존성
├── README.md                  # 이 파일
├── .env                       # API 키 (git에 포함되지 않음)
└── .env.example               # 환경변수 템플릿
```

## 에러 처리

서버는 다음 경우에 명확한 에러 메시지를 제공합니다:
- 유효하지 않은 Steam ID 또는 App ID
- API 키 누락
- 속도 제한 초과
- 네트워크 오류
- Steam API 오류

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

## 기여

기여를 환영합니다! 이슈나 풀 리퀘스트를 자유롭게 제출해 주세요.

## 참고 자료

- [Steam Web API 문서](https://steamapi.xpaw.me/)
- [FastMCP 문서](https://gofastmcp.com/)
- [Steam Community 개발자 포털](https://steamcommunity.com/dev)

## 라이선스

MIT License - 자세한 내용은 LICENSE 파일을 참조하세요
