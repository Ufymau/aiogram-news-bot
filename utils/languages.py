from typing import Dict, List

"""
A file in which all keyboard templates are stored in dictionary format.
"""

LANGUAGES: Dict[str, str] = {
    "en": "English 🇬🇧",
    "ru": "Русский 🇷🇺",
    "pt": "Português 🇵🇹",
    "es": "Español 🇪🇸",
    "de": "Deutsch 🇩🇪",
    "fr": "Français 🇫🇷",
    # "zh": "中文 🇨🇳",
    # "ja": "日本語 🇯🇵",
    "ar": "العربية 🇸🇦",
    # "hi": "हिन्दी 🇮🇳",
}

SELECTED_LANGUAGE_MESSAGES: Dict[str, str] = {
    "ru": "Отлично! Вы выбрали Русский 🇷🇺",
    "en": "Great! You chose English 🇬🇧",
    "es": "¡Genial! Has seleccionado Español 🇪🇸",
    "de": "Super! Sie haben Deutsch ausgewählt 🇩🇪",
    "fr": "Super ! Vous avez choisi le Français 🇫🇷",
    "zh": "太好了！您选择了中文 🇨🇳",
    "ja": "素晴らしい！日本語を選択しました 🇯🇵",
    "ar": "رائع! لقد اخترت العربية 🇸🇦",
    "hi": "बहुत बढ़िया! आपने हिन्दी चुनी है 🇮🇳",
    "pt": "Ótimo! Você escolheu Português 🇵🇹"
}

NEWS_QUESTION: Dict[str, str] = {
    "ru": "Какие новости вы хотите читать?",
    "en": "Which news do you want to read?",
    "es": "¿Qué noticias quieres leer?",
    "de": "Welche Nachrichten möchten Sie lesen?",
    "fr": "Quelles actualités souhaitez-vous lire?",
    "zh": "您想阅读哪些新闻？",
    "ja": "どのニュースを読みたいですか？",
    "ar": "ما الأخبار التي تريد قراءتها؟",
    "hi": "आप कौन-सी खबरें पढ़ना चाहते हैं?",
    "pt": "Quais notícias você quer ler?"
}

NEWS_BUTTONS: Dict[str, List[str]] = {
    "ru": ["Все новости", "Новости по ключу"],
    "en": ["All news", "News by keyword"],
    "es": ["Todas las noticias", "Noticias por palabra clave"],
    "de": ["Alle Nachrichten", "Nachrichten nach Schlüsselwort"],
    "fr": ["Toutes les actualités", "Actualités par mot-clé"],
    "zh": ["所有新闻", "按关键词新闻"],
    "ja": ["すべてのニュース", "キーワード別ニュース"],
    "ar": ["كل الأخبار", "الأخبار حسب الكلمة المفتاحية"],
    "hi": ["सभी खबरें", "कीवर्ड द्वारा खबरें"],
    "pt": ["Todas as notícias", "Notícias por palavra-chave"]
}

ENTER_KEYWORDS_PROMPT: Dict[str, str] = {
    "ru": "Введите ключевые слова через запятую (например: Bitcoin, AI, SOL):",
    "en": "Enter keywords separated by commas (e.g., Bitcoin, AI, SOL):",
    "es": "Ingrese palabras clave separadas por comas (por ejemplo: Bitcoin, AI, SOL):",
    "de": "Geben Sie Schlüsselwörter durch Kommas getrennt ein (z.B. Bitcoin, AI, SOL):",
    "fr": "Entrez des mots-clés séparés par des virgules (par ex. : Bitcoin, AI, SOL):",
    "zh": "请输入以逗号分隔的关键词（例如：Bitcoin, AI, SOL）：",
    "ja": "カンマで区切ったキーワードを入力してください（例：Bitcoin, AI, SOL）：",
    "ar": "أدخل الكلمات المفتاحية مفصولة بفواصل (مثال: Sol, AI, Bitcoin):",
    "hi": "कीवर्ड कॉमा से अलग करें (जैसे: Bitcoin, AI, SOL):",
    "pt": "Digite palavras-chave separadas por vírgulas (ex.: Bitcoin, AI, SOL):"
}

EMPTY_INPUT_RETRY: Dict[str, str]= {
    "ru": "Пустой ввод, попробуйте снова",
    "en": "Empty input, please try again",
    "es": "Entrada vacía, inténtelo de nuevo",
    "de": "Leere Eingabe, bitte versuchen Sie es erneut",
    "fr": "Entrée vide, veuillez réessayer",
    "zh": "输入为空，请重试",
    "ja": "入力が空です。もう一度お試しください。",
    "ar": "الإدخال فارغ، يرجى المحاولة مرة أخرى",
    "hi": "खाली इनपुट, कृपया पुनः प्रयास करें",
    "pt": "Entrada vazia, por favor tente novamente"
}

SEARCH_RESULTS_TITLE: Dict[str, str] = {
    "ru": "Результаты поиска:",
    "en": "Search results:",
    "es": "Resultados de la búsqueda:",
    "de": "Suchergebnisse:",
    "fr": "Résultats de la recherche :",
    "zh": "搜索结果：",
    "ja": "検索結果：",
    "ar": "نتائج البحث:",
    "hi": "खोज परिणाम:",
    "pt": "Resultados da pesquisa:"
}

NO_FRESH_NEWS = {
    "ru": "Свежих новостей по вашему запросу нет.",
    "en": "No fresh news for your query.",
    "es": "No hay noticias nuevas para su consulta.",
    "de": "Keine aktuellen Nachrichten zu Ihrer Anfrage.",
    "fr": "Pas de nouvelles fraîches pour votre requête.",
    "zh": "没有关于您的查询的新鲜新闻。",
    "ja": "ご指定の条件に該当する新しいニュースはありません。",
    "ar": "لا توجد أخبار جديدة لطلبك.",
    "hi": "आपकी खोज के लिए ताज़ा खबरें नहीं हैं।",
    "pt": "Não há notícias recentes para sua consulta."
}

LINK = {
    "ru": "ссылка",
    "en": "link",
    "es": "enlace",
    "de": "Link",
    "fr": "lien",
    "zh": "链接",
    "ja": "リンク",
    "ar": "رابط",
    "hi": "लिंक",
    "pt": "link"
}

