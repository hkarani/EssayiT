import datetime
import time
import logging
from django.utils import timezone
from telegram import ParseMode, Update, CallbackQuery
from telegram.ext import CallbackContext, ConversationHandler

from tgbot.handlers.onboarding import static_text
from tgbot.handlers.utils.info import extract_user_data_from_update
from tgbot.handlers.utils.texts import get_user_text_message
from tgbot.models import User
from verification.models import UserVerificationDetails
from tgbot.handlers.onboarding.keyboards import (
    make_keyboard_for_start_command,
    make_keyboard_for_wrong_code,
    make_keyboard_for_reenter_email
)
from tgbot.handlers.onboarding.keyboards import (
    make_keyboard_for_get_email, 
    make_keyboard_for_wrong_code, 
    make_keyboard_for_writer_or_client_choice,
    make_keyboard_for_reenter_email
) 
from verification.tasks import (
        send_verfication_email, 
        email_regex_check, 
        generate_five_digit_code, 
        code_regex_check
)


GET_EMAIL, VALIDATE_EMAIL_AND_SEND_CODE ,VERIFY_CODE, LETS_GO ,CHOOSE_USER_TYPE, RESEND_CODE, PRE_START = range(7)

#Constants 
WRITER, CLIENT, GOING_BACK = range(7,10)

def start_menu(update: Update, context: CallbackContext) -> str:
    print("Command start called")
    user_id = extract_user_data_from_update(update)['user_id']
    user, first_time_user = User.get_user_and_created(update, context)
    user_type = UserVerificationDetails.get_user_type(user_id)
    print(user_type)
    user_types_and_texts_dict = {
        "WRITER": "Welcome writer",
        "CLIENT": "Welcome Client",
        "FIRST_TIME_USER":static_text.start_created.format(first_name=user.first_name),
        "UNVERIFIED":static_text.start_not_created.format(first_name=user.first_name) ,
        None: static_text.start_created.format(first_name=user.first_name)
    }
    text = user_types_and_texts_dict[user_type]
    new_users = ["FIRST_TIME_USER", "UNVERIFIED", None]
    if(user_type in new_users):        
        UserVerificationDetails.create_user_verification_details(user_id)
        UserVerificationDetails.update_user_type(user_id, "UNVERIFIED")
        essay_it_intro = static_text.essay_it_bot_introduction_text        
        context.bot.send_message(chat_id = user_id,text=text)
        time.sleep(2)
        context.bot.send_message(
            chat_id = user_id,
            text=essay_it_intro,
            reply_markup= make_keyboard_for_start_command(),
            parse_mode=ParseMode.HTML
        )
        return LETS_GO    
    
    if(user_type == 'CLIENT'):
        text = "This is the menu for the clients"
        context.bot.send_message(
            chat_id = user_id, 
            text=text,
            reply_markup= make_keyboard_for_start_command(),
            parse_mode=ParseMode.HTML
        )
    
    if(user_type == 'WRITER'):
        text = "This is the menu for the writers"
        context.bot.send_message(
            chat_id = user_id, 
            text=text,
            reply_markup= make_keyboard_for_start_command(),
            parse_mode=ParseMode.HTML
        )
 
    

def lets_go(update: Update, context: CallbackContext) -> str:
    # callback_data: SECRET_LEVEL_BUTTON variable from manage_data.py
    """ Pressed 'secret_level_button_text' after /start command"""
    print("Lets go")
    text = static_text.pick_one_writer_or_client
    update.callback_query.answer()
    update.callback_query.edit_message_text( text=text, reply_markup=make_keyboard_for_writer_or_client_choice())
    return CHOOSE_USER_TYPE

def client_choice(update: Update, context: CallbackContext):
    context.user_data[CLIENT] = True
    user_id = extract_user_data_from_update(update)['user_id']
    print("Clients_choice_function run")
    verify_text = static_text.enter_email    
    update.callback_query.answer()
    update.callback_query.edit_message_text( text=verify_text, reply_markup=make_keyboard_for_get_email())
    UserVerificationDetails.update_user_type(user_id, "CLIENT")
    return VALIDATE_EMAIL_AND_SEND_CODE

def writer_choice(update: Update, context: CallbackContext):
    context.user_data[CLIENT] = True
    user_id = extract_user_data_from_update(update)['user_id']
    print("Writers_choice_function run")
    verify_text = static_text.enter_email
    update.callback_query.answer()
    update.callback_query.edit_message_text( text=verify_text, reply_markup=make_keyboard_for_get_email())
    UserVerificationDetails.update_user_type(user_id, "WRITER")
    return VALIDATE_EMAIL_AND_SEND_CODE

    
def get_email(update: Update, context: CallbackContext):
    """ Pressed 'verify_button_text' after let's go command"""
    user_id = extract_user_data_from_update(update)['user_id']
    verify_text = static_text.enter_email
    
    context.bot.edit_message_text(
        text=verify_text,
        chat_id=user_id,
        reply_markup=make_keyboard_for_get_email(),
        message_id=update.callback_query.message.message_id,
        parse_mode=ParseMode.HTML
    )    
    return VALIDATE_EMAIL_AND_SEND_CODE

