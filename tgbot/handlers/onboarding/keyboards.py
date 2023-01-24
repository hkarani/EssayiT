from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from tgbot.handlers.onboarding.manage_data import (
    LETS_GO_BUTTON,
    RESEND_CODE,
    GO_BACK_TO_START,
    REENTER_EMAIL,
    IS_CLIENT,
    IS_WRITER,
    SHOW_ME
)

from tgbot.handlers.onboarding.static_text import (
    back_to_let_go,
    client_choice, 
    writer_choice,
    resend_code,
    back_to_start,
    reenter_email,
    lets_go_button_text,
    show_me
)

def make_keyboard_for_start_command() -> InlineKeyboardMarkup:
    buttons = [[
        
        InlineKeyboardButton(lets_go_button_text, callback_data=f'{LETS_GO_BUTTON}'),
        
    ]
    ]

    return InlineKeyboardMarkup(buttons)

def make_keyboard_for_writer_or_client_choice() -> InlineKeyboardMarkup:
    buttons = [
        [
         InlineKeyboardButton(client_choice, callback_data=f'{IS_CLIENT}')         
        ],
        [ 
          InlineKeyboardButton(writer_choice, callback_data=f'{IS_WRITER}')          
        ]
    ]

    return InlineKeyboardMarkup(buttons)

def make_keyboard_for_get_email() -> InlineKeyboardMarkup:
    buttons = [[        
        InlineKeyboardButton(back_to_let_go, callback_data=f'{GO_BACK_TO_START}')
    ]]

    return InlineKeyboardMarkup(buttons)

def make_keyboard_for_wrong_code() -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(resend_code, callback_data=f'{RESEND_CODE}')
        ],
        [
            InlineKeyboardButton(back_to_start, callback_data=f'{GO_BACK_TO_START}')            
        ]
    ]    
    return InlineKeyboardMarkup(buttons)

def make_keyboard_for_reenter_email() -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(reenter_email, callback_data=f'{REENTER_EMAIL}')
        ],
        [
            InlineKeyboardButton(back_to_start, callback_data=f'{GO_BACK_TO_START}')            
        ]
    ]
    
    return InlineKeyboardMarkup(buttons)
