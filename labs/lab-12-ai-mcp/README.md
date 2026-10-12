# 🧪 Лабораторная работа №12: Контекстная инженерия для ИИ, MCP и протокол HITL

> **Практический полигон к Модулю 12.**  
> Учимся настраивать репозиторий для эффективного и безопасного взаимодействия с ИИ-агентами: создаем `.github/copilot-instructions.md`, оформляем `AGENTS.md`, конфигурируем коннектор MCP и отрабатываем сценарий «От задачи к PR» с непреложным правилом Human-in-the-Loop.

[![Lab](https://img.shields.io/badge/Lab-12-blue?style=flat-square)](#)
[![Complexity](https://img.shields.io/badge/Complexity-Intermediate%2FAdvanced-orange?style=flat-square)](#)
[![Theme](https://img.shields.io/badge/Focus-AI%20Context%20%26%20MCP%20Guardrails-purple?style=flat-square)](#)

---

## 🎯 Цели полигона

По итогам выполнения этой работы вы:
1. Создадите файл инструкций для GitHub Copilot: `.github/copilot-instructions.md`.
2. Оформите системный манифест для автономных агентов `AGENTS.md` с фиксацией рамок дозволенного и команд проверки.
3. Сконфигурируете коннектор Model Context Protocol (MCP) для работы с репозиторием.
4. Отработаете полный цикл решения задачи через агента (симуляция Jules / Copilot Workspace): Issue ➔ ветка ➔ PR.
5. Проведете строгий аудит сгенерированного кода по протоколу HITL (проверка на Package Hallucination и скрытые уязвимости).

---

## 🛠️ Шаг 1: Создание `.github/copilot-instructions.md`

Чтобы GitHub Copilot в веб-интерфейсе и редакторах понимал специфику вашего проекта и не предлагал устаревший код, зададим проектные стандарты.

### 1. Создаем директорию и файл:
```bash
mkdir -p .github
touch .github/copilot-instructions.md
```

### 2. Заполняем правила проекта:
Откройте `.github/copilot-instructions.md` и вставьте:

```markdown
# Инструкции для GitHub Copilot в репозитории

## 1. Базовый стек и версии
- Язык: Python 3.12+ (строгая статическая типизация через typing).
- Форматирование: PEP 8, длина строки 100 символов.
- Логирование: использовать библиотеку loguru или стандартный logging, запрет на print().

## 2. Архитектурные правила
- Следовать модульной структуре: бизнес-логика отделена от интерфейса и роутов.
- При создании новых утилит обязательно документировать их в README.md и CHANGELOG.md (закон синхронности истины).

## 3. Требования к тестам
- Все функции должны сопровождаться юнит-тестами на pytest.
- Тесты должны проверять как успешное выполнение, так и краевые случаи (None, пустые строки, некорректные типы).

## 4. Безопасность (AI OPSEC)
- Никогда не хардкодить токены, пароли и секреты в примерах кода.
- Использовать переменные окружения через os.getenv() или pydantic-settings.
```

Зафиксируйте файл:
```bash
git add .github/copilot-instructions.md
git commit -m "docs(ai): add copilot-instructions configuration"
```

---

## 🛠️ Шаг 2: Создание манифеста агентов `AGENTS.md`

Для автономных агентов (Claude Code, Google Jules, Cursor, Antigravity) создадим единый манифест правил в корне проекта.

Создайте файл `AGENTS.md` следующего содержания:

```markdown
# AGENTS.md — Манифест правил для ИИ-агентов

Добро пожаловать в репозиторий. Вы действуете в роли AI Software Engineer.
Перед началом любых изменений ознакомьтесь с ограничениями:

## 1. Границы полномочий и безопасность
- ❌ ЗАПРЕЩЕНО: выполнять прямой git push в ветку main/init.
- ❌ ЗАПРЕЩЕНО: сливать Pull Request'ы напрямую (принцип Human-in-the-Loop).
- ❌ ЗАПРЕЩЕНО: добавлять зависимости без проверки их существования в официальных реестрах.
- ✅ РАЗРЕШЕНО: исследовать кодовую базу, создавать feature-ветки, писать код, запускать тесты, открывать Pull Request.

## 2. Обязательный санитарный конвейер
Перед открытием любого Pull Request агент обязан убедиться в выполнении проверок:
- Линтер: ruff check .
- Тесты: pytest tests/
- Документация: обновлены README.md и секция [Unreleased] в CHANGELOG.md.

## 3. Формат сообщений коммитов
Все коммиты должны строго следовать стандарту Conventional Commits:
feat(scope): краткое описание
fix(scope): исправление бага
docs(scope): обновление документации
```

Зафиксируйте файл:
```bash
git add AGENTS.md
git commit -m "docs(ai): establish AGENTS.md operational guardrails"
```

---

## 🛠️ Шаг 3: Конфигурация коннектора Model Context Protocol (MCP)

Чтобы ИИ-ассистент в вашей среде (Cursor, VS Code, Claude Desktop, Antigravity) мог работать с репозиторием через стандартизированный протокол MCP, создается файл конфигурации.

Создайте пример конфигурации `mcp-config.example.json`:

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "github_pat_11A...your_fine_grained_token_here"
      }
    }
  }
}
```

> **Внимание (OPSEC & Fine-Grained PAT):**  
> 1. Никогда не коммитьте боевой токен! Файл с токеном должен быть надежно скрыт в `.gitignore`.  
> 2. **Используйте Fine-Grained PAT (`github_pat_...`)**, а не устаревший Classic `ghp_...`. Настройте скоуп строго на один репозиторий с ограниченными правами (Contents: Read, Pull Requests: Read & Write) и сроком жизни не более 30 дней.

---

## 🛠️ Шаг 4: Отработка сценария «От Issue к PR» (Паттерн Jules / Workspace)

Смоделируем сценарий, по которому работают современные автономные агенты:

### 1. Постановка задачи (Создание Issue):
Создайте тикет с описанием задачи:
* **Заголовок:** `feat: добавить валидатор email-адресов`
* **Описание:** 
  > Необходимо реализовать функцию `validate_email(email: str) -> bool` в `src/validators.py`.  
  > Функция должна проверять базовую структуру email (наличие `@`, доменной точки, отсутствие пробелов).  
  > Написать тесты в `tests/test_validators.py`.

### 2. Агентная разработка (ветка фичи):
Создайте ветку:
```bash
git switch -c feat/email-validator
```

Создайте модуль валидации `src/validators.py`:
```python
# src/validators.py
import re

EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")

def validate_email(email: str) -> bool:
    """Проверяет корректность формата адреса электронной почты."""
    if not isinstance(email, str):
        return False
    return bool(EMAIL_REGEX.match(email.strip()))
```

Создайте тест `tests/test_validators.py`:
```python
# tests/test_validators.py
from src.validators import validate_email

def test_valid_emails():
    assert validate_email("user@example.com") is True
    assert validate_email("dev.ops+test@domain.org") is True

def test_invalid_emails():
    assert validate_email("plainaddress") is False
    assert validate_email("@missinguser.com") is False
    assert validate_email("user@domain") is False
    assert validate_email("") is False
```

### 3. Закон неразрывного PR:
Обновите `CHANGELOG.md` в секции `[Unreleased]`:
```markdown
### Added
- Модуль валидации email-адресов `validate_email` (`src/validators.py`).
```

### 4. Создание коммита и отправка PR:
```bash
git add src/validators.py tests/test_validators.py CHANGELOG.md
git commit -m "feat(validator): add validate_email helper with test suite"
git push -u origin feat/email-validator
```

Создайте Pull Request на GitHub с текстом:  
`Closes #<номер_тикета>`

---

## 🛠️ Шаг 5: Протокол аудита HITL (Human-in-the-Loop)

Перед тем как нажать зеленую кнопку слияния, проведите обязательный аудит кода:

1. **Проверка на галлюцинации библиотек (Package Hallucination):**  
   Использует ли сгенерированный код стандартную библиотеку `re` или пытается импортировать сомнительный внешний пакет? (В нашем коде используется стандартный модуль Python `re` — отлично!).
2. **Проверка тестов:**  
   Запустите тесты локально: `pytest tests/test_validators.py`. Убедитесь, что все тесты зеленые.
3. **Проверка диффа (Diff Inspection):**  
   Нет ли лишних изменений в других файлах? Нет ли случайных изменений окончаний строк CRLF?
4. **Утверждение (Merge):**  
   Только после прохождения всех 3 проверок человек нажимает **Squash and Merge**.

---

## 🏆 Критерии готовности (Definition of Done)

* [ ] В каталоге `.github/` создан и закоммичен файл `copilot-instructions.md`.
* [ ] В корне проекта присутствует манифест `AGENTS.md` с описанием правил для ИИ.
* [ ] Добавлен шаблон конфигурации MCP сервера `mcp-config.example.json`.
* [ ] Отработан сценарий «Issue ➔ Ветка ➔ Код с тестами ➔ PR с синхронным Changelog».
* [ ] Проведен аудит по протоколу HITL.

Поздравляем! Вы полностью оснащены современными инструментами AI-кодинга и умеете безопасно дирижировать агентами в промышленном контуре!
---

## 🧭 Навигация

* 🔙 **Теория модуля:** [Модуль 12: AI-кодинг & MCP](../../docs/12-ai-coding-mcp/README.md)
* 🗺️ **Навигатор курса:** [Главная страница курса](../../README.md)
* ⏭️ **Следующий модуль:** [Модуль 13: Человеко-агентные команды](../../docs/13-human-agent-teams/README.md)
