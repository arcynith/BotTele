import os
import logging
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    ConversationHandler,
    filters,
)

# Load environment variables dari file .env
load_dotenv()

# Konfigurasi logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# Ambil token dari .env
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Definisi State untuk percakapan
CHOOSING, GET_USERNAME = range(2)

def get_main_menu_keyboard():
    """Membuat keyboard menu utama dengan tombol Inline."""
    keyboard = [
        [
            InlineKeyboardButton("1. Diamond", callback_data="Diamond"),
            InlineKeyboardButton("2. Cash", callback_data="Cash"),
        ],
        [
            InlineKeyboardButton("3. Poin", callback_data="Poin"),
            InlineKeyboardButton("4. Lokasi", callback_data="Lokasi"),
        ],
        [
            InlineKeyboardButton("🔄 Coba Lagi", callback_data="retry"),
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handler /start: Menampilkan menu utama."""
    reply_markup = get_main_menu_keyboard()
    await update.message.reply_text(
        "Halo Bang! Selamat datang.\nSilakan pilih layanan di bawah ini:",
        reply_markup=reply_markup,
    )
    return CHOOSING

async def handle_button_click(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Menangani klik pada tombol Inline."""
    query = update.callback_query
    await query.answer()
    
    choice_data = query.data
    
    if choice_data == "retry":
        # Reset menu jika tombol 'Coba Lagi' ditekan
        await query.edit_message_text(
            text="Menu sudah di-reset bg. Silakan pilih layanan lagi:",
            reply_markup=get_main_menu_keyboard()
        )
        return CHOOSING
    
    # Simpan pilihan layanan dan minta username
    context.user_data["menu_choice"] = choice_data
    await query.edit_message_text(
        text=f"Oit! Kamu pilih *{choice_data}*.\n\nSekarang, silakan ketik *usernamenya* bg:",
        parse_mode="Markdown"
    )
    return GET_USERNAME

async def handle_username(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Menangani input username dan menampilkan konfirmasi + menu lagi."""
    username = update.message.text
    choice_name = context.user_data.get("menu_choice", "Layanan")

    reply_markup = get_main_menu_keyboard()
    await update.message.reply_text(
        f"Sipp mantap bg!\n\n"
        f"Layanan: *{choice_name}*\n"
        f"Username: *{username}*\n\n"
        f"Pesanan kamu lagi diproses ya.\n"
        "Ada lagi yang mau dibantu?",
        parse_mode="Markdown",
        reply_markup=reply_markup,
    )
    return CHOOSING

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Membatalkan sesi."""
    await update.message.reply_text("Siap bg, kalau butuh lagi ketik /start ya!", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

def main() -> None:
    if not BOT_TOKEN or BOT_TOKEN == "TOKEN_BOT_ANDA_DI_SINI":
        print("ERROR: BOT_TOKEN salah atau belum diisi di file .env!")
        return

    # Bangun aplikasi
    application = Application.builder().token(BOT_TOKEN).build()

    # Conversation Handler buat alur: Start -> Pilih Menu -> Input Username
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            CHOOSING: [
                CallbackQueryHandler(handle_button_click)
            ],
            GET_USERNAME: [
                MessageHandler(filters.TEXT & ~(filters.COMMAND), handle_username),
            ],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
        allow_reentry=True
    )

    application.add_handler(conv_handler)
    application.add_handler(CommandHandler("start", start))

    print("Bot sudah kembali normal bg... Tekan Ctrl+C buat berhenti.")
    application.run_polling()

if __name__ == "__main__":
    main()
