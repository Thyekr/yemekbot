import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    MessageHandler, ContextTypes, filters
)

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = 8503159266

MENU = {
    "hamburger": ("🍔 Hamburger", 100),
    "pizza": ("🍕 Pizza", 250),
    "tost": ("🥪 Tost", 110),
    "icecek": ("🥤 İçecek", 30)
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🍔 Hamburger - 100 TL", callback_data="hamburger")],
        [InlineKeyboardButton("🍕 Pizza - 250 TL", callback_data="pizza")],
        [InlineKeyboardButton("🥪 Tost - 110 TL", callback_data="tost")],
        [InlineKeyboardButton("🥤 İçecek - 30 TL", callback_data="icecek")]
    ]

    await update.message.reply_text(
        "🍽️ Yemek Botumuza Hoş Geldin!\n\n"
        "Menüden siparişini seç.\n"
        "🚚 TESLİMAT ÜCRETSİZ!",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def select(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    product = MENU.get(query.data)
    if product:
        context.user_data["product"] = product
        await query.message.reply_text(
            f"Seçimin: {product[0]}\n"
            f"Fiyat: {product[1]} TL\n\n"
            "📍 Lütfen teslimat adresini yaz."
        )

async def address(update: Update, context: ContextTypes.DEFAULT_TYPE):
    product = context.user_data.get("product")

    if not product:
        await update.message.reply_text("Önce /start yazarak ürün seç.")
        return

    user = update.effective_user
    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=(
            "🛒 YENİ SİPARİŞ!\n\n"
            f"Ürün: {product[0]}\n"
            f"Fiyat: {product[1]} TL\n"
            "Teslimat: ÜCRETSİZ\n"
            f"Müşteri: {user.first_name}\n"
            f"Adres: {update.message.text}"
        )
    )

    await update.message.reply_text(
        "✅ Siparişin alındı!\n"
        "🚚 Teslimat ücretsizdir.\n"
        "Teşekkür ederiz!"
    )
    context.user_data.clear()

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(select))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, address))
    app.run_polling()

if __name__ == "__main__":
    main()
