import telebot
from telebot import types
import os

# --- আপনার সেটিংস দিন ---
BOT_TOKEN = "8732492077:AAHbkr72fcZybH-aVyxQgcJWXJHEjUVXlPA"  # BotFather থেকে পাওয়া টোকেন
ADMIN_ID = 6805684286               # এডমিনের টেলিগ্রাম আইডি (সংখ্যায়)

bot = telebot.TeleBot(BOT_TOKEN)
DATA_FILE = "user.txt"

# ফাইলে মোট কতটি লাইন/কোড জমা হয়েছে তা বের করার ফাংশন
def get_user_count():
    if not os.path.exists(DATA_FILE):
        return 0
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return sum(1 for line in f if line.strip())

# এডমিনের জন্য কাস্টম কিবোর্ড
def get_admin_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_file = types.KeyboardButton("📁 ফাইল ডাউনলোড (user.txt)")
    btn_count = types.KeyboardButton("📊 মোট ডাটা সংখ্যা")
    markup.row(btn_file, btn_count)
    return markup

# /start হ্যান্ডলার
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name

    # এডমিন আসলে এডমিন প্যানেল দেখাবে
    if user_id == ADMIN_ID:
        admin_text = (
            "╭━━━━━━━━━━━━━━━━━━━━━━━━╮\n"
            "   👑  **এডমিন কন্ট্রোল প্যানেল**  👑\n"
            "╰━━━━━━━━━━━━━━━━━━━━━━━━╯\n\n"
            f"স্বাগতম এডমিন **{user_name}**!\n"
            f"📊 বর্তমানে মোট কোড জমা হয়েছে: `{get_user_count()}` টি।\n\n"
            "নিচের বাটন ব্যবহার করে যেকোনো সময় ফাইল নামিয়ে নিতে পারেন।"
        )
        bot.send_message(message.chat.id, admin_text, parse_mode="Markdown", reply_markup=get_admin_keyboard())
        return

    # সাধারণ ইউজারের জন্য আকর্ষণীয় বক্স ডিজাইন
    welcome_text = (
        "╭━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╮\n"
        "   🎬  **ওয়েলকাম টু আরিয়ান স্টুডিও**  🎬\n"
        "╰━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╯\n\n"
        f"হ্যালো **{user_name}**! 👋\n\n"
        "┌─────────────────────────────┐\n"
        "│  📝 **নির্দেশনা:**                    │\n"
        "│  আপনার **স্টুডিও কোডটি** পাঠান।      │\n"
        "│                             │\n"
        "│  ⚠️ **শর্ত:**                          │\n"
        "│  কোডটি অবশ্যই **২৫ অক্ষরের** হতে হবে। │\n"
        "└─────────────────────────────┘\n\n"
        "👇 _অনুগ্রহ করে নিচে আপনার কোডটি লিখে সেন্ড করুন:_"
    )
    
    # সাধারণ ইউজারের কিবোর্ড রিমুভ রাখা হলো যেন পরিষ্কার দেখায়
    bot.send_message(message.chat.id, welcome_text, parse_mode="Markdown", reply_markup=types.ReplyKeyboardRemove())

# টেক্সট মেসেজ ও বাটন ক্লিকের হ্যান্ডলার
@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    user_id = message.from_user.id
    text = message.text.strip()

    # --- ১. এডমিন বাটন অ্যাকশন ---
    if user_id == ADMIN_ID:
        if text == "📁 ফাইল ডাউনলোড (user.txt)":
            if os.path.exists(DATA_FILE) and os.path.getsize(DATA_FILE) > 0:
                with open(DATA_FILE, "rb") as doc:
                    bot.send_document(
                        ADMIN_ID,
                        doc,
                        caption=f"📁 **আরিয়ান স্টুডিও ডাটা ফাইল**\n📊 মোট কোড সংখ্যা: `{get_user_count()}` টি।",
                        parse_mode="Markdown"
                    )
            else:
                bot.send_message(ADMIN_ID, "⚠️ এখনো কোনো ইউজার কোড জমা দেয়নি। ফাইল খালি!")
            return

        elif text == "📊 মোট ডাটা সংখ্যা":
            count = get_user_count()
            bot.send_message(ADMIN_ID, f"📊 বর্তমানে ডাটাবেজে মোট **{count}** টি কোড জমা রয়েছে।", parse_mode="Markdown")
            return

    # --- ২. সাধারণ ইউজারের কোড যাচাই ---
    code_length = len(text)

    # কোড ২৫ অক্ষর না হলে সতর্কবার্তা
    if code_length != 25:
        error_msg = (
            "❌ **কোডটি সঠিক নয়!**\n\n"
            f"আপনার দেওয়া কোডটি ছিল `{code_length}` অক্ষরের।\n"
            "⚠️ কোডটি অবশ্যই **ঠিক ২৫ অক্ষরের** হতে হবে। আবার চেষ্টা করুন।"
        )
        bot.reply_to(message, error_msg, parse_mode="Markdown")
        return

    # ২৫ অক্ষরের হলে ফাইলে সেভ করা
    username = f"@{message.from_user.username}" if message.from_user.username else "No Username"
    entry = f"User ID: {user_id} | Username: {username} | Code: {text}\n"

    with open(DATA_FILE, "a", encoding="utf-8") as f:
        f.write(entry)

    # কনফার্মেশন মেসেজ
    success_msg = (
        "╭━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╮\n"
        "   ✅ **কোড সফলভাবে জমা নেওয়া হয়েছে!**\n"
        "╰━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╯\n\n"
        "ধন্যবাদ! আরিয়ান স্টুডিওর সাথে থাকার জন্য।"
    )
    bot.reply_to(message, success_msg, parse_mode="Markdown")

    # --- ৩. প্রতি ১০০ জনে অটোমেটিক এডমিনকে ফাইল সেন্ড ---
    total_count = get_user_count()
    if total_count > 0 and total_count % 100 == 0:
        try:
            with open(DATA_FILE, "rb") as doc:
                bot.send_document(
                    ADMIN_ID,
                    doc,
                    caption=f"🎉 **অভিনন্দন এডমিন!**\nবটে নতুন ১০০টি কোড পূরণ হয়েছে!\n📊 সর্বমোট কোড: `{total_count}` টি।",
                    parse_mode="Markdown"
                )
        except Exception as e:
            print(f"এডমিনকে অটো-ফাইল পাঠাতে ব্যর্থ: {e}")

# বট রান করা
if __name__ == "__main__":
    print("🚀 আরিয়ান স্টুডিও বট সফলভাবে চালু হয়েছে...")
    bot.infinity_polling()
