# 🧪 Лабораторная работа №13: Оркестрация Агентной Триады и гибридный спринт

> **Практический полигон к Модулю 13.**  
> Осваиваем дирижирование смешанной командой «Человек + Агенты»: настраиваем шаблон задач с критериями Definition of Done (DoD), моделируем этапы Агентной Триады (Исследователь ➔ Билдер ➔ Аудитор) и проводим финальный арбитраж по канону Human-in-the-Loop.

[![Lab](https://img.shields.io/badge/Lab-13-blue?style=flat-square)](#)
[![Complexity](https://img.shields.io/badge/Complexity-Advanced-red?style=flat-square)](#)
[![Focus](https://img.shields.io/badge/Pattern-Multi--Agent%20Orchestration-success?style=flat-square)](#)

---

## 🎯 Цели полигона

По итогам выполнения этой работы вы:
1. Создадите специализированный шаблон задач с критериями Definition of Done (DoD) для гибридных команд.
2. Отработаете этап **Исследователя (Researcher / Planner)**: сбор контекста и формирование спецификации без написания кода.
3. Отработаете этап **Билдера (Builder / Coder)**: реализацию задачи строго по спецификации в изолированной ветке с тестами.
4. Смоделируете этап **Аудитора (Auditor / Red Team)**: беспристрастное ревью PR на уязвимости, AI Slop и галлюцинации пакетов с оформлением `Suggested Changes`.
5. Проведете финальный арбитраж Человека-Тимлида (HITL) и выполните безопасное слияние Squash and Merge.

---

## 🛠️ Шаг 1: Создание шаблона задач с Definition of Done

Чтобы задачи ставились четко и без двусмысленностей, создадим в `.github/ISSUE_TEMPLATE/` шаблон задачи для агентов.

Создайте файл `.github/ISSUE_TEMPLATE/agent_task.md`:

```markdown
---
name: "🤖 Агентная задача (Agent Task)"
description: "Структурированное задание для ИИ-агентов с критериями DoD"
title: "[AGENT]: "
labels: ["agent-task", "needs-triage"]
---

### 🎯 1. Цель задачи (User Story)
<!-- Опишите, ЧТО нужно сделать и ЗАЧЕМ -->

### 📋 2. Входные требования и контекст
- **Затронутые модули:** `src/...`
- **Зависимости:** (только проверенные стандартные библиотеки)
- **Ограничения:** 

### ✅ 3. Критерии приемки (Acceptance Criteria)
- [ ] Функция корректно обрабатывает стандартные входные данные
- [ ] Обработаны краевые случаи (пустые строки, некорректные типы, None)
- [ ] Время выполнения не превышает установленных лимитов

### 🛡️ 4. Definition of Done (DoD) перед открытием PR
- [ ] Все юнит-тесты на `pytest` зеленые
- [ ] Линтер `ruff check` завершился с кодом 0
- [ ] Документация в `README.md` и запись в `CHANGELOG.md` синхронизированы
- [ ] Нет галлюцинированных зависимостей и вымышленных пакетов
- [ ] Коммиты оформлены по стандарту Conventional Commits
```

Зафиксируйте создание шаблона:
```bash
git add .github/ISSUE_TEMPLATE/agent_task.md
git commit -m "feat(templates): add agent task issue template with strict DoD"
```

---

## 🛠️ Шаг 2: Моделирование Фазы 1: Исследователь (Planner)

Представим, что мы получили задачу: **«Реализовать генератор безопасных криптографических токенов для сессий»**.

### Поведение Агента-Исследователя:
Исследователь **НЕ ПИШЕТ РАБОЧИЙ КОД**. Он изучает кодовую базу, ищет стандартные библиотеки и формулирует спецификацию.

Создайте файл спецификации `docs/specs/token-generator-spec.md`:

```markdown
# Архитектурная спецификация: Модуль генерации токенов

## 1. Анализ библиотек
- ❌ Отклонено: использование `random` (не является криптографически стойким, уязвимо к предсказанию сида).
- ❌ Отклонено: установка внешних пакетов из npm/PyPI (риск зависимости, bloat).
- ✅ Выбрано: стандартный модуль Python `secrets` и класс `secrets.token_urlsafe`.

## 2. Контракт функции
- Путь: `src/security.py`
- Сигнатура: `generate_secure_token(nbytes: int = 32) -> str`
- Валидация: `nbytes` должен быть целым положительным числом >= 16.

## 3. План реализации для Билдера
1. Создать `src/security.py` с функцией `generate_secure_token`.
2. Написать тесты `tests/test_security.py` (проверка длины, энтропии и валидации аргументов).
3. Обновить `CHANGELOG.md` в секции `[Unreleased]`.
```

Зафиксируйте спецификацию:
```bash
git add docs/specs/token-generator-spec.md
git commit -m "docs(spec): create architecture plan for secure token generator"
```

---

## 🛠️ Шаг 3: Моделирование Фазы 2: Билдер (Builder)

Билдер берет спецификацию от Исследователя и пишет код **строго по плану в отдельной ветке**.

### 1. Создаем ветку:
```bash
git switch -c feat/secure-token-generator
```

### 2. Создаем код `src/security.py`:
```python
# src/security.py
import secrets

def generate_secure_token(nbytes: int = 32) -> str:
    """Генерирует криптографически стойкий URL-безопасный токен."""
    if not isinstance(nbytes, int) or nbytes < 16:
        raise ValueError("Параметр nbytes должен быть целым числом не менее 16")
    return secrets.token_urlsafe(nbytes)
```

### 3. Создаем тесты `tests/test_security.py`:
```python
# tests/test_security.py
import pytest
from src.security import generate_secure_token

def test_token_generation_length():
    token = generate_secure_token(32)
    assert isinstance(token, str)
    assert len(token) > 32

def test_token_uniqueness():
    token1 = generate_secure_token(32)
    token2 = generate_secure_token(32)
    assert token1 != token2

def test_invalid_nbytes():
    with pytest.raises(ValueError):
        generate_secure_token(8)  # Меньше 16 байт недопустимо
```

### 4. Синхронное обновление документации (DoD):
В `CHANGELOG.md` (секция `[Unreleased]`):
```markdown
### Added
- Модуль криптографической генерации токенов `generate_secure_token` (`src/security.py`).
```

### 5. Фиксация коммита и открытие PR:
```bash
git add src/security.py tests/test_security.py CHANGELOG.md
git commit -m "feat(security): implement cryptographically secure token generator"
git push -u origin feat/secure-token-generator
```

---

## 🛠️ Шаг 4: Моделирование Фазы 3: Аудитор (Auditor / Red Team)

Аудитор заходит в открытый Pull Request с позиций «Красной Команды» и проверяет код по чек-листу:

* [x] **Проверка на галлюцинации библиотек:** Использован стандартный модуль `secrets` вместо непроверенных внешних пакетов. Чисто!
* [x] **Проверка на AI Slop:** Код лаконичен (8 строк), без лишних абстракций, фабрик и оверинжиниринга. Чисто!
* [x] **Проверка краевых случаев:** Отрицательные и слишком малые `nbytes` вызывают `ValueError`. Чисто!
* [x] **Проверка синхронности:** `CHANGELOG.md` обновлен в том же коммите. Чисто!

Если Аудитор находит мелкое замечание (например, отсутствие docstring с примером), он оставляет в PR комментарий с синтаксисом ` ```suggestion `:

```markdown
```suggestion
def generate_secure_token(nbytes: int = 32) -> str:
    """Генерирует криптографически стойкий URL-безопасный токен.
    
    Пример:
        >>> token = generate_secure_token(32)
        >>> len(token) >= 32
        True
    """
```
```

---

## 🛠️ Шаг 5: Финальный арбитраж Человека (HITL)

Человек-Тимлид проверяет:
1. Прохождение всех автоматических проверок GitHub Actions (зеленый значок).
2. Одобрение (Approve) от Аудитора.
3. Соблюдение бизнес-целей.

После этого Тимлид нажимает **Squash and Merge**. Ветка `feat/secure-token-generator` автоматически удаляется. Задача закрыта!

---

## 🏆 Критерии готовности (Definition of Done)

* [ ] Создан шаблон задачи `.github/ISSUE_TEMPLATE/agent_task.md` с критериями DoD.
* [ ] Отработан этап Исследователя (архитектурная спецификация без преждевременного кодинга).
* [ ] Отработан этап Билдера (код с юнит-тестами строго по спецификации).
* [ ] Отработан этап Аудитора (Zero-Trust аудит на галлюцинации и AI Slop).
* [ ] Проведен финальный человеческий контроль по протоколу HITL.

Поздравляем! Вы освоили высший пилотаж современной программной инженерии — слаженное дирижирование гибридными командами людей и кремниевых агентов!
