"""
    Onboarding conversations
"""

from telegram.ext import (
    Updater, Dispatcher, Filters,
    CommandHandler, MessageHandler,
    CallbackQueryHandler,ConversationHandler
)

from tgbot.handlers.onboarding import handlers as onboarding_handlers
from tgbot.handlers.onboarding.manage_data import (
    RESEND_CODE,
    REENTER_EMAIL,
    GO_BACK_TO_START,
    LETS_GO_BUTTON,
    IS_WRITER,
    IS_CLIENT,
    SHOW_ME,
    PRE_START_DATA
)


choose_user_type_handlers = [
    CallbackQueryHandler(onboarding_handlers.client_choice, pattern=f"^{IS_CLIENT}"),
    CallbackQueryHandler(onboarding_handlers.writer_choice, pattern=f"^{IS_WRITER}")
]

validate_email_and_send_code_handlers = [
    MessageHandler(Filters.text, onboarding_handlers.validate_user_email_and_send_code),
    CallbackQueryHandler(onboarding_handlers.lets_go, pattern=f"^{REENTER_EMAIL}"),
    CallbackQueryHandler(onboarding_handlers.start_menu, pattern=f"^{GO_BACK_TO_START}"),
    
]

verify_code_handlers = [
    CallbackQueryHandler(onboarding_handlers.lets_go, pattern=f"^{REENTER_EMAIL}"),
    CallbackQueryHandler(onboarding_handlers.start_menu, pattern=f"^{GO_BACK_TO_START}"),
    MessageHandler(Filters.text, onboarding_handlers.handle_code_verification),
    CallbackQueryHandler(onboarding_handlers.resend_code, pattern=f"^{RESEND_CODE}")    
]

onboarding_conversation = ConversationHandler(
    entry_points=[CommandHandler("start", onboarding_handlers.start_menu)],
    states= {
        onboarding_handlers.LETS_GO: [CallbackQueryHandler(onboarding_handlers.lets_go, pattern=f"^{LETS_GO_BUTTON}")],
        onboarding_handlers.CHOOSE_USER_TYPE:choose_user_type_handlers,
        onboarding_handlers.GET_EMAIL: [MessageHandler(Filters.text, onboarding_handlers.get_email)],
        onboarding_handlers.VALIDATE_EMAIL_AND_SEND_CODE: validate_email_and_send_code_handlers,
        onboarding_handlers.VERIFY_CODE: verify_code_handlers
    }, 
    fallbacks=[
        CommandHandler("start", onboarding_handlers.start_menu),
    ]                         
)

