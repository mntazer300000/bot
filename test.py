import telebot
from scholarly import scholarly

# ضع التوكن الخاص بك هنا
TOKEN = "7638655114:AAFZ2qQrjvjdIix3pLquTKghcNUIR7XLMn4"
bot = telebot.TeleBot(TOKEN)

# دالة البحث عن المصادر
def search_scholar(query):
    results = scholarly.search_pubs(query)
    sources = []
    
    for i in range(3):  # جلب أول 3 نتائج فقط
        try:
            article = next(results)
            title = article.get('bib', {}).get('title', 'عنوان غير متوفر')
            url = article.get('pub_url', 'رابط غير متوفر')
            sources.append(f"📌 *{title}*\n🔗 {url}")
        except StopIteration:
            break
    
    return "\n\n".join(sources) if sources else "لم يتم العثور على مصادر."

# عند استلام أي رسالة، يقوم البوت بالبحث عن المصادر
@bot.message_handler(func=lambda message: True)
def fetch_sources(message):
    bot.send_message(message.chat.id, "🔍 يتم البحث عن المصادر، يرجى الانتظار...")
    sources = search_scholar(message.text)
    bot.send_message(message.chat.id, sources, parse_mode="Markdown")

# تشغيل البوت
bot.polling()
