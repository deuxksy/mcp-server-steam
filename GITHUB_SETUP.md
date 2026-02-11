# GitHub 설정 방법

## 1. GitHub Personal Access Token 생성
1. https://github.com/settings/tokens 접속
2. 'Generate new token (classic)' 클릭
3. Note: 'mcp-server-steam' 입력
4. 'Generate token' 클릭
5. 생성된 토큰 복사 (권한: repo, workflow)
6. 이 토큰 안전하게 보관\!

## 2. Git 저장소 추가
```bash
git remote add origin https://YOUR_USERNAME:${GITHUB_TOKEN}@github.com/crong/mcp-server-steam.git
git branch -M main
git push -u origin main
```

## 3. .gitignore에 토큰 추가
```bash
echo '.gitignore' >> .gitignore
echo 'GITHUB_TOKEN' >> .gitignore
```