#Get user email input    
def validate_user_email_and_send_code(update: Update, context: CallbackContext):
    user_id = extract_user_data_from_update(update)['user_id']
    email_from_chat = str(update.effective_message.text)
    verification_code = generate_five_digit_code()    
    if email_regex_check(email_from_chat):
        if(UserVerificationDetails.check_if_email_is_taken(user_id=user_id,email = email_from_chat)):
            UserVerificationDetails.create_user_verification_details(user_id, **{'email' : email_from_chat ,'verification_code': verification_code})
            text = "This email is taken please enter another email"
            update.message.reply_text(text=text,)
        else:
            UserVerificationDetails.create_user_verification_details(user_id, **{'email' : email_from_chat ,'verification_code': verification_code})
            UserVerificationDetails.increment_email_attempts(user_id=user_id)
            if (UserVerificationDetails.get_email_entry_attempts(user_id) <= 4):
                text = static_text.text_asking_for_email_code.format(
                    email_entered =  email_from_chat
                )
                send_verfication_email(email_from_chat)
                update.message.reply_text(text=text, reply_markup=make_keyboard_for_reenter_email())
                return VERIFY_CODE
            else: 
                blocked_user_text = static_text.blocked_user_text  
                update.message.reply_text(
                    text=blocked_user_text     
                )
    else:             
        
        UserVerificationDetails.create_user_verification_details(user_id)
        UserVerificationDetails.increment_email_attempts(user_id=user_id)
        if (UserVerificationDetails.get_email_entry_attempts(user_id) <= 4):
            wrong_email_text = static_text.wrong_email_entry    
            update.message.reply_text(
                    text=wrong_email_text,       
            )
        else: 
            blocked_user_text = static_text.blocked_user_text  
            update.message.reply_text(
                    text=blocked_user_text,                              
        )

   
def handle_code_verification(update: Update, context: CallbackContext):
    user_id = extract_user_data_from_update(update)['user_id']
    verification_code = UserVerificationDetails.get_verification_code(user_id)
    code_received = update.effective_message.text
    code_verification_attempts = UserVerificationDetails.get_code_verification_attempts(user_id)
    
    if (code_regex_check(code_received)):
        UserVerificationDetails.increment_code_attempts(user_id)
        if(code_verification_attempts <= 5):
            print('1')
            code_received = int(code_received)
            if(code_received == verification_code):
                print('2')
                welcome_text = static_text.welcome_to_essay_it
                update.message.reply_text(text=welcome_text)
                return ConversationHandler.END
            else:
                print('2.1')
                user_email = UserVerificationDetails.get_user_email_by_id(user_id=user_id)
                wrong_code_text = static_text.wrong_code_entry.format(
                    email =  user_email
                )
                update.message.reply_text(text=wrong_code_text, reply_markup=make_keyboard_for_wrong_code())    
        else:
            print('3')
            too_many_attempts = static_text.blocked_user_text
            update.message.reply_text(text=too_many_attempts)
    else:
        print(3.1)
        user_email = UserVerificationDetails.get_user_email_by_id(user_id=user_id)
        code_failed_regex = static_text.failed_regex.format(
            email = user_email
        )
        update.message.reply_text(
            text=code_failed_regex,
            reply_markup=make_keyboard_for_wrong_code()
        )

def resend_code(update: Update, context: CallbackContext) -> str:
    verification_code = generate_five_digit_code()
    user_id = extract_user_data_from_update(update)['user_id']
    UserVerificationDetails.update_verifcation_code(user_id, verification_code)
    user_email = UserVerificationDetails.get_user_email_by_id(user_id=user_id)    
    text = static_text.text_asking_for_email_code.format(
                email_entered =  user_email
    )
    context.bot.edit_message_text(
        text=text,
        chat_id=user_id,
        reply_markup=make_keyboard_for_get_email(),
        message_id=update.callback_query.message.message_id,
        parse_mode=ParseMode.HTML
    ) 
    return VERIFY_CODE
    


def go_back_to_start(update: Update, context: CallbackContext):
    user, first_time_user = User.get_user_and_created(update, context)
    writer = False
    client = True
    
    if writer:
        text = "Welcome writer"
    elif client:
        text = "Welcome Client"
    elif first_time_user:
        text = static_text.start_created.format(first_name=user.first_name)
    elif user:
        text = static_text.start_not_created.format(first_name=user.first_name)
    essay_it_intro = static_text.essay_it_bot_introduction_text
    update.message.reply_text(
        text=essay_it_intro,
        reply_markup=make_keyboard_for_start_command(),
        parse_mode=ParseMode.HTML
    )
    

user_type_conversation = {
    "WRITER": WRITER,
    "CLIENT": CLIENT,
    "FIRST_TIME_USER": LETS_GO,
    "UNVERIFIED" : LETS_GO        
}


    