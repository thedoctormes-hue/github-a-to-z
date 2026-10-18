# 🧪 Лабораторная работа №6: Настройка первого CI-робота и публикация на Pages

> **Цель работы:** Написать свой первый сценарий автоматизации в GitHub Actions, настроить защиту от зависания (`timeout-minutes`), увидеть прохождение тестов в облаке и опубликовать рабочий сайт через GitHub Pages.

---

## 📋 Пошаговый сценарий

### Шаг 1. Создание веб-страницы проекта
Перейди в свой учебный репозиторий на компьютере и убедись, что находишься в ветке `main`:
```bash
cd test-git-lab
git switch main
git pull
```

Создай файл `index.html` в корне проекта:
```html
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Мой первый сайт на GitHub Pages</title>
    <style>
        body { font-family: sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; background: #0d1117; color: #58a6ff; }
        .card { text-align: center; border: 1px solid #30363d; padding: 40px; border-radius: 12px; background: #161b22; }
        h1 { margin-bottom: 8px; color: #f0f6fc; }
    </style>
</head>
<body>
    <div class="card">
        <h1>🚀 Мой проект в эфире!</h1>
        <p>Этот сайт автоматически опубликован через <b>GitHub Pages</b>.</p>
        <p>Проверено роботом <b>GitHub Actions</b> ✅</p>
    </div>
</body>
</html>
```

---

### Шаг 2. Создание первого сценария автоматизации
Создай специальную папку `.github/workflows/`:
```bash
mkdir -p .github/workflows
```

Внутри этой папки создай файл `ci.yml`:
```yaml
name: Проверка проекта (CI)

on:
  push:
    branches: [ main ]
    paths:
      - 'index.html'
      - '.github/workflows/**'

permissions:
  contents: read

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

jobs:
  validate:
    runs-on: ubuntu-latest
    timeout-minutes: 5 # Защита от зависания и сжигания квоты минут!

    steps:
      - name: 1. Скачать репозиторий
        uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683 # v4.2.2

      - name: 2. Проверить HTML разметку
        run: |
          if grep -q "<h1>" index.html; then
            echo "✅ Заголовок h1 найден!"
          else
            echo "❌ Ошибка: заголовок h1 не найден в index.html!"
            exit 1
          fi

      - name: 3. Отчет о проверке
        run: echo "Все автоматические проверки пройдены успешно!"
```

---

### Шаг 3. Отправка сценария в облако
Закоммить файлы и отправь их на GitHub:
```bash
git add index.html .github/workflows/ci.yml
git commit -m "ci: добавлен первый workflow проверки и стартовая страница index.html"
git push origin main
```

---

### Шаг 4. Наблюдение за работой робота
1. Открой свой репозиторий в браузере на GitHub.
2. Перейди во вкладку **Actions**.
3. Ты увидишь, как запустился твой рабочий процесс `Проверка проекта (CI)`!
4. Кликни по нему: ты увидишь логи выполнения каждого шага в реальном времени.
5. Через 15–20 секунд задание загорится яркой зеленой галочкой: **Completed: Success**!

---

### Шаг 5. Включение хостинга GitHub Pages

> [!IMPORTANT]
> **⚠️ Тарифный радар для выполнения шага:**  
> GitHub Pages работает бесплатно **только в публичных репозиториях**. Если ваш учебный репозиторий был создан как Private, зайдите в **Settings ➔ General ➔ Danger Zone ➔ Change repository visibility** и временно переключите его в **Public**, иначе раздел Pages потребует платный план GitHub Pro.
1. В репозитории перейди во вкладку **Settings**.
2. В левой колонке найди раздел **Pages**.
3. В блоке **Build and deployment**:
   * **Source:** выбери `Deploy from a branch`.
   * **Branch:** выбери `main` и папку `/(root)`.
4. Нажми кнопку **Save**.
5. Подожди около минуты и обнови страницу: сверху появится зеленая плашка с прямой ссылкой на твой сайт вида:  
   `https://твой-логин.github.io/test-git-lab/`
6. Открой эту ссылку на компьютере или смартфоне — твой сайт работает в открытом интернете! 🎉

---

## ✅ Критерии успешного выполнения
1. В репозитории создан файл `.github/workflows/ci.yml`.
2. В сценарии корректно настроены параметры `timeout-minutes: 5` и фильтр `paths:`.
3. Во вкладке **Actions** отображается успешный запуск с зеленой галочкой.
4. Включен GitHub Pages, и сайт `index.html` доступен по публичной ссылке в интернете.
---

## 🧭 Навигация

* 🔙 **Теория модуля:** [Модуль 6: Роботы на службе](../../docs/06-actions-pages/README.md)
* 🗺️ **Навигатор курса:** [Главная страница курса](../../README.md)
* ⏭️ **Следующий модуль:** [Модуль 7: Арсенал инженера будущего](../../docs/07-pro-tools/README.md)
