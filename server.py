#!/usr/bin/env python3
"""
mcp-server-steam - MCP Server for Steam Web API

A comprehensive Model Context Protocol server that provides access to
Steam user profiles, game information, achievements, and community features.

Requirements:
    - Steam Web API key from https://steamcommunity.com/dev/apikey
    - Set STEAM_API_KEY environment variable

Usage:
    uv run python server.py
"""

import json
import logging
from contextlib import asynccontextmanager

from fastmcp import FastMCP
from pydantic import Field

from config import settings

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app):
    """Lifespan context manager for startup/shutdown."""
    logger.info("Starting mcp-server-steam...")

    # Validate API key on startup
    if not settings.steam_api_key or settings.steam_api_key == "your_steam_api_key_here":
        raise ValueError(
            "Invalid STEAM_API_KEY. Get your API key from "
            "https://steamcommunity.com/dev/apikey and set it in .env file"
        )

    logger.info("Steam API key validated successfully")

    yield

    logger.info("Shutting down mcp-server-steam...")


# Create main server instance
mcp = FastMCP(
    name="steam-mcp-server",
    instructions="""
    Comprehensive MCP server for Steam Web API integration.

    Provides access to:
    - User profiles and stats
    - Game information and store data
    - Achievements and playtime
    - Workshop items
    - Community features

    All tools require valid Steam IDs or App IDs.
    """,
    lifespan=lifespan,
)


# ============================================================================
# Profile Tools
# ============================================================================

@mcp.tool()
async def get_user_profile(
    steam_id: str = Field(description="64-bit Steam ID of the user (e.g., 76561198000000000)")
) -> dict[str, any]:
    """Get Steam user profile by Steam ID.

    Args:
        steam_id: Valid 64-bit Steam ID

    Returns:
        User profile dictionary with persona, avatar URLs, account state, etc.
    """
    from steam_client import SteamAPIClient

    async with SteamAPIClient() as client:
        params = {"steamids": steam_id}
        result = await client.get("ISteamUser", "GetPlayerSummaries", params=params)

        if not result.get("response", {}).get("players"):
            raise ValueError(f"No profile found for Steam ID: {steam_id}")

        return result["response"]["players"][0]


@mcp.tool()
async def get_friends_list(
    steam_id: str = Field(description="64-bit Steam ID of the user"),
    relationship: str = Field(
        default="all",
        description="Filter by relationship type: 'all', 'friend'"
    )
) -> list[dict[str, any]]:
    """Get Steam user's friend list.

    Args:
        steam_id: Valid 64-bit Steam ID
        relationship: Filter friends by relationship type

    Returns:
        List of friends with Steam ID, relationship, and friend_since timestamp
    """
    from steam_client import SteamAPIClient

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
    steam_id: str = Field(description="64-bit Steam ID of the user"),
    include_app_info: bool = Field(
        default=True,
        description="Include game names and metadata"
    ),
    include_played_free_games: bool = Field(
        default=False,
        description="Include free games that have been played"
    )
) -> list[dict[str, any]]:
    """Get all games owned by a Steam user.

    Args:
        steam_id: Valid 64-bit Steam ID
        include_app_info: Include game names and metadata
        include_played_free_games: Include free games that have been played

    Returns:
        List of owned games with appid, playtime_forever, last_played, etc.
    """
    from steam_client import SteamAPIClient

    async with SteamAPIClient() as client:
        params = {
            "steamid": steam_id,
            "include_appinfo": str(include_app_info).lower(),
            "include_played_free_games": str(include_played_free_games).lower(),
            "format": "json"
        }
        result = await client.get("IPlayerService", "GetOwnedGames", version="v0001", params=params)

        games = result.get("response", {}).get("games", [])
        return games


@mcp.tool()
async def get_recently_played_games(
    steam_id: str = Field(description="64-bit Steam ID of the user"),
    count: int = Field(
        default=10,
        description="Number of recent games to return (max 50)"
    )
) -> list[dict[str, any]]:
    """Get recently played games for a Steam user.

    Args:
        steam_id: Valid 64-bit Steam ID
        count: Number of recent games to return

    Returns:
        List of recently played games with appid, name, playtime_2weeks, playtime_forever
    """
    from steam_client import SteamAPIClient

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
    steam_id: str = Field(description="64-bit Steam ID of the user")
) -> dict[str, any]:
    """Get Steam level for a user.

    Args:
        steam_id: Valid 64-bit Steam ID

    Returns:
        Dictionary with player_level field
    """
    from steam_client import SteamAPIClient

    async with SteamAPIClient() as client:
        params = {"steamid": steam_id}
        result = await client.get("IPlayerService", "GetSteamLevel", params=params)

        return result.get("response", {})


