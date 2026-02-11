# mcp-server-steam 프로젝트 컨텍스트

## 프로젝트 개요
FastMCP 3.0 beta2를 사용하여 Steam Web API와 통합하는 MCP 서버

## 주요 엔티티

### SteamAPIClient
- Async HTTP 클라이언트 (httpx)
- Rate limiting: 100회/분
- 에러 처리 및 재시도 로직
- 세션 관리 (async context manager)

### MCP Tools (16개)
- 프로필 도구: 6개
- 게임 도구: 5개
- 커뮤니티 도구: 4개
- 유틸리티: 1개

## 비즈니스 로직

### Steam ID 변환
1. 사용자가 vanity URL 제공 (steamcommunity.com/id/username)
2. resolve_vanity_url로 64-bit Steam ID 변환
3. 변환된 Steam ID로 다른 도구 호출

### Rate Limiting
- Token bucket 알고리즘
- 100 requests/minute
- 자동으로 대기 및 재시도

### 에러 처리
- SteamAPIError: 베이스 에러
- SteamRateLimitError: Rate limit 초과
- SteamAuthError: API 키 인증 실패
- SteamNotFoundError: 리소스를 찾을 수 없음

## 데이터 구조

### 사용자 프로필
```json
{
  "steamid": "76561198000000000",
  "personaname": "사용자명",
  "avatarfull": "아바타 URL",
  "personastate": 0,
  "loccountrycode": "KR"
}
```

### 게임 라이브러리
```json
[
  {
    "appid": 730,
    "name": "Counter-Strike 2",
    "playtime_forever": 12345,
    "playtime_2weeks": 600
  }
]
```
- playtime_forever: 총 플레이시간 (분 단위)
- playtime_2weeks: 최근 2주간 플레이시간 (분 단위)

## API 제약사항

### Steam Web API
- 도메인: api.steampowered.com
- 인증: API 키 필요
- Rate limit: 100회/분

### HTTP 엔드포인트
- Store API: store.steampowered.com
- News API: api.steampowered.com
- Reviews: store.steampowered.com/appreviews/{appid}
