# Integration Tests

## Что такое интеграционные тесты?

**Unit тесты** тестируют отдельные функции изолированно (с моками).
**Интеграционные тесты** тестируют весь стек вместе: Router → Service → CRUD → Database.

## Разница

| Unit тесты | Интеграционные тесты |
|------------|----------------------|
| ✅ Моки БД | ✅ Реальная тестовая БД |
| ✅ Быстрые | ⚠️ Медленнее |
| ✅ Изолированные | ✅ Тестируют взаимодействие |
| ✅ Много тестов | ✅ Меньше, но важнее |

## Настройка

### 1. Убедитесь, что PostgreSQL запущен

```bash
# Через Docker
docker-compose up db -d

# Или локально
pg_isready
```

### 2. Создайте тестовую БД (опционально)

Фикстура попытается создать БД автоматически, но можно создать вручную:

```bash
# Локально
createdb expensetracker_test

# Или через Docker
docker exec -it expense-tracker-db psql -U postgres -c "CREATE DATABASE expensetracker_test;"
```

### 3. Установите переменную окружения (опционально)

По умолчанию используется:
```
postgresql://postgres:postgres@localhost:5432/expensetracker_test
```

Или установите свою:
```bash
export TEST_DATABASE_URL=postgresql://user:password@host:port/dbname
```

## Запуск

```bash
# Все интеграционные тесты
make test-integration

# Или напрямую
pytest app/tests/integration/ -v

# Конкретный тест
pytest app/tests/integration/test_expenses_integration.py::TestExpenseServiceIntegration::test_create_expense_integration -v
```

## Как работают фикстуры

1. **`test_db_pool`** (session scope) - создает пул соединений один раз
2. **`test_db_schema`** (session scope) - создает таблицы один раз
3. **`test_conn`** (function scope) - дает соединение для каждого теста с автоматическим rollback
4. **`expense_service`** (function scope) - создает ExpenseService с тестовым соединением

## Изоляция тестов

Каждый тест:
- Получает свое соединение с БД
- Автоматически делает rollback после теста
- Не влияет на другие тесты

## Что тестировать?

✅ **Тестируем:**
- Полный workflow (Create → Read → Update → Delete)
- Реальные SQL запросы
- Взаимодействие между слоями
- Персистентность данных

❌ **НЕ тестируем:**
- Валидацию (это для unit тестов моделей)
- Обработку ошибок БД (это для unit тестов CRUD)
- HTTP статусы (это для unit тестов роутеров)
