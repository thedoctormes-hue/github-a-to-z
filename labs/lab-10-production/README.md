# Лабораторная работа №10: Настройка промышленного контура безопасности

## 🎯 Цель работы
1. Внедрить файл `.gitattributes` для ликвидации войны CRLF/LF.
2. Настроить локальную подпись коммитов (Commit Signing) для получения бейджа `Verified`.
3. Оформить серию коммитов по стандарту Conventional Commits.
4. Настроить правила защиты ветки (Branch Protection Rule) в репозитории.
5. Провести проверку Pull Request и применить правку через Suggested Changes.

---

## 🛠️ Шаг 1. Создание файла `.gitattributes`

1. В корне вашего учебного репозитория создайте файл `.gitattributes`:
   ```gitattributes
   # Автоопределение текстовых файлов и нормализация в LF
   * text=auto eol=lf

   *.md text eol=lf
   *.py text eol=lf
   *.js text eol=lf
   *.json text eol=lf
   *.yml text eol=lf
   *.yaml text eol=lf

   # Бинарные файлы
   *.png binary
   *.jpg binary
   *.webp binary
   *.ico binary
   ```
2. Сделайте коммит по стандарту Conventional Commits:
   ```bash
   git add .gitattributes
   git commit -m "chore(git): add .gitattributes to normalize line endings"
   ```

---

## 🛠️ Шаг 2. Настройка подписи коммитов через SSH

1. Узнай путь к своему публичному SSH-ключу (обычно `~/.ssh/id_ed25519.pub`).
2. Включи использование SSH для подписи в Git:
   ```bash
   git config --global gpg.format ssh
   git config --global user.signingkey ~/.ssh/id_ed25519.pub
   git config --global commit.gpgsign true
   ```
3. Сделай тестовый коммит:
   ```bash
   git commit --allow-empty -m "chore(security): test cryptographic commit signature"
   ```
4. Отправь в свой репозиторий:
   ```bash
   git push origin main
   ```
5. Открой историю коммитов на GitHub: рядом с последним коммитом должен красоваться зеленый бейдж **`Verified`**!

---

## 🛠️ Шаг 3. Включение Branch Protection для ветки `main`

1. Зайди в свой репозиторий на GitHub ➔ вкладка **Settings** ➔ в левом меню **Branches**.
2. В блоке **Branch protection rules** нажми кнопку **Add rule** (или создай новый **Ruleset**).
3. В поле **Branch name pattern** введи: `main`.
4. Включи флажки:
   * [x] **Require a pull request before merging**
   * [x] **Require approvals** (выстави 1)
   * [x] **Do not allow bypassing the above settings**
5. Нажми **Save changes** внизу страницы.
6. Попробуй сделать прямой пуш в `main` из терминала:  
   `git push origin main`  
   *Результат:* GitHub физически отклонит отправку с ошибкой *«Protected branch: Changes must be made through a pull request»*. Защита работает!

---

## 🛠️ Шаг 4. Практика Suggested Changes при код-ревью

1. Создай ветку `feat/calc-update`:
   ```bash
   git switch -c feat/calc-update
   ```
2. Добавь строку с намеренной мелкой опечаткой (например, `result = 4 + 4 # opecatka`).
3. Запушь и открой Pull Request.
4. Открой вкладку **Files changed** в PR.
5. Нажми синий плюсик на строке с опечаткой ➔ нажми иконку **Add a suggestion** ➔ исправь опечатку в предложении.
6. Нажми **Commit suggestion**.
7. При слиянии PR выбери режим **Squash and merge**.

---

## 🏁 Критерий успешности
- [ ] В корне проекта лежит `.gitattributes`.
- [ ] В истории коммитов на GitHub отображается зеленый бейдж `Verified`.
- [ ] Ветка `main` защищена правилом Branch Protection.
- [ ] Ты умеешь использовать `Suggested Changes` и слияние через `Squash and merge`.
