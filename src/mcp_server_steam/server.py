#!/usr/bin/env python3
"""
mcp-server-steam - MCP Server for Steam Web API

AI 최적화된 Steam Web API MCP 서버.

Claude Desktop 등 AI 어시스턴스와 함께 사용하기 위해 설계되었습니다.

Requirements:
    - Steam Web API key from https://steamcommunity.com/dev/apikey
    - Set STEAM_API_KEY environment variable

Usage:
    uv run python server.py
"""

import json
import logging
from contextlib import asynccontextmanager
from typing import Any

from fastmcp import FastMCP
from pydantic import Field

from mcp_server_steam.config import settings

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app):
    """Lifespan context manager for startup/shutdown."""
    from mcp_server_steam import __version__

    logger.info("Starting mcp-server-steam v%s...", __version__)

    # Validate API key on startup
    if not settings.steam_api_key or settings.steam_api_key == "your_steam_api_key_here":
        raise ValueError(
            "Invalid STEAM_API_KEY. Get your API key from "
            "https://steamcommunity.com/dev/apikey and set it in .env file"
        )

    logger.info("Steam API key validated successfully")

    yield

    logger.info("Shutting down mcp-server-steam...")


# AI를 위한 종합적인 프롬프트
AI_INSTRUCTIONS = """
## Steam MCP Server 사용 가이드

이 서버는 Steam Web API와 상호작용하기 위한 16개 도구를 제공합니다.

## 🎯 일반적인 사용 패턴

### 1. 사용자 프로필 조회 (가장 일반적인 작업)
```
사용자: "내 Steam 프로필 조회해줘" 또는 "내 스팀 정보 보여줘"
AI: resolve_vanity_url로 vanity URL을 Steam ID로 변환 시도
AI: get_user_profile로 프로필 조회
```

### 2. 게임 라이브러리 분석
```
사용자: "내 게임 목록 보여줘" 또는 "무슨 게임을 가지고 있어?"
AI: get_user_profile로 Steam ID 획득
AI: get_owned_games로 소유 게임 목록 조회
AI: 플레이타임 순으로 정렬하여 요약
```

### 3. 특정 게임 정보 조회
```
사용자: "엘든 링 GO 정보 알려줘"
AI: search_games로 "ELDEN RING" 검색
AI: get_game_details로 상세 정보 조회
```

### 4. 업적 및 통계
```
사용자: "내 업적 현황 알려줘"
AI: get_owned_games로 게임 목록 획득
AI: get_player_achievements로 각 게임 업적 조회
AI: get_global_achievement_percentages로 전체 플레이어 대비 비교
```

## 🔗 도구 간의 관계

### 필수 선행 도구
- **resolve_vanity_url** → **모든 프로필 도구**의 선행 조건
  - 사용자가 vanity URL(steamcommunity.com/id/username)만 알 경우
  - 먼저 resolve_vanity_url로 Steam ID(64-bit)를 변환해야 함

### 데이터 흐름
```
resolve_vanity_url (선택)
    ↓
get_user_profile (Steam ID 획득)
    ↓
get_owned_games, get_friends_list, etc. (프로필 기반 작업)
```

## ⚠️ 중요한 고려사항

### Steam ID 형식
- 64-bit 숫자: 76561198000000000
- vanity URL: "username" (steamcommunity.com/id/username 부분)
- 도구마다 필요한 형식이 다름

### App ID 형식
- 게임 식별자: 730 (CS2), 570 (Dota 2) 등
- search_games로 먼저 찾으면 App ID를 확인할 수 있음

### 요율성 고려
- 한 번의 API 호출로 최대한 많은 정보 획득
- include_app_info=True로 게임 정보 포함 (get_owned_games)
- 필요한 데이터만 요청하여 rate limit 준수

### 에러 처리
- Steam ID가 유효하지 않음: "프로필을 찾을 수 없습니다"
- 비공개 프로필: "접근 권한이 없습니다"
- Rate limit: "잠시 후 다시 시도해주세요"

## 📊 데이터 구조 이해

### 사용자 프로필 응답
{
  "steamid": "76561198000000000",
  "personaname": "사용자명",
  "avatarfull": "아바타 URL",
  "personastate": 0,  # 오프라인/온라인 상태
  "loccountrycode": "KR"
}

### 소유 게임 응답
[
  {
    "appid": 730,
    "name": "Counter-Strike 2",
    "playtime_forever": 12345,  # 총 플레이시간(분)
    "playtime_2weeks": 600,     # 최근 2주 플레이시간(분)
    "has_community_visible_stats": true
  }
]

### 업적 응답
[
  {
    "name": "업적 이름",
    "achieved": true,
    "unlocktime": 1234567890,  # Unix timestamp
    "description": "업적 설명"
  }
]
"""


