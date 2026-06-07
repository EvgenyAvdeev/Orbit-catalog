# Стадия сборки фронтенда
FROM node:20-alpine as frontend-builder

WORKDIR /app/front

# Копируем только файлы с зависимостями
COPY front/package*.json ./

# Устанавливаем все зависимости
RUN npm install && \
    npm install echarts@5.4.3 echarts-gl@2.0.9 --save --legacy-peer-deps

# Копируем остальные файлы проекта
COPY front/ .

# Собираем проект
RUN npm run build

# Проверим структуру собранных файлов
RUN ls -la /app/front/dist/

# Финальная стадия
FROM python:3.12-slim

WORKDIR /app

# Копируем собранный фронтенд из dist в корень front
COPY --from=frontend-builder /app/front/dist /app/front

# Копируем и устанавливаем Python зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем бэкенд файлы
COPY models/ ./models/
COPY tables/ ./tables/
COPY repo/ ./repo/
COPY routers/ ./routers/
COPY database.py .
COPY settings.py .
COPY app.py .
COPY __init__.py .
COPY CLI.py .
COPY create_tables.py .
COPY DB_calc_and_fill.py .
COPY DB_calc/ ./DB_calc/
COPY redis_client.py .
COPY dependencies.py .
COPY create_tables.py .
COPY doc/docs.pdf docs/docs.pdf
COPY script/orbit_visibility.ipynb script/orbit_visibility.ipynb
COPY load_data.py .
COPY yandex.py .
COPY deploy.py .
EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
