import sqlite3

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton
from aiogram.utils import executor
from crud_functions import *

api = 'token'  <<<-----------------------------------------------------<<<
bot = Bot(token= api)
dp = Dispatcher(bot, storage= MemoryStorage())

# ===== инициализируем клавиатуру =====
# kb = InlineKeyboardMarkup()
# =====================================
# ======================= Создаем кнопки и добавляем к клавитауре =================
# button1 = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data= 'calories')
# button2 = InlineKeyboardButton(text= 'Формулы расчёта', callback_data='formulas')
# button3 = InlineKeyboardButton(text= 'Купить', callback_data= 'Купить')
# kb.add(button1, button2)
# kb.add(button3)

# ===>> Клавиатура Reply
kb = ReplyKeyboardMarkup(resize_keyboard=True)

button1 = KeyboardButton(text='Рассчитать норму калорий')
button2 = KeyboardButton(text= 'Формулы расчёта')
button3 = KeyboardButton(text= 'Купить')
kb.add(button1, button2)
kb.add(button3)

# =========>> Keyboard Buying >>=============
kb_buy = InlineKeyboardMarkup(resize_keyboard=True)
but_prod1 = InlineKeyboardButton(text= 'Product1', callback_data= 'product_buying')
but_prod2 = InlineKeyboardButton(text= 'Product2', callback_data= 'product_buying')
but_prod3 = InlineKeyboardButton(text= 'Product3', callback_data= 'product_buying')
but_prod4 = InlineKeyboardButton(text= 'Product4', callback_data= 'product_buying')
kb_buy.add(but_prod1,but_prod2,but_prod3,but_prod4)


key_board2 = InlineKeyboardMarkup()
bu_ = InlineKeyboardButton(text = '/start', callback_data= '/start')
key_board2.insert(bu_)

class UserState(StatesGroup):
    age= State()
    growth= State()
    weight= State()

# price = {1:200, 2: 250, 3: 500, 4: 1250}
# picture = {1: 'jp1.jpg', 2: 'jp2.jpg', 3: 'jp3.jpg', 4: 'jp4.jpg'}

# @dp.message_handler(text= 'Купить')
# async def get_buying_list(message):
#     with open('jp1.jpg', 'rb') as img1:
#         await message.answer(f'Название: Product1 |Описание: Описание1 |Цена: {price[1]}')
#         await message.answer_photo(img1)
#     for i in range(2, 5):
#         current_pic = picture[i]
#         with open(current_pic, 'rb') as img:
#             await message.answer(f'Название: Product{i} |Описание: Описание{i} |Цена: {price[i]}')
#             await message.answer_photo(img)
#     await message.answer('Выберите продукт для покупки: ', reply_markup= kb_buy)

# >>  альтернативный код с SQL =================================================================

@dp.message_handler(text= 'Купить')
async def get_buying_list(message):
    connection = sqlite3.connect('Products.db')
    cursor = connection.cursor()
    cursor.execute('select * from Products')
    products = cursor.fetchall()
    for product in products:
        with open(product[4], 'rb') as image:
            await message.answer(f'Название: {product[1]} |Описание: {product[2]} |Цена: {product[3]}')
            await message.answer_photo(image)
    await message.answer('Выберите продукт для покупки: ', reply_markup=kb_buy)
    connection.close()
#==============================================================================================






@dp.callback_query_handler(text= 'product_buying')
async def send_confirm_message(call):
    await call.message.answer('Вы успешно приобрели продукт!')
    await call.answer()

@dp.message_handler(text= 'Формулы расчёта')
async def get_formulas(message):
    await message.answer('формулы Миффлина-Сан Жеора:\n(10 x вес (кг) + 6.25 x рост (см) – 5 x возраст (г) + 5) x A')
    await message.answer('Минимальная активность: A = 1,2.\nЭкстра-активность: A = 1,9')


@dp.message_handler(text= ['Рассчитать норму калорий', '1'])
async def set_age(message):
    await message.answer('Введите свой возраст: ')
    await UserState.age.set()

@dp.message_handler(state = UserState.age)
async  def set_growth(message, state):
    await state.update_data(age = message.text)
    await message.answer('Введите свой рост: ')
    await UserState.growth.set()

@dp.message_handler(state = UserState.growth)
async  def add_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer('Введите свой вес: ')
    await UserState.weight.set()

@dp.message_handler(state= UserState.weight)
async def send_calories(message, state):
    await  state.update_data(weight= message.text)
    data = await state.get_data()
    calories = 10 * int(data['weight']) + 6.25 * int(data['growth']) - 5 * int(data['age']) + 5
    await message.answer(f'Ваша суточная норма калорий составляет {calories}')
    await state.finish()

@dp.callback_query_handler(text= '/start')
async def main_menu(call):
    await call.message.answer('Выберите опцию', reply_markup= kb)
    await call.answer()

@dp.message_handler(text= '/start')
async def main_menu(message):
    await message.answer('Выберите опцию', reply_markup= kb)

@dp.message_handler()
async def greeting(message):
    await message.answer('Для начала работы нажмите start', reply_markup= key_board2)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates= True)
