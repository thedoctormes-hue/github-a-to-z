# 🧪 Лабораторная работа №14: Цитадель безопасности & Разведка телеметрии

> **Цель полигона:** на практике развернуть комплексную систему киберзащиты репозитория, активировать граф зависимостей Dependabot, внедрить политику безопасности `SECURITY.md`, поднять рейтинг Community Standards до 100% с помощью `PULL_REQUEST_TEMPLATE.md`, настроить воркфлоу CodeQL и научиться считывать OSINT-телеметрию во вкладке Insights.

---

## 📋 План учений

1. [Шаг 1: Активация Dependency Graph и Dependabot](#шаг-1-активация-dependency-graph-и-dependabot)
2. [Шаг 2: Создание политики безопасности SECURITY.md](#шаг-2-создание-политики-безопасности-securitymd)
3. [Шаг 3: Шаблон Pull Request (PULL_REQUEST_TEMPLATE.md) и взятие 100% Community Standards](#шаг-3-шаблон-pull-request-pull_request_templatemd-и-взятие-100-community-standards)
4. [Шаг 4: Настройка воркфлоу CodeQL Analysis (.github/workflows/codeql.yml)](#шаг-4-настройка-воркфлоу-codeql-analysis-githubworkflowscodeqlyml)
5. [Шаг 5: Анализ вкладки Insights (Traffic, Bus Factor и Network)](#шаг-5-анализ-вкладки-insights-traffic-bus-factor-и-network)
6. [Критерии готовности (Definition of Done)](#критерии-готовности-definition-of-done)

---

## Шаг 1: Активация Dependency Graph и Dependabot

По умолчанию в приватных репозиториях GitHub граф зависимостей может находиться в выключенном состоянии.

1. Откройте ваш репозиторий на GitHub.
2. Перейдите во вкладку **Insights** ➔ выберите в левом меню **Dependency graph**.
3. Если отображается баннер *«Dependency graph is disabled»*, нажмите зеленую кнопку **Enable the dependency graph**.
4. Перейдите во вкладку **Settings** репозитория ➔ раздел слева **Code security and analysis** (или **Security and quality**):
   * Убедитесь, что включены:
     * **Dependency graph** — `Enabled`.
     * **Dependabot alerts** — `Enabled`.
     * **Dependabot security updates** — `Enabled`.
     * **Secret scanning** и **Push protection** — `Enabled`.

> [!TIP]
> Теперь при появлении любой критической уязвимости в зависимостях проекта GitHub сам пришлет уведомление и автоматически откроет PR с обновленной версией библиотеки.

---

## Шаг 2: Создание политики безопасности `SECURITY.md`

Создайте в корне репозитория файл **`SECURITY.md`**:

```markdown
# 🛡️ Security Policy

## Поддерживаемые версии

Мы поддерживаем и выпускаем обновления безопасности для следующих версий проекта:

| Версия | Поддержка безопасности |
| :--- | :--- |
| `1.4.x` | :white_check_mark: Поддерживается |
| `1.3.x` | :white_check_mark: Поддерживается |
| `< 1.3.0`| :x: Устарела (не поддерживается) |

## Сообщение об уязвимости (Reporting a Vulnerability)

Мы серьезно относимся к безопасности нашего проекта и данных пользователей.

> ⚠️ **Пожалуйста, НЕ создавайте публичные GitHub Issues для сообщений об уязвимостях.**  
> Публичные сообщения об уязвимостях могут поставить под угрозу всех пользователей до выпуска официального исправления.

### Как сообщить об уязвимости приватно:

1. **Рекомендуемый способ (Private Vulnerability Reporting):**
   * Перейдите во вкладку **Security and quality** этого репозитория.
   * Нажмите **Advisories** ➔ **Report a vulnerability**.
   * Заполните описание проблемы, шаги воспроизведения (PoC) и потенциальное воздействие.

2. **Запасной канал:**
   * Отправьте письмо на адрес службы безопасности: `security@example.com` (при необходимости зашифруйте PGP-ключом).

### Сроки реакции (SLA)
* Первичный ответ исследователю: в течение **48 часов**.
* Оценка угрозы и план выпуска патча: в течение **7 рабочих дней**.
* Мы обязуемся уведомить вас о выпуске релиза с исправлением и указать вас в благодарностях (Hall of Fame), если вы не возражаете.

## Безопасная гавань (Safe Harbor)

Если вы действуете в рамках этичного исследования (не уничтожаете данные, не нарушаете работу сервиса и даете нам разумное время на исправление перед публикацией), мы обязуемся не предпринимать юридических мер против вас.
```

---

## Шаг 3: Шаблон Pull Request (`PULL_REQUEST_TEMPLATE.md`) и взятие 100% Community Standards

Чтобы довести чеклист зрелости сообщества в разделе **Insights ➔ Community** до заветных **100%**, репозиторию требуется официальный шаблон оформления Pull Request.

Создайте файл **`.github/PULL_REQUEST_TEMPLATE.md`**:

```markdown
## 🎯 Описание Pull Request

<!-- Кратко опишите суть предлагаемых изменений и их архитектурную причину. -->

---

### 📦 Тип изменений
- [ ] 🚀 Новая функциональность (`feat`)
- [ ] 🐛 Исправление ошибки (`fix`)
- [ ] 📝 Обновление документации (`docs`)
- [ ] 🧹 Рефакторинг и гигиена кода (`refactor` / `chore`)
- [ ] 🛡️ Исправление безопасности (`security`)

---

### 🔗 Связанная задача
Closes #<!-- укажите номер задачи, например Closes #14 -->

---

### 🧪 Чеклист самопроверки (Definition of Done)
- [ ] Код протестирован локально, новые тесты добавлены (если применимо).
- [ ] Документация синхронизирована по закону неразрывного PR (`README.md`, `CHANGELOG.md`).
- [ ] В коде отсутствуют захардкоженные пароли, токены и приватные ключи (OPSEC check).
- [ ] Не используются галлюцинированные библиотеки или раздутые зависимости.
- [ ] Переводы строк нормализованы (`LF`), линтеры и форматирование проходят чисто.
```

---

## Шаг 4: Настройка воркфлоу CodeQL Analysis (`.github/workflows/codeql.yml`)

Подключим боевой SAST-сканер кода CodeQL от GitHub.

Создайте файл **`.github/workflows/codeql.yml`**:

```yaml
name: "CodeQL Security Scan"

on:
  push:
    branches: [ "init", "main" ]
  pull_request:
    branches: [ "init", "main" ]
  schedule:
    - cron: '0 6 * * 1' # Запуск каждый понедельник в 06:00 UTC

jobs:
  analyze:
    name: Analyze Code Security
    runs-on: ubuntu-latest
    permissions:
      actions: read
      contents: read
      security-events: write

    strategy:
      fail-fast: false
      matrix:
        language: [ 'javascript-typescript', 'python' ]

    steps:
    - name: Checkout repository
      uses: actions/checkout@v4

    - name: Initialize CodeQL
      uses: github/codeql-action/init@v3
      with:
        languages: ${{ matrix.language }}

    - name: Perform CodeQL Analysis
      uses: github/codeql-action/analyze@v3
      with:
        category: "/language:${{matrix.language}}"
```

---

## Шаг 5: Анализ вкладки Insights (Traffic, Bus Factor и Network)

1. Откройте **Insights** ➔ **Community standards**:
   * Проверьте, что все 8 пунктов отмечены зелеными галочками, а прогресс-бар показывает **100%**.
2. Откройте **Insights** ➔ **Traffic**:
   * Оцените количество уникальных посетителей и клонов за последние 14 дней.
   * Изучите список **Top Referrers** (откуда приходят запросы) и **Popular Content** (какие файлы читают чаще всего).
3. Откройте **Insights** ➔ **Contributors**:
   * Оцените распределение нагрузки и рассчитайте **Bus Factor** проекта.
4. Откройте **Insights** ➔ **Network**:
   * Изучите топологическую карту коммитов и проверьте наличие форков.

---

## Критерии готовности (Definition of Done)

- [x] Активирован **Dependency graph** и включены алерты Dependabot.
- [x] В корне проекта развернут файл **`SECURITY.md`**.
- [x] В каталоге `.github/` развернут шаблон **`PULL_REQUEST_TEMPLATE.md`**.
- [x] Раздел **Insights ➔ Community standards** имеет оценку **100%**.
- [x] В каталоге `.github/workflows/` настроен автоматический сканер **`codeql.yml`**.
- [x] Проведен аудит вкладки **Insights** (Traffic, Contributors, Pulse).
---

## 🧭 Навигация

* 🔙 **Теория модуля:** [Модуль 14: Цитадель безопасности & Телеметрия](../../docs/14-security-insights/README.md)
* 🗺️ **Навигатор курса:** [Главная страница курса](../../README.md)
* 🏆 **Поздравляем!** Вы успешно прошли все 14 модулей и лабораторий курса «GitHub от А до Я»!
