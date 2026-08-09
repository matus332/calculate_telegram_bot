from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# markup to /start menu
markup_start = InlineKeyboardMarkup()
menu_start = InlineKeyboardButton("Меню", callback_data="menu_start")
markup_start.add(menu_start)
back_to_menu = InlineKeyboardButton("⬅️ Назад", callback_data="back_to_menu")


back_to_reports_markup = InlineKeyboardMarkup()
back_to_reports_button = InlineKeyboardButton("⬅️ Назад", callback_data="back_to_reports")
back_to_reports_markup.add(back_to_reports_button)


# markup to /menu
markup_menu = InlineKeyboardMarkup()
expenses_menu_button = InlineKeyboardButton(
    "💸 Расходы", callback_data="expenses_menu_button"
)
saving_menu_button = InlineKeyboardButton(
    "💰 Сбережения", callback_data="saving_menu_button"
)
report_money_button = InlineKeyboardButton("📈 Сводки", callback_data="report_money_button")
markup_menu.add(expenses_menu_button, saving_menu_button, report_money_button)

#markup to reports
report_money_markup = InlineKeyboardMarkup()
daily_report_button = InlineKeyboardButton("📅 За день", callback_data="daily_report_button")
weekly_report_button = InlineKeyboardButton("📊 За неделю", callback_data="weekly_report_button")

monthly_report_button = InlineKeyboardButton("🗓 За месяц", callback_data="monthly_report_button")

yearly_report_button = InlineKeyboardButton("📈 За год", callback_data="yearly_report_button")

report_money_markup.add(
    back_to_menu,
    daily_report_button,
    weekly_report_button,
    monthly_report_button,
    yearly_report_button,
)


# markup to /menu -> "Cбережения"
saving_markup = InlineKeyboardMarkup()
saving_dollars_button = InlineKeyboardButton(
    "💲 Доллары", callback_data="saving_dollars_button"
)
saving_grn_cash_button = InlineKeyboardButton(
    "💵 Наличные ₴", callback_data="saving_grn_cash_button"
)
saving_grn_card_button = InlineKeyboardButton(
    "💳 Карта ₴", callback_data="saving_grn_card_button"
)

saving_markup.add(
    back_to_menu, saving_dollars_button, saving_grn_cash_button, saving_grn_card_button
)


# markup to "$"
dollar_markup = InlineKeyboardMarkup()
dollar_balance_button = InlineKeyboardButton(
    "💰 Баланс", callback_data="dollar_balance_button"
)
deposit_dollar_button = InlineKeyboardButton(
    "➕ Пополнить", callback_data="deposit_dollar_button"
)
withdraw_dollar_button = InlineKeyboardButton(
    "➖ Снять", callback_data="withdraw_dollar_button"
)
back_to_saving = InlineKeyboardButton("⬅️ Назад", callback_data="back_to_saving")
dollar_markup.add(
    back_to_saving, dollar_balance_button, deposit_dollar_button, withdraw_dollar_button
)


# markup back to "$"
dollar_balance_markup = InlineKeyboardMarkup()
back_to_dollar = InlineKeyboardButton("⬅️ Назад", callback_data="back_to_dollar")
dollar_balance_markup.add(back_to_dollar)


# markup to "cash ₴"
grn_cash_markup = InlineKeyboardMarkup()
grn_cash_balance_button = InlineKeyboardButton(
    "💰 Баланс", callback_data="grn_cash_balance_button"
)
deposit_grn_cash_button = InlineKeyboardButton(
    "➕ Пополнить", callback_data="deposit_grn_cash_button"
)
withdraw_grn_cash_button = InlineKeyboardButton(
    "➖ Снять", callback_data="withdraw_grn_cash_button"
)
grn_cash_markup.add(
    back_to_saving,
    grn_cash_balance_button,
    deposit_grn_cash_button,
    withdraw_grn_cash_button,
)


# markup to "card ₴"
grn_card_markup = InlineKeyboardMarkup()
grn_card_balance_button = InlineKeyboardButton(
    "💰 Баланс", callback_data="grn_card_balance_button"
)
deposit_grn_card_button = InlineKeyboardButton(
    "➕ Пополнить", callback_data="deposit_grn_card_button"
)
withdraw_grn_card_button = InlineKeyboardButton(
    "➖ Снять", callback_data="withdraw_grn_card_button"
)
grn_card_markup.add(
    back_to_saving,
    grn_card_balance_button,
    deposit_grn_card_button,
    withdraw_grn_card_button,
)

# ----------------------------------------------------------------------------

# expenses markup
expenses_markup = InlineKeyboardMarkup()
products_button = InlineKeyboardButton("🛒 Продукты", callback_data="expenses:products")
clothes_button = InlineKeyboardButton("👕 Одежда", callback_data="expenses:clothes")
pet_button = InlineKeyboardButton("🐶 Питомец", callback_data="expenses:pets")
gym_button = InlineKeyboardButton("🏋️ Зал", callback_data="expenses:gym")
entertainment_button = InlineKeyboardButton(
    "🎮 Развлечения", callback_data="expenses:entertainment"
)
restaurant_button = InlineKeyboardButton(
    "🍽 Рестораны", callback_data="expenses:restaurant"
)
beauty_button = InlineKeyboardButton("🧴 Красота", callback_data="expenses:beauty")
home_button = InlineKeyboardButton("🏠 Дом", callback_data="expenses:home")
alco_button = InlineKeyboardButton("🍷 Алкоголь", callback_data="expenses:alco")
coffee_button = InlineKeyboardButton("☕️ Кофе", callback_data="expenses:coffee")
taxi_button = InlineKeyboardButton("🚕 Такси", callback_data="expenses:taxi")
another_button = InlineKeyboardButton("🔍 Другое", callback_data="expenses:another")
expenses_markup.add(
    back_to_menu,
    products_button,
    clothes_button,
    pet_button,
    gym_button,
    entertainment_button,
    restaurant_button,
    beauty_button,
    home_button,
    alco_button,
    coffee_button,
    taxi_button,
    another_button,
)
back_to_expenses = InlineKeyboardButton("⬅️ Назад", callback_data="back_to_expenses")

cancel_input_markup = InlineKeyboardMarkup()
cancel_input_button = InlineKeyboardButton("⬅️ Назад", callback_data="cancel_input")
cancel_input_markup.add(cancel_input_button)

income_cancel_markup = InlineKeyboardMarkup()

income_cancel_button = InlineKeyboardButton(
    "⬅️ Назад", callback_data="cancel_income_input"
)

income_cancel_markup.add(income_cancel_button)
