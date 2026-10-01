from aiogram import types
from data.COMPONENTS_DATA import COMPONENTS
from texts import (
    build_check_status,
    start_text, 
    select_components_text,  
    )
from keyboards import (
    start_keyboard, 
    start_new_build_keyboard, 
    select_components_keyboard , 
    select_component_keyboard, 

    select_first_type_component_keyboard,
    select_second_type_component_keyboard,
    select_final_component_keyboard

    )
from data.User_builds_data import user_builds


CATEGORY_MENUS = {
    "CPU": {
        "text": "Choose CPU brand:",
        "keyboard": select_first_type_component_keyboard("CPU"),
    },
    "MOTHERBOARD": {
        "text": "Choose Motherboard brand:",
        "keyboard": select_first_type_component_keyboard("MOTHERBOARD"),
    },
    "RAM": {
        "text": "Choose RAM brand:",
        "keyboard": select_first_type_component_keyboard("RAM"),
    },
    "GPU": {
        "text": "Choose GPU brand:",
        "keyboard": select_first_type_component_keyboard("GPU"),
    },
    "PU": {
        "text": "Choose Power unit brand:",
        "keyboard": select_first_type_component_keyboard("PU"),
    },
    "CASE": {
        "text": "Choose Case brand:",
        "keyboard": select_first_type_component_keyboard("CASE"),
    },
}


async def start_new_build(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    if user_id not in user_builds:
        user_builds[user_id] = {
            "CPU" : None,
            "MOTHERBOARD" : None,
            "RAM" : None,
            "GPU" : None,
            "PU" : None,
            "CASE" : None,
        }

    await callback.message.edit_text(
            build_check_status(user_builds[user_id]),
            reply_markup=start_new_build_keyboard()
            )

async def select_components(callback: types.CallbackQuery):
    await callback.message.edit_text(
            select_components_text,
            reply_markup=select_components_keyboard()
            )

async def back_to_main(callback: types.CallbackQuery):
    await callback.message.edit_text(
        start_text,
        reply_markup=start_keyboard()
    )

async def back_to_build(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    build = user_builds.get(user_id)
    
    if build is None:
        await callback.answer("Build not found")
        return
    
    await callback.message.edit_text(
        build_check_status(build),
        reply_markup=start_new_build_keyboard()
    )


async def select_component(callback: types.CallbackQuery):
    data = callback.data
    if data == "OpenChoiceCPU":
        text = "Choose CPU search method:"
        keyboard=select_component_keyboard(component_type="CPU")

    elif data == "OpenChoiceMotherboard":
        text = "Choose motherboard search method:"
        keyboard=select_component_keyboard(component_type="MOTHERBOARD")
        
    elif data == "OpenChoiceRAM":
        text = "Choose RAM search method:"
        keyboard=select_component_keyboard(component_type="RAM")
        
    elif data == "OpenChoiceGPU":
        text = "Choose GPU search method:"
        keyboard=select_component_keyboard(component_type="GPU")
        
    elif data == "OpenChoicePowerUnit":
        text = "Choose Power unit search method:"
        keyboard=select_component_keyboard(component_type="PU")
        
    elif data == "OpenChoiceCase":
        text = "Choose Case search method:"
        keyboard=select_component_keyboard(component_type="CASE")
        
    else:
        await callback.answer("Unknown component")
        return
    
    await callback.message.edit_text(
        text,
        reply_markup=keyboard
    )
    
async def select_first_type_component(callback, component_type):
    menu = CATEGORY_MENUS.get(component_type)
    if menu is None:
        await callback.answer("Unknown component")
        return
    await callback.message.edit_text(
        menu["text"],
        reply_markup=menu["keyboard"]
    )

async def select_second_type_component(callback, parts):
    component_type = parts[0]
    brand = parts[1]
    data_source = COMPONENTS.get(component_type)
    brand_data = data_source.get(brand) 

    series_list = list(brand_data.keys())
    
    await callback.message.edit_text(
        f"Choose {brand} series:",
        reply_markup=select_second_type_component_keyboard(component_type, brand, series_list)
    )

async def select_final_component(callback, parts):
    component_type = parts[0]   
    brand = parts[1]            
    subtype = parts[2]         

    models = COMPONENTS.get(component_type, {}).get(brand, {}).get(subtype)

    await callback.message.edit_text(
        f"Choose {subtype} model:",
        reply_markup=select_final_component_keyboard(component_type, brand, subtype, models)
    )


def find_component_by_id(component_type, component_id):
    from data.COMPONENTS_DATA import COMPONENTS
    component_data = COMPONENTS.get(component_type)
    for brand, series_dict in component_data.items():
        for series_name, components in series_dict.items():
            for component in components:
                if component["id"] == component_id:
                    return component
    return None

async def add_component_in_build(callback, parts):
    component_type = parts[0]
    component_id = parts[1]
    component = find_component_by_id(component_type, component_id)
    user_id = callback.from_user.id
    if user_id not in user_builds:
        user_builds[user_id] = {
                    "CPU" : None,
                    "MOTHERBOARD" : None,
                    "RAM" : None,
                    "GPU" : None,
                    "PU" : None,
                    "CASE" : None,
                }
    user_builds[user_id][parts[0]] = component
    await callback.answer(f"✅ {component['name']} selected!")
    await callback.message.edit_text(
        build_check_status(user_builds[user_id]),
        reply_markup=start_new_build_keyboard()
    )
    
     
























