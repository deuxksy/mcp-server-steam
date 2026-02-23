# PyPI Packaging Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** mcp-server-steam 프로젝트를 PyPI에 배포 가능한 표준 Python 패키지로 변환

**Architecture:** 표준 src/ 레이아웃을 사용하여 패키지 구조 재구성하고, GitHub Actions를 통해 자동으로 PyPI에 배포합니다. hatchling을 빌드 백엔드로 사용합니다.

**Tech Stack:** Python 3.10+, hatchling, GitHub Actions, PyPI, TestPyPI

---

## Task 1: src/ 디렉토리 구조 생성

**Files:**
- Create: `src/mcp_server_steam/__init__.py`
- Create: `src/mcp_server_steam/__main__.py`
- Create: `src/mcp_server_steam/tools/` (directory)

**Step 1: src/ 디렉토리 생성**

```bash
mkdir -p src/mcp_server_steam/tools
```

Expected output: (no output, directory created)

**Step 2: 디렉토리 구조 확인**

```bash
ls -la src/mcp_server_steam/
```

Expected output:
```
drwxr-xr-x tools/
```

**Step 3: 커밋**

```bash
git add src/
git commit -m "chore: create src/mcp_server_steam directory structure"
```

---

## Task 2: __init__.py 생성

**Files:**
- Create: `src/mcp_server_steam/__init__.py`

**Step 1: __init__.py 파일 생성**

```python
"""mcp-server-steam - MCP Server for Steam Web API."""

__version__ = "1.0.0"

# Import will be added after server.py is moved
# from mcp_server_steam.server import main

__all__ = ["__version__"]
```

파일 생성: `src/mcp_server_steam/__init__.py`

**Step 2: 파일 확인**

```bash
cat src/mcp_server_steam/__init__.py
```

Expected output: 파일 내용이 표시됨

**Step 3: 커밋**

```bash
git add src/mcp_server_steam/__init__.py
git commit -m "feat: add package __init__.py with version info"
```

---

## Task 3: __main__.py 생성

**Files:**
- Create: `src/mcp_server_steam/__main__.py`

**Step 1: __main__.py 파일 생성**

```python
"""Entry point for python -m mcp_server_steam."""

from mcp_server_steam import main

if __name__ == "__main__":
    main()
```

파일 생성: `src/mcp_server_steam/__main__.py`

**Step 2: 파일 확인**

```bash
cat src/mcp_server_steam/__main__.py
```

Expected output: 파일 내용이 표시됨

**Step 3: 커밋**

```bash
git add src/mcp_server_steam/__main__.py
git commit -m "feat: add __main__.py for python -m execution"
```

---

## Task 4: server.py를 src/로 이동 및 import 수정

**Files:**
- Move: `server.py` → `src/mcp_server_steam/server.py`
- Modify: `src/mcp_server_steam/server.py`

**Step 1: server.py 이동**

```bash
mv server.py src/mcp_server_steam/server.py
```

**Step 2: 이동 확인**

```bash
ls -la src/mcp_server_steam/server.py
```

Expected output: 파일이 존재함

**Step 3: import 경로 수정**

`src/mcp_server_steam/server.py` 파일의 25번째 줄 수정:

변경 전:
```python
from config import settings
```

변경 후:
```python
from mcp_server_steam.config import settings
```

**Step 4: main() 함수 확인 및 export 추가

파일 끝부분에 main() 함수가 있는지 확인하고, __init__.py에서 import할 수 있도록 합니다.

```bash
grep -n "^def main" src/mcp_server_steam/server.py
```

Expected output: `^def main` 함수의 라인 번호

**Step 5: __init__.py 업데이트**

`src/mcp_server_steam/__init__.py` 파일 수정:

```python
"""mcp-server-steam - MCP Server for Steam Web API."""

__version__ = "1.0.0"

from mcp_server_steam.server import main

__all__ = ["main", "__version__"]
```

**Step 6: 커밋**

```bash
git add src/mcp_server_steam/server.py src/mcp_server_steam/__init__.py
git commit -m "refactor: move server.py to src/ and update imports"
```

---

## Task 5: config.py를 src/로 이동

**Files:**
- Move: `config.py` → `src/mcp_server_steam/config.py`
- Modify: `src/mcp_server_steam/steam_client.py` (이후 작업에서 import 수정)

**Step 1: config.py 이동**

