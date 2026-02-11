"""Game information and store tools for mcp-server-steam."""

from typing import Any

from pydantic import Field


async def get_game_details(
    app_ids: list[int] = Field(description="List of Steam App IDs to query"),
    language: str = Field(
        default="english",
        description="Language for game details"
    ),
    filters: str = Field(
        default="basic",
        description="Detail level: 'basic', 'details', 'all'"
    )
) -> list[dict[str, Any]]:
    """Get game details from Steam store.

    Args:
        app_ids: List of Steam App IDs
        language: Language for results
        filters: Detail level for response

    Returns:
        List of game details including name, developers, publishers, price, genres, etc.
    """
    from steam_client import SteamAPIClient

    async with SteamAPIClient() as client:
        # For game details, use store.steampowered.com API
        url = f"https://store.steampowered.com/api/appdetails?appids={','.join(map(str, app_ids))}&l={language}"

        if filters == "all":
            url += "&filters=price_overview,media,genres,screenshots,movies,recommendations,released"

        async with client._client:
            response = await client._client.get(url)
            response.raise_for_status()
            result = response.json()

        # Parse response which uses app IDs as keys
        games = []
        for app_id, app_data in result.items():
            if app_data.get("success"):
                games.append(app_data["data"])

        return games


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
) -> list[dict[str, Any]]:
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


async def get_global_achievement_percentages(
    app_id: int = Field(description="Steam App ID of the game")
) -> list[dict[str, Any]]:
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


async def search_games(
    query: str = Field(description="Search query for games"),
    count: int = Field(
        default=25,
        description="Number of results to return (max 50)"
    )
) -> list[dict[str, Any]]:
    """Search for games on Steam.

    Args:
        query: Search query string
        count: Number of results to return

    Returns:
        List of matching games with app_id, name, release_date, price
    """
    from steam_client import SteamAPIClient

    async with SteamAPIClient() as client:
        # Use store search API
        url = f"https://store.steampowered.com/api/storesearch/?term={query}&l=english&cc=US"

        async with client._client:
            response = await client._client.get(url)
            response.raise_for_status()
            result = response.json()

        items = result.get("items", [])[:count]
        return items


async def get_game_schema(
    app_id: int = Field(description="Steam App ID of the game"),
    language: str = Field(
        default="english",
        description="Language for achievement names and descriptions"
    )
) -> dict[str, Any]:
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
