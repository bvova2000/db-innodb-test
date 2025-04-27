# 📚 db-innodb-test

Тестирование производительности вставки и выборки в MySQL InnoDB с разными индексами и настройками `innodb_flush_log_at_trx_commit`.

---

## 📦 Структура проекта

- **docker-compose.yml** — поднятие MySQL сервера
- **app.py** — Flask сервер для вставки пользователей через `/insert_user`
- **insert_data_threaded.py** — многопоточная вставка данных напрямую
- **insert_single_row.py** — однопоточная вставка для теста реального влияния `flush_log`
- **siege тесты** — нагрузочное тестирование вставки через HTTP

---

### 1. Поднять MySQL

```bash
docker-compose up -d
```

Ожидать старта MySQL сервера (`localhost:3306`, пользователь `root`, пароль `root`).

---

### 2. Запустить Flask сервер

```bash
pip install flask mysql-connector-python faker
python app.py
```
Сервер стартует на `http://127.0.0.1:8080`.

---

### 3. Проверить вставку одного пользователя

Открыть в браузере:

```
http://127.0.0.1:8080/insert_user
```

Ответ: `User inserted via GET`.

---

### 4. Нагрузить сервер через Siege

Пример команды:

```bash
siege -c 5 -r 1000 http://127.0.0.1:8080/insert_user
```

- `-c 5` — 5 одновременных клиентов
- `-r 1000` — каждый клиент делает 1000 запросов

---

### 5. Изменение innodb_flush_log_at_trx_commit

Перед каждым тестом в терминале:

```bash
docker exec -it mysql-test mysql -uroot -proot -e "SET GLOBAL innodb_flush_log_at_trx_commit=0;"
```
или
```bash
docker exec -it mysql-test mysql -uroot -proot -e "SET GLOBAL innodb_flush_log_at_trx_commit=1;"
```
или
```bash
docker exec -it mysql-test mysql -uroot -proot -e "SET GLOBAL innodb_flush_log_at_trx_commit=2;"
```

---

## 📈 Что тестировалось

### 1. Выборка по дате рождения `date_of_birth`

Запрос:

```sql
SELECT * FROM users WHERE date_of_birth BETWEEN '1990-01-01' AND '1991-01-01' LIMIT 100;
```

Проверено:
- Без индекса
- С BTREE-индексом
- Повторная выборка с использованием InnoDB Adaptive Hash Index

---

### 2. Вставка пользователей

- Многопоточная вставка (`insert_data_threaded.py`) на 1 миллион записей
- Асинхронная вставка (опционально)
- Вставка через HTTP сервер (`app.py`) + нагрузка `siege`
- Тестирование с разными `innodb_flush_log_at_trx_commit`

---

## 📊 Результаты вставки через Siege (Находяться в файле insert_results.txt)


**Вывод:**  
- При `innodb_flush_log_at_trx_commit=1` скорость вставки заметно ниже (до ~20%).
- При `0` и `2` вставка происходит быстрее, особенно при высокой нагрузке.

---

## 📋 Быстрая проверка по шагам

```bash
docker-compose up -d
python app.py
siege -c 5 -r 1000 http://127.0.0.1:8080/insert_user
```
Поменять значение `innodb_flush_log_at_trx_commit`, повторить нагрузку и сравнить результаты.