@mcp.tool()
async def get_player_achievements(
    steam_id: str = Field(description="64-bit Steam ID of the user"),
    app_id: int = Field(description="Steam App ID of the game"),
    language: str = Field(
        default="english",
        description="Language for achievement names (e.g., 'english', 'spanish')"
    )
) -> list[dict[str, any]]:
    """Get achievement progress for a specific game.

    Args:
        steam_id: Valid 64-bit Steam ID
        app_id: Steam App ID of the game
        language: Language for achievement text

    Returns:
        List of achievements with achieved status, unlock time, name, description
    """
    from steam_client import SteamAPIClient

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
    app_ids: list[int] = Field(description="List of Steam App IDs to query"),
    language: str = Field(
        default="english",
        description="Language for game details"
    )
) -> list[dict[str, any]]:
    """Get game details from Steam store.

    Args:
        app_ids: List of Steam App IDs
        language: Language for results

    Returns:
        List of game details including name, developers, publishers, price, genres, etc.
    """
    from steam_client import SteamAPIClient
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
    app_id: int = Field(description="Steam App ID of the game"),
    count: int = Field(
        default=5,
        description="Number of news items to return (max 20)"
    ),
    max_length: int = Field(
        default=300,
        description="Maximum length of each news item in characters"
    )
) -> list[dict[str, any]]:
    """Get news and updates for a specific game.

    Args:
        app_id: Steam App ID of the game
        count: Number of news items to return
        max_length: Maximum length of each news item

    Returns:
        List of news items with title, url, date, contents, feed_label
    """
    from steam_client import SteamAPIClient

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
    app_id: int = Field(description="Steam App ID of the game")
) -> list[dict[str, any]]:
    """Get global achievement percentages for a game.

    Args:
        app_id: Steam App ID of the game

    Returns:
        List of achievements with percentage of players who unlocked each
    """
    from steam_client import SteamAPIClient

    async with SteamAPIClient() as client:
        params = {"gameid": app_id, "l": "english"}
        result = await client.get("ISteamUserStats", "GetGlobalAchievementPercentagesForApp", version="v0002", params=params)

        achievements = result.get("achievementpercentages", {}).get("achievements", [])
        return achievements


@mcp.tool()
async def search_games(
    query: str = Field(description="Search query for games"),
    count: int = Field(
        default=25,
        description="Number of results to return (max 50)"
    )
) -> list[dict[str, any]]:
    """Search for games on Steam.

    Args:
        query: Search query string
        count: Number of results to return

    Returns:
        List of matching games with app_id, name, release_date, price
    """
    from steam_client import SteamAPIClient
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
    app_id: int = Field(description="Steam App ID of the game"),
    language: str = Field(
        default="english",
        description="Language for achievement names and descriptions"
    )
) -> dict[str, any]:
    """Get achievement and stats schema for a game.

    Args:
        app_id: Steam App ID of game
        language: Language for achievement text

    Returns:
        Game schema with achievements, stats, and available stats
    """
    from steam_client import SteamAPIClient

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
    app_id: int = Field(description="Steam App ID of the game"),
    query_type: int = Field(
        default=1,
        description="Query type: 1=RankedByVote, 2=RankedByPublicationDate, etc."
    ),
    page: int = Field(
        default=1,
        description="Page number for pagination"
    ),
    count: int = Field(
        default=30,
        description="Number of items per page (max 100)"
    )
) -> list[dict[str, any]]:
    """Get Steam Workshop items for a game.

    Args:
        app_id: Steam App ID of the game
        query_type: Type of query (1=RankedByVote, 2=RankedByPublicationDate, etc.)
        page: Page number for pagination
        count: Number of items per page

    Returns:
        List of workshop items with publishedfileid, title, creator, subscriptions, etc.
    """
    from steam_client import SteamAPIClient

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
        description="List of published file IDs (workshop item IDs)"
    )
) -> list[dict[str, any]]:
    """Get detailed information about workshop items.

    Args:
        published_file_ids: List of workshop item IDs

    Returns:
        List of detailed workshop item information
    """
    from steam_client import SteamAPIClient

    async with SteamAPIClient() as client:
        params = {
            "publishedfileids": ",".join(map(str, published_file_ids))
        }
        result = await client.get("IPublishedFileService", "GetDetails", version="v0001", params=params)

        files = result.get("response", {}).get("publishedfiledetails", [])
        return files


@mcp.tool()
async def get_user_reviews(
    app_id: int = Field(description="Steam App ID of the game"),
    review_type: str = Field(
        default="all",
        description="Review type filter: 'all', 'positive', 'negative'"
    ),
    count: int = Field(
        default=10,
        description="Number of reviews to return (max 100)"
    )
) -> list[dict[str, any]]:
    """Get user reviews for a game.

    Args:
        app_id: Steam App ID of the game
        review_type: Type of reviews to return
        count: Number of reviews to return

    Returns:
        List of user reviews with author, content, rating, playtime, etc.
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
    steam_ids: list[str] = Field(description="List of 64-bit Steam IDs")
) -> list[dict[str, any]]:
    """Get VAC and game ban status for players.

    Args:
        steam_ids: List of 64-bit Steam IDs

    Returns:
        List of ban information including VAC bans, game bans, days since last ban
    """
    from steam_client import SteamAPIClient

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
    vanity_url: str = Field(description="Steam custom URL or vanity ID (e.g., 'username' from steamcommunity.com/id/username)")
) -> dict[str, any]:
    """Resolve Steam vanity URL to 64-bit Steam ID.

    Args:
        vanity_url: Custom profile ID or vanity URL

    Returns:
        Dictionary with steamid (64-bit ID) and success status
    """
    from steam_client import SteamAPIClient

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
    """Provides server configuration and API information."""
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
            "requests_per_minute": 100
        },
        "documentation": "https://steamapi.xpaw.me/"
    }, indent=2)


@mcp.resource("steam://supported-games")
def get_supported_games() -> str:
    """Provides a list of commonly queried game App IDs."""
    common_games = {
        "counter_strike_2": 730,
        "dota_2": 570,
        "team_fortress_2": 440,
        "portal_2": 620,
        "half_life_2": 220,
        "left_4_dead_2": 550,
        "skyrim": 72850,
        "gta_v": 271590
    }
    return json.dumps(common_games, indent=2)


# ============================================================================
# Main Entry Point
# ============================================================================

if __name__ == "__main__":
    mcp.run()
