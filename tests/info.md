# Запуск unit-тестов
```bash
pytest файл_с_тестом_или_директория -v -s 
```

# Запуск нагрузочного тестирования
```bash
docker run --rm \
    --network="host" \
    -v $(pwd):/tests \
    justb4/jmeter:latest \
    -n -t /tests/load_test_номер.jmx \
    -l /tests/results_номер.jtl \
    -e -o /tests/report_номер
```
