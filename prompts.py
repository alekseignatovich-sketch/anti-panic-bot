def get_guide_prompt(user_data, lang='ru'):
    """
    Промпт для Groq (оптимизирован под Llama 3.1)
    """
    symptoms = ', '.join(user_data.get('symptoms', ['сердцебиение'])) or 'сердцебиение'
    triggers = user_data.get('triggers', 'стресс на работе')
    helpful = user_data.get('helpful', 'глубокое дыхание')
    context = user_data.get('context', 'в одиночестве дома')
    intensity = user_data.get('intensity', 'средняя')
    
    if lang == 'ru':
        prompt = f"""
Ты — дружелюбный психолог-практик, специалист по самопомощи при тревожных состояниях.
Создай персонализированный гайд для человека с такими данными:

Симптомы: {symptoms}
Триггеры: {triggers}
Что помогало раньше: {helpful}
Где чаще всего происходит: {context}
Интенсивность: {intensity}

ПРАВИЛА:
1. НЕ ставь диагнозы и НЕ заменяй врача
2. Всегда добавляй дисклеймер в конце
3. Используй простой, тёплый тон без жаргона
4. Давай конкретные шаги (не абстракции)
5. Если упоминаются мысли о смерти — НЕМЕДЛЕННО направь к специалисту

Структура ответа:
1. Короткое введение (2 предложения)
2. Скрипт "Скорой помощи" — пошагово для острого приступа
3. Техники заземления (подбери под симптомы)
4. Ежедневная профилактика (3 простых действия)
5. Когда обращаться к врачу (красные флаги)
6. Дисклеймер

Отвечай ТОЛЬКО на русском. Используй эмодзи для структуры. Максимум 1200 символов.
"""
    else:
        prompt = f"""
You are a friendly psychologist specializing in anxiety self-help.
Create a personalized guide for someone with:

Symptoms: {symptoms}
Triggers: {triggers}
What helped before: {helpful}
Context: {context}
Intensity: {intensity}

RULES:
1. Do NOT diagnose or replace a doctor
2. Always add disclaimer at the end
3. Use warm, simple language
4. Give concrete steps

Structure:
1. Short intro (2 sentences)
2. Emergency script for acute attack
3. Grounding techniques
4. Daily prevention (3 actions)
5. When to see a professional
6. Disclaimer

Answer in English only. Use emojis. Max 1200 characters.
"""
    
    return prompt