```bash
mv config.py src/mcp_server_steam/config.py
```

**Step 2: 이동 확인**

```bash
ls -la src/mcp_server_steam/config.py
```

Expected output: 파일이 존재함

**Step 3: 커밋**

```bash
git add src/mcp_server_steam/config.py
git commit -m "refactor: move config.py to src/"
```

---

## Task 6: steam_client.py를 src/로 이동 및 import 수정

**Files:**
- Move: `steam_client.py` → `src/mcp_server_steam/steam_client.py`
- Modify: `src/mcp_server_steam/steam_client.py`
- Modify: `src/mcp_server_steam/tools/profile.py`
- Modify: `src/mcp_server_steam/tools/games.py`
- Modify: `src/mcp_server_steam/tools/community.py`

**Step 1: steam_client.py 이동**

```bash
mv steam_client.py src/mcp_server_steam/steam_client.py
```

**Step 2: 이동 확인**

```bash
ls -la src/mcp_server_steam/steam_client.py
```

Expected output: 파일이 존재함

**Step 3: steam_client.py에서 config import 수정**

`src/mcp_server_steam/steam_client.py`의 10번째 줄 수정:

변경 전:
```python
from config import settings
```

변경 후:
```python
from mcp_server_steam.config import settings
```

**Step 4: tools/profile.py에서 steam_client import 수정**

`src/mcp_server_steam/tools/profile.py`의 23번째 줄 근처 수정:

변경 전:
```python
    from steam_client import SteamAPIClient
```

변경 후:
```python
    from mcp_server_steam.steam_client import SteamAPIClient
```

**Step 5: tools/games.py에서 steam_client import 수정**

```bash
grep -n "from steam_client import" src/mcp_server_steam/tools/games.py
```

만약 import가 있다면:
```python
from mcp_server_steam.steam_client import SteamAPIClient
```

**Step 6: tools/community.py에서 steam_client import 수정**

```bash
grep -n "from steam_client import" src/mcp_server_steam/tools/community.py
```

만약 import가 있다면:
```python
from mcp_server_steam.steam_client import SteamAPIClient
```

**Step 7: 커밋**

```bash
git add src/mcp_server_steam/steam_client.py src/mcp_server_steam/tools/
git commit -m "refactor: move steam_client.py to src/ and update all imports"
```

---

## Task 7: tools/ 디렉토리를 src/로 이동

**Files:**
- Move: `tools/` → `src/mcp_server_steam/tools/`

**Step 1: tools/ 내용 이동 (이미 이동됨)**

