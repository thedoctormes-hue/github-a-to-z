#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GITHUBREPO: Intelligent Repository Quality Auditor & Benchmarking Engine
Official CLI companion and quality standard for «GitHub from A to Z» (TheNovaNodes)
Repository: https://github.com/thedoctormes-hue/github-a-to-z

Evaluates any GitHub repository against the 5 Maturity Dimensions of github-a-to-z:
  1. Presentation & Community Standards (L1)
  2. Git Flow & Root Hygiene (L2)
  3. CI/CD Pipeline Resilience (L3)
  4. DevSecOps Citadel (L4)
  5. AI-Ready 2026 Orchestration (L5)

Outputs a comprehensive Mobile-First Markdown Report with Scorecard (0-100),
Defects list (P0/P1/P2), Actionable Drop-in Remediations, and canonical links to course modules.
"""

import sys
import os
import re
import json
import subprocess
import argparse
import base64
from typing import Dict, Any, List, Optional, Tuple

COURSE_URL = "https://github.com/thedoctormes-hue/github-a-to-z"

CONVENTIONAL_COMMIT_REGEX = re.compile(
    r"^(feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert)(\([a-zA-Z0-9_\-\./]+\))?(!)?:\s+.+"
)
SHA_PIN_REGEX = re.compile(r"uses:\s+[^@\s]+@[a-f0-9]{40}")

def run_gh_api(endpoint: str, timeout: int = 15) -> Tuple[bool, Optional[Any], str]:
    """Execute gh api request and return (success, parsed_json, error_msg)."""
    cmd = ["gh", "api", endpoint]
    try:
        proc = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=timeout
        )
        if proc.returncode == 0:
            try:
                data = json.loads(proc.stdout)
                return True, data, ""
            except json.JSONDecodeError:
                return True, proc.stdout, ""
        else:
            return False, None, proc.stderr.strip()
    except subprocess.TimeoutExpired:
        return False, None, f"Timeout after {timeout}s"
    except Exception as e:
        return False, None, str(e)

def parse_repo_slug(raw_input: Optional[str]) -> Optional[Tuple[str, str]]:
    """Extract (owner, repo) from URL, slug, or current git repository."""
    if not raw_input or raw_input.strip() in (".", "./", ""):
        try:
            out = subprocess.check_output(
                ["git", "config", "--get", "remote.origin.url"],
                text=True,
                stderr=subprocess.PIPE
            ).strip()
            if out:
                raw_input = out
        except Exception:
            return None

    if not raw_input:
        return None

    raw = raw_input.strip().rstrip("/")
    # AppSec: Reject shell injection characters
    if re.search(r"[\$`;&|<>\r\n]", raw):
        return None
    # Handle git clone URLs: git@github.com:owner/repo.git
    ssh_match = re.search(r"github\.com:([\w\-\.]+)/([\w\-\.]+?)(?:\.git)?$", raw)
    if ssh_match:
        return ssh_match.group(1), ssh_match.group(2)
    # Handle https://github.com/owner/repo
    https_match = re.search(r"github\.com/([\w\-\.]+)/([\w\-\.]+?)(?:\.git)?(?:/.*)?$", raw)
    if https_match:
        return https_match.group(1), https_match.group(2)
    # Handle owner/repo
    slug_match = re.match(r"^([\w\-\.]+)/([\w\-\.]+)$", raw)
    if slug_match:
        return slug_match.group(1), slug_match.group(2)
    return None

def check_file_exists(owner: str, repo: str, file_path: str) -> Tuple[bool, Optional[str]]:
    """Check if file exists in the repository and return (exists, content_str)."""
    ok, data, err = run_gh_api(f"repos/{owner}/{repo}/contents/{file_path}")
    if not ok or not data:
        return False, None
    if isinstance(data, dict) and "content" in data:
        try:
            encoding = data.get("encoding", "base64")
            if encoding == "base64":
                raw_bytes = base64.b64decode(data["content"])
                return True, raw_bytes.decode("utf-8", errors="replace")
            return True, data["content"]
        except Exception:
            return True, None
    return True, None

def audit_repository(owner: str, repo: str) -> Dict[str, Any]:
    """Execute complete multi-dimensional audit of repository against the Course Standard."""
    report = {
        "owner": owner,
        "repo": repo,
        "full_name": f"{owner}/{repo}",
        "url": f"https://github.com/{owner}/{repo}",
        "scores": {
            "l1_presentation": 0,
            "l2_git_hygiene": 0,
            "l3_cicd": 0,
            "l4_security": 0,
            "l5_ai_readiness": 0,
            "total": 0,
        },
        "details": {},
        "remediations": [],
    }

    # 1. Fetch Repository Metadata
    ok_meta, meta, err_meta = run_gh_api(f"repos/{owner}/{repo}")
    if not ok_meta or not meta:
        report["error"] = f"Failed to access repository {owner}/{repo}: {err_meta}"
        return report

    is_private = meta.get("private", False) or (meta.get("visibility") == "private")
    report["meta"] = {
        "description": meta.get("description") or "",
        "stars": meta.get("stargazers_count", 0),
        "forks": meta.get("forks_count", 0),
        "open_issues": meta.get("open_issues_count", 0),
        "default_branch": meta.get("default_branch", "main"),
        "license": meta.get("license", {}).get("spdx_id") if meta.get("license") else None,
        "topics": meta.get("topics", []),
        "is_fork": meta.get("fork", False),
        "has_discussions": meta.get("has_discussions", False),
        "is_private": is_private,
        "visibility": meta.get("visibility", "PRIVATE" if is_private else "PUBLIC"),
    }

    # 2. Community Profile
    ok_comm, comm, _ = run_gh_api(f"repos/{owner}/{repo}/community/profile")
    comm_files = comm.get("files", {}) if (ok_comm and comm) else {}
    health_pct = comm.get("health_percentage", 0) if (ok_comm and comm) else 0
    report["details"]["community_health"] = health_pct

    # ==========================================
    # DIMENSION 1: Presentation & Community (L1)
    # ==========================================
    l1_score = 0
    has_readme = bool(comm_files.get("readme") or check_file_exists(owner, repo, "README.md")[0])
    has_license = bool(report["meta"]["license"])
    has_desc = bool(report["meta"]["description"].strip())
    has_topics = len(report["meta"]["topics"]) > 0
    has_contributing = bool(comm_files.get("contributing") or check_file_exists(owner, repo, "CONTRIBUTING.md")[0] or check_file_exists(owner, repo, ".github/CONTRIBUTING.md")[0])
    has_coc = bool(comm_files.get("code_of_conduct") or check_file_exists(owner, repo, "CODE_OF_CONDUCT.md")[0] or check_file_exists(owner, repo, ".github/CODE_OF_CONDUCT.md")[0])

    if has_readme:
        l1_score += 4
    else:
        report["remediations"].append({
            "level": "P0",
            "title": "Отсутствует витрина проекта (README.md)",
            "guide": f"{COURSE_URL}/blob/main/docs/01-web-basics/README.md",
            "fix": "Создайте README.md с описанием, быстрым стартом, архитектурой и бейджами статуса."
        })

    if has_license:
        l1_score += 4
    else:
        report["remediations"].append({
            "level": "P1",
            "title": "Отсутствует открытая лицензия (LICENSE)",
            "guide": f"{COURSE_URL}/blob/main/docs/08-releases-licenses/README.md",
            "fix": "Добавьте файл LICENSE (MIT, Apache 2.0 или GPLv3), чтобы код имел легальный статус Open Source."
        })

    if has_desc:
        l1_score += 4
    else:
        report["remediations"].append({
            "level": "P2",
            "title": "Пустое поле 'About / Description' в шапке репозитория",
            "guide": f"{COURSE_URL}/blob/main/docs/01-web-basics/README.md",
            "fix": "Заполните краткое описание репозитория и ссылку на сайт в блоке 'About'."
        })

    if has_topics:
        l1_score += 4
    else:
        report["remediations"].append({
            "level": "P2",
            "title": "Не настроены тематические теги (Topics)",
            "guide": f"{COURSE_URL}/blob/main/docs/01-web-basics/README.md",
            "fix": "Добавьте 3-5 тематических тегов (например: ai, python, devops, mcp) для индексации в поиске."
        })

    if has_contributing or has_coc:
        l1_score += 4
    else:
        report["remediations"].append({
            "level": "P1",
            "title": "Отсутствуют правила участия сообщества (CONTRIBUTING.md / CODE_OF_CONDUCT.md)",
            "guide": f"{COURSE_URL}/blob/main/docs/05-project-management/README.md",
            "fix": "Добавьте регламент приёма PR (CONTRIBUTING.md) и кодекс поведения сообщества."
        })

    report["scores"]["l1_presentation"] = l1_score

    # ==========================================
    # DIMENSION 2: Git Flow & Root Hygiene (L2)
    # ==========================================
    l2_score = 0
    has_gitignore = check_file_exists(owner, repo, ".gitignore")[0]
    has_gitattributes = check_file_exists(owner, repo, ".gitattributes")[0]
    has_issue_template = bool(comm_files.get("issue_template") or check_file_exists(owner, repo, ".github/ISSUE_TEMPLATE.md")[0] or check_file_exists(owner, repo, ".github/ISSUE_TEMPLATE")[0])
    has_pr_template = bool(comm_files.get("pull_request_template") or check_file_exists(owner, repo, ".github/PULL_REQUEST_TEMPLATE.md")[0])

    if has_gitignore:
        l2_score += 5
    else:
        report["remediations"].append({
            "level": "P0",
            "title": "Отсутствует первая линия обороны (.gitignore)",
            "guide": f"{COURSE_URL}/blob/main/docs/04-security-opsec/README.md",
            "fix": "Добавьте .gitignore для исключения мусора ОС (.DS_Store), логов, виртуальных окружений и секретов."
        })

    if has_gitattributes:
        l2_score += 5
    else:
        report["remediations"].append({
            "level": "P1",
            "title": "Отсутствует кроссплатформенная нормализация (.gitattributes)",
            "guide": f"{COURSE_URL}/blob/main/docs/10-production-standards/README.md",
            "fix": "Добавьте .gitattributes с директивой '* text=auto eol=lf' для предотвращения конфликтов CRLF/LF."
        })

    if has_issue_template or has_pr_template:
        l2_score += 5
    else:
        report["remediations"].append({
            "level": "P2",
            "title": "Отсутствуют шаблоны задач и PR (.github/ISSUE_TEMPLATE / PULL_REQUEST_TEMPLATE.md)",
            "guide": f"{COURSE_URL}/blob/main/docs/05-project-management/README.md",
            "fix": "Настройте стандартные шаблоны тикетов и PR для повышения качества входящих багрепортов."
        })

    # Check Conventional Commits in last 10 commits
    ok_commits, commits, _ = run_gh_api(f"repos/{owner}/{repo}/commits?per_page=10")
    conventional_count = 0
    total_commits = 0
    if ok_commits and isinstance(commits, list) and commits:
        total_commits = len(commits)
        for c in commits:
            msg = c.get("commit", {}).get("message", "").split("\n")[0].strip()
            # Ignore merge commits
            if msg.startswith("Merge pull request") or msg.startswith("Merge branch"):
                conventional_count += 1
            elif CONVENTIONAL_COMMIT_REGEX.match(msg):
                conventional_count += 1
    
    commit_ratio = (conventional_count / total_commits) if total_commits > 0 else 0
    report["details"]["conventional_commits_ratio"] = round(commit_ratio * 100)
    if commit_ratio >= 0.7:
        l2_score += 5
    elif commit_ratio >= 0.4:
        l2_score += 2.5
        report["remediations"].append({
            "level": "P2",
            "title": f"Частичное соблюдение Conventional Commits ({round(commit_ratio*100)}%)",
            "guide": f"{COURSE_URL}/blob/main/docs/10-production-standards/README.md",
            "fix": "Используйте семантические префиксы в коммитах: feat:, fix:, docs:, chore:, refactor:, ci:."
        })
    else:
        report["remediations"].append({
            "level": "P1",
            "title": f"Низкая семантическая дисциплина коммитов ({round(commit_ratio*100)}% Conventional Commits)",
            "guide": f"{COURSE_URL}/blob/main/docs/10-production-standards/README.md",
            "fix": "Переведите коммиты команды на канон Conventional Commits для автоматической генерации changelog."
        })

    report["scores"]["l2_git_hygiene"] = l2_score

    # ==========================================
    # DIMENSION 3: CI/CD Pipeline Resilience (L3)
    # ==========================================
    l3_score = 0
    ok_wf, wf_data, _ = run_gh_api(f"repos/{owner}/{repo}/actions/workflows")
    workflows = wf_data.get("workflows", []) if (ok_wf and wf_data) else []
    active_workflows = [w for w in workflows if w.get("state") == "active"]
    report["details"]["active_workflows_count"] = len(active_workflows)

    has_active_ci = len(active_workflows) > 0
    has_timeouts = False
    has_concurrency = False
    has_minimal_permissions = False
    all_actions_sha_pinned = True
    analyzed_workflow_count = 0

    has_codeql = False
    has_codeql_cargo_cult = False
    has_alternative_sast = False
    has_fake_tests = False

    if has_active_ci:
        # Inspect workflow contents
        for wf in active_workflows:
            wf_path = wf.get("path")
            if not wf_path or not wf_path.startswith(".github/workflows"):
                continue
            exists, content = check_file_exists(owner, repo, wf_path)
            if exists and content:
                analyzed_workflow_count += 1
                if "timeout-minutes:" in content or "timeout:" in content:
                    has_timeouts = True
                if "concurrency:" in content:
                    has_concurrency = True
                if "permissions:" in content:
                    has_minimal_permissions = True
                
                # Check SHA pinning
                uses_lines = [l for l in content.splitlines() if "uses:" in l and not l.strip().startswith("#")]
                for u in uses_lines:
                    if "./" in u or "docker://" in u:
                        continue
                    if not SHA_PIN_REGEX.search(u):
                        all_actions_sha_pinned = False

                # Detect CodeQL vs SAST
                if "codeql-action" in content or "codeql" in wf_path.lower():
                    has_codeql = True
                    # Detect cargo-cult suppression of CodeQL failures in private repos
                    if re.search(r"upload:\s*['\"]?(never|false)['\"]?", content, re.IGNORECASE) or \
                       re.search(r"continue-on-error:\s*true", content, re.IGNORECASE):
                        has_codeql_cargo_cult = True

                # Detect alternative open SAST tools
                if any(tool in content.lower() for tool in ["gosec", "bandit", "trivy", "semgrep", "ruff check"]):
                    has_alternative_sast = True

                # Detect fake tests (test -f or wc -l without real test runners)
                if ("test -f " in content or "wc -l" in content) and not any(
                    runner in content for runner in [
                        "go test", "pytest", "python -m unittest", "npm test", "yarn test",
                        "cargo test", "validate_links", "markdownlint", "ruff", "gosec"
                    ]
                ):
                    has_fake_tests = True
    else:
        all_actions_sha_pinned = False
        report["remediations"].append({
            "level": "P0",
            "title": "Отсутствуют настроенные конвейеры автоматизации (GitHub Actions)",
            "guide": f"{COURSE_URL}/blob/main/docs/06-actions-pages/README.md",
            "fix": "Настройте базовый CI воркфлоу (.github/workflows/ci.yml) для автопроверки тестов и линтеров."
        })

    # Automated check / build in CI
    if has_active_ci:
        if has_fake_tests:
            report["remediations"].append({
                "level": "P0",
                "title": "Фиктивное тестирование в CI: проверка файлов (test -f / wc -l) вместо реальных тестов",
                "guide": f"{COURSE_URL}/blob/main/docs/06-actions-pages/README.md",
                "fix": "Устраните карго-культ: замените проверку наличия файлов на запуск реальных тестов (go test / pytest) или валидацию ссылок (validate_links.py)."
            })
        else:
            l3_score += 5

    # Timeouts & Concurrency
    if has_timeouts or has_concurrency:
        l3_score += 5
    elif has_active_ci:
        report["remediations"].append({
            "level": "P1",
            "title": "В GitHub Actions отсутствуют лимиты времени (timeout-minutes) и защита от гонок (concurrency)",
            "guide": f"{COURSE_URL}/blob/main/docs/06-actions-pages/README.md",
            "fix": "Добавьте 'timeout-minutes: 5-10' и блок 'concurrency: cancel-in-progress: true' для экономии минут раннеров."
        })

    # Minimal permissions
    if has_minimal_permissions:
        l3_score += 5
    elif has_active_ci:
        report["remediations"].append({
            "level": "P1",
            "title": "В воркфлоу не зафиксирован принцип наименьших привилегий (permissions: contents: read)",
            "guide": f"{COURSE_URL}/blob/main/docs/14-security-insights/README.md",
            "fix": "Явно задайте 'permissions: contents: read' на уровне файла воркфлоу, чтобы защититься от захвата токена GITHUB_TOKEN."
        })

    # Basic active CI bonus
    if has_active_ci:
        l3_score += 5

    report["scores"]["l3_cicd"] = min(l3_score, 20)

    # ==========================================
    # DIMENSION 4: DevSecOps Fortress (L4)
    # ==========================================
    l4_score = 0
    has_security_policy = check_file_exists(owner, repo, "SECURITY.md")[0] or check_file_exists(owner, repo, ".github/SECURITY.md")[0]
    has_dependabot = (
        check_file_exists(owner, repo, ".github/dependabot.yml")[0] or
        check_file_exists(owner, repo, ".github/dependabot.yaml")[0] or
        check_file_exists(owner, repo, "renovate.json")[0] or
        check_file_exists(owner, repo, "renovate.json5")[0] or
        check_file_exists(owner, repo, ".github/renovate.json")[0] or
        check_file_exists(owner, repo, ".github/renovate.json5")[0] or
        check_file_exists(owner, repo, ".renovaterc")[0] or
        check_file_exists(owner, repo, ".renovaterc.json")[0]
    )

    if has_security_policy:
        l4_score += 5
    else:
        report["remediations"].append({
            "level": "P1",
            "title": "Отсутствует политика безопасности и регламент раскрытия уязвимостей (SECURITY.md)",
            "guide": f"{COURSE_URL}/blob/main/docs/14-security-insights/README.md",
            "fix": "Добавьте SECURITY.md с регламентом ответственного раскрытия уязвимостей (Responsible Disclosure)."
        })

    # SAST Evaluation & Anti-Cargo-Cult Enforcement
    valid_sast = (has_codeql and not has_codeql_cargo_cult) or has_alternative_sast
    if valid_sast:
        l4_score += 5
    else:
        if has_codeql_cargo_cult:
            report["remediations"].append({
                "level": "P0",
                "title": "Карго-культ CodeQL: результаты сканирования глушатся ('upload: never' / 'continue-on-error')",
                "guide": f"{COURSE_URL}/blob/main/docs/14-security-insights/README.md",
                "fix": "В приватных репозиториях без GHAS загрузка SARIF блокируется (403). Замените CodeQL на открытый SAST (securego/gosec для Go, bandit/ruff для Python, trivy) с прямым выводом в лог CI."
            })
        elif is_private:
            report["remediations"].append({
                "level": "P1",
                "title": "Отсутствует открытый статический SAST-анализ кода (gosec / bandit / trivy)",
                "guide": f"{COURSE_URL}/blob/main/docs/14-security-insights/README.md",
                "fix": "В приватном репозитории без GHAS внедрите открытый SAST (securego/gosec для Go, bandit для Python) вместо неработающего CodeQL."
            })
        else:
            report["remediations"].append({
                "level": "P2",
                "title": "Отсутствует статический SAST-анализ кода (CodeQL / Static Analysis)",
                "guide": f"{COURSE_URL}/blob/main/docs/14-security-insights/README.md",
                "fix": "Внедрите воркфлоу CodeQL (.github/workflows/codeql.yml) для поиска уязвимостей в AST-графе."
            })

    if has_dependabot:
        l4_score += 5
    else:
        report["remediations"].append({
            "level": "P1",
            "title": "Не настроен автоматический мониторинг зависимостей (Dependabot / Renovate)",
            "guide": f"{COURSE_URL}/blob/main/docs/10-production-standards/README.md",
            "fix": "Создайте .github/dependabot.yml или renovate.json для регулярного авто-сканирования библиотек и экшенов на CVE."
        })

    if analyzed_workflow_count > 0 and all_actions_sha_pinned:
        l4_score += 5
    else:
        if has_active_ci:
            report["remediations"].append({
                "level": "P0",
                "title": "Уязвимость цепочки поставок: Экшены вызываются по мутабельным тегам без SHA-пиннинга",
                "guide": f"{COURSE_URL}/blob/main/docs/14-security-insights/README.md",
                "fix": "Зафиксируйте все вызовы 'uses: actions/checkout@...' по полному 40-значному SHA коммита (SLSA / OpenSSF Scorecard standard)."
            })

    report["scores"]["l4_security"] = l4_score

    # ==========================================
    # DIMENSION 5: AI-Ready 2026 (L5)
    # ==========================================
    l5_score = 0
    has_agents_md = check_file_exists(owner, repo, "AGENTS.md")[0]
    has_llms_txt = check_file_exists(owner, repo, "llms.txt")[0] or check_file_exists(owner, repo, ".well-known/llms.txt")[0]
    has_copilot_instructions = (
        check_file_exists(owner, repo, ".github/copilot-instructions.md")[0] or
        check_file_exists(owner, repo, ".cursorrules")[0] or
        check_file_exists(owner, repo, ".cursor/rules")[0]
    )

    if has_agents_md:
        l5_score += 8
    else:
        report["remediations"].append({
            "level": "P1",
            "title": "Отсутствует системный контракт для ИИ-агентов (AGENTS.md)",
            "guide": f"{COURSE_URL}/blob/main/AGENTS.md",
            "fix": "Создайте AGENTS.md со стандартами архитектуры, директивой против сикофантии и рабочими режимами агентов."
        })

    if has_llms_txt:
        l5_score += 6
    else:
        report["remediations"].append({
            "level": "P2",
            "title": "Отсутствует открытый контекстный стандарт для нейросетей (llms.txt)",
            "guide": f"{COURSE_URL}/blob/main/llms.txt",
            "fix": "Добавьте манифест llms.txt для эффективного RAG и скармливания контекста LLM-ассистентам без мусора."
        })

    if has_copilot_instructions:
        l5_score += 6
    else:
        report["remediations"].append({
            "level": "P2",
            "title": "Не настроен проектный брендбук Copilot (.github/copilot-instructions.md)",
            "guide": f"{COURSE_URL}/blob/main/docs/12-ai-coding-mcp/README.md",
            "fix": "Создайте .github/copilot-instructions.md для передачи проектных стандартов в GitHub Copilot / Cursor."
        })

    report["scores"]["l5_ai_readiness"] = l5_score

    # Compute Total
    total = l1_score + l2_score + l3_score + l4_score + l5_score
    report["scores"]["total"] = total

    # Tier Assignment
    if total >= 90:
        report["tier"] = "🏆 Diamond (Enterprise Цитадель)"
        report["tier_desc"] = "Бескомпромиссный золотой стандарт качества, безопасности и AI-готовности."
    elif total >= 75:
        report["tier"] = "🥇 Gold (Production Ready)"
        report["tier_desc"] = "Надёжный промышленный репозиторий с отличной базой автоматизации."
    elif total >= 50:
        report["tier"] = "🥈 Silver (Maturing Project)"
        report["tier_desc"] = "Зрелый проект, но присутствуют слепые зоны в безопасности или CI/CD."
    elif total >= 25:
        report["tier"] = "🥉 Bronze (Early Stage)"
        report["tier_desc"] = "Базовый уровень, требующий серьёзного подтягивания гигиены и автоматизации."
    else:
        report["tier"] = "⚠️ Raw / Chaotic (Требуется санация)"
        report["tier_desc"] = "Критический дефицит базовых практик Git и стандартов сообщества."

    return report

def format_markdown_report(report: Dict[str, Any]) -> str:
    """Format audit results in compact, beautiful Mobile-First Markdown Card format."""
    if "error" in report:
        return f"🚨 **Ошибка аудита репозитория:** {report['error']}"

    owner = report["owner"]
    repo = report["repo"]
    meta = report["meta"]
    scores = report["scores"]
    total = scores["total"]
    tier = report["tier"]

    p0_count = sum(1 for r in report["remediations"] if r["level"] == "P0")
    p1_count = sum(1 for r in report["remediations"] if r["level"] == "P1")
    p2_count = sum(1 for r in report["remediations"] if r["level"] == "P2")

    lines = [
        f"## 🛸 GITHUBREPO: Паспорт Качества Репозитория",
        f"",
        f"**Репозиторий:** [{owner}/{repo}](https://github.com/{owner}/{repo})",
        f"**Видимость:** `{meta.get('visibility', 'PUBLIC')}`",
        f"**Статус:** {tier}",
        f"**Индекс качества:** `{total} / 100 баллов`",
        f"",
        f"---",
        f"",
        f"### 📊 Матрица 5 Измерений (Maturity Radar)",
        f"",
        f"• **1. Витрина & Сообщество (L1):** `{scores['l1_presentation']} / 20`",
        f"• **2. Git Flow & Чистота корня (L2):** `{scores['l2_git_hygiene']} / 20`",
        f"• **3. Автоматизация CI/CD (L3):** `{scores['l3_cicd']} / 20`",
        f"• **4. Цитадель Безопасности (L4):** `{scores['l4_security']} / 20`",
        f"• **5. Интеллект & AI-Ready 2026 (L5):** `{scores['l5_ai_readiness']} / 20`",
        f"",
        f"---",
        f"",
        f"### 🛡️ Сводка Находок (Defects Summary)",
        f"• 🚨 **P0 (Критические):** `{p0_count}`",
        f"• ⚠️ **P1 (Архитектурные):** `{p1_count}`",
        f"• 💡 **P2 (Рекомендации):** `{p2_count}`",
        f"",
        f"---",
        f"",
        f"### 🛠️ Дорожная Карта Доведения до Идеала (Actionable Roadmap)",
        f"",
    ]

    if not report["remediations"]:
        lines.append("🎉 **Замечаний не обнаружено!** Репозиторий полностью соответствует бескомпромиссному канону «GitHub от А до Я».")
    else:
        for idx, rem in enumerate(report["remediations"], 1):
            badge = "🚨 [P0]" if rem["level"] == "P0" else ("⚠️ [P1]" if rem["level"] == "P1" else "💡 [P2]")
            lines.append(f"#### {idx}. {badge} {rem['title']}")
            lines.append(f"• **Что сделать:** {rem['fix']}")
            lines.append(f"• 📖 **Канон курса:** [Изучить в «GitHub от А до Я»]({rem['guide']})")
            lines.append("")

    lines.extend([
        "---",
        "",
        "### 📦 Готовые Рецепты для Внедрения (Drop-in Snippets)",
        "",
        "#### 1. Кроссплатформенный `.gitattributes` (LF Normalization):",
        "```gitattributes",
        "* text=auto eol=lf",
        "*.py text eol=lf",
        "*.js text eol=lf",
        "*.ts text eol=lf",
        "*.md text eol=lf",
        "*.sh text eol=lf",
        "*.yml text eol=lf",
        "*.png binary",
        "*.jpg binary",
        "*.tar.gz binary",
        "```",
        "",
        "#### 2. Минимальный шаблон `AGENTS.md` (System Contract 2026):",
        "```markdown",
        "# 🤖 AGENTS.md — Системный контракт для ИИ-агентов",
        "> Стандарт взаимодействия для автономных LLM-ассистентов (Cursor, Windsurf, Claude Code, Copilot, Antigravity).",
        "",
        "## 1. Архитектура и Grounding",
        "- Стек: [Укажите язык, фреймворки и структуру папок]",
        "- CWD: Рабочая директория проекта",
        "",
        "## 2. Директива против сикофантии (Anti-Sycophancy)",
        "- Никакого маркетингового шума («AI slop»).",
        "- Честно указывать на баги, утечки и неоптимальности.",
        "",
        "## 3. Правила изменений",
        "- Ветки feat/*, fix/*, коммиты по Conventional Commits.",
        "- Обязательный запуск линтеров и тестов перед PR.",
        "```",
        "",
        "#### 3. Открытый SAST воркфлоу для Go (.github/workflows/security.yml):",
        "```yaml",
        "name: Security Scan",
        "on:",
        "  push:",
        "    branches: [ main, master ]",
        "  pull_request:",
        "    branches: [ main, master ]",
        "concurrency:",
        "  group: ${{ github.workflow }}-${{ github.ref }}",
        "  cancel-in-progress: true",
        "permissions:",
        "  contents: read",
        "jobs:",
        "  gosec:",
        "    runs-on: ubuntu-latest",
        "    timeout-minutes: 10",
        "    steps:",
        "      - uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683 # v4.2.2",
        "      - uses: securego/gosec@master",
        "        with:",
        "          args: ./...",
        "```",
        "",
        "#### 4. Открытый SAST воркфлоу для Python (.github/workflows/security.yml):",
        "```yaml",
        "name: Security Scan",
        "on:",
        "  push:",
        "    branches: [ main, master ]",
        "  pull_request:",
        "    branches: [ main, master ]",
        "concurrency:",
        "  group: ${{ github.workflow }}-${{ github.ref }}",
        "  cancel-in-progress: true",
        "permissions:",
        "  contents: read",
        "jobs:",
        "  security:",
        "    runs-on: ubuntu-latest",
        "    timeout-minutes: 10",
        "    steps:",
        "      - uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683 # v4.2.2",
        "      - uses: actions/setup-python@42375524e23c412d93fb67b49958b491fce71c38 # v5.4.0",
        "        with:",
        "          python-version: '3.11'",
        "      - run: |",
        "          pip install bandit ruff",
        "          ruff check .",
        "          bandit -r . -ll",
        "```",
        "",
        f"Стандарт качества: [«GitHub от А до Я»]({COURSE_URL}) | TheNovaNodes Network 🛸"
    ])

    return "\n".join(lines)

def main():
    parser = argparse.ArgumentParser(
        description="Audit a GitHub repository against the «GitHub from A to Z» standard (Scorecard 0-100)."
    )
    parser.add_argument(
        "repo",
        nargs="?",
        default=".",
        help="GitHub repo URL, slug ('owner/repo'), or '.' / omit for current git repo (default: current directory)."
    )
    parser.add_argument("--json", action="store_true", help="Output raw JSON report")
    args = parser.parse_args()

    slug = parse_repo_slug(args.repo)
    if not slug:
        print(f"Error: Could not parse GitHub repository from '{args.repo}'", file=sys.stderr)
        print("Usage: python3 scripts/audit_repo.py [<owner/repo> | <repo_url> | .]", file=sys.stderr)
        sys.exit(1)

    owner, repo = slug
    report = audit_repository(owner, repo)

    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print(format_markdown_report(report))

if __name__ == "__main__":
    main()
