import asyncio
import requests
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from telegram.request import HTTPXRequest

BOT_TOKEN = "8240516135:AAG319_Vet49_I4V_igrg-4b2XtjCwUFH2Q"
API = "https://ayaanmods.site/number.php?key=annonymous&number="

# Updated keyboard with more buttons
keyboard = ReplyKeyboardMarkup(
    [
        ["📱 Phone Lookup"],                    # Row 1
        ["ℹ️ About", "📞 Contact Developer"]    # Row 2
    ],
    resize_keyboard=True
)

def fetch_api(num):
    try:
        r = requests.get(API + num, timeout=30)
        if r.status_code == 200:
            return r.json()
        return None
    except:
        return None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome to Vishal Hack Number Info Bot\n\n"
        "Use the buttons below to navigate:",
        reply_markup=keyboard
    )

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    # Handle different button presses
    if text == "📱 Phone Lookup":
        await update.message.reply_text("📞 Send 10 digit mobile number:")
        return

    elif text == "ℹ️ About":
        about_text = (
            "🤖 **About this Bot**\n\n"
            "This bot fetches mobile number details from an online database.\n"
            "• Simply click 'Phone Lookup' and send a 10-digit number.\n"
            "• Information may include name, address, circle, etc.\n"
            "• Data is provided by third-party API.\n\n"
            "**Note:** Not all numbers may be available."
        )
        await update.message.reply_text(about_text, parse_mode='Markdown')
        return

    elif text == "📞 Contact Developer":
        contact_text = (
            "📬 **Contact Developer**\n\n"
            "👤 **Name:** Vishal Hacker\n"
            "📧 **Email:** vishalkumar993163@gmail.com\n"
            "📱 **Telegram:** @vishal_hacker_99\n"
            "🔗 **Channel:** [Join Here](https://youtube.com/@vishulol99?si=OxMduqS0-YJx-StR)\n\n"
            "For any queries or feedback, feel free to reach out!"
        )
        await update.message.reply_text(contact_text, parse_mode='Markdown', disable_web_page_preview=True)
        return

    # If it's a 10-digit number (from Phone Lookup flow)
    if text.isdigit() and len(text) == 10:
        msg = await update.message.reply_text(f"🔍 Fetching info for {text}...")

        data = await asyncio.to_thread(fetch_api, text)

        if data and "result" in data and len(data["result"]) > 0:
            d = data["result"][0]
            
            reply = f"""✅ INFORMATION HACK
━━━━━━━━━━━━━━━━━━━━━━
👤 Name: {d.get('name', 'NA')}
👨 Father: {d.get('father_name', 'NA')}
🏠 Address: {d.get('address', 'NA')}
📍 Circle: {d.get('circle', 'NA')}
📱 Mobile: {d.get('mobile', 'NA')}
📞 Alternate: {d.get('alternate', 'NA')}
📧 Email: {d.get('email', 'NA')}
🆔 ID: {d.get('id', 'NA')}
━━━━━━━━━━━━━━━━━━━━━━
🔍 Number Searched: {text}
━━━━━━━━━━━━━━━━━━━━━━
👑 Developer: Vishal Hacker"""

            await msg.edit_text(reply)
        else:
            await msg.edit_text("❌ No information found for this number")
        return

    # If input is invalid
    await update.message.reply_text(
        "⚠️ Invalid input\nPlease use the buttons below:",
        reply_markup=keyboard
    )

def main():
    print("Bot Started...")

    request = HTTPXRequest(
        connect_timeout=30,
        read_timeout=30,
    )

    app = ApplicationBuilder().token(BOT_TOKEN).request(request).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))
    app.run_polling()

if __name__ == "__main__":
    main()