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
from typing import Dict, Any, List, Optional, Tuple, Set

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

def fetch_repo_tree(owner: str, repo: str, default_branch: str = "main") -> Optional[Set[str]]:
    """Fetch complete repository tree in a single recursive API call (O(1) lookups)."""
    ok, data, _ = run_gh_api(f"repos/{owner}/{repo}/git/trees/{default_branch}?recursive=1")
    if ok and isinstance(data, dict) and "tree" in data:
        return {item["path"] for item in data["tree"] if "path" in item}
    return None

def is_file_present(tree: Optional[Set[str]], path: str, owner: str, repo: str) -> bool:
    """Check file presence via git tree cache, falling back to contents API if needed."""
    if tree is not None:
        return path in tree
    return check_file_exists(owner, repo, path)[0]

def has_directory_contents(tree: Optional[Set[str]], prefix: str, owner: str, repo: str) -> bool:
    """Check if any file exists under directory prefix."""
    if tree is not None:
        clean_prefix = prefix.rstrip("/") + "/"
        return any(p.startswith(clean_prefix) for p in tree)
    return check_file_exists(owner, repo, prefix)[0]

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

    # 3. Fetch Repository Tree for fast O(1) in-memory checks
    default_branch = report["meta"]["default_branch"]
    repo_tree = fetch_repo_tree(owner, repo, default_branch)

    # ==========================================
    # DIMENSION 1: Presentation & Community (L1)
    # ==========================================
    l1_score = 0
    has_readme = bool(comm_files.get("readme") or is_file_present(repo_tree, "README.md", owner, repo))
    has_license = bool(report["meta"]["license"] or is_file_present(repo_tree, "LICENSE", owner, repo) or is_file_present(repo_tree, "LICENSE.md", owner, repo))
    has_desc = bool(report["meta"]["description"].strip())
    has_topics = len(report["meta"]["topics"]) > 0
    has_contributing = bool(
        comm_files.get("contributing") or
        is_file_present(repo_tree, "CONTRIBUTING.md", owner, repo) or
        is_file_present(repo_tree, ".github/CONTRIBUTING.md", owner, repo)
    )
    has_coc = bool(
        comm_files.get("code_of_conduct") or
        is_file_present(repo_tree, "CODE_OF_CONDUCT.md", owner, repo) or
        is_file_present(repo_tree, ".github/CODE_OF_CONDUCT.md", owner, repo)
    )

    # 1. README.md (5 pts)
    if has_readme:
        l1_score += 5
    else:
        report["remediations"].append({
            "level": "P0",
            "title": "Отсутствует витрина проекта (README.md)",
            "guide": f"{COURSE_URL}/blob/main/docs/01-web-basics/README.md",
            "fix": "Создайте README.md с описанием, быстрым стартом, архитектурой и бейджами статуса."
        })

    # 2. LICENSE (5 pts)
    if has_license:
        l1_score += 5
    else:
        report["remediations"].append({
            "level": "P1",
            "title": "Отсутствует открытая лицензия (LICENSE)",
            "guide": f"{COURSE_URL}/blob/main/docs/08-releases-licenses/README.md",
            "fix": "Добавьте файл LICENSE (MIT, Apache 2.0 или GPLv3), чтобы код имел легальный статус Open Source."
        })

    # 3. About & Topics (5 pts)
    if has_desc and has_topics:
        l1_score += 5
    elif has_desc or has_topics:
        l1_score += 2.5
        missing = "тематические теги (Topics)" if not has_topics else "описание (About / Description)"
        report["remediations"].append({
            "level": "P2",
            "title": f"Частично заполнена шапка репозитория (отсутствуют {missing})",
            "guide": f"{COURSE_URL}/blob/main/docs/01-web-basics/README.md",
            "fix": f"Заполните {missing} в блоке About для лучшей индексации в поиске GitHub."
        })
    else:
        report["remediations"].append({
            "level": "P2",
            "title": "Не заполнены описание (About) и тематические теги (Topics)",
            "guide": f"{COURSE_URL}/blob/main/docs/01-web-basics/README.md",
            "fix": "Заполните краткое описание репозитория и добавьте 3-5 тегов (Topics) в блоке 'About'."
        })

    # 4. Community Standards (5 pts)
    if has_contributing and has_coc:
        l1_score += 5
    elif has_contributing or has_coc:
        l1_score += 2.5
        missing = "CODE_OF_CONDUCT.md" if not has_coc else "CONTRIBUTING.md"
        report["remediations"].append({
            "level": "P2",
            "title": f"Частичные правила сообщества (рекомендуется добавить {missing})",
            "guide": f"{COURSE_URL}/blob/main/docs/05-project-management/README.md",
            "fix": f"Добавьте {missing} для полноценного управления вкладом сообщества."
        })
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
    has_gitignore = is_file_present(repo_tree, ".gitignore", owner, repo)
    has_gitattributes = is_file_present(repo_tree, ".gitattributes", owner, repo)
    has_issue_template = bool(
        comm_files.get("issue_template") or
        is_file_present(repo_tree, ".github/ISSUE_TEMPLATE.md", owner, repo) or
        has_directory_contents(repo_tree, ".github/ISSUE_TEMPLATE", owner, repo)
    )
    has_pr_template = bool(
        comm_files.get("pull_request_template") or
        is_file_present(repo_tree, ".github/PULL_REQUEST_TEMPLATE.md", owner, repo) or
        has_directory_contents(repo_tree, ".github/PULL_REQUEST_TEMPLATE", owner, repo)
    )

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

    if has_issue_template and has_pr_template:
        l2_score += 5
    elif has_issue_template or has_pr_template:
        l2_score += 2.5
        missing = "PULL_REQUEST_TEMPLATE.md" if not has_pr_template else "ISSUE_TEMPLATE"
        report["remediations"].append({
            "level": "P2",
            "title": f"Частичные шаблоны тикетов (отсутствует {missing})",
            "guide": f"{COURSE_URL}/blob/main/docs/05-project-management/README.md",
            "fix": f"Добавьте {missing} для стандартизации входящих тикетов и PR."
        })
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
    all_workflows_have_timeouts = True
    has_concurrency = False
    has_minimal_permissions = False
    all_actions_sha_pinned = True
    analyzed_workflow_count = 0

    has_codeql = False
    has_codeql_cargo_cult = False
    has_alternative_sast = False
    has_fake_tests = False

    if has_active_ci:
        for wf in active_workflows:
            wf_path = wf.get("path")
            if not wf_path or not wf_path.startswith(".github/workflows"):
                continue
            exists, content = check_file_exists(owner, repo, wf_path)
            if exists and content:
                analyzed_workflow_count += 1
                
                # Check timeout-minutes in this workflow (ignoring comments)
                wf_has_timeout = False
                wf_has_concurrency = False
                wf_has_permissions = False
                
                for line in content.splitlines():
                    stripped = line.strip()
                    if stripped.startswith("#"):
                        continue
                    if "timeout-minutes:" in stripped or "timeout:" in stripped:
                        wf_has_timeout = True
                    if "concurrency:" in stripped:
                        wf_has_concurrency = True
                    if "permissions:" in stripped and "write-all" not in content:
                        wf_has_permissions = True
                
                if not wf_has_timeout:
                    all_workflows_have_timeouts = False
                if wf_has_concurrency:
                    has_concurrency = True
                if wf_has_permissions:
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
                    # Check for cargo-cult in CodeQL:
                    # 1. upload: never or upload: false
                    if re.search(r"upload:\s*['\"]?(never|false)['\"]?", content, re.IGNORECASE):
                        has_codeql_cargo_cult = True
                    # 2. continue-on-error: true strictly associated with CodeQL step
                    codeql_steps = re.findall(
                        r"uses:\s+github/codeql-action[^\n]+\n(?:[ \t]+[^\n]+\n)*?[ \t]+continue-on-error:\s*true",
                        content,
                        re.IGNORECASE
                    )
                    if codeql_steps:
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

        if analyzed_workflow_count == 0:
            all_workflows_have_timeouts = False
    else:
        all_workflows_have_timeouts = False
        all_actions_sha_pinned = False
        report["remediations"].append({
            "level": "P0",
            "title": "Отсутствуют настроенные конвейеры автоматизации (GitHub Actions)",
            "guide": f"{COURSE_URL}/blob/main/docs/06-actions-pages/README.md",
            "fix": "Настройте базовый CI воркфлоу (.github/workflows/ci.yml) для автопроверки тестов и линтеров."
        })

    # 1. Active CI with real tests (5 pts)
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

    # 2. Timeout protection (5 pts)
    if has_active_ci and all_workflows_have_timeouts:
        l3_score += 5
    elif has_active_ci:
        report["remediations"].append({
            "level": "P1",
            "title": "В воркфлоу отсутствуют обязательные лимиты времени (timeout-minutes)",
            "guide": f"{COURSE_URL}/blob/main/docs/06-actions-pages/README.md",
            "fix": "Добавьте 'timeout-minutes: 5-10' во все джобы для защиты от зависаний и перерасхода квоты минут."
        })

    # 3. Concurrency protection (5 pts)
    if has_active_ci and has_concurrency:
        l3_score += 5
    elif has_active_ci:
        report["remediations"].append({
            "level": "P1",
            "title": "Отсутствует управление параллельными сборками (concurrency: cancel-in-progress: true)",
            "guide": f"{COURSE_URL}/blob/main/docs/06-actions-pages/README.md",
            "fix": "Настройте блок concurrency с 'cancel-in-progress: true' для автоматической отмены устаревших очередей."
        })

    # 4. Minimal permissions (5 pts)
    if has_active_ci and has_minimal_permissions:
        l3_score += 5
    elif has_active_ci:
        report["remediations"].append({
            "level": "P1",
            "title": "В воркфлоу не зафиксирован принцип наименьших привилегий (permissions: contents: read)",
            "guide": f"{COURSE_URL}/blob/main/docs/14-security-insights/README.md",
            "fix": "Явно задайте 'permissions: contents: read' на уровне файла воркфлоу (или джобы), избегая антипаттерна write-all."
        })

    report["scores"]["l3_cicd"] = l3_score

    # ==========================================
    # DIMENSION 4: DevSecOps Fortress (L4)
    # ==========================================
    l4_score = 0
    has_security_policy = (
        is_file_present(repo_tree, "SECURITY.md", owner, repo) or
        is_file_present(repo_tree, ".github/SECURITY.md", owner, repo)
    )
    
    dependabot_paths = [
        ".github/dependabot.yml", ".github/dependabot.yaml",
        "renovate.json", "renovate.json5",
        ".github/renovate.json", ".github/renovate.json5",
        ".renovaterc", ".renovaterc.json"
    ]
    has_dependabot = any(is_file_present(repo_tree, p, owner, repo) for p in dependabot_paths)

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
    has_agents_md = (
        is_file_present(repo_tree, "AGENTS.md", owner, repo) or
        is_file_present(repo_tree, ".github/AGENTS.md", owner, repo)
    )
    has_llms_txt = (
        is_file_present(repo_tree, "llms.txt", owner, repo) or
        is_file_present(repo_tree, ".well-known/llms.txt", owner, repo) or
        has_directory_contents(repo_tree, "docs", owner, repo)
    )
    has_copilot_instructions = (
        is_file_present(repo_tree, ".github/copilot-instructions.md", owner, repo) or
        is_file_present(repo_tree, ".cursorrules", owner, repo) or
        has_directory_contents(repo_tree, ".cursor/rules", owner, repo)
    )

    if has_agents_md:
        l5_score += 8
    else:
        report["remediations"].append({
            "level": "P1",
            "title": "Отсутствует системный контракт для ИИ-агентов (AGENTS.md)",
            "guide": f"{COURSE_URL}/blob/main/AGENTS.md",
            "fix": "Создайте AGENTS.md (в корне или .github/) со стандартами архитектуры, директивой против сикофантии и рабочими режимами агентов."
        })

    if has_llms_txt:
        l5_score += 6
    else:
        report["remediations"].append({
            "level": "P2",
            "title": "Отсутствует открытый контекстный стандарт для нейросетей (llms.txt или архитектура в docs/)",
            "guide": f"{COURSE_URL}/blob/main/llms.txt",
            "fix": "Добавьте манифест llms.txt или структурированную документацию в docs/ для скармливания контекста LLM без шума."
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

    # Dynamic Drop-in Snippets (only render if relevant remediations exist)
    snippets_to_show = []
    
    if any("gitattributes" in r["title"].lower() for r in report["remediations"]):
        snippets_to_show.append((
            "Кроссплатформенный `.gitattributes` (LF Normalization):",
            "gitattributes",
            "* text=auto eol=lf\n*.py text eol=lf\n*.js text eol=lf\n*.ts text eol=lf\n*.md text eol=lf\n*.sh text eol=lf\n*.yml text eol=lf\n*.png binary\n*.jpg binary\n*.tar.gz binary"
        ))

    if any("agents.md" in r["title"].lower() for r in report["remediations"]):
        snippets_to_show.append((
            "Минимальный шаблон `AGENTS.md` (System Contract 2026):",
            "markdown",
            "# 🤖 AGENTS.md — Системный контракт для ИИ-агентов\n> Стандарт взаимодействия для автономных LLM-ассистентов (Cursor, Windsurf, Claude Code, Copilot, Antigravity).\n\n## 1. Архитектура и Grounding\n- Стек: [Укажите язык, фреймворки и структуру папок]\n- CWD: Рабочая директория проекта\n\n## 2. Директива против сикофантии (Anti-Sycophancy)\n- Никакого маркетингового шума («AI slop»).\n- Честно указывать на баги, утечки и неоптимальности.\n\n## 3. Правила изменений\n- Ветки feat/*, fix/*, коммиты по Conventional Commits.\n- Обязательный запуск линтеров и тестов перед PR."
        ))

    if any("sast" in r["title"].lower() or "codeql" in r["title"].lower() for r in report["remediations"]):
        snippets_to_show.append((
            "Открытый SAST воркфлоу для Go (.github/workflows/security.yml):",
            "yaml",
            "name: Security Scan\non:\n  push:\n    branches: [ main, master ]\n  pull_request:\n    branches: [ main, master ]\nconcurrency:\n  group: ${{ github.workflow }}-${{ github.ref }}\n  cancel-in-progress: true\npermissions:\n  contents: read\njobs:\n  gosec:\n    runs-on: ubuntu-latest\n    timeout-minutes: 10\n    steps:\n      - uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683 # v4.2.2\n      - uses: securego/gosec@58ebae0d0b6748ae43d8ef4751f04cf30b0a8e1b # v2.22.1\n        with:\n          args: ./..."
        ))
        snippets_to_show.append((
            "Открытый SAST воркфлоу для Python (.github/workflows/security.yml):",
            "yaml",
            "name: Security Scan\non:\n  push:\n    branches: [ main, master ]\n  pull_request:\n    branches: [ main, master ]\nconcurrency:\n  group: ${{ github.workflow }}-${{ github.ref }}\n  cancel-in-progress: true\npermissions:\n  contents: read\njobs:\n  security:\n    runs-on: ubuntu-latest\n    timeout-minutes: 10\n    steps:\n      - uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683 # v4.2.2\n      - uses: actions/setup-python@42375524e23c412d93fb67b49958b491fce71c38 # v5.4.0\n        with:\n          python-version: '3.11'\n      - run: |\n          pip install bandit ruff\n          ruff check .\n          bandit -r . -ll"
        ))

    if snippets_to_show:
        lines.extend([
            "---",
            "",
            "### 📦 Готовые Рецепты для Внедрения (Drop-in Snippets)",
            "",
        ])
        for idx, (title, lang, content) in enumerate(snippets_to_show, 1):
            lines.append(f"#### {idx}. {title}")
            lines.append(f"```{lang}")
            lines.append(content)
            lines.append("```")
            lines.append("")

    lines.extend([
        "---",
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
