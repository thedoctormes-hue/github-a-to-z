# 🚀 GitHub от А до Я: Полный практический курс

> **Изучаем GitHub прямо внутри GitHub: от первого клика в браузере до CI/CD, релизов, лицензий, архитектуры, цифровой гигиены, вайбкодинга, AI-агентов через MCP, человеко-агентных команд и цитадели безопасности.**  
> Никаких оторванных от жизни слайдов. Только живые репозитории, практические полигоны, культура Git и реальные инструменты 2026 года.

[![Status](https://img.shields.io/badge/Status-Complete%20v1.5-success?style=flat-square)](#)
[![CheatSheet](https://img.shields.io/badge/CheatSheet-Шпаргалка%20Git%20&%20GitHub-yellow?style=flat-square)](CHEATSHEET.md)
[![Format](https://img.shields.io/badge/Format-100%25%20Markdown-blue?style=flat-square)](#)
[![Changelog](https://img.shields.io/badge/Changelog-Keep%20a%20Changelog-blueviolet?style=flat-square)](CHANGELOG.md)
[![Glossary](https://img.shields.io/badge/Glossary-Словарь%20терминов-orange?style=flat-square)](GLOSSARY.md)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)
[![Code of Conduct](https://img.shields.io/badge/Contributor%20Covenant-2.1-4baaaa.svg?style=flat-square)](CODE_OF_CONDUCT.md)
[![Security](https://img.shields.io/badge/Security-Policy%20&%20Advisories-red?style=flat-square)](SECURITY.md)
[![Community Profile](https://img.shields.io/badge/Community%20Profile-100%25-brightgreen?style=flat-square)](#)
[![Audience](https://img.shields.io/badge/Level-From%20Zero%20to%20Hero-purple?style=flat-square)](#)

---

## 🧭 Навигатор курса

* ⚡ **[Шпаргалка разработчика (CHEATSHEET.md)](CHEATSHEET.md)** — карманный экспресс-навигатор по всем командам Git, GitHub CLI, трюкам и стандартам курса.
* 📖 **[Словарь терминов (Глоссарий)](GLOSSARY.md)** — карманный переводчик с языка программистов на понятный русский.
* 📜 **[Журнал изменений (CHANGELOG.md)](CHANGELOG.md)** — официальная хроника обновлений по канону Keep a Changelog.
* ⚖️ **[Лицензия проекта (MIT)](LICENSE)** — юридический статус материалов курса.
* 🛡️ **[Кодекс поведения (CODE_OF_CONDUCT)](CODE_OF_CONDUCT.md)** — стандарты уважения, этикет и правила сообщества.
* 🤝 **[Правила участия (CONTRIBUTING)](CONTRIBUTING.md)** — как сдавать домашние задания и оформлять PR.
* 🛡️ **[Политика безопасности (SECURITY.md)](SECURITY.md)** — регламент ответственного раскрытия уязвимостей (Responsible Disclosure).

---

## 🗺️ Дорожная карта курса (Curriculum)

```
[Уровень 1: Веб-орбита] ──> [Уровень 2: Консоль & SSH / gh] ──> [Уровень 3: Ветки & PR]
                                                                          │
[Уровень 8: Релизы & Лицензии] <── [Уровень 7: CLI & MCP] <── [Уровень 4-6: OPSEC, Штаб & CI/CD]
         │
         └──> [Уровень 9: Архитектура] ──> [Уровень 10: Production-стандарты]
                                                        │
[Уровень 13: Команды & Hybrid] <── [Уровень 12: AI-кодинг & MCP] <── [Уровень 11: Гигиена & Docs]
         │
         └──> [Уровень 14: Цитадель безопасности & Телеметрия (Security & Insights)]
```

### 📍 [Модуль 0: Разведка на местности (Зачем тебе GitHub)](docs/00-intro/README.md)
* Пять жизненных ситуаций новичка: от бесконечного `Ctrl+Z` до Proof of Work в резюме.
* Git против GitHub: программа на компьютере против облачной платформы (аналогия Word vs Google Диск).
* Базовый словарь: Репозиторий, Коммит, README.

### 📍 [Модуль 1: Веб-орбита (GitHub без консоли)](docs/01-web-basics/README.md)
* Регистрация и правила выбора никнейма (твой персональный бренд).
* Три золотых правила старта проекта (Закон бункера: Private First, README-First, Цифровой нотариус).
* Секретный репозиторий `username/username`: визитка твоего профиля.
* **Ачивки профиля (GitHub Achievements):** Pull Shark, Quickdraw, Galaxy Brain, Pair Extraordinaire и правила OPSEC против накруток.
* Волшебная клавиша `.` (VS Code for Web прямо в браузере).
* Экспресс-шпаргалка по Markdown за 5 минут.
* Лабораторная №1: создание и оформление красивого профиля.

### 📍 [Модуль 2: Мост к терминалу (Консоль, SSH & легкий вход через gh)](docs/02-terminal-ssh/README.md)
* Установка Git (Windows, macOS, Linux).
* Базовая идентификация: `user.name` и `user.email`.\n* Безопасная аутентификация:
  * Классический путь: генерация ключей SSH (`ed25519`).
  * Современный экспресс-путь: моментальный вход через GitHub CLI (`gh auth login`).
* Золотой цикл Git: `git init` ➔ `git status` ➔ `git add` ➔ `git commit` ➔ `git push`.
* Синхронизация изменений: `git pull` и `git fetch`.

### 📍 [Модуль 3: Командная инженерия (Ветки, PR & Конфликты)](docs/03-branches-pr/README.md)
* Синдром «Бешеного экскаватора»: почему `main` неприкосновенен.
* Ветка как «Карантин» для безопасных экспериментов (`git switch -c`).
* Pull Request: как читать Diff (зеленые и красные строки).
* Принцип HITL (Human-in-the-Loop): «Агент предлагает — Человек утверждает».
* Клонирование (`clone`) против Форка (`fork`).
* Разбор конфликтов слияния: препарируем `<<<<<<< HEAD` спокойно и без паники.

### 📍 [Модуль 4: Цифровой щит & OPSEC (Безопасность)](docs/04-security-opsec/README.md)
* Анатомия ловушки: почему удаление файла в Git не удаляет пароли из истории.
* Правило OPSEC: «Скомпрометированный ключ = Мертвый ключ (Revoke & Rotate)».
* Идеальный `.gitignore` для учебного и боевого проекта.
* Паттерн `.env` (секреты) против `.env.example` (публичный шаблон).
* Облачный радар GitHub: включение **Push Protection**.
* Стратегия «Лаборатория против Витрины» (The Clean-Slate Release): как выпустить чистый релиз v1.0.0 без мусорной истории черновика.

### 📍 [Модуль 5: Проектный штаб (Issue Ops, Discussions & Projects)](docs/05-project-management/README.md)
* **Лейблы (Labels):** цветовая семафора, глобальный маяк `good first issue` для новичков и фильтрация.
* Разделение этикета: **Issues** (баги и задачи) против **Discussions** (вопросы и общение).
* **Эмоциональный щит и деэскалация:** почему мы благодарим даже за агрессивные тикеты («принцип айкидо») и отделение фактов от шума.
* **Штатные инструменты модерации:** Hide comment, Lock conversation, Block user.
* **Кодекс поведения (Code of Conduct):** защита сообщества через `CODE_OF_CONDUCT.md`.
* Два подхода превращения задачи в код: магические слова `Closes #ID` vs кнопка `Create a branch`.
* GitHub Projects (v2): Канбан-доски с автопилотом статусов и трассируемостью.
* Команда: Коллабораторы (Write access) vs Контрибьюторы (Fork + PR).
* Секретный репозиторий `username/.github`: глобальные шаблоны для всех проектов сразу.

### 📍 [Модуль 6: Роботы на службе (GitHub Actions & Pages)](docs/06-actions-pages/README.md)
* Что такое CI/CD на пальцах: конвейер вместо ручного труда.
* Экономика минут: безлимит для Public, 2000 минут/месяц для Private.
* 4 правила экономии: `timeout-minutes: 5`, фильтры `paths:`, кэш зависимостей.
* **Self-Hosted Runners:** собственный сервер за 0 минут списания (+ закон безопасности OPSEC).
* Анатомия YAML: `on`, `jobs`, `runs-on`, `steps`.
* **Бейджи статуса (Status Badges) & Shields.io:** живой статус CI и витрина в README.
* Бесплатный хостинг сайтов через GitHub Pages за 60 секунд.

### 📍 [Модуль 7: Арсенал инженера будущего (CLI, MCP & AI-агенты)](docs/07-pro-tools/README.md)
* **GitHub CLI (`gh`):** топ-5 консольных команд для скорости.
* **Model Context Protocol (MCP) и ИИ-агенты:**
  * 🟢 Зеленая зона (Must Have): безопасные инструменты для ИИ.
  * 🔴 Красная зона (Must Disable): почему категорически запрещены `merge_pull_request`, `delete_*` и прямой пуш в `main`.
* **Черная магия Git (`git reflog`):** воскрешение случайно удаленных веток и коммитов за 2 шага.

### 📍 [Модуль 8: Выход на орбиту (Релизы, Лицензии & Ground Rules)](docs/08-releases-licenses/README.md)
* **Ground Rules (Табу Git):** шесть категорий файлов, которые категорически нельзя коммитить (тяжелые медиа, дампы баз, артефакты сборки).
* **Юридический щит (Лицензии):** парадокс «All Rights Reserved», подробный разбор MIT, Apache 2.0, GNU GPL v3 и Unlicense.
* **Анатомия официального релиза:** Семантическое версионирование (SemVer `vMAJOR.MINOR.PATCH`), теги в терминале (`git tag`) и публикация GitHub Releases с автогенерацией Release Notes.

### 📍 [Модуль 9: Инженерная гигиена & Архитектура (Синхронизация, FSD, ADR и борьба с хаосом)](docs/09-architecture-hygiene/README.md)
* **Синхронизация локального и удаленного репозитория:** почему `git fetch` безопаснее слепого `git pull`, ювелирный `git pull --rebase`, спасительный карман `git stash` и генеральная уборка мертвых веток через `git fetch --prune`.
* **Гигиена корня и организация каталогов:** запрет на «свалку в корне», разделение ответственности (`src/`, `docs/`, `tests/`, `scripts/`, `assets/`, `configs/`).
* **Модели каталогизации:**
  * Слоистая архитектура против Вертикальных слайсов (Vertical Slice Architecture).
  * Feature-Sliced Design (FSD): понятный путеводитель по уровням `app/` ➔ `pages/` ➔ `widgets/` ➔ `features/` ➔ `entities/` ➔ `shared/` и золотое правило однонаправленного импорта.
* **Архитектурный журнал решений (ADR — Architecture Decision Records):** шаблон и культура фиксации ключевых решений («почему мы выбрали X вместо Y»).
* **Антипаттерны и инженерный сленг:**
  * Спагетти-код: симптомы клубка и пошаговый рефакторинг.
  * Костыли, Велосипеды и Технический долг: когда это допустимо и как не утонуть в процентах.
  * **Карго-культ (Cargo Cult Programming):** бездумное копирование чужих паттернов, микросервисов и оверинжиниринг.
  * Разговорный словарь разработчика (Пуллреквест, Дропнуть, Черипик, Откатить, Задеплоить, Хотфикс, Прод).

### 📍 [Модуль 10: Production-стандарты & Командный аудит (Кроссплатформенность, Защита и Чистая история)](docs/10-production-standards/README.md)
* **Война окончаний строк (CRLF против LF):** как избежать ложного коммита на 10 000 строк и настроить обязательный `.gitattributes`.
* **Три стратегии слияния PR:** Merge Commit vs Rebase vs **Squash and Merge** (почему прод выбирает «Один PR = Один атомарный коммит»).
* **Conventional Commits:** стандарты семантических сообщений коммитов (`feat:`, `fix:`, `refactor:`, `docs:`, `chore:`, `BREAKING CHANGE:`).
* **Цифровой нотариус (Commit Signing):** подпись коммитов через SSH-ключ или GPG, верифицированный бейдж `Verified` на GitHub и защита от спуфинга автора.
* **Автономная безопасность с Dependabot:** авто-сканирование уязвимостей в зависимостях (`package.json`, `requirements.txt`, `go.mod`) и автоматические PR с фиксами.
* **Правила защиты веток (Branch Protection & Rulesets):** обязательный Code Review перед слиянием, прохождение CI-чеков и жесткий запрет `force-push` в прод.
* **Культура Code Review и Suggested Changes:** как предлагать точечные правки в один клик прямо в интерфейсе GitHub PR.

### 📍 [Модуль 11: Инженерная гигиена & Культура документации (Docs-as-Code & Санитарные кордоны)](docs/11-hygiene-and-docs/README.md)
* **Главный закон надежности:** «Пишем то, что делаем, делаем то, что пишем» (культура Single Source of Truth).
* **Анатомия катастрофы: Documentation Drift (Гниение документации):** почему старая документация хуже её отсутствия и почему новичок теряет 4 часа на несуществующих флагах.
* **Закон неразрывного PR (Atomic Docs & Code):** обязательное обновление документации в том же коммите/PR, где изменился код.
* **Разоблачение мифа о «самодокументированном коде»:** код отвечает на вопрос *КАК*, но документация раскрывает *ЗАЧЕМ* и бизнес-контекст.
* **Культура Docs-as-Code и стандарт Keep a Changelog:** профессиональное ведение `CHANGELOG.md` (`Added`, `Changed`, `Deprecated`, `Removed`, `Fixed`, `Security`).
* **Санитария рабочей машины (`~/.gitignore_global`):** защита от позорных коммитов `.DS_Store`, `Thumbs.db` и `.idea/` во все репозитории мира.
* **Санитарный кордон Pre-commit хуков:** автоматический барьер против небрежного форматирования и утечек секретов до создания коммита.
* **Гигиена веточных кладбищ:** автоматическое удаление веток на GitHub (`Automatically delete head branches`) и чистка локальных веток через `git branch -d`.
* **Атомарность коммитов:** категорический запрет на смешивание рефакторинга с правкой бизнес-логики.
* **Гигиена зависимостей и борьба с Bloat:** поучительный кейс `left-pad`, коммит lock-файлов и сканирование уязвимостей.
* **Гигиена внимания (Notification Fatigue):** победа над спамом в GitHub через правильный выбор режимов Watch (Participating vs Releases) и Inbox Zero.

### 📍 [Модуль 12: Новая эра: AI-кодинг, Вайбкодинг, GitHub Copilot, Google Jules и протокол MCP](docs/12-ai-coding-mcp/README.md)
* **Революция Вайбкодинга (Vibe Coding):** манифест Андрея Карпатого — от написания строк к дирижированию ансамблем ИИ-агентов.
* **Две стороны медали:** сверхзвуковое прототипирование за 2 часа против AI Slop, потери контроля и галлюцинаций библиотек (Package Hallucination).
* **Экосистема GitHub Copilot:** Copilot Workspace (решение Issue в спецификацию, план и PR в облаке), Copilot Edits, автогенерация описаний PR и автоматическое ревью.
* **Настройка репозитория для Copilot:** `.github/copilot-instructions.md` как проектный брендбук для ИИ.
* **Google Jules:** автономный облачный AI-инженер, решающий задачи в изолированных песочницах с прогоном тестов.
* **Model Context Protocol (MCP):** архитектура открытого USB-C стандарта (Host ➔ Client ➔ Servers), GitHub MCP Server и безопасное разграничение прав.
* **Контекстная инженерия репозитория:** создание `AGENTS.md` и `.cursorrules` для ликвидации галлюцинаций.
* **Кибербезопасность (AI OPSEC):** векторы Indirect Prompt Injection через тикеты (Issues) и защита изоляцией.
* **Железный закон HITL (Human-in-the-Loop):** ИИ генерирует код, но Человек всегда держит палец на кнопке слияния.

### 📍 [Модуль 13: Синтез разумов: Человеко-агентные команды & Hybrid Engineering](docs/13-human-agent-teams/README.md)
* **Сравнительная анатомия:** Люди против ИИ-агентов (сильные стороны, уязвимости, комплементарность).
* **Адаптация практик человеческих команд (Agile / Scrum для ИИ):**
  * Спецификация как контракт (Spec-Driven Development) вместо расплывчатых диалогов.
  * Definition of Ready (DoR) и жесткий Definition of Done (DoD) для агентов.
  * Блокировка регрессий и контрактные тесты (Safety Harness).
* **Архитектурный паттерн «Агентная Триада» (Agent Triad Pattern):**
  * Planner (Архитектор) ➔ Builder (Инженер) ➔ Auditor (Красная Команда / Red Team) ➔ Human TL (Режиссер и слияние).
* **Специфические патологии ИИ и методы купирования:**
  * Сикофантия (Sycophancy) и соглашательство — как заставить агента сомневаться и спорить.
  * Дрейф контекста (Context Drift) в длинных цепочках вызовов.
  * Опасность Automation Bias (слепое доверие человека к сгенерированному артефакту).
* **GitHub как Single Pane of Glass:** единая панель управления для гибридной команды (Issue Ops, PR Reviews, Projects, Discussions).

### 📍 [Модуль 14: Цитадель безопасности & Телеметрия штаба (Security and quality, Insights & OSINT)](docs/14-security-insights/README.md)
* **Раздел Security and quality:**
  * Политика безопасности `SECURITY.md` и канон Responsible Disclosure (табу на публичные тикеты с 0-day).
  * Private Vulnerability Reporting (PVR) и совместный патчинг в секретной песочнице (Temporary Private Fork).
  * Регистрация международных номеров CVE и публикация бюллетеней в GitHub Security Advisories (GHSA).
  * Превентивное сканирование секретов (Secret Scanning) и Push Protection (блокировка токенов до пуша).
  * Семантический статический анализ кода CodeQL (SAST): поиск уязвимостей (SQLi, XSS, RCE, Path Traversal) в AST-графе без запуска приложения.
  * Активация графа зависимостей (Dependency Graph), алерты Dependabot и экспорт цифрового паспорта ПО SBOM (SPDX/CycloneDX).
* **Раздел Insights (Аналитический радар и OSINT):**
  * Оперативный срез Pulse (24ч, 7 дней, месяц) для статус-отчетов без созвонов.
  * График Contributors и выявление «Bus Factor» (фактора автобуса).
  * Чеклист Community Standards: достижение 100% рейтинга зрелости репозитория.
  * Раздел Traffic: уникальные посетители, клоны, Top Referrers (откуда идут люди) и Popular Content (спасение данных от 14-дневного удаления).
  * Анализ Code Frequency, рентген сети и скрытых форков (Network Graph & Forks).
  * Экономика CI/CD минут и выявление узких мест в Actions usage & performance metrics.

---

## 🧪 Лабораторные полигоны (Hands-on Labs)

Каждый модуль сопровождается практическим заданием в каталоге `labs/`:

| Полигон | Задание | Навык |
| :--- | :--- | :--- |
| **[Lab 01](labs/lab-01-profile/README.md)** | Создать README-визитку профиля с динамическими бейджами | Web UI, Markdown, Git Profile |
| **[Lab 02](labs/lab-02-terminal/README.md)** | Связать терминал с GitHub (SSH или `gh auth`) и запушить проект | Terminal, SSH, `gh`, `git push` |
| **[Lab 03](labs/lab-03-conflicts/README.md)** | Создать ветку, смоделировать конфликт слияния и решить его | Branches, Merge Conflicts, PR |
| **[Lab 04](labs/lab-04-security/README.md)** | Сконфигурировать `.gitignore` и протестировать Push Protection | OPSEC, Git Hygiene |
| **[Lab 05](labs/lab-05-projects/README.md)** | Развернуть доску GitHub Projects, связать Issue и PR через `Closes #` | Issue Ops, Projects v2 |
| **[Lab 06](labs/lab-06-actions/README.md)** | Написать GitHub Action с таймаутом и опубликовать сайт на Pages | CI/CD, GitHub Pages |
| **[Lab 07](labs/lab-07-cli-mcp/README.md)** | Работа в `gh` CLI, воскрешение ветки через `reflog` и конфиг MCP | GitHub CLI, Reflog, MCP Security |
| **[Lab 08](labs/lab-08-release/README.md)** | Добавить лицензию MIT, поставить тег `v1.0.0` и выпустить Release | Licenses, SemVer, GitHub Releases |
| **[Lab 09](labs/lab-09-architecture/README.md)** | Отработать `stash`, `prune`, навести порядок в корне и написать ADR | Git Sync, Root Hygiene, ADR |
| **[Lab 10](labs/lab-10-production/README.md)** | Настроить `.gitattributes`, включить SSH Commit Signing и сделать PR со Squash | `.gitattributes`, Commit Signing, Conventional Commits |
| **[Lab 11](labs/lab-11-hygiene-docs/README.md)** | Настроить `~/.gitignore_global`, автоудаление веток, pre-commit и синхронный CHANGELOG | Pre-commit, Docs-as-Code, Keep a Changelog |
| **[Lab 12](labs/lab-12-ai-mcp/README.md)** | Настроить `copilot-instructions.md`, `AGENTS.md`, MCP и прогнать цикл «От Issue к PR» с аудитом | AI Context, MCP, HITL Audit |
| **[Lab 13](labs/lab-13-human-agent-teams/README.md)** | Сформировать DoD, прогнать цикл Триады (Planner ➔ Builder ➔ Auditor) и провести финальный HITL-ревью | Hybrid Engineering, Agent Triad, Sycophancy Mitigation |
| **[Lab 14](labs/lab-14-security-insights/README.md)** | Активировать Dependency Graph, развернуть `SECURITY.md`, шаблон PR и настроить CodeQL | Security & Quality, Insights, CodeQL, SBOM, OSINT |

---

## 📁 Структура репозитория

```text
github-a-to-z/
├── README.md                   # Главная страница и навигатор по курсу
├── CHEATSHEET.md              # Интерактивная шпаргалка и быстрый навигатор по курсу
├── GLOSSARY.md                 # Карманный словарь терминов с аналогиями
├── CHANGELOG.md                # Официальный журнал изменений (Keep a Changelog)
├── LICENSE                     # Официальная лицензия MIT
├── CODE_OF_CONDUCT.md          # Кодекс поведения и стандарты сообщества
├── CONTRIBUTING.md             # Инструкция по выполнению домашних заданий
├── .gitattributes              # Кроссплатформенная нормализация окончаний строк (LF)
├── SECURITY.md                 # Официальная политика безопасности (Responsible Disclosure)
├── docs/                       # Теоретические и практические главы (00 - 14)
│   ├── ...
│   ├── 13-human-agent-teams/
│   └── 14-security-insights/
├── labs/                       # Шаблоны и задания лабораторных работ (01 - 14)
│   ├── ...
│   ├── lab-13-human-agent-teams/
│   └── lab-14-security-insights/
├── scripts/                    # Автоматизация и валидация целостности ссылок
│   └── validate_links.py
└── .github/                    # Рабочие шаблоны GitHub для репозитория
    ├── copilot-instructions.md # Конфигурация стандартов для GitHub Copilot
    ├── PULL_REQUEST_TEMPLATE.md# Шаблон оформления Pull Request (100% Community Standards)
    ├── ISSUE_TEMPLATE/
    └── workflows/
        └── codeql.yml          # Автоматический SAST-сканер уязвимостей CodeQL
```

---

## 🚦 С чего начать?

Переходите к **[Модулю 0: Разведка на местности](docs/00-intro/README.md)**, держите под рукой **[Шпаргалку разработчика](CHEATSHEET.md)** или загляните в **[Словарь терминов](GLOSSARY.md)**!
