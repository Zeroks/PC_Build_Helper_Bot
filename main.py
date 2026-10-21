import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
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
    check_build,
    select_first_type_component,
    select_second_type_component,
    select_final_component,
    add_component_in_build,
    search_in_base,
    )

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

Commands_dict = {
    "NewBuild": start_new_build,
    "BackMain": back_to_main,
    "OpenComponents" : select_components,
    "CheckBuild" : check_build,
    "BackBuild": back_to_build,

    "OpenChoiceCPU": select_component,
    "OpenChoiceMotherboard": select_component,
    "OpenChoiceRAM": select_component,
    "OpenChoiceGPU": select_component,
    "OpenChoicePowerUnit": select_component,            
    "OpenChoiceCase": select_component,                                                                        
}

class SearchStates(StatesGroup):
    waiting_for_query = State()



@dp.message(Command('start'))
async def start_comand(message: types.Message):
     await message.answer(
        start_text,
        reply_markup=start_keyboard()
        )
     logger.info(f"User {message.from_user.id} started")


@dp.callback_query(lambda c: c.data.startswith("Select"))
async def handle_select_component(callback: types.CallbackQuery, state: FSMContext):
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
    elif data.startswith("SelectBySearch_"):
        component_type = data.replace("SelectBySearch_", "")
        await state.update_data(search_type=component_type)
        await state.set_state(SearchStates.waiting_for_query)
        await callback.message.edit_text(
            f"🔍 Enter {component_type} name:"
        )
    else:
        return

@dp.message(SearchStates.waiting_for_query)
async def process_search(message: types.Message, state: FSMContext):
    data = await state.get_data()
    search_type = data["search_type"]
    query = message.text.strip().lower()
    results = search_in_base(search_type, query)
    if not results:
        await message.answer("❌ Nothing found. Try another query or press Back.")
        return
    buttons = []
    for comp in results:
        buttons.append([
            InlineKeyboardButton(
                text=comp["name"],
                callback_data=f"SelectComponent_{search_type}_{comp['id']}"
            )
        ])
    buttons.append([InlineKeyboardButton(text="◀️Back", callback_data="BackComponents")])

    await message.answer(
        f"🔍 Found {len(results)} result(s):",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons)
    )
    await state.clear()

@dp.callback_query(lambda c: c.data == "BackComponents")
async def handle_back_from_search(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await select_components(callback)




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