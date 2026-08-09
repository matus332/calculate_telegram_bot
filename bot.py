import datetime

import telebot
from apscheduler.schedulers.background import BackgroundScheduler
import os

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from database import (
    get_dollar_balance,
    deposit_dollar,
    withdraw_dollar,
    get_grn_cash_balance,
    deposit_grn_cash,
    withdraw_grn_cash,
    deposit_grn_card,
    get_grn_card_balance,
    withdraw_grn_card,
    add_expense, daily_report_expenses, weekly_report_expenses, monthly_report_expenses, yearly_report_expenses,
    add_user, get_all_users,
)
from dotenv import load_dotenv

from keyboards import (
    markup_start,
    markup_menu,
    saving_markup,
    dollar_markup,
    grn_cash_markup,
    grn_card_markup,
    expenses_markup,
    back_to_expenses,
    cancel_input_markup,
    income_cancel_markup, report_money_markup, back_to_reports_markup,
)

load_dotenv()
BOT_TOKEN = os.environ.get("BOT_TOKEN")

bot = telebot.TeleBot(BOT_TOKEN)

category_names = {
    "products": "🛒 Продукты",
    "clothes": "👕 Одежда",
    "pets": "🐶 Питомец",
    "gym": "🏋️ Зал",
    "entertainment": "🎮 Развлечения",
    "restaurant": "🍽 Рестораны",
    "beauty": "🧴 Красота",
    "home": "🏠 Дом",
    "alco": "🍷 Алкоголь",
    "coffee": "☕️ Кофе",
    "taxi": "🚕 Такси",
    "another": "🔍 Другое",
}

@bot.message_handler(commands=["start"])
def send_welcome(message):
    add_user(message.from_user.id)
    bot.reply_to(
        message,
        "Привет! 👋\n"
        "Я помогу тебе учитывать расходы, доходы и накопления.\n"
        "Выбери нужное действие в меню ниже.",
        reply_markup=markup_start,
    )


@bot.message_handler(commands=["menu"])
def send_menu(message):
    bot.reply_to(
        message, "📊 Главное меню\n" "Выберите нужный раздел:", reply_markup=markup_menu
    )


@bot.message_handler(commands=["help"])
def send_help(message):
    bot.reply_to(
        message,
        "🤖 Доступные команды:\n\n"
        "/start — Запустить бота\n"
        "/menu — Открыть главное меню\n"
        "/help — Помощь",
        reply_markup=markup_start,
    )


# Dollar
def process_dollar_deposit(message):
    try:
        amount = int(message.text)
    except ValueError:
        message = bot.send_message(
            message.chat.id, "⚠️ Некорректный ввод\n\n" "Введите сумму числом:"
        )
        bot.register_next_step_handler(message, process_dollar_deposit)
        return

    if amount <= 0:
        message = bot.send_message(
            message.chat.id,
            "⚠️ Некорректная сумма\n\n"
            "Сумма должна быть больше 0.\n"
            "✏️ Введите другую сумму:",
        )
        bot.register_next_step_handler(message, process_dollar_deposit)
        return

    deposit_dollar(message.from_user.id, amount)

    dollar_balance = get_dollar_balance(message.from_user.id)

    bot.send_message(
        message.chat.id,
        f"✅ Счёт успешно пополнен\n\n"
        f"➕ Сумма: {amount} $\n"
        f"💰 Баланс: {dollar_balance} $",
        reply_markup=dollar_markup,
    )


def process_dollar_withdraw(message):
    try:
        amount = int(message.text)
    except ValueError:
        message = bot.send_message(
            message.chat.id, "⚠️ Некорректный ввод\n\n" "Введите сумму числом:"
        )
        bot.register_next_step_handler(message, process_dollar_withdraw)
        return

    if amount <= 0:
        message = bot.send_message(
            message.chat.id,
            "⚠️ Некорректная сумма\n\n"
            "Сумма должна быть больше 0.\n"
            "✏️ Введите другую сумму:",
        )
        bot.register_next_step_handler(message, process_dollar_withdraw)
        return

    dollar_balance = get_dollar_balance(message.from_user.id)
    if dollar_balance is None:
        dollar_balance = 0

    if dollar_balance < amount:
        message = bot.send_message(
            message.chat.id, f"❌ Недостаточно средств\n💰 Баланс: {dollar_balance}$"
        )
        bot.register_next_step_handler(message, process_dollar_withdraw)
        return

    withdraw_dollar(message.from_user.id, amount)

    dollar_balance = get_dollar_balance(message.from_user.id)

    bot.send_message(
        message.chat.id,
        f"✅ Средства успешно сняты\n\n"
        f"➖ Сумма: {amount} $\n"
        f"💰 Баланс: {dollar_balance} $",
        reply_markup=dollar_markup,
    )


