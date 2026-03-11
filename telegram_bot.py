import logging
from telegram import (
    Update,
    InlineQueryResultArticle,
    InputTextMessageContent,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from telegram.ext import (
    filters,
    ApplicationBuilder,
    CallbackQueryHandler,
    ContextTypes,
    ConversationHandler,
    CommandHandler,
    InlineQueryHandler,
    MessageHandler
)
from uuid import uuid4

from cashback_service import CashbackService


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)


class TelegramCashbackBot:
    def __init__(self):
        self.cashback_handler = CashbackService()
        self.application = ApplicationBuilder().token("TOKEN").build()

        # Обработчики команд
        start_handler = CommandHandler("start", self.start)

        self.application.add_handler(start_handler)
        self.application.add_handler(CallbackQueryHandler(self.button_callback))

    def run_bot(self) -> None:
        """
        Запуск бота
        :return:
        """
        self.application.run_polling()

    def get_main_menu_keyboard(self):
        keyboard = [
            [InlineKeyboardButton("Все кешбэки", callback_data="view_all")]
        ]
        return InlineKeyboardMarkup(keyboard)

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Обработчик команды /start
        :param update: данные из Telegram, сообщение, юзер и т.д.
        :param context: данные о состоянии бота
        :return:
        """
        reply_markup = self.get_main_menu_keyboard()
        await update.message.reply_text(
            "Добро пожаловать в кешбэе бот!\n\n"
            "Выберите действие:",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )

    async def button_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()

        if query.data == "view_all":
            info = self.cashback_handler.get_cashback_info()
            await query.edit_message_text(
                info,
                parse_mode="Markdown",
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton("Назад", callback_data="main_menu")
                ]])
            )

        elif query.data == "main_menu":
            reply_markup = self.get_main_menu_keyboard()
            await query.edit_message_text(
                "Выберите действие:",
                reply_markup=reply_markup,
                parse_mode="Markdown"
            )


def main() -> None:
    """
    Главная функция
    :return:
    """
    cashback_bot = TelegramCashbackBot()
    cashback_bot.run_bot()


if __name__ == "__main__":
    main()
