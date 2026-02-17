import os
import logging

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)


# Logging sederhana supaya kalau ada error bisa langsung terlihat di console.
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


# Token bot dibaca dari environment variable.
# Di lokal maupun di server (Render, Railway, dll) kita set BOT_TOKEN,
# sehingga token tidak disimpan langsung di source code.
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    # Kalau token belum di-set, hentikan program dengan pesan yang jelas.
    raise RuntimeError(
        "Environment variable BOT_TOKEN belum di-set. "
        "Lihat bagian konfigurasi di README.md."
    )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handler untuk perintah /start.

    Mengirim pesan menu utama dan menampilkan keyboard dengan tombol 1, 2, dan 3.
    """
    # Satu baris berisi tombol "1", "2", "3"
    keyboard = [["1", "2", "3"]]

    reply_markup = ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True,  # tombol menyesuaikan ukuran layar
        one_time_keyboard=False,  # keyboard tetap muncul setelah ditekan
    )

    await update.message.reply_text(
        "Menu Utama - Pilih tombol di bawah",
        reply_markup=reply_markup,
    )


async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handler untuk semua pesan teks biasa (bukan command).

    Mengecek tombol mana yang ditekan dan mengirim balasan yang sesuai.
    """
    if not update.message:
        # Untuk berjaga-jaga jika update tidak berisi message.
        logger.warning("Menerima update tanpa message.")
        return

    text = update.message.text

    if text == "1":
        await update.message.reply_text("Anda menekan tombol 1")
    elif text == "2":
        await update.message.reply_text("Anda menekan tombol 2")
    elif text == "3":
        await update.message.reply_text("Anda menekan tombol 3")
    else:
        await update.message.reply_text(
            "Silakan pilih salah satu tombol di keyboard: 1, 2, atau 3."
        )


def main() -> None:
    """
    Entry point program.

    Membangun Application, mendaftarkan handler,
    lalu menjalankan bot dengan metode polling.
    """
    application = Application.builder().token(BOT_TOKEN).build()

    # /start → handler start()
    application.add_handler(CommandHandler("start", start))

    # Semua teks biasa → handler handle_button()
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_button)
    )

    print("Bot sedang berjalan... Tekan Ctrl+C untuk menghentikan.")
    application.run_polling()


if __name__ == "__main__":
    main()
