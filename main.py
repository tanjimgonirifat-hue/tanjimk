import telebot
from flask import Flask, render_template_string, request, redirect
import threading
import json
import os
import requests

# আপনার নতুন টোকেন সরাসরি এখানে দেওয়া হলো
API_TOKEN = "8710716253:AAHHAd7NQhVrIjeo_RM3UVfBmtR0cKcHTJE"
bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

CONFIG_FILE = 'bot_settings.json'

def load_config():
    if not os.path.exists(CONFIG_FILE):
        default_data = {
            "btn1_name": "🧾 কাজ শুরু", "btn2_name": "💰 প্রোফাইল",
            "btn3_name": "💳 উইথড্র", "btn4_name": "📞 সাপোর্ট",
            "task_cali": "✨ NEW TASK ✨\n🔗 লিঙ্ক: {link}",
            "success_msg": "✅ সেভ হয়েছে।"
        }
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(default_data, f)
    with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_config(data):
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# অ্যাডমিন প্যানেল UI
@app.route('/')
def index():
    config = load_config()
    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head><title>Admin Panel</title>
    <style>body{background:#0d1117;color:white;font-family:sans-serif;padding:20px;}.card{background:#161b22;padding:15px;margin-bottom:10px;border-radius:10px;border:1px solid #333;}textarea{width:100%;height:60px;background:#010409;color:#58a6ff;border:1px solid #444;}button{background:#238636;color:white;padding:15px;width:100%;border:none;cursor:pointer;font-weight:bold;}</style>
    </head>
    <body>
        <h2>🛠️ Tanjim Master Admin</h2>
        <form action="/update" method="POST">
            {% for key, value in config.items() %}
            <div class="card"><label>{{ key }}</label><br><textarea name="{{ key }}">{{ value }}</textarea></div>
            {% endfor %}
            <button type="submit">SAVE SETTINGS</button>
        </form>
    </body></html>''', config=config)

@app.route('/update', methods=['POST'])
def update():
    save_config(request.form.to_dict())
    return redirect('/')

# বট লজিক
@bot.message_handler(commands=['start'])
def start(message):
    c = load_config()
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(c['btn1_name'], c['btn2_name'], c['btn3_name'], c['btn4_name'])
    bot.send_message(message.chat.id, f"স্বাগতম {message.from_user.first_name}!", reply_markup=markup)

@bot.message_handler(func=lambda m: True)
def handle_msg(message):
    c = load_config()
    if message.text == c['btn1_name']:
        bot.send_message(message.chat.id, c['task_cali'].format(link="https://google.com"))
    elif message.text == c['btn4_name']:
        bot.send_message(message.chat.id, "সাপোর্ট আইডি: @TanjimZc1234")

# সার্ভার রান করার ফাংশন
def run_web():
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

if __name__ == '__main__':
    # ফ্লাস্ক ওয়েব সার্ভার চালু
    t = threading.Thread(target=run_web)
    t.daemon = True
    t.start()
    
    print("✅ Server and Bot Started!")
    # বট পোলিং শুরু
    try:
        bot.infinity_polling(timeout=10, long_polling_timeout=5)
    except Exception as e:
        print(f"Error: {e}")
      
