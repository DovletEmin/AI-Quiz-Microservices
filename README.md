# 📘 Quiz Generator (FastAPI + NLP)

Генератор вопросов и вариантов ответов на основе текста.  
Использует **FastAPI**, **spaCy** и **NLTK (WordNet)** для извлечения ключевых слов, подбора синонимов и генерации правдоподобных отвлекающих вариантов.

---

## ⚡ Возможности

- 📌 Извлечение ключевых слов из текста (Nouns / Proper Nouns)
- 🧩 Автоматическая генерация вариантов ответа:
  - Синонимы (WordNet)
  - Семантически похожие слова (spaCy)
  - Отвлекающие варианты из текста
- 🔥 REST API на FastAPI
- ✅ Тесты (pytest)

---

## 🚀 Установка и запуск

### 1. Клонируем репозиторий

```bash
git clone https://github.com/DovletEmin/AI-Quiz-Microservices.git
cd services
```

### 2. Создаём виртуальное окружение

```bash
python -m venv venv
source venv/bin/activate   # Linux / Mac
venv\Scripts\activate      # Windows
```

### 3. Устанавливаем зависимости

```bash
pip install -r requirements.txt
```

#### ⚠️ Если en_core_web_sm ещё не скачан:

```bash
python -m spacy download en_core_web_sm
```