# GRN CASH
def process_grn_deposit_cash(message):
    try:
        amount = int(message.text)
    except ValueError:
        message = bot.send_message(
            message.chat.id, "⚠️ Некорректный ввод\n\n" "Введите сумму числом:"
        )
        bot.register_next_step_handler(message, process_grn_deposit_cash)
        return

    if amount <= 0:
        message = bot.send_message(
            message.chat.id,
            "⚠️ Некорректная сумма\n\n"
            "Сумма должна быть больше 0.\n"
            "✏️ Введите другую сумму:",
        )
        bot.register_next_step_handler(message, process_grn_deposit_cash)
        return

    deposit_grn_cash(message.from_user.id, amount)

    grn_balance = get_grn_cash_balance(message.from_user.id)

    bot.send_message(
        message.chat.id,
        f"✅ Счёт успешно пополнен\n\n"
        f"➕ Сумма: {amount} ₴\n"
        f"💰 Баланс: {grn_balance} ₴",
        reply_markup=grn_cash_markup,
    )


def process_grn_cash_withdraw(message):
    try:
        amount = int(message.text)
    except ValueError:
        message = bot.send_message(
            message.chat.id, "⚠️ Некорректный ввод\n\n" "Введите сумму числом:"
        )
        bot.register_next_step_handler(message, process_grn_cash_withdraw)
        return

    if amount <= 0:
        message = bot.send_message(
            message.chat.id,
            "⚠️ Некорректная сумма\n\n"
            "Сумма должна быть больше 0.\n"
            "✏️ Введите другую сумму:",
        )
        bot.register_next_step_handler(message, process_grn_cash_withdraw)
        return

    grn_balance = get_grn_cash_balance(message.from_user.id)
    if grn_balance is None:
        grn_balance = 0

    if grn_balance < amount:
        message = bot.send_message(
            message.chat.id, f"❌ Недостаточно средств\nБаланс: {grn_balance}₴"
        )
        bot.register_next_step_handler(message, process_grn_cash_withdraw)
        return

    withdraw_grn_cash(message.from_user.id, amount)

    grn_balance = get_grn_cash_balance(message.from_user.id)

    bot.send_message(
        message.chat.id,
        f"✅ Средства успешно сняты\n\n"
        f"➖ Сумма: {amount} ₴\n"
        f"💰 Баланс: {grn_balance} ₴",
        reply_markup=grn_cash_markup,
    )


# GRN CARD
def process_grn_deposit_card(message):
    try:
        amount = int(message.text)
    except ValueError:
        message = bot.send_message(
            message.chat.id, "⚠️ Некорректный ввод\n\n" "Введите сумму числом:"
        )
        bot.register_next_step_handler(message, process_grn_deposit_card)
        return

    if amount <= 0:
        message = bot.send_message(
            message.chat.id,
            "⚠️ Некорректная сумма\n\n"
            "Сумма должна быть больше 0.\n"
            "✏️ Введите другую сумму:",
        )
        bot.register_next_step_handler(message, process_grn_deposit_card)
        return

    deposit_grn_card(message.from_user.id, amount)

    grn_balance = get_grn_card_balance(message.from_user.id)

    bot.send_message(
        message.chat.id,
        f"✅ Счёт успешно пополнен\n\n"
        f"➕ Сумма: {amount} ₴\n"
        f"💰 Баланс: {grn_balance} ₴",
        reply_markup=grn_card_markup,
    )


def process_grn_card_withdraw(message):
    try:
        amount = int(message.text)
    except ValueError:
        message = bot.send_message(
            message.chat.id, "⚠️ Некорректный ввод\n\n" "Введите сумму числом:"
        )
        bot.register_next_step_handler(message, process_grn_card_withdraw)
        return

    if amount <= 0:
        message = bot.send_message(
            message.chat.id,
            "⚠️ Некорректная сумма\n\n"
            "Сумма должна быть больше 0.\n"
            "✏️ Введите другую сумму:",
        )
        bot.register_next_step_handler(message, process_grn_card_withdraw)
        return

    grn_balance = get_grn_card_balance(message.from_user.id)
    if grn_balance is None:
        grn_balance = 0

    if grn_balance < amount:
        message = bot.send_message(
            message.chat.id, f"❌ Недостаточно средств\nБаланс: {grn_balance}₴"
        )
        bot.register_next_step_handler(message, process_grn_card_withdraw)
        return

    withdraw_grn_card(message.from_user.id, amount)

    grn_balance = get_grn_card_balance(message.from_user.id)

    bot.send_message(
        message.chat.id,
        f"✅ Средства успешно сняты\n\n"
        f"➖ Сумма: {amount} ₴\n"
        f"💰 Баланс: {grn_balance} ₴",
        reply_markup=grn_card_markup,
    )


