# 🧪 Лабораторная работа №7: Арсенал Pro-инструментов (CLI, Reflog и MCP)

> **Цель работы:** Освоить консольное управление через GitHub CLI, провести спасательную операцию удаленного кода через `git reflog` и составить безопасную конфигурацию MCP-инструментов для ИИ-ассистента.

---

## 📋 Пошаговый сценарий

### Шаг 1. Экспресс-тест GitHub CLI (`gh`)
Убедись, что GitHub CLI авторизован на компьютере:
```bash
gh auth status
```

Попробуй выполнить три быстрые команды прямо из терминала:
```bash
# 1. Посмотреть информацию о текущем репозитории
gh repo view

# 2. Создать новую задачу через консоль
gh issue create --title "test: проверить работу утилиты gh" --body "Создано автоматически из терминала"

# 3. Посмотреть список открытых задач
gh issue list
```
*Обрати внимание: всё создается и синхронизируется с сайтом за 2 секунды без открытия браузера!*

---

### Шаг 2. Спасательная операция: Воскрешение через `git reflog` 🚑

Сейчас мы смоделируем кошмар любого разработчика и сразу научимся его побеждать.

1. Создай экспериментальную ветку и сделай в ней важный коммит:
   ```bash
   git switch -c secret-feature
   echo "Супер-важный код, который писался неделю" > secret.py
   git add secret.py
   git commit -m "feat: критически важная функция"
   ```

2. Переключись в `main` и **принудительно удали эту ветку**:
   ```bash
   git switch main
   git branch -D secret-feature
   ```
   *Git удалил ветку. Файл `secret.py` исчез с диска.*

3. **Запускаем спасательную операцию:**
   Открой журнал черного ящика:
   ```bash
   git reflog
   ```
   Найди строку с сообщением: `commit: feat: критически важная функция`.  
   В начале строки будет 7-значный хэш (например, `a1b2c3d`).

4. **Воскреси ветку:**
   ```bash
   git switch -c resurrected-feature <твой-хэш>
   ```

5. Проверь папку: файл `secret.py` снова на диске, а история коммитов полностью восстановлена! Катастрофа предотвращена.

---

### Шаг 3. Создание безопасного конфигурационного файла MCP 🛡️

Представь, что ты настраиваешь ИИ-ассистента (например, в Cursor, Antigravity или Claude) для работы со своим репозиторием.

Создай в проекте образец безопасного файла настроек `mcp-config.example.json`:

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "YOUR_FINE_GRAINED_TOKEN"
      },
      "securityPolicy": {
        "allowedTools": [
          "get_file_contents",
          "search_code",
          "search_repositories",
          "create_branch",
          "create_or_update_file",
          "create_pull_request",
          "list_issues",
          "add_issue_comment"
        ],
        "strictlyForbiddenTools": [
          "merge_pull_request",
          "delete_branch",
          "delete_file",
          "delete_repository",
          "push_to_main",
          "manage_secrets",
          "manage_collaborators"
        ]
      }
    }
  }
}
```

Закоммить этот пример:
```bash
git add mcp-config.example.json
git commit -m "docs: добавлен шаблон безопасной конфигурации MCP"
git push origin main
```

---

## ✅ Критерии успешного выполнения
1. Проверена работа команд `gh repo view` и `gh issue list`.
2. Успешно смоделировано удаление ветки и ее восстановление через `git reflog`.
3. В репозиторий добавлен шаблон безопасной конфигурации `mcp-config.example.json` с разделением разрешенных и запрещенных инструментов.
