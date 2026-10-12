# Changelog

Все заметные изменения в образовательном курсе **«GitHub от А до Я»** документируются в этом файле.

Формат основан на [Keep a Changelog](https://keepachangelog.com/ru/1.1.0/),
и проект следует принципам [Семантического версионирования](https://semver.org/lang/ru/).

---

## [Unreleased]

### Added
- **`CONTRIBUTING.md`**: Официальное руководство для студентов и контрибьюторов по сдаче лабораторных работ, правилам форков, ветвлению, Conventional Commits и стандартам Definition of Done.
- **Двусторонняя навигация в лабораториях (Labs Navigation Matrix)**: В каждую из 14 лабораторных работ добавлен блок «🧭 Навигация» с прямыми переходами назад к теории соответствующего модуля, к следующему модулю курса и на главную страницу `README.md`.

### Fixed
- **Целостность относительных ссылок (Relative Path Integrity)**: Исправлены некорректные относительные пути `../labs/` на `../../labs/` в модулях `docs/02` — `docs/10`.
- **Связность Модуля 1 и Лабораторной 1**: Добавлен прямой переход из `docs/01-web-basics/README.md` в `labs/lab-01-profile/README.md`.
- **Анкоры кириллических заголовков и пунктуации (Slug Integrity)**:
  - `GLOSSARY.md`: исправлены анкоры алфавитного указателя (`#английские-термины-az`, `#русские-термины-ая`) и терминов с разделителями (`/`, `&`).
  - `docs/11-hygiene-and-docs/README.md`: исправлен анкор раздела с тире (один дефис вместо двух).
  - `docs/14-security-insights/README.md`: нормализованы 10 анкоров оглавления, содержавших разделитель `&` (один дефис вместо двойного).

### Added
- **Модуль 14 (Цитадель безопасности & Телеметрия штаба: Security and quality, Insights, CodeQL, SBOM и OSINT репозитория):**
  - Подробный разбор вкладки **Security and quality**: политика `SECURITY.md`, Responsible Disclosure, запрет публичных тикетов для эксплойтов.
  - Канал Private Vulnerability Reporting (PVR) и процесс безопасного патчинга через Temporary Private Fork.
  - Регистрация международных CVE и публикация бюллетеней в GitHub Security Advisories (GHSA).
  - Превентивное сканирование секретов (Secret Scanning) и блокировка пушей с токенами (Push Protection).
  - Семантический статический анализ кода движком CodeQL (SAST): поиск уязвимостей (SQLi, XSS, RCE, Path Traversal) на графе AST и потоках данных (Source ➔ Taint ➔ Sink).
  - Активация графа зависимостей (Dependency Graph), алерты Dependabot и экспорт цифрового паспорта ПО SBOM (SPDX/CycloneDX).
  - Подробный разбор вкладки **Insights**: оперативный срез Pulse (24ч, 7 дней, месяц), график активности Contributors и расчет Bus Factor (фактора автобуса).
  - Официальный скоринг Community Standards и получение рейтинга 100%.
  - Раздел Traffic: метрики уникальных посетителей, клонов, Top Referrers (источники трафика) и Popular Content (ограничение 14 дней).
  - Частота кода (Code Frequency), карта коммитов, рентген сети и форков (Network Graph & Forks).
  - Экономика и производительность Actions usage & performance metrics.
- **Лабораторная работа №14:**
  - Активация Dependency Graph и Dependabot alerts в веб-интерфейсе.
  - Развертывание корневого файла `SECURITY.md` с политикой Responsible Disclosure и контактами безопасности.
  - Создание официального шаблона Pull Request `.github/PULL_REQUEST_TEMPLATE.md` для взятия 100% Community Standards.
  - Настройка боевого воркфлоу CodeQL Analysis (`.github/workflows/codeql.yml`).
  - Практический аудит вкладки Insights (Traffic, Bus Factor, Community score).
- Корневой файл политики безопасности `SECURITY.md`.
- Официальный шаблон Pull Request `.github/PULL_REQUEST_TEMPLATE.md`.
- CI/CD воркфлоу статического сканирования `.github/workflows/codeql.yml`.

### Changed
- Обновлен `GLOSSARY.md` (добавлены термины CodeQL, Community Standards, CVE, Dependency Graph, GHSA, Network Graph, PVR, Pulse, SAST, SBOM, Secret Scanning, Security Policy, Top Referrers, Traffic).
- Актуализирована витрина `README.md` (дорожная карта 14 уровней, матрица 14 лабораторий, бейджи, дерево репозитория).

---

## [1.4.0] - 2026-10-12

### Added
- **Модуль 13 (Синтез разумов: Человеко-агентные команды & Hybrid Engineering):**
  - Сравнительная анатомия: Человек-инженер против ИИ-агента (скорость, выносливость, амнезия контекста, эго, ответственность).
  - Перенос институтов человеческой командной инженерии на ИИ: онбординг через `AGENTS.md`, постановка задач через Definition of Done (DoD).
  - Паттерн «Агентная Триада» (The Agent Triad Pattern): разделение властей на Исследователя (Planner), Билдера (Coder) и Аудитора (Red Team).
  - Борьба с синдромом угодничества (Sycophancy) и презумпция незнания: протокол «Не уверен — остановись и спроси человека».
  - GitHub как Единый Центр Управления (Single Pane of Glass): взаимодействие людей и кремниевых агентов через Issues, PR и GitHub Actions.
  - Опасности гибридных команд: эффект автопилота (Automation Bias), деградация контекста (Context Drift) и методы защиты.
  - Манифест гибридной инженерии (Hybrid Engineering Manifesto).
- **Лабораторная работа №13:**
  - Создание специализированного шаблона `.github/ISSUE_TEMPLATE/agent_task.md` с критериями DoD.
  - Практика оркестрации Агентной Триады: фаза архитектурной спецификации, фаза реализации в ветке, фаза аудита и человеческий арбитраж HITL.

---

## [1.3.0] - 2026-10-12

### Added
- **Модуль 12 (Новая эра: AI-кодинг, Вайбкодинг, GitHub Copilot, Google Jules и протокол MCP):**
  - Феномен вайбкодинга (Vibe Coding) Андрея Карпатого: переход от ручного кодинга к дирижированию моделями.
  - Две стороны медали: сверхзвуковая скорость прототипирования против накопления AI Slop и угрозы Package Hallucinations.
  - Экосистема GitHub Copilot: Copilot Workspace (от Issue к плану и PR в браузере), Copilot Edits, Copilot PR Summaries и Code Review.
  - Автономный облачный инженер Google Jules: цикл решения тикетов в изолированной облачной песочнице с автотестами.
  - Model Context Protocol (MCP): открытый индустриальный стандарт Anthropic, архитектура Host-Client-Server, GitHub MCP Server.
  - Контекстная инженерия репозитория: конфигурация `.github/copilot-instructions.md`, `AGENTS.md` и `.cursorrules`.
  - Кибербезопасность в эпоху AI (AI OPSEC): векторы Indirect Prompt Injection через Issues/PR и непреложный закон HITL (Human-in-the-Loop).
- **Лабораторная работа №12:**
  - Настройка `.github/copilot-instructions.md`, манифеста `AGENTS.md`, конфигурации MCP и отработка полного цикла «От Issue к PR» с проверкой на галлюцинации и ручным слиянием HITL.
- Корневой конфигурационный файл `.github/copilot-instructions.md`.

---

## [1.2.0] - 2026-10-12

### Added
- **Модуль 11 (Инженерная гигиена & Культура документации):**
  - Принцип «Пишем то, что делаем, делаем то, что пишем» и ликвидация документационного дрифта (Documentation Drift).
  - Разоблачение мифа о «самодокументированном коде» (разница между «КАК» и «ЗАЧЕМ»).
  - Docs-as-Code: стандарт Keep a Changelog, триада репозитория (`README.md`, `CHANGELOG.md`, `CONTRIBUTING.md`).
  - Глобальная санитария машины: настройка `~/.gitignore_global` против мусора macOS (`.DS_Store`) и Windows (`Thumbs.db`).
  - Санитарные предкоммитные кордоны (Pre-commit hooks).
  - Ликвидация веточных свалок: настройка GitHub «Automatically delete head branches».
  - Атомарность коммитов: правило разделения рефакторинга и бизнес-логики.
  - Гигиена зависимостей: борьба с синдромом сороки (Dependency Bloat) и фиксация lock-файлов.
  - Гигиена внимания: защита от Notification Fatigue (Watching, Participating, Ignore, GitHub Inbox).
- **Лабораторная работа №11:**
  - Практика настройки `~/.gitignore_global`, создания pre-commit хука и оформления неразрывного коммита (код + дока + changelog).
- Корневой файл `CHANGELOG.md` в репозитории как практический образец Keep a Changelog.

---

## [1.1.0] - 2026-10-12

### Added
- **Модуль 09 (Инженерная гигиена & Архитектура):**
  - Синхронизация репозиториев: `git fetch` против `git pull`, `git pull --rebase`, карман `git stash`, чистка устаревших ссылок `git fetch --prune`.
  - Гигиена корня (Root Hygiene) и организация структуры каталогов.
  - Модели каталогизации: Layered vs Vertical Slices, Feature-Sliced Design (FSD) и однонаправленный поток импортов.
  - Журнал архитектурных решений (ADR — Architecture Decision Records).
  - Антипаттерны: спагетти-код, костыли, велосипеды, технический долг, карго-культ (Cargo Cult Programming).
  - Словарь профессионального сленга разработчиков.
- **Лабораторная работа №09:**
  - Отработка `stash`, `prune`, рефакторинг структуры корня и составление ADR (`docs/adr/0001-init-structure.md`).
- **Модуль 10 (Production-стандарты & Командный аудит):**
  - Кроссплатформенная война CRLF vs LF и конфигурация `.gitattributes`.
  - Стратегии слияния PR: Merge Commit, Rebase, Squash and Merge.
  - Семантические коммиты (Conventional Commits).
  - Цифровой нотариус: криптографическая подпись коммитов через SSH-ключ (`Verified` бейдж).
  - Автономный мониторинг безопасности зависимостей через Dependabot.
  - Защита веток (Branch Protection Rulesets) и правила Code Review (Suggested Changes).
- **Лабораторная работа №10:**
  - Настройка `.gitattributes`, включение SSH-подписи коммитов, создание PR по стандарту Conventional Commits и слияние через Squash.
- Корневой конфигурационный файл `.gitattributes` (`* text=auto eol=lf`).

### Changed
- Обновлен `GLOSSARY.md` (добавлены архитектурные, сленговые и продакшн-термины).
- Обновлена дорожная карта и структура проекта в `README.md`.

---

## [1.0.0] - 2026-10-12

### Added
- **Модуль 00 (Разведка на местности):** Зачем нужен GitHub, 5 жизненных ситуаций, Git vs GitHub.
- **Модуль 01 (Веб-орбита):** Регистрация, закон бункера, профиль-визитка, достижения (Achievements), веб-редактор.
- **Модуль 02 (Мост к терминалу):** Установка Git, SSH-ключи (`ed25519`), GitHub CLI (`gh`), базовый цикл коммитов.
- **Модуль 03 (Командная инженерия):** Ветки, Pull Requests, чтение диффа, принцип HITL, форки, разрешение конфликтов слияния.
- **Модуль 04 (Цифровой щит & OPSEC):** Безопасность секретов, `.gitignore`, `.env`, Push Protection, Clean-Slate релиз.
- **Модуль 05 (Проектный штаб):** Issue Ops, Discussions, цветовые лейблы, Projects v2 Канбан, Кодекс поведения (`CODE_OF_CONDUCT.md`), деэскалация конфликтов.
- **Модуль 06 (Роботы на службе):** Введение в CI/CD, GitHub Actions, экономика минут, Self-Hosted Runners, бейджи статуса, GitHub Pages.
- **Модуль 07 (Арсенал инженера будущего):** GitHub CLI pro-команды, MCP протокол для ИИ-агентов (безопасные зоны), `git reflog`.
- **Модуль 08 (Выход на орбиту):** Табу-файлы Git, юридические лицензии (MIT, Apache 2.0, GPLv3), семантическое версионирование SemVer и GitHub Releases.
- Практические лабораторные полигоны с Lab 01 по Lab 08.
- Карманный словарь терминов `GLOSSARY.md` с аналогиями и русскоязычным предметным указателем.
- Юридическая лицензия MIT (`LICENSE`) и правила участия (`CONTRIBUTING.md`).
- Стандарты сообщества и кодекс поведения (`CODE_OF_CONDUCT.md`).
- Шаблоны issues (`.github/ISSUE_TEMPLATE/`) и CI воркфлоу (`.github/workflows/ci.yml`).