def process_expense(message, payment_method, category):
    try:
        amount = int(message.text)
    except ValueError:
        message = bot.send_message(
            message.chat.id, "⚠️ Некорректный ввод\n\n" "Введите сумму числом:"
        )
        bot.register_next_step_handler(
            message, process_expense, payment_method, category
        )
        return

    if amount <= 0:
        message = bot.send_message(
            message.chat.id,
            "⚠️ Некорректная сумма\n\n"
            "Сумма должна быть больше 0.\n"
            "✏️ Введите другую сумму",
        )
        bot.register_next_step_handler(
            message, process_expense, payment_method, category
        )
        return

    if payment_method == "card":
        balance = get_grn_card_balance(message.from_user.id)
    elif payment_method == "cash":
        balance = get_grn_cash_balance(message.from_user.id)
    else:
        bot.send_message(
            message.chat.id,
            "❌ Неизвестный способ оплаты"
        )
        return

    if balance is None:
        balance = 0

    if balance < amount:
        message = bot.send_message(
            message.chat.id,
            f"❌ Недостаточно средств\n\n"
            f"💰 Доступно: {balance} ₴\n"
            f"✏️ Введите другую сумму",
        )
        bot.register_next_step_handler(
            message, process_expense, payment_method, category
        )
        return

    if payment_method == "card":
        withdraw_grn_card(message.from_user.id, amount)

    elif payment_method == "cash":
        withdraw_grn_cash(message.from_user.id, amount)

    else:
        bot.send_message(
            message.chat.id,
            "❌ Неизвестный способ оплаты"
        )
        return

    add_expense(message.from_user.id, amount, payment_method, category)

    if payment_method == "card":
        balance = get_grn_card_balance(message.from_user.id)

    elif payment_method == "cash":
        balance = get_grn_cash_balance(message.from_user.id)

    else:
        bot.send_message(
            message.chat.id,
            "❌ Неизвестный способ оплаты"
        )
        return

    category_name = category_names.get(category, category)

    bot.send_message(
        message.chat.id,
        f"✅ Покупка успешно записана\n\n"
        f"💸 Сумма: {amount} ₴\n"
        f"🛒 Категория: {category_name}\n"
        f"💰 Остаток: {balance} ₴",
        reply_markup=expenses_markup,
    )

def send_daily_report(user_id):
    date = datetime.date.today()
    daily_expenses = daily_report_expenses(user_id, date)

    text = "📅 Расходы за сегодня\n\n"
    total = 0

    for category, amount in daily_expenses:
        category_name = category_names.get(category, category)
        text += f"{category_name} — {amount} ₴\n"
        total += amount

    text += f"\n💸 Всего за день: {total}₴"

    bot.send_message(
        user_id,
        text
    )

def send_daily_reports_to_all():
    users = get_all_users()

    for user in users:
        user_id = user[0]
        send_daily_report(user_id)

def send_weekly_report(user_id):
    end_date = datetime.date.today()
    start_date = end_date - datetime.timedelta(days=end_date.weekday())

    weekly_expenses = weekly_report_expenses(user_id, start_date, end_date)
    text = "📅 Расходы за неделю\n\n"
    total = 0

    for category, amount in weekly_expenses:
        category_name = category_names.get(category, category)
        text += f"{category_name} — {amount} ₴\n"
        total += amount

    text += f"\n💸 Всего за неделю: {total}₴"

    bot.send_message(user_id, text)


def send_weekly_reports_to_all():
    users = get_all_users()

    for user in users:
        user_id = user[0]
        send_weekly_report(user_id)

def send_monthly_report(user_id):
    end_date = datetime.date.today()

    start_date = end_date.replace(day=1)

    monthly_report = monthly_report_expenses(user_id, start_date, end_date)
    text = "📅 Расходы за месяц\n\n"
    total = 0

    for category, amount in monthly_report:
        category_name = category_names.get(category, category)
        text += f"{category_name} — {amount} ₴\n"
        total += amount

    text += f"\n💸 Всего за месяц: {total}₴"

    bot.send_message(user_id, text)

def send_monthly_reports_to_all():
    users = get_all_users()

    for user in users:
        user_id = user[0]
        send_monthly_report(user_id)

