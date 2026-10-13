# 🚀 GitHub from A to Z: Full Practical Course (i18n Hub)

> **Learn GitHub directly inside GitHub: from first browser clicks to advanced CI/CD, SemVer releases, licenses, architecture, digital hygiene, vibe coding, Model Context Protocol (MCP), human-agent teams, and DevSecOps fortress.**  
> No disconnected slides. Only real-world repositories, hands-on labs, Git culture, and cutting-edge 2026 developer tooling.

[![Status](https://img.shields.io/badge/Status-Complete%20v1.8-success?style=flat-square)](#)
[![Language](https://img.shields.io/badge/Language-English%20%28In%20Progress%29-blue?style=flat-square)](#)
[![Main Version](https://img.shields.io/badge/Source-Russian%20%F0%9F%87%B7%F0%9F%87%BA-brightgreen?style=flat-square)](../../README.md)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](../../CONTRIBUTING.md)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](../../LICENSE)

---

## 🌐 Language Navigation / Языковая навигация

* 🇷🇺 **[Русская версия (Каноническая)](../../README.md)** — Полный курс (14 модулей + 14 лабораторий + шпаргалка + Зал славы).
* 🇬🇧 **English Version (This Hub)** — Community-driven internationalization hub and translation roadmap.

---

## 🧭 Table of Contents

1. [About the Project](#about-the-project)
2. [How to Contribute to Translations](#how-to-contribute-to-translations)
3. [Curriculum & Translation Status](#curriculum-translation-status)
4. [Hall of Fame & Your First PR](#hall-of-fame-your-first-pr)
5. [Useful Links](#useful-links)

---

## About the Project

**«GitHub from A to Z»** is an open-source, hands-on curriculum created to take learners from absolute zero to production-grade GitHub engineering. Unlike traditional courses, it covers modern 2026 workflows including:
- **AI & Vibe Coding:** GitHub Copilot, Google Jules, and Anthropic Model Context Protocol (MCP).
- **Hybrid Engineering:** Agent Triad pattern (Planner ➔ Builder ➔ Auditor) and Human-in-the-Loop (HITL) governance.
- **Enterprise DevSecOps:** AST static code scanning with GitHub CodeQL, Secret Scanning, Push Protection, and SBOM generation.
- **NASA Flight Rules:** Emergency rescue playbooks for Git disasters in [`CHEATSHEET.md`](../../CHEATSHEET.md).

---

## How to Contribute to Translations

We invite the global Open Source community to translate this course into English and other languages!

### Step-by-Step Translation Workflow:
1. **Fork the repository:** Click **Fork** on [thedoctormes-hue/github-a-to-z](https://github.com/thedoctormes-hue/github-a-to-z).
2. **Create a feature branch:**
   ```bash
   git switch -c docs/i18n-module-00
   ```
3. **Choose an untranslated module:**
   - Look at the [Curriculum & Translation Status](#curriculum-translation-status) table below.
   - Pick a module from `docs/` or a lab from `labs/`.
   - Create the corresponding file in `docs/en/<module-folder>/README.md`.
4. **Translate with precision:**
   - Keep code blocks, ASCII diagrams, Mermaid graphs, and relative links intact.
   - Maintain the friendly, engaging tone and pedagogical metaphors.
5. **Verify link integrity:**
   ```bash
   python3 scripts/validate_links.py
   ```
6. **Submit a Pull Request:**
   - Use conventional commit: `docs(i18n): translate module 00 to English`.
   - Open a PR against `main`. Our automated GitHub Actions bot will verify your submission!

---

## Curriculum & Translation Status

| Module | Title | Russian Source | English Status |
| :--- | :--- | :--- | :--- |
| **Module 00** | Ground Reconnaissance (Why GitHub) | [docs/00-intro](../../docs/00-intro/README.md) | 🟡 Help Wanted |
| **Module 01** | Web Orbit (GitHub without Console) | [docs/01-web-basics](../../docs/01-web-basics/README.md) | 🟡 Help Wanted |
| **Module 02** | Bridge to Terminal (SSH & gh CLI) | [docs/02-terminal-ssh](../../docs/02-terminal-ssh/README.md) | 🟡 Help Wanted |
| **Module 03** | Team Engineering (Branches, PRs, Conflicts) | [docs/03-branches-pr](../../docs/03-branches-pr/README.md) | 🟡 Help Wanted |
| **Module 04** | Digital Shield & OPSEC | [docs/04-security-opsec](../../docs/04-security-opsec/README.md) | 🟡 Help Wanted |
| **Module 05** | Project HQ (Issues, Projects v2, Moderation) | [docs/05-project-management](../../docs/05-project-management/README.md) | 🟡 Help Wanted |
| **Module 06** | Robots on Duty (Actions & Pages) | [docs/06-actions-pages](../../docs/06-actions-pages/README.md) | 🟡 Help Wanted |
| **Module 07** | Future Arsenal (CLI, Reflog, MCP) | [docs/07-pro-tools](../../docs/07-pro-tools/README.md) | 🟡 Help Wanted |
| **Module 08** | Orbit Launch (Releases, SemVer, Licenses) | [docs/08-releases-licenses](../../docs/08-releases-licenses/README.md) | 🟡 Help Wanted |
| **Module 09** | Architecture Hygiene (FSD, ADR, Sync) | [docs/09-architecture-hygiene](../../docs/09-architecture-hygiene/README.md) | 🟡 Help Wanted |
| **Module 10** | Production Standards (Signing, Squash, Rules) | [docs/10-production-standards](../../docs/10-production-standards/README.md) | 🟡 Help Wanted |
| **Module 11** | Documentation Culture & Docs-as-Code | [docs/11-hygiene-and-docs](../../docs/11-hygiene-and-docs/README.md) | 🟡 Help Wanted |
| **Module 12** | AI Coding, Vibe Coding, Copilot, Jules & MCP | [docs/12-ai-coding-mcp](../../docs/12-ai-coding-mcp/README.md) | 🟡 Help Wanted |
| **Module 13** | Hybrid Teams & Agent Triad | [docs/13-human-agent-teams](../../docs/13-human-agent-teams/README.md) | 🟡 Help Wanted |
| **Module 14** | Security Fortress & Telemetry (Security & Insights) | [docs/14-security-insights](../../docs/14-security-insights/README.md) | 🟡 Help Wanted |

---

## Hall of Fame & Your First PR

After completing the course or contributing a translation, immortalize your name in the **[Graduates Hall of Fame (GRADUATES.md)](../../GRADUATES.md)**!

Follow the 8-step guide in [`GRADUATES.md`](../../GRADUATES.md) to submit your first Pull Request. Our automated **Graduate PR Verifier & Welcome Bot** will greet you and guide your submission to merge.

---

## Useful Links

* 🇷🇺 **Main Course (Russian):** [README.md](../../README.md)
* 🛰️ **Repository Reconnaissance Guide:** [docs/repo-reconnaissance.md](../repo-reconnaissance.md)
* 🤖 **AI Agent Protocol & LLM Context:** [AGENTS.md](../../AGENTS.md) | [llms.txt](../../llms.txt)
* ⚡ **Developer Cheatsheet & Flight Rules:** [CHEATSHEET.md](../../CHEATSHEET.md)
* 🎓 **Hall of Fame:** [GRADUATES.md](../../GRADUATES.md)
* 🤝 **Contributing Guidelines:** [CONTRIBUTING.md](../../CONTRIBUTING.md)
* 🛡️ **Security Policy:** [SECURITY.md](../../SECURITY.md)
* 📜 **Changelog:** [CHANGELOG.md](../../CHANGELOG.md)
