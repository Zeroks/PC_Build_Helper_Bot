from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from data.COMPONENTS_DATA import COMPONENTS

def start_keyboard():
    buttons = [ 
        [
            InlineKeyboardButton(text="New build",callback_data="NewBuild"),
            InlineKeyboardButton(text="My builds", callback_data="MyBuilds")
        ],
        [
            InlineKeyboardButton(text="Compare builds", callback_data="Compare"),
            InlineKeyboardButton(text="Help", callback_data="Help")
        ] 
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def start_new_build_keyboard():
    buttons = [
        [
            InlineKeyboardButton(text="🔍Add component", callback_data="OpenComponents"),
            InlineKeyboardButton(text="🧐Check build", callback_data="CheckBuild"),
            InlineKeyboardButton(text="💾Save build", callback_data="SaveBuild")
        ],
        [
            InlineKeyboardButton(text="🏠Back to main", callback_data="BackMain"), 
        ]
        
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def select_components_keyboard():
    buttons = [
        [InlineKeyboardButton(text="🧠CPU",callback_data="OpenChoiceCPU")],
        [InlineKeyboardButton(text="🔌Motherboard",callback_data="OpenChoiceMotherboard")],
        [InlineKeyboardButton(text="⚡RAM",callback_data="OpenChoiceRAM")],
        [InlineKeyboardButton(text="🎮GPU",callback_data="OpenChoiceGPU")],
        [InlineKeyboardButton(text="🔋Power unit",callback_data="OpenChoicePowerUnit")],
        [InlineKeyboardButton(text="📦Case",callback_data="OpenChoiceCase")],
        [
            InlineKeyboardButton(text="◀️Back", callback_data="BackBuild"),
            InlineKeyboardButton(text="🏠Back to main", callback_data="BackMain")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def check_result_keyboard():
    buttons = [
        [
            InlineKeyboardButton(text="🔍Add component", callback_data="OpenComponents"),
            InlineKeyboardButton(text="🧐Check build", callback_data="CheckBuild"),
            InlineKeyboardButton(text="💾Save build", callback_data="SaveBuild")
        ],
        [
            InlineKeyboardButton(text="◀️Back", callback_data="BackBuild"),
            InlineKeyboardButton(text="🏠Back to main", callback_data="BackMain"), 
        ]
            
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def select_component_keyboard(component_type):
    buttons = [
        [InlineKeyboardButton(text="Search by category",callback_data=f"SelectByCategory_{component_type}")],
        [InlineKeyboardButton(text="Search by name",callback_data=f"SelectBySearch_{component_type}")],
        [InlineKeyboardButton(text="◀️Back",callback_data="BackComponents")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def select_first_type_component_keyboard(component_type):
    brands = COMPONENTS[component_type].keys()
    buttons = [
            [
                InlineKeyboardButton(
                    text = brand,
                    callback_data=f"SelectBrand_{component_type}_{brand}"
                )
                for brand in brands
            ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def select_second_type_component_keyboard(component_type, brand, series_list):
    buttons = [
        [
            InlineKeyboardButton(
                text=series,
                callback_data=f"SelectSeries_{component_type}_{brand}_{series}"
            )
            for series in series_list
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def select_final_component_keyboard(component_type, brand, subcategory, models_list):
    buttons = [
        [
            InlineKeyboardButton(
                text=model["name"],
                callback_data=f"SelectComponent_{component_type}_{model['id']}"
            )
        ]
        for model in models_list
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)













