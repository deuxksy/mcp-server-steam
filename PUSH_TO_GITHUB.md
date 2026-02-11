# GitHub 원격 저장소 설정 방법

## 1. GitHub Personal Access Token 생성

1. https://github.com/settings/tokens 접속
2. **'Generate new token (classic)'** 클릭 ⭐
3. Note 입력: `mcp-server-steam`
4. 필요한 권한 체크:
   - ✅ repo (전체 저장소 접근)
   - ✅ workflow (GitHub Actions)
5. **'Generate token'** 클릭
6. 생성된 토큰을 **반드시 복사**하세요! (다시 볼 수 없음)

```
복사할 토큰 예시:
ghp_abc123xyzdefghij456klmno...
```

⚠️ **중요**: 토큰을 안전하게 보관하세요!

---

## 2. Git 원격 저장소 추가

```bash
# 방법 1: HTTPS with token (권장)
git remote add origin https://YOUR_USERNAME:GITHUB_TOKEN@github.com/crong/mcp-server-steam.git

# 방법 2: SSH (SSH key 설정 필요)
git remote add origin git@github.com:crong/mcp-server-steam.git
```

**본인 정보를 YOUR_USERNAME과 GITHUB_TOKEN으로 교체하세요**

---

## 3. 브랜치 설정

```bash
# 메인 브랜치를 main으로 설정 (기본값)
git branch -M main

# 현재 브랜치 확인
git branch
```

---

## 4. 첫 푸시

```bash
# 원격 저장소와 브랜치 연결
git push -u origin main

# -u: upstream 설정을 설정하며, 원격 저장소 정보를 업데이트
# main: 푸시할 브랜치
```

---

## 5. .gitignore에 토큰 추가

```bash
# .gitignore 파일에 추가
echo '.gitignore' >> .gitignore
echo 'GITHUB_TOKEN' >> .gitignore
```

---

## 🚀 전체 커맨드

```bash
# 전체 과정 한 번에
git remote add origin https://YOUR_USERNAME:GITHUB_TOKEN@github.com/crong/mcp-server-steam.git
git branch -M main
git push -u origin main
```

---

## ✅ 완료 후

```bash
# 푸시 완료 확인
git remote -v

# GitHub에서 저장소 확인
# https://github.com/crong/mcp-server-steam
```