def send_yearly_report(user_id):
    end_date = datetime.date.today()

    start_date = end_date.replace(month=1, day=1)

    yearly_report = yearly_report_expenses(user_id, start_date, end_date)
    text = "📅 Расходы за год\n\n"
    total = 0

    for category, amount in yearly_report:
        category_name = category_names.get(category, category)
        text += f"{category_name} — {amount} ₴\n"
        total += amount

    text += f"\n💸 Всего за год: {total}₴"

    bot.send_message(user_id, text)

def send_yearly_reports_to_all():
    users = get_all_users()

    for user in users:
        user_id = user[0]
        send_yearly_report(user_id)

@bot.callback_query_handler(func=lambda call: True)
def callback_menu(call):

    if call.data == "menu_start":
        bot.edit_message_text(
            text="📊 Главное меню\n" "Выберите нужный раздел:",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=markup_menu,
        )

    elif call.data == "report_money_button":
        bot.edit_message_text(
            text="📈 Сводки",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=report_money_markup,
        )

    elif call.data == "saving_menu_button":
        bot.edit_message_text(
            text="💰 Сбережения",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=saving_markup,
        )

    elif call.data == "saving_dollars_button":
        bot.edit_message_text(
            text="💲 Долларовый счёт",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=dollar_markup,
        )

    elif call.data == "dollar_balance_button":
        dollar_balance = get_dollar_balance(call.from_user.id)
        if dollar_balance is None:
            dollar_balance = 0
        bot.edit_message_text(
            text=f"💰 Баланс: {dollar_balance}$",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=dollar_markup,
        )

    elif call.data == "deposit_dollar_button":
        bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
        message = bot.send_message(
            call.message.chat.id,
            "➕ Введите сумму пополнения:",
            reply_markup=income_cancel_markup,
        )
        bot.register_next_step_handler(message, process_dollar_deposit)

    elif call.data == "withdraw_dollar_button":
        bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
        message = bot.send_message(
            call.message.chat.id,
            "➖ Введите сумму снятия:",
            reply_markup=income_cancel_markup,
        )
        bot.register_next_step_handler(message, process_dollar_withdraw)

    elif call.data == "back_to_saving":
        bot.edit_message_text(
            text="💰 Мои сбережения:",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=saving_markup,
        )

    elif call.data == "back_to_menu":
        bot.edit_message_text(
            text="📊 Главное меню\n" "Выберите нужный раздел:",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=markup_menu,
        )

    elif call.data == "saving_grn_cash_button":
        bot.edit_message_text(
            text="💵 Наличные ₴",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=grn_cash_markup,
        )

    elif call.data == "grn_cash_balance_button":
        grn_balance = get_grn_cash_balance(call.from_user.id)
        if grn_balance is None:
            grn_balance = 0
        bot.edit_message_text(
            text=f"💰 Баланс(cash): {grn_balance}₴",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=grn_cash_markup,
        )

    elif call.data == "deposit_grn_cash_button":
        bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
        message = bot.send_message(
            call.message.chat.id,
            "➕ Введите сумму пополнения:",
            reply_markup=income_cancel_markup,
        )
        bot.register_next_step_handler(message, process_grn_deposit_cash)

    elif call.data == "withdraw_grn_cash_button":
        bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
        message = bot.send_message(
            call.message.chat.id,
            "➖ Введите сумму снятия:",
            reply_markup=income_cancel_markup,
        )
        bot.register_next_step_handler(message, process_grn_cash_withdraw)

    elif call.data == "saving_grn_card_button":
        bot.edit_message_text(
            text="💳 Карта ₴",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=grn_card_markup,
        )

    elif call.data == "grn_card_balance_button":
        grn_balance = get_grn_card_balance(call.from_user.id)
        if grn_balance is None:
            grn_balance = 0
        bot.edit_message_text(
            text=f"💰 Баланс(card): {grn_balance}₴",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=grn_card_markup,
        )

    elif call.data == "deposit_grn_card_button":
        bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
        message = bot.send_message(
            call.message.chat.id,
            "➕ Введите сумму пополнения:",
            reply_markup=income_cancel_markup,
        )
        bot.register_next_step_handler(message, process_grn_deposit_card)

    elif call.data == "withdraw_grn_card_button":
        bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
        message = bot.send_message(
            call.message.chat.id,
            "➖ Введите сумму снятия:",
            reply_markup=income_cancel_markup,
        )
        bot.register_next_step_handler(message, process_grn_card_withdraw)

    elif call.data == "expenses_menu_button":
        bot.edit_message_text(
            text="💸 Выберите категорию расходов",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=expenses_markup,
        )

    elif call.data == "back_to_expenses":
        bot.edit_message_text(
            text="💸 Выберите категорию расходов",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=expenses_markup,
        )

    elif call.data.startswith("expenses:"):
        category = call.data.split(":")[1]
        payment_markup = InlineKeyboardMarkup()
        card_button = InlineKeyboardButton(
            "Card ₴", callback_data=f"payment:card:{category}"
        )
        cash_button = InlineKeyboardButton(
            "Cash ₴", callback_data=f"payment:cash:{category}"
        )
        payment_markup.add(back_to_expenses, card_button, cash_button)

        bot.edit_message_text(
            text="💳 Выберите способ оплаты:",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=payment_markup,
        )

    elif call.data.startswith("payment:"):
        parts = call.data.split(":")

        payment_method = parts[1]
        category = parts[2]

        if payment_method == "card":
            balance = get_grn_card_balance(call.from_user.id)

        elif payment_method == "cash":
            balance = get_grn_cash_balance(call.from_user.id)

        if balance is None:
            balance = 0

        bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)

        message = bot.send_message(
            call.message.chat.id,
            f"💰 Баланс: {balance}₴\n🛒 Введите сумму покупки:",
            reply_markup=cancel_input_markup,
        )

        bot.register_next_step_handler(
            message, process_expense, payment_method, category
        )

    elif call.data == "cancel_input":
        bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)

        bot.edit_message_text(
            text="💸 Выберите категорию расходов:",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=expenses_markup,
        )

    elif call.data == "cancel_income_input":
        bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)

        bot.edit_message_text(
            text="💰 Мои сбережения:",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=saving_markup,
        )

    elif call.data == "back_to_reports":
        bot.edit_message_text(
            text="📈 Сводки",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=report_money_markup,
        )

    elif call.data == "daily_report_button":
        date = datetime.date.today()
        daily_expenses = daily_report_expenses(call.from_user.id, date)
        text = "📅 Расходы за сегодня\n\n"
        total = 0

        for category, amount in daily_expenses:
            category_name = category_names.get(category, category)
            text += f"{category_name} — {amount} ₴\n"
            total += amount

        text += f"\n💸 Всего за день: {total}₴"

        bot.edit_message_text(
            text=text,
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=back_to_reports_markup
        )

    elif call.data == "weekly_report_button":
        end_date = datetime.date.today()

        start_date = end_date - datetime.timedelta(days=end_date.weekday())


        weekly_report = weekly_report_expenses(call.from_user.id, start_date, end_date)
        text = "📅 Расходы за неделю\n\n"
        total = 0

        for category, amount in weekly_report:
            category_name = category_names.get(category, category)
            text += f"{category_name} — {amount} ₴\n"
            total += amount

        text += f"\n💸 Всего за неделю: {total}₴"

        bot.edit_message_text(
            text=text,
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=back_to_reports_markup
        )

    elif call.data == "monthly_report_button":
        end_date = datetime.date.today()

        start_date = end_date.replace(day=1)

        monthly_report = monthly_report_expenses(call.from_user.id, start_date, end_date)
        text = "📅 Расходы за месяц\n\n"
        total = 0

        for category, amount in monthly_report:
            category_name = category_names.get(category, category)
            text += f"{category_name} — {amount} ₴\n"
            total += amount

        text += f"\n💸 Всего за месяц: {total}₴"

        bot.edit_message_text(
            text=text,
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=back_to_reports_markup
        )

    elif call.data == "yearly_report_button":
        end_date = datetime.date.today()

        start_date = end_date.replace(month=1, day=1)

        yearly_report = yearly_report_expenses(call.from_user.id, start_date, end_date)
        text = "📅 Расходы за год\n\n"
        total = 0

        for category, amount in yearly_report:
            category_name = category_names.get(category, category)
            text += f"{category_name} — {amount} ₴\n"
            total += amount

        text += f"\n💸 Всего за год: {total}₴"

        bot.edit_message_text(
            text=text,
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=back_to_reports_markup
        )

def run_bot():
    scheduler = BackgroundScheduler(timezone="Europe/Kyiv")

    scheduler.add_job(
        send_daily_reports_to_all,
        "cron",
        hour=20,
        minute=0,
    )

    scheduler.add_job(
        send_weekly_reports_to_all,
        "cron",
        day_of_week="sun",
        hour=20,
        minute=0,
    )

    scheduler.add_job(
        send_monthly_reports_to_all,
        "cron",
        day="last",
        hour=20,
        minute=0,
    )

    scheduler.add_job(
        send_yearly_reports_to_all,
        "cron",
        month=12,
        day=31,
        hour=20,
        minute=0,
    )
    scheduler.start()


    bot.remove_webhook()
    bot.infinity_polling()


if __name__ == "__main__":
    run_bot()
