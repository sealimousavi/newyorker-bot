import logging
import os
import requests
from dotenv import load_dotenv
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext, ConversationHandler

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
FLASK_API_URL = os.getenv("FLASK_API_URL", "http://localhost:5000/cover")

# فعال کردن لاگ‌ها
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# تعریف مراحل گفتگو
YEAR, MONTH, DAY = range(3)

# دستورات شروع
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text(
        "🎂 برای پیدا کردن جلد مجله‌ی نیویورکر خودت، سال تولدت رو وارد کن."
    )
    return YEAR

# دستیار سال
async def handle_year(update: Update, context: CallbackContext):
    user_input = update.message.text.strip()

    try:
        year = int(user_input)  # اعتبارسنجی ورودی سال
        if year < 1900 or year > 2024:
            raise ValueError("سال خارج از محدوده")

        context.user_data['year'] = year
        await update.message.reply_text(f" حالا لطفاً ماه تولد خودت رو وارد کن.")
        return MONTH

    except ValueError:
        await update.message.reply_text("⚠️ لطفاً یک سال معتبر بین ۱۹۰۰ و ۲۰۲۴ وارد کن.")
        return YEAR

# دستیار ماه
async def handle_month(update: Update, context: CallbackContext):
    user_input = update.message.text.strip()

    try:
        month = int(user_input)  # اعتبارسنجی ورودی ماه
        if month < 1 or month > 12:
            raise ValueError("ماه خارج از محدوده")

        context.user_data['month'] = month
        await update.message.reply_text(f" حالا لطفاً روز تولد خودت رو وارد کن.")
        return DAY

    except ValueError:
        await update.message.reply_text("⚠️ لطفاً یک ماه معتبر بین ۱ و ۱۲ وارد کن.")
        return MONTH

# دستیار روز
async def handle_day(update: Update, context: CallbackContext):
    user_input = update.message.text.strip()

    try:
        day = int(user_input)  # اعتبارسنجی ورودی روز
        if day < 1 or day > 31:
            raise ValueError("روز خارج از محدوده")

        context.user_data['day'] = day
        birthday = f"{context.user_data['year']}-{context.user_data['month']:02d}-{context.user_data['day']:02d}"

        # تماس با API Flask برای دریافت نزدیکترین جلد مجله
        response = requests.get(FLASK_API_URL, params={"birthday": birthday})
        if response.status_code == 200:
            data = response.json()
            msg = (
                f"🗓️ جلد مجله‌ی نیویورکر به سبک تاریخ تولد شما! ({birthday}):\n\n"
                f"🎨 *{data['title']}*\n"
                f"📰 منتشر شده: {data['date']}\n"
                f"🖼️ [مشاهده جلد مجله]({data['image_url']})"
            )
            await update.message.reply_photo(photo=data["image_url"], caption=msg, parse_mode=ParseMode.MARKDOWN)
        else:
            await update.message.reply_text("اوپس! مشکلی در پیدا کردن جلد مجله شما پیش آمد.")
        
        return ConversationHandler.END

    except ValueError:
        await update.message.reply_text("⚠️ لطفاً یک روز معتبر بین ۱ و ۳۱ وارد کن.")
        return DAY

# دستیار خطا
async def error(update: Update, context: CallbackContext):
    logger.warning(f"Update {update} caused error {context.error}")

# راه‌اندازی اصلی بات با استفاده از ConversationHandler
def main():
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    conversation_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            YEAR: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_year)],
            MONTH: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_month)],
            DAY: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_day)],
        },
        fallbacks=[MessageHandler(filters.TEXT & ~filters.COMMAND, start)],
    )

    application.add_handler(conversation_handler)
    application.add_error_handler(error)

    application.run_polling()

if __name__ == '__main__':
    main()

