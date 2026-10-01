import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.client.session.aiohttp import AiohttpSession
from dotenv import load_dotenv
from loguru import logger
from keyboards import start_keyboard
from texts import start_text

from functions import (
    start_new_build, 
    back_to_main, 
    select_components, 
    back_to_build, 
    select_component, 
    select_first_type_component,
    select_second_type_component,
    select_final_component,
    add_component_in_build,
    )

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

Commands_dict = {
    "NewBuild": start_new_build,
    "BackMain": back_to_main,
    "OpenComponents" : select_components,
    "BackBuild": back_to_build,

    "OpenChoiceCPU": select_component,
    "OpenChoiceMotherboard": select_component,
    "OpenChoiceRAM": select_component,
    "OpenChoiceGPU": select_component,
    "OpenChoicePowerUnit": select_component,            
    "OpenChoiceCase": select_component,                                                                        

    "BackComponents": select_components,
}



@dp.message(Command('start'))
async def start_comand(message: types.Message):
     await message.answer(
        start_text,
        reply_markup=start_keyboard()
        )
     logger.info(f"User {message.from_user.id} started")


@dp.callback_query(lambda c: c.data.startswith("Select"))
async def handle_select_cpu(callback: types.CallbackQuery):
    data = callback.data
    if data.startswith("SelectByCategory_"):
        component_type = data.replace("SelectByCategory_", "")
        await select_first_type_component(callback, component_type)

    elif data.startswith("SelectBrand_"):
        parts = data.replace("SelectBrand_", "").split("_", 1)
        await select_second_type_component(callback, parts)
    elif data.startswith("SelectSeries_"):
        parts = data.replace("SelectSeries_", "").split("_", 2)
        await select_final_component(callback, parts)
    elif data.startswith("SelectComponent_"):
        parts = data.replace("SelectComponent_", "").split("_", 1)
        await add_component_in_build(callback, parts)
    else:
        return



@dp.callback_query()
async def check_callback(callback: types.CallbackQuery):
    handler = Commands_dict.get(callback.data)
    if handler:
        await handler(callback)
    else:
        await callback.answer("Unknown command")


async def main():
    await dp.start_polling(bot)

if __name__=="__main__":
    asyncio.run(main())