# Create main server instance
mcp = FastMCP(
    name="mcp-server-steam",
    instructions=AI_INSTRUCTIONS,
    lifespan=lifespan,
)


# ============================================================================
# Profile Tools
# ============================================================================

@mcp.tool()
async def get_user_profile(
    steam_id: str = Field(
        description="Steam 사용자의 64-bit ID입니다. 예: 76561198000000000. vanity URL(steamcommunity.com/id/xxx)이 있는 경우 먼저 resolve_vanity_url 도구로 변환하세요."
    )
) -> dict[str, Any]:
    """
    Steam 사용자 프로필을 조회합니다.

    반환 데이터: 사용자명(personaname), 아바타 URL(avatarfull), 온라인 상태(personastate),
    국가(loccountrycode), 프로필 URL(profileurl) 등을 포함합니다.

    사용 예시: steam_id="76561198000000000"
    """
    from mcp_server_steam.steam_client import SteamAPIClient

    async with SteamAPIClient() as client:
        params = {"steamids": steam_id}
        result = await client.get("ISteamUser", "GetPlayerSummaries", params=params)

        if not result.get("response", {}).get("players"):
            raise ValueError(f"No profile found for Steam ID: {steam_id}")

        return result["response"]["players"][0]


@mcp.tool()
async def get_friends_list(
    steam_id: str = Field(
        description="친구 목록을 조회할 사용자의 64-bit Steam ID입니다."
    ),
    relationship: str = Field(
        default="all",
        description="친구 관계 필터. 'all'=모든 친구, 'friend'=친구만"
    )
) -> list[dict[str, Any]]:
    """
    Steam 사용자의 친구 목록을 조회합니다.

    반환 데이터: 각 친구의 Steam ID(steamid), 친구 맺은 날짜(friend_since timestamp),
    관계(relationship) 등을 포함합니다.

    사용 예시: steam_id="76561198000000000", relationship="all"
    """
    from mcp_server_steam.steam_client import SteamAPIClient

    async with SteamAPIClient() as client:
        params = {
            "steamid": steam_id,
            "relationship": relationship
        }
        result = await client.get("ISteamUser", "GetFriendList", params=params)

        friends_list = result.get("response", {}).get("friends", [])
        return friends_list


@mcp.tool()
async def get_owned_games(
    steam_id: str | None = Field(
        default=None,
        description="게임 라이브러리를 조회할 사용자의 64-bit Steam ID입니다. 설정하지 않으면 환경변수 STEAM_USER_ID를 사용합니다."
    ),
    include_app_info: bool = Field(
        default=True,
        description="게임 이름과 메타데이터를 포함할지 여부입니다. 기본값은 true입니다."
    ),
    include_played_free_games: bool = Field(
        default=False,
        description="플레이한 적 있는 무료 게임을 포함할지 여부입니다."
    )
) -> list[dict[str, Any]]:
    """
    사용자가 소유한 모든 게임을 조회합니다.

    반환 데이터: 각 게임의 App ID(appid), 이름(name), 총 플레이시간(playtime_forever, 분 단위),
    최근 플레이시간(playtime_2weeks, 분 단위), 마지막 플레이 날짜(last_played, Unix timestamp) 등을 포함합니다.

    플레이시간은 '분' 단위입니다. 60시간 = 3600분입니다.

    사용 예시: steam_id="76561198000000000", include_app_info=True
    """
    from mcp_server_steam.steam_client import SteamAPIClient
    from mcp_server_steam.config import settings

    # steam_id가 없으면 환경 변수 사용
    target_steam_id = steam_id or settings.steam_user_id
    if not target_steam_id:
        raise ValueError("steam_id 파라미터가 없고 환경변수 STEAM_USER_ID도 설정되지 않았습니다.")

    async with SteamAPIClient() as client:
        params = {
            "steamid": target_steam_id,
            "include_appinfo": str(include_app_info).lower(),
            "include_played_free_games": str(include_played_free_games).lower(),
            "format": "json"
        }
        result = await client.get("IPlayerService", "GetOwnedGames", version="v0001", params=params)

        games = result.get("response", {}).get("games", [])
        return games


