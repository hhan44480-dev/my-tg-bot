import re
import os
from threading import Thread
from flask import Flask
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Render အတွက် Web Server ဆောက်ခြင်း (၂၄ နာရီ မပိတ်ဘဲ အလုပ်လုပ်စေရန်)
web_app = Flask('')

@web_app.route('/')
def home():
    return "Bot is running 24/7!"

def run_web_server():
    # Render က ပေးမယ့် Port သို့မဟုတ် သာမန် Port 8080 ကို သုံးခြင်း
    port = int(os.environ.get("PORT", 8080))
    web_app.run(host='0.0.0.0', port=port)

# ဈေးနှုန်းများ သတ်မှတ်ခြင်း
PRICE_LIKE_1K = 4500
PRICE_VIEW_1K = 1000

user_sessions = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_sessions[user_id] = None
    
    reply_keyboard = [['TikTok Like ဝယ်ယူရန်', 'TikTok View ဝယ်ယူရန်']]
    await update.message.reply_text(
        "မင်္ဂလာပါ Hana Digital Service Bot မှ ကြိုဆိုပါတယ်။\n\n"
        "ဝန်ဆောင်မှု ရွေးချယ်ရန် အောက်က ခလုတ်ကို နှိပ်ပါဗျာ။",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
    )

async def like_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_sessions[user_id] = "like"
    await update.message.reply_text(
        "❤️ TikTok Like ဝန်ဆောင်မှု ဈေးနှုန်းများ ❤️\n\n"
        "Like 1k = 4,500 ကျပ်\n"
        "Like 10k = 45,000 ကျပ်\n\n"
        "ဝယ်ယူလိုသည့် ပမာဏကို စာရိုက်ပြီး ပို့ပေးပါ (ဥပမာ- 2k သို့မဟုတ် 5k)"
    )

async def view_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_sessions[user_id] = "view"
    await update.message.reply_text(
        "👁️ TikTok View ဝန်ဆောင်မှု ဈေးနှုန်းများ 👁️\n\n"
        "View 1k = 1,000 ကျပ်\n"
        "View 10k = 10,000 ကျပ်\n\n"
        "ဝယ်ယူလိုသည့် ပမာဏကို စာရိုက်ပြီး ပို့ပေးပါ (ဥပမာ- 5k သို့မဟုတ် 10k)"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_text = update.message.text.lower().replace(" ", "").strip()
    match = re.match(r"^(\d+)k$", user_text)
    
    if match:
        k_amount = int(match.group(1))
        if 1 <= k_amount <= 100:
            current_choice = user_sessions.get(user_id)
            if current_choice == "like":
                total_price = k_amount * PRICE_LIKE_1K
                service_name = f"TikTok Like"
            elif current_choice == "view":
                total_price = k_amount * PRICE_VIEW_1K
                service_name = f"TikTok View"
            else:
                await update.message.reply_text("ကျေးဇူးပြု၍ အောက်က ခလုတ်ကို အရင်နှိပ်ပြီးမှ အရေအတွက် ရိုက်ပေးပါဗျာ။")
                return

            reply_message = (
                f"💬 သင်ဝယ်ယူမည့်ပမာဏ: {service_name} {k_amount}k\n"
                f"💰 ကျသင့်ငွေ စုစုပေါင်း: {total_price:,} ks\n\n"
                f"📱 ပေးချေရမည့် payment က: 09403095335\n"
                f"[ kpay ] or [ wave ]\n\n"
                f"HanHtooAung\n\n"
                f"Payment လေးကိုလွှဲပေးပါရန်။ Ngwelswပြီးပါက ဖြတ်ပိုင်း Screenshot နှင့် သင့် TikTok ဗီဒီယို Link ကို ဒီထဲသို့ တိုက်ရိုက် ပို့ပေးပါ။"
            )
            await update.message.reply_text(reply_message)
        else:
            await update.message.reply_text("ကျွန်တော်တို့ Bot တွင် 1k မှ 100k အထိသာ အလိုအလျောက် တွက်ချက်ပေးနိုင်ပါသည်။")
    else:
        await update.message.reply_text("လူကြီးမင်း ပေးပို့ချက်ကို မှတ်သားထားပါတယ်။ လူကိုယ်တိုင် စစ်ဆေးပြီး အကြောင်းပြန်ပေးပါမည်။")

if __name__ == '__main__':
    # ⚠️ ဒီနေရာမှာ သင့်ရဲ့ Bot Token အစစ်ကို သေချာထည့်ပါ
    TOKEN = '8863863150:AAFy53xNPxaURkiaMuqZbe_nUF3BCAFFpTU'
    
    # Web Server ကို နောက်ကွယ်ကနေ သီးသန့် Run ပေးခြင်း
    server_thread = Thread(target=run_web_server)
    server_thread.daemon = True
    server_thread.start()
    
    # Telegram Bot ကို မောင်းနှင်ခြင်း
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.Text(['TikTok Like ဝယ်ယူရန်']), like_menu))
    app.add_handler(MessageHandler(filters.Text(['TikTok View ဝယ်ယူရန်']), view_menu))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("Bot is ready and Web Server is running...")
    app.run_polling()
  
