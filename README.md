# 🚀 GitHub от А до Я: Полный практический курс

> **Изучаем GitHub прямо внутри GitHub: от первого клика в браузере до CI/CD, релизов, лицензий и AI-агентов через MCP.**  
> Никаких оторванных от жизни слайдов. Только живые репозитории, практические полигоны, культура Git и реальные инструменты 2026 года.

[![Status](https://img.shields.io/badge/Status-Complete%20v1.0-success?style=flat-square)](#)
[![Format](https://img.shields.io/badge/Format-100%25%20Markdown-blue?style=flat-square)](#)
[![Glossary](https://img.shields.io/badge/Glossary-Словарь%20терминов-orange?style=flat-square)](GLOSSARY.md)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)
[![Code of Conduct](https://img.shields.io/badge/Contributor%20Covenant-2.1-4baaaa.svg?style=flat-square)](CODE_OF_CONDUCT.md)
[![Audience](https://img.shields.io/badge/Level-From%20Zero%20to%20Hero-purple?style=flat-square)](#)

---

## 🧭 Навигатор курса

* 📖 **[Словарь терминов (Глоссарий)](GLOSSARY.md)** — карманный переводчик с языка программистов на понятный русский.
* ⚖️ **[Лицензия проекта (MIT)](LICENSE)** — юридический статус материалов курса.
* 🛡️ **[Кодекс поведения (CODE_OF_CONDUCT)](CODE_OF_CONDUCT.md)** — стандарты уважения, этикет и правила сообщества.
* 🤝 **[Правила участия (CONTRIBUTING)](CONTRIBUTING.md)** — как сдавать домашние задания и оформлять PR.

---

## 🗺️ Дорожная карта курса (Curriculum)

```
[Уровень 1: Веб-орбита] ──> [Уровень 2: Консоль & SSH / gh] ──> [Уровень 3: Ветки & PR]
                                                                          │
[Уровень 8: Релизы & Лицензии] <── [Уровень 7: CLI & MCP] <── [Уровень 4-6: OPSEC, Штаб & CI/CD]
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
* Базовая идентификация: `user.name` и `user.email`.
* Безопасная аутентификация:
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

---

## 📁 Структура репозитория

```text
github-a-to-z/
├── README.md                   # Главная страница и навигатор по курсу
├── GLOSSARY.md                 # Карманный словарь терминов с аналогиями
├── LICENSE                     # Официальная лицензия MIT
├── CODE_OF_CONDUCT.md          # Кодекс поведения и стандарты сообщества
├── CONTRIBUTING.md             # Инструкция по выполнению домашних заданий
├── docs/                       # Теоретические и практические главы (00 - 08)
├── labs/                       # Шаблоны и задания лабораторных работ (01 - 08)
└── .github/                    # Рабочие шаблоны GitHub для репозитория
    ├── ISSUE_TEMPLATE/
    └── workflows/
```

---

## 🚦 С чего начать?

Переходите к **[Модулю 0: Разведка на местности](docs/00-intro/README.md)** или загляните в **[Словарь терминов](GLOSSARY.md)**!