@mcp.tool()
async def get_recently_played_games(
    steam_id: str = Field(
        description="최근 플레이한 게임을 조회할 사용자의 64-bit Steam ID입니다."
    ),
    count: int = Field(
        default=10,
        description="반환할 최근 게임 수입니다. 최대 50개까지 가능합니다."
    )
) -> list[dict[str, Any]]:
    """
    최근 플레이한 게임 목록을 조회합니다.

    반환 데이터: 최근에 플레이한 게임들의 App ID, 이름, 최근 2주간 플레이시간,
    총 플레이시간 등을 포함합니다.

    사용 예시: steam_id="76561198000000000", count=10
    """
    from mcp_server_steam.steam_client import SteamAPIClient

    async with SteamAPIClient() as client:
        params = {
            "steamid": steam_id,
            "count": count
        }
        result = await client.get("IPlayerService", "GetRecentlyPlayedGames", version="v0001", params=params)

        games = result.get("response", {}).get("games", [])
        return games


@mcp.tool()
async def get_steam_level(
    steam_id: str = Field(
        description="Steam 레벨을 조회할 사용자의 64-bit Steam ID입니다."
    )
) -> dict[str, Any]:
    """
    사용자의 Steam 레벨을 조회합니다.

    반환 데이터: 사용자의 Steam 레벨(player_level)을 포함합니다.

    사용 예시: steam_id="76561198000000000"
    """
    from mcp_server_steam.steam_client import SteamAPIClient

    async with SteamAPIClient() as client:
        params = {"steamid": steam_id}
        result = await client.get("IPlayerService", "GetSteamLevel", params=params)

        return result.get("response", {})


@mcp.tool()
async def get_player_achievements(
    steam_id: str = Field(
        description="업적을 조회할 사용자의 64-bit Steam ID입니다."
    ),
    app_id: int = Field(
        description="업적을 조회할 게임의 Steam App ID입니다. 예: 730(CS2), 570(Dota 2)"
    ),
    language: str = Field(
        default="english",
        description="업적 이름 언어입니다. 'english', 'korean' 등을 지원합니다."
    )
) -> list[dict[str, Any]]:
    """
    특정 게임의 업적 진행상황을 조회합니다.

    반환 데이터: 각 업적의 이름(name), 달성 여부(achieved), 달성 시간(unlocktime, Unix timestamp),
    설명(description) 등을 포함합니다.

    사용 예시: steam_id="76561198000000000", app_id=730, language="english"
    """
    from mcp_server_steam.steam_client import SteamAPIClient

    async with SteamAPIClient() as client:
        params = {
            "steamid": steam_id,
            "appid": app_id,
            "l": language
        }
        result = await client.get("ISteamUserStats", "GetPlayerAchievements", version="v0001", params=params)

        achievements = result.get("response", {}).get("achievements", [])
        return achievements


# ============================================================================
# Game Tools
# ============================================================================