이미 Task 6에서 tools/*.py 파일들의 import를 수정했으므로, tools/ 디렉토리 전체를 이동합니다.

```bash
# 기존 tools/ 디렉토리 확인
ls -la tools/
```

**Step 2: 새로운 tools/ 위치 확인**

```bash
ls -la src/mcp_server_steam/tools/
```

Expected output:
```
__init__.py
community.py
games.py
profile.py
```

**Step 3: 기존 tools/ 디렉토리 삭제**

```bash
rm -rf tools/
```

**Step 4: 커밋**

```bash
git add tools/ src/mcp_server_steam/tools/
git commit -m "refactor: move tools/ directory to src/mcp_server_steam/"
```

---

## Task 8: pyproject.toml 업데이트

**Files:**
- Modify: `pyproject.toml`

**Step 1: pyproject.toml 백업**

```bash
cp pyproject.toml pyproject.toml.bak
```

**Step 2: pyproject.toml 전체 내용 교체**

다음 내용으로 `pyproject.toml` 파일을 완전히 교체:

```toml
[project]
name = "mcp-server-steam"
version = "1.0.0"
description = "MCP Server for Steam Web API integration"
readme = "README.md"
requires-python = ">=3.10"
license = {text = "MIT"}
authors = [
    {name = "Crong", email = "deuxksy@gmail.com"}
]
maintainers = [
    {name = "Crong", email = "deuxksy@gmail.com"}
]
keywords = ["mcp", "steam", "steam-api", "model-context-protocol"]
classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Topic :: Software Development :: Libraries :: Python Modules",
]
dependencies = [
    "fastmcp==3.0.0b2",
    "httpx>=0.27.0",
    "python-dotenv>=1.0.0",
    "pydantic>=2.0.0",
    "pydantic-settings>=2.0.0",
]

[project.urls]
Homepage = "https://github.com/deuxksy/mcp-server-steam"
Repository = "https://github.com/deuxksy/mcp-server-steam"
Issues = "https://github.com/deuxksy/mcp-server-steam/issues"

[project.scripts]
mcp-server-steam = "mcp_server_steam:main"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src/mcp_server_steam"]

[tool.hatch.build.targets.sdist]
include = [
    "/src",
    "/tests",
    "/README.md",
    "/LICENSE",
]

[dependency-groups]
dev = []
```

**Step 3: 파일 확인**

```bash
cat pyproject.toml
```

Expected output: 업데이트된 내용이 표시됨

**Step 4: 백업 삭제**

```bash
rm pyproject.toml.bak
```

**Step 5: 커밋**

```bash
git add pyproject.toml
git commit -m "chore: update pyproject.toml for PyPI packaging"
```

---

## Task 9: MANIFEST.in 생성

**Files:**
- Create: `MANIFEST.in`

**Step 1: MANIFEST.in 파일 생성**

```
include README.md
include LICENSE
include pyproject.toml
recursive-include src/mcp_server_steam *.py
```

파일 생성: `MANIFEST.in`

**Step 2: 파일 확인**

```bash
cat MANIFEST.in
```

Expected output: 파일 내용이 표시됨

**Step 3: 커밋**

```bash
git add MANIFEST.in
git commit -m "chore: add MANIFEST.in for package distribution"
```

---

## Task 10: GitHub Actions 워크플로우 생성

**Files:**
- Create: `.github/workflows/publish.yml`

**Step 1: .github/workflows/ 디렉토리 생성**

```bash
mkdir -p .github/workflows
```

**Step 2: publish.yml 파일 생성**

```yaml
name: Publish to PyPI

on:
  push:
    tags:
      - 'v*'

permissions:
  contents: read

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install uv
        run: curl -LsSf https://astral.sh/uv/install.sh | sh

      - name: Build package
        run: uvx --from hatchling hatch build

      - name: Publish to TestPyPI
        if: contains(github.ref, '-test')
        env:
          TESTPYPI_API_TOKEN: ${{ secrets.TESTPYPI_API_TOKEN }}
        run: |
          uvx twine upload --repository testpypi dist/*
          echo "Published to TestPyPI: https://test.pypi.org/project/mcp-server-steam/"

      - name: Publish to PyPI
        if: (!contains(github.ref, '-test'))
        env:
          PYPI_API_TOKEN: ${{ secrets.PYPI_API_TOKEN }}
        run: |
          uvx twine upload dist/*
          echo "Published to PyPI: https://pypi.org/project/mcp-server-steam/"
```

파일 생성: `.github/workflows/publish.yml`

**Step 3: 파일 확인**

```bash
cat .github/workflows/publish.yml
```

Expected output: 파일 내용이 표시됨

**Step 4: 커밋**

```bash
git add .github/workflows/publish.yml
git commit -m "ci: add GitHub Actions workflow for PyPI publishing"
```

---

## Task 11: 로컬 빌드 테스트

**Files:**
- None (local build test)

**Step 1: 패키지 빌드**

```bash
uvx --from hatchling hatch build
```

Expected output:
```
...
dist/mcp_server_steam-1.0.0-py3-none-any.whl
dist/mcp-server_steam-1.0.0.tar.gz
```

**Step 2: 빌드 결과 확인**

```bash
ls -lh dist/
```

Expected output: wheel과 tar.gz 파일이 있음

**Step 3: wheel 내용물 확인 (선택사항)**

```bash
uvx --from zipfile unzip -l dist/mcp_server_steam-1.0.0-py3-none-any.whl | head -30
```

Expected output: 패키지 내용물이 표시됨

---

## Task 12: 로컬 설치 테스트

**Files:**
- None (local install test)

**Step 1: 가상 환경 생성**

```bash
python -m venv test_env
source test_env/bin/activate  # Windows: test_env\Scripts\activate
```

**Step 2: 패키지 설치**

```bash
pip install dist/mcp_server_steam-1.0.0-py3-none-any.whl
```

Expected output:
```
Successfully installed mcp-server-steam-1.0.0
```

**Step 3: import 테스트**

```bash
python -c "from mcp_server_steam import main; print('Import successful')"
```

Expected output:
```
Import successful
```

**Step 4: CLI 명령어 테스트**

```bash
mcp-server-steam --help 2>&1 | head -5
```

Expected output: MCP 서버가 시작되거나 도움말이 표시됨 (API 키 없으므로 에러 가능)

**Step 5: 가상 환경 정리**

```bash
deactivate
rm -rf test_env
```

---

## Task 13: dist/ 정리 및 최종 커밋

**Files:**
- Delete: `dist/` (build artifacts)

**Step 1: dist/ 디렉토리 추가**

```bash
echo "dist/" >> .gitignore
```

**Step 2: .gitignore 확인**

```bash
tail -5 .gitignore
```

Expected output: `dist/`가 포함됨

**Step 3: 커밋**

```bash
git add .gitignore
git commit -m "chore: add dist/ to gitignore"
```

---

## Task 14: README.md 업데이트 (PyPI 섹션 추가)

**Files:**
- Modify: `README.md`

**Step 1: README.md에 PyPI 설치 섹션 추가**

README.md 파일의 설치 방법 섹션 앞에 다음 내용 추가:

```markdown
## PyPI에서 설치

PyPI에 게시된 후 다음과 같이 설치할 수 있습니다:

\`\`\`bash
pip install mcp-server-steam
\`\`\`

설치 후 다음과 같이 실행합니다:

\`\`\`bash
mcp-server-steam
\`\`\`

## 소스에서 설치

또는 소스 코드에서 직접 설치합니다:
```

그리고 기존 "## 설치 방법"을 "## 소스에서 설치"로 변경

**Step 2: README.md 확인**

```bash
head -50 README.md
```

Expected output: PyPI 섹션이 추가됨

**Step 3: 커밋**

```bash
git add README.md
git commit -m "docs: add PyPI installation instructions to README"
```

---

## Task 15: 변경사항 정리 및 최종 푸시

**Files:**
- None (final push)

**Step 1: Git 상태 확인**

```bash
git status
```

Expected output: working tree clean 또는 변경사항 없음

**Step 2: 변경사항 확인**

```bash
git log --oneline -10
```

Expected output: 최근 커밋들이 표시됨

**Step 3: 원격에 푸시**

```bash
git push origin main
```

Expected output: 푸시 성공 메시지

---

## 검증 단계

### TestPyPI 배포 테스트

**Step 1: TestPyPI API 토큰 생성**

1. https://test.pypi.org/account/register/ 에서 계정 생성
2. https://test.pypi.org/manage/account/token/ 에서 API 토큰 생성
3. GitHub Settings → Secrets and variables → Actions → New repository secret
4. Name: `TESTPYPI_API_TOKEN`, Value: 생성한 토큰

**Step 2: TestPyPI 테스트 태그 생성 및 푸시**

```bash
git tag v1.0.0-test
git push origin v1.0.0-test
```

**Step 3: GitHub Actions 워크플로우 확인**

https://github.com/deuxksy/mcp-server-steam/actions 에서 워크플로우 실행 확인

**Step 4: TestPyPI에서 설치 테스트**

```bash
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ mcp-server-steam
mcp-server-steam --help
```

### PyPI 공식 배포

**Step 1: PyPI API 토큰 생성**

1. https://pypi.org/account/register/ 에서 계정 생성 (또는 로그인)
2. https://pypi.org/manage/account/token/ 에서 API 토큰 생성
3. GitHub Settings → Secrets and variables → Actions → New repository secret
4. Name: `PYPI_API_TOKEN`, Value: 생성한 토큰

**Step 2: 공식 태그 생성 및 푸시**

```bash
git tag v1.0.1
git push origin v1.0.1
```

**Step 3: PyPI에서 패키지 확인**

https://pypi.org/project/mcp-server-steam/ 방문

**Step 4: PyPI에서 설치 테스트**

```bash
pip install mcp-server-steam
mcp-server-steam --help
```

---

## 완료 기준

✅ src/mcp_server_steam/ 구조로 패키지 재구성
✅ pyproject.toml이 PyPI 요구사항 충족
✅ MANIFEST.in 추가
✅ GitHub Actions 워크플로우 추가
✅ 로컬 빌드 성공
✅ 로컬 설치 및 import 테스트 성공
✅ TestPyPI 배포 성공
✅ PyPI 공식 배포 성공
✅ `pip install mcp-server-steam`로 설치 가능
✅ `mcp-server-steam` CLI 명령어 작동
