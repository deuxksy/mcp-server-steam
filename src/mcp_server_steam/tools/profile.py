"""User profile and statistics tools for mcp-server-steam."""

from typing import Any

from pydantic import Field


# Tool functions will be registered in server.py
# Each function is a standalone async function that will be decorated with @mcp.tool


async def get_user_profile(
    steam_id: str = Field(description="64-bit Steam ID of the user (e.g., 76561198000000000)")
) -> dict[str, Any]:
    """Get Steam user profile by Steam ID.

    Args:
        steam_id: Valid 64-bit Steam ID

    Returns:
        User profile dictionary with persona, avatar URLs, account state, etc.
    """
    from mcp_server_steam.steam_client import SteamAPIClient

    async with SteamAPIClient() as client:
        params = {"steamids": steam_id}
        result = await client.get("ISteamUser", "GetPlayerSummaries", params=params)

        if not result.get("response", {}).get("players"):
            raise ValueError(f"No profile found for Steam ID: {steam_id}")

        return result["response"]["players"][0]


async def get_friends_list(
    steam_id: str = Field(description="64-bit Steam ID of the user"),
    relationship: str = Field(
        default="all",
        description="Filter by relationship type: 'all', 'friend'"
    )
) -> list[dict[str, Any]]:
    """Get Steam user's friend list.

    Args:
        steam_id: Valid 64-bit Steam ID
        relationship: Filter friends by relationship type

    Returns:
        List of friends with Steam ID, relationship, and friend_since timestamp
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
) -> list[dict[str, Any]]:
    """Get all games owned by a Steam user.

    Args:
        steam_id: Valid 64-bit Steam ID
        include_app_info: Include game names and metadata
        include_played_free_games: Include free games that have been played

    Returns:
        List of owned games with appid, playtime_forever, last_played, etc.
    """
    from mcp_server_steam.steam_client import SteamAPIClient

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


async def get_recently_played_games(
    steam_id: str = Field(description="64-bit Steam ID of the user"),
    count: int = Field(
        default=10,
        description="Number of recent games to return (max 50)"
    )
) -> list[dict[str, Any]]:
    """Get recently played games for a Steam user.

    Args:
        steam_id: Valid 64-bit Steam ID
        count: Number of recent games to return

    Returns:
        List of recently played games with appid, name, playtime_2weeks, playtime_forever
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


async def get_steam_level(
    steam_id: str = Field(description="64-bit Steam ID of the user")
) -> dict[str, Any]:
    """Get Steam level for a user.

    Args:
        steam_id: Valid 64-bit Steam ID

    Returns:
        Dictionary with player_level field
    """
    from mcp_server_steam.steam_client import SteamAPIClient

    async with SteamAPIClient() as client:
        params = {"steamid": steam_id}
        result = await client.get("IPlayerService", "GetSteamLevel", params=params)

        return result.get("response", {})


async def get_player_achievements(
    steam_id: str = Field(description="64-bit Steam ID of the user"),
    app_id: int = Field(description="Steam App ID of the game"),
    language: str = Field(
        default="english",
        description="Language for achievement names (e.g., 'english', 'spanish')"
    )
) -> list[dict[str, Any]]:
    """Get achievement progress for a specific game.

    Args:
        steam_id: Valid 64-bit Steam ID
        app_id: Steam App ID of the game
        language: Language for achievement text

    Returns:
        List of achievements with achieved status, unlock time, name, description
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