@mcp.tool()
async def get_game_details(
    app_ids: list[int] = Field(
        description="상세 정보를 조회할 게임들의 Steam App ID 리스트입니다. 최대 100개까지 한 번에 조회 가능합니다."
    ),
    language: str = Field(
        default="english",
        description="게임 정보 언어입니다. 'english', 'korean' 등을 지원합니다."
    )
) -> list[dict[str, Any]]:
    """
    Steam 상점에서 게임 상세 정보를 조회합니다.

    반환 데이터: 각 게임의 이름(name), 개발사(developers), 퍼블리셔(publishers),
    가격 정보(price_overview), 장르(genres), 릴리스 날짜(release_date),
    플랫폼(true/false), 메타데이터 등을 포함합니다.

    사용 예시: app_ids=[730, 570, 440], language="english"
    """
    from mcp_server_steam.steam_client import SteamAPIClient
    import httpx

    async with SteamAPIClient() as client:
        url = f"https://store.steampowered.com/api/appdetails?appids={','.join(map(str, app_ids))}&l={language}"

        async with client._client:
            response = await client._client.get(url)
            response.raise_for_status()
            result = response.json()

        games = []
        for app_id, app_data in result.items():
            if app_data.get("success"):
                games.append(app_data["data"])

        return games


@mcp.tool()
async def get_game_news(
    app_id: int = Field(
        description="뉴스를 조회할 게임의 Steam App ID입니다."
    ),
    count: int = Field(
        default=5,
        description="반환할 뉴스 개수입니다. 최대 20개까지 가능합니다."
    ),
    max_length: int = Field(
        default=300,
        description="각 뉴스 항목의 최대 길이입니다(문자 수)."
    )
) -> list[dict[str, Any]]:
    """
    특정 게임의 뉴스와 업데이트를 조회합니다.

    반환 데이터: 각 뉴스의 제목(title), 내용(contents), URL(url),
    날짜(date), 피드 라벨(feed_label) 등을 포함합니다.

    사용 예시: app_id=730, count=5, max_length=300
    """
    from mcp_server_steam.steam_client import SteamAPIClient

    async with SteamAPIClient() as client:
        params = {
            "appid": app_id,
            "count": count,
            "maxlength": max_length
        }
        result = await client.get("ISteamNews", "GetNewsForApp", version="v0002", params=params)

        news_items = result.get("appnews", {}).get("newsitems", [])
        return news_items


@mcp.tool()
async def get_global_achievement_percentages(
    app_id: int = Field(
        description="업적 통계를 조회할 게임의 Steam App ID입니다."
    )
) -> list[dict[str, Any]]:
    """
    게임의 전역 업적 달성률을 조회합니다.

    반환 데이터: 각 업적의 이름(name)과 전체 플레이어 중 달성한 비율(percentage)을 포함합니다.
    이를 통해 해당 업적이 희규한지 일반적인지 파악할 수 있습니다.

    사용 예시: app_id=730
    """
    from mcp_server_steam.steam_client import SteamAPIClient

    async with SteamAPIClient() as client:
        params = {"gameid": app_id, "l": "english"}
        result = await client.get("ISteamUserStats", "GetGlobalAchievementPercentagesForApp", version="v0002", params=params)

        achievements = result.get("achievementpercentages", {}).get("achievements", [])
        return achievements


@mcp.tool()
async def search_games(
    query: str = Field(
        description="게임 검색어입니다. 영어 검색이 더 정확합니다."
    ),
    count: int = Field(
        default=25,
        description="반환할 검색 결과 수입니다. 최대 50개까지 가능합니다."
    )
) -> list[dict[str, Any]]:
    """
    Steam에서 게임을 검색합니다.

    반환 데이터: 일치하는 게임들의 App ID(id), 이름(name), 출시일(released),
    가격(price) 등을 포함합니다.

    검색 팁: 정확한 게임명을 아는 경우 영어로 검색하거나 App ID를 사용하세요.

    사용 예시: query="action", count=25
    """
    from mcp_server_steam.steam_client import SteamAPIClient
    import httpx

    async with SteamAPIClient() as client:
        url = f"https://store.steampowered.com/api/storesearch/?term={query}&l=english&cc=US"

        async with client._client:
            response = await client._client.get(url)
            response.raise_for_status()
            result = response.json()

        items = result.get("items", [])[:count]
        return items


