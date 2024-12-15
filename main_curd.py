from aiogram import Dispatcher, Bot, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from crud_functions import get_all_products
from config import api

dp = Dispatcher(Bot(token= api), storage= MemoryStorage())


@dp.message_handler()
async def anyway_func(message):
    products = get_all_products()
    for prod in products:
        with open(prod[4], 'rb') as img:
            await message.answer(f'Название:  {prod[1]} | Описание: {prod[2]} | Цена: {prod[3]}')
            await message.answer_photo(img)

executor.start_polling(dp,)