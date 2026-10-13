# 🚀 GitHub from A to Z: Full Practical Course (i18n Hub)

> **Learn GitHub directly inside GitHub: from first browser clicks to advanced CI/CD, SemVer releases, licenses, architecture, digital hygiene, vibe coding, Model Context Protocol (MCP), human-agent teams, and DevSecOps fortress.**  
> No disconnected slides. Only real-world repositories, hands-on labs, Git culture, and cutting-edge 2026 developer tooling.

[![Status](https://img.shields.io/badge/Status-Complete%20v1.9-success?style=flat-square)](#)
[![Website](https://img.shields.io/badge/Website-GitHub%20Pages%20Live-brightgreen?style=flat-square)](https://thedoctormes-hue.github.io/github-a-to-z/)
[![Discussions](https://img.shields.io/badge/Discussions-Join%20the%20Community-purple?style=flat-square)](https://github.com/thedoctormes-hue/github-a-to-z/discussions)
[![Docker Package](https://img.shields.io/badge/Package-ghcr.io%20%7C%20Docker-blue?style=flat-square&logo=docker)](https://github.com/thedoctormes-hue/github-a-to-z/pkgs/container/github-a-to-z)
[![Certification](https://img.shields.io/badge/Certification-GitHub%20Foundations%20Prep-blueviolet?style=flat-square&logo=github)](../certification/foundations.md)
[![Student Pack](https://img.shields.io/badge/Education-Student%20Developer%20Pack-orange?style=flat-square&logo=github)](../education/student-pack.md)
[![Classroom](https://img.shields.io/badge/Education-GitHub%20Classroom%20Autograding-blueviolet?style=flat-square&logo=github)](../education/classroom.md)
[![Language](https://img.shields.io/badge/Language-English%20%28In%20Progress%29-blue?style=flat-square)](README.md)
[![Main Version](https://img.shields.io/badge/Source-Russian%20%F0%9F%87%B7%F0%9F%87%BA-brightgreen?style=flat-square)](../../README.md)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](../../CONTRIBUTING.md)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](../../LICENSE)

---

## 🌐 Language Navigation / Языковая навигация

* 📖 **[Interactive Online Book (GitHub Pages)](https://thedoctormes-hue.github.io/github-a-to-z/)** — Official web portal powered by Rust mdBook with full-text search and offline reading.
* 🐳 **[Offline Docker Package (GHCR)](https://github.com/thedoctormes-hue/github-a-to-z/pkgs/container/github-a-to-z)** — Run the complete interactive course locally without internet: `docker run -d -p 3000:80 ghcr.io/thedoctormes-hue/github-a-to-z:latest`.
* 🏅 **[GitHub Foundations Certification Prep Guide](../certification/foundations.md)** — Official exam domains, test-taking strategy, and 25-question practice exam with detailed answers.
* 🎒 **[GitHub Education & Student Developer Pack Guide](../education/student-pack.md)** — Step-by-step guide to claiming free GitHub Pro, Copilot, and $200k+ in developer perks.
* 🧪 **[GitHub Classroom & Autograding Guide](../education/classroom.md)** — Automating student assignments, running Autograding via GitHub Actions, and anti-cheat best practices.
* 🇷🇺 **[Русская версия (Каноническая)](../../README.md)** — Полный курс (14 модулей + 14 лабораторий + шпаргалка + Зал славы).
* 🇬🇧 **English Version (This Hub)** — Community-driven internationalization hub and translation roadmap.
* 💬 **[Translation Coordination Discussion #38](https://github.com/thedoctormes-hue/github-a-to-z/discussions/38)** — Join our community call for translators and reserve chapters!

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