@mcp.tool()
async def get_game_schema(
    app_id: int = Field(
        description="게임 스키마를 조회할 게임의 Steam App ID입니다."
    ),
    language: str = Field(
        default="english",
        description="업적 이름과 설명의 언어입니다."
    )
) -> dict[str, Any]:
    """
    게임의 업적과 통계 스키마를 조회합니다.

    반환 데이터: 게임의 �적들(achievements), 사용 가능한 통계(availableGameStats),
    통계 정의(gameStats) 등을 포함합니다.

    사용 예시: app_id=730, language="english"
    """
    from mcp_server_steam.steam_client import SteamAPIClient

    async with SteamAPIClient() as client:
        params = {
            "appid": app_id,
            "l": language
        }
        result = await client.get("ISteamUserStats", "GetSchemaForGame", version="v0002", params=params)

        return result.get("response", {})


# ============================================================================
# Community Tools
# ============================================================================

@mcp.tool()
async def get_workshop_items(
    app_id: int = Field(
        description="워크샵 아이템을 조회할 게임의 Steam App ID입니다."
    ),
    query_type: int = Field(
        default=1,
        description="쿼리 유형입니다. 1=추천순, 2=최신순, 3=구독순 등."
    ),
    page: int = Field(
        default=1,
        description="페이지 번호입니다. 결과가 많은 경우 다음 페이지를 조회하세요."
    ),
    count: int = Field(
        default=30,
        description="페이지당 아이템 수입니다. 최대 100개까지 가능합니다."
    )
) -> list[dict[str, Any]]:
    """
    Steam Workshop 아이템을 조회합니다.

    반환 데이터: 각 아이템의 파일 ID(publishedfileid), 제목(title),
    생성자(creator), 구독 수(subscriptions), 좋아요 수(favorites),
    파일 크기(file_size), 설명 등을 포함합니다.

    사용 예시: app_id=4000(Garry's Mod), query_type=1, page=1, count=30
    """
    from mcp_server_steam.steam_client import SteamAPIClient

    async with SteamAPIClient() as client:
        params = {
            "key": client.api_key,
            "appid": app_id,
            "query_type": query_type,
            "page": page,
            "pagesize": count,
            "numperpage": count
        }
        result = await client.get("IPublishedFileService", "QueryFiles", version="v0001", params=params)

        files = result.get("response", {}).get("publishedfiledetails", [])
        return files


@mcp.tool()
async def get_workshop_item_details(
    published_file_ids: list[int] | list[str] = Field(
        description="상세 정보를 조회할 워크샵 아이템들의 published file ID 리스트입니다."
    )
) -> list[dict[str, Any]]:
    """
    워크샵 아이템의 상세 정보를 조회합니다.

    반환 데이터: 각 아이템의 상세 메타데이터, 설명, 태그, 미리보기 이미지,
    의존성, 구독/좋아요 통계 등을 포함합니다.

    사용 예시: published_file_ids=[12345678, 87654321]
    """
    from mcp_server_steam.steam_client import SteamAPIClient

    async with SteamAPIClient() as client:
        params = {
            "publishedfileids": ",".join(map(str, published_file_ids))
        }
        result = await client.get("IPublishedFileService", "GetDetails", version="v0001", params=params)

        files = result.get("response", {}).get("publishedfiledetails", [])
        return files


@mcp.tool()
async def get_user_reviews(
    app_id: int = Field(
        description="리뷰를 조회할 게임의 Steam App ID입니다."
    ),
    review_type: str = Field(
        default="all",
        description="리뷰 필터입니다. 'all'=전체, 'positive'=긍정, 'negative'=부정"
    ),
    count: int = Field(
        default=10,
        description="반환할 리뷰 수입니다. 최대 100개까지 가능합니다."
    )
) -> list[dict[str, Any]]:
    """
    게임의 사용자 리뷰를 조회합니다.

    반환 데이터: 각 리뷰의 작성자(author, Steam ID 포함), 내용(content),
    추천 수(votes_up), 비추천 수(votes_down), 총 플레이시간(author.playtime_forever),
    작성일(timestamp), 리뷰 길이 등을 포함합니다.

    사용 예시: app_id=730, review_type="all", count=10
    """
    import httpx

    url = f"https://store.steampowered.com/appreviews/{app_id}"

    async with httpx.AsyncClient() as client:
        params = {
            "json": "1",
            "filter": review_type,
            "num_per_page": count
        }

        response = await client.get(url, params=params)
        response.raise_for_status()
        result = response.json()

    reviews = result.get("reviews", [])
    return reviews


