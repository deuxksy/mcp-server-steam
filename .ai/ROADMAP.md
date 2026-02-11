# mcp-server-steam 로드맵

## 버전
- **v1.0.0** (2026-02-11) - 초기 릴리스
  - FastMCP 3.0 beta2 기반 MCP 서버
  - Steam Web API 통합 (16개 도구)
  - AI 최적화 완성

---

## v1.0.0 (현재) - 완료된 기능

### ✅ 구현 완료

#### MCP 서버 코어
- [x] FastMCP 3.0 beta2 기반 서버 구조
- [x] Steam Web API 클라이언트 (httpx, async)
- [x] Rate Limiting (100회/분)
- [x] 에러 처리 및 재시도 로직
- [x] 환경 변수 관리 (pydantic-settings)

#### 프로필 도구 (6개)
- [x] get_user_profile - Steam 사용자 프로필
- [x] get_friends_list - 친구 목록
- [x] get_owned_games - 소유 게임
- [x] get_recently_played_games - 최근 플레이
- [x] get_steam_level - Steam 레벨
- [x] get_player_achievements - 업적 진행상황

#### 게임 도구 (5개)
- [x] get_game_details - 게임 상세 정보
- [x] get_game_news - 게임 뉴스
- [x] get_global_achievement_percentages - 전역 업적 통계
- [x] search_games - 게임 검색
- [x] get_game_schema - 게임 스키마

#### 커뮤니티 도구 (4개)
- [x] get_workshop_items - 워크샵 아이템
- [x] get_workshop_item_details - 워크샵 상세
- [x] get_user_reviews - 사용자 리뷰
- [x] get_player_bans - 밴 상태

#### 유틸리티 도구 (1개)
- [x] resolve_vanity_url - vanity URL → Steam ID 변환

#### 리소스 (2개)
- [x] steam://config - 서버 설정
- [x] steam://supported-games - 일반적인 게임 App ID

---

## 🔜 향후 계획 (v1.1.0+)

### v1.1.0 - 안정화 및 버그 수정
- [ ] Steam API 응답 캐싱 추가
- [ ] 에러 메시지 한글화 개선
- [ ] 요청 간 병렬화
- [ ] 테스트 코드 추가

### v1.2.0 - 기능 확장
- [ ] Steam Friends 요청 최적화 (pagination)
- [ ] 게임 스크린샷 기능
- [ ] 사용자 게임 통계 대시보드
- [ ] 위클리팩(Workshop) 구독 관리

### v1.3.0 - 고급 기능
- [ ] 실시간 게임 뉴스 알림
- [ ] 사용자별 커스텀 프롬프트 지원
- [ ] 멀티플레이어 게임 라이브러리 비교
- [ ] 업적 달성 추천 시스템

### v2.0.0 - 주요 변경사항
- [ ] FastMCP 4.0 stable으로 업그레이드
- [ ] GraphQL 지원 (Steam에서 제공 시)
- [ ] WebSocket을 통한 실시간 이벤트

---

## 📊 개발 우선순위

1. **안정화**: 현재 구현의 버그 수정, 테스트
2. **기능 확장**: 사용자 요구 기능 추가
3. **성능 최적화**: 캐싱, 요청 최적화
4. **문서화**: README, API 문서 보완

---

## 🐛 알려진 이슈

### v1.0.0
- Steam Store API 호출 시 URL 오타 (steampowered) 수정 필요
- 일부 게임 검색 결과가 부정확할 수 있음

### 해결책
- URL 오타 수정 완료
- 응답 데이터 검증 로직 추가
