"""Community features tools for mcp-server-steam."""

from typing import Any

from pydantic import Field


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
) -> list[dict[str, Any]]:
    """Get Steam Workshop items for a game.

    Args:
        app_id: Steam App ID of the game
        query_type: Type of query (1=RankedByVote, 2=RankedByPublicationDate, etc.)
        page: Page number for pagination
        count: Number of items per page

    Returns:
        List of workshop items with publishedfileid, title, creator, subscriptions, etc.
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


async def get_workshop_item_details(
    published_file_ids: list[int] | list[str] = Field(
        description="List of published file IDs (workshop item IDs)"
    )
) -> list[dict[str, Any]]:
    """Get detailed information about workshop items.

    Args:
        published_file_ids: List of workshop item IDs

    Returns:
        List of detailed workshop item information
    """
    from mcp_server_steam.steam_client import SteamAPIClient

    async with SteamAPIClient() as client:
        params = {
            "publishedfileids": ",".join(map(str, published_file_ids))
        }
        result = await client.get("IPublishedFileService", "GetDetails", version="v0001", params=params)

        files = result.get("response", {}).get("publishedfiledetails", [])
        return files


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
) -> list[dict[str, Any]]:
    """Get user reviews for a game.

    Args:
        app_id: Steam App ID of the game
        review_type: Type of reviews to return
        count: Number of reviews to return

    Returns:
        List of user reviews with author, content, rating, playtime, etc.
    """
    # Use store review API
    url = f"https://store.steampowered.com/appreviews/{app_id}"

    import httpx
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


async def get_player_bans(
    steam_ids: list[str] = Field(description="List of 64-bit Steam IDs")
) -> list[dict[str, Any]]:
    """Get VAC and game ban status for players.

    Args:
        steam_ids: List of 64-bit Steam IDs

    Returns:
        List of ban information including VAC bans, game bans, days since last ban
    """
    from mcp_server_steam.steam_client import SteamAPIClient

    async with SteamAPIClient() as client:
        params = {
            "steamids": ",".join(steam_ids)
        }
        result = await client.get("ISteamUser", "GetPlayerBans", version="v0001", params=params)

        players = result.get("response", {}).get("players", [])
        return players