@mcp.tool()
async def get_player_bans(
    steam_ids: list[str] = Field(
        description="밴 상태를 조회할 사용자들의 64-bit Steam ID 리스트입니다. 최대 100개까지 가능합니다."
    )
) -> list[dict[str, Any]]:
    """
    플레이어들의 VAC와 게임 밴 상태를 조회합니다.

    반환 데이터: 각 플레이어의 Steam ID(SteamID), VAC 밴 여부(VACBanned),
    VAC 밴 횟수(numberOfVACBans), 게임 밴 여부, 게임 밴 횟수,
    마지막 밴 이후 날짜(DaysSinceLastBan) 등을 포함합니다.

    사용 예시: steam_ids=["76561198000000000", "76561198000000001"]
    """
    from mcp_server_steam.steam_client import SteamAPIClient

    async with SteamAPIClient() as client:
        params = {
            "steamids": ",".join(steam_ids)
        }
        result = await client.get("ISteamUser", "GetPlayerBans", version="v0001", params=params)

        players = result.get("response", {}).get("players", [])
        return players


# ============================================================================
# Utility Tools
# ============================================================================

@mcp.tool()
async def resolve_vanity_url(
    vanity_url: str = Field(
        description="변환할 Steam 커스텀 URL 또는 vanity ID입니다. steamcommunity.com/id/xxx에서 xxx 부분입니다."
    )
) -> dict[str, Any]:
    """
    Steam 커스텀 URL(vanity URL)을 64-bit Steam ID로 변환합니다.

    반환 데이터: 변환된 64-bit Steam ID(steamid)와 성공 여부(success)를 포함합니다.

    중요: 대부분의 다른 도구들은 64-bit Steam ID가 필요합니다.
    사용자가 커스텀 URL만 제공한 경우 먼저 이 도구로 변환해야 합니다.

    사용 예시: vanity_url="robinwalker" 또는 vanity_url="customusername"
    """
    from mcp_server_steam.steam_client import SteamAPIClient

    async with SteamAPIClient() as client:
        params = {"vanityurl": vanity_url}
        result = await client.get("ISteamUser", "ResolveVanityURL", version="v0001", params=params)

        response = result.get("response", {})
        if not response.get("success"):
            raise ValueError(f"Could not resolve vanity URL: {vanity_url}")

        return {"steamid": response["steamid"], "success": True}


# ============================================================================
# Resources
# ============================================================================

@mcp.resource("steam://config")
def get_config() -> str:
    """
    서버 설정과 API 정보를 제공합니다.

    AI가 서버의 기능, 제한사항, 문서 링크 등을 이해하는 데 사용합니다.
    """
    return json.dumps({
        "version": "1.0.0",
        "api_base": "https://api.steampowered.com",
        "features": [
            "user_profiles",
            "game_info",
            "achievements",
            "workshop",
            "reviews"
        ],
        "rate_limit": {
            "requests_per_minute": 100,
            "description": "Steam API는 분당 100회 호출로 제한됩니다."
        },
        "documentation": "https://steamapi.xpaw.me/"
    }, indent=2, ensure_ascii=False)


@mcp.resource("steam://supported-games")
def get_supported_games() -> str:
    """
    자주 조회되는 게임들의 App ID 매핑을 제공합니다.

    AI가 특정 게임의 App ID를 빠르게 찾는 데 사용합니다.
    """
    common_games = {
        "counter_strike_2": 730,
        "dota_2": 570,
        "team_fortress_2": 440,
        "portal_2": 620,
        "half_life_2": 220,
        "left_4_dead_2": 550,
        "skyrim": 72850,
        "gta_v": 271590,
        "elden_ring": 1245620,
        "baldurs_gate_3": 1086940
    }
    return json.dumps(common_games, indent=2, ensure_ascii=False)


# ============================================================================
# Main Entry Point
# ============================================================================

def main():
    """Main entry point for mcp-server-steam CLI."""
    mcp.run()


if __name__ == "__main__":
    main()
