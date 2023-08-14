from telegram import Update
from telegram.ext import (
    CommandHandler, ConversationHandler, filters, MessageHandler
)

from callback_funcs import (
    cancel, start, description, question_18,
    question_19, question_20, question_21, question_22, question_23,
    question_24, question_25, question_26, question_27, question_28,
    question_29, question_30, question_31, question_32, question_33,
    question_34, question_35, question_36, question_37, question_38,
    question_39, question_40, question_41, question_42, question_43,
    question_44, question_45, question_46, question_47, question_48,
    question_49, question_50, question_51, question_52, question_53,
    question_54, question_55, question_56, question_57, question_58,
    question_59, question_60, question_61, question_62, question_63,
    question_64, question_65, question_66, question_67, question_68,
    question_69, question_70, question_71, question_72, question_73,
    question_74, question_75, question_76, question_77, question_78,
    question_79, question_80, question_81, question_82, question_83,
    question_84, question_85, question_86, question_87, QUESTION_18,
    QUESTION_19, QUESTION_20, QUESTION_21, QUESTION_22, QUESTION_23,
    QUESTION_24, QUESTION_25, QUESTION_26, QUESTION_27, QUESTION_28,
    QUESTION_29, QUESTION_30, QUESTION_31, QUESTION_32, QUESTION_33,
    QUESTION_34, QUESTION_35, QUESTION_36, QUESTION_37, QUESTION_38,
    QUESTION_39, QUESTION_40, QUESTION_41, QUESTION_42, QUESTION_43,
    QUESTION_44, QUESTION_45, QUESTION_46, QUESTION_47, QUESTION_48,
    QUESTION_49, QUESTION_50, QUESTION_51, QUESTION_52, QUESTION_53,
    QUESTION_54, QUESTION_55, QUESTION_56, QUESTION_57, QUESTION_58,
    QUESTION_59, QUESTION_60, QUESTION_61, QUESTION_62, QUESTION_63,
    QUESTION_64, QUESTION_65, QUESTION_66, QUESTION_67, QUESTION_68,
    QUESTION_69, QUESTION_70, QUESTION_71, QUESTION_72, QUESTION_73,
    QUESTION_74, QUESTION_75, QUESTION_76, QUESTION_77, QUESTION_78,
    QUESTION_79, QUESTION_80, QUESTION_81, QUESTION_82, QUESTION_83,
    QUESTION_84, QUESTION_85, QUESTION_86, QUESTION_87, DESCRIPTION
)
from keyboards import CANCEL_COMMAND, MAGIC_WORD_FOR_START_THIS_HANDLER, NEXT


FILTER = filters.Regex("^(а|б)$")


task_2_handler = ConversationHandler(
        entry_points=[
            MessageHandler(
                filters.Regex(MAGIC_WORD_FOR_START_THIS_HANDLER),
                start
            )
        ],
        states={
            QUESTION_18: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, question_18)
            ],
            QUESTION_19: [MessageHandler(FILTER, question_19)],
            QUESTION_20: [MessageHandler(FILTER, question_20)],
            QUESTION_21: [MessageHandler(FILTER, question_21)],
            QUESTION_22: [MessageHandler(FILTER, question_22)],
            QUESTION_23: [MessageHandler(FILTER, question_23)],
            QUESTION_24: [MessageHandler(FILTER, question_24)],
            QUESTION_25: [MessageHandler(FILTER, question_25)],
            QUESTION_26: [MessageHandler(FILTER, question_26)],
            QUESTION_27: [MessageHandler(FILTER, question_27)],
            QUESTION_28: [MessageHandler(FILTER, question_28)],
            QUESTION_29: [MessageHandler(FILTER, question_29)],
            QUESTION_30: [MessageHandler(FILTER, question_30)],
            QUESTION_31: [MessageHandler(FILTER, question_31)],
            QUESTION_32: [MessageHandler(FILTER, question_32)],
            QUESTION_33: [MessageHandler(FILTER, question_33)],
            QUESTION_34: [MessageHandler(FILTER, question_34)],
            QUESTION_35: [MessageHandler(FILTER, question_35)],
            QUESTION_36: [MessageHandler(FILTER, question_36)],
            QUESTION_37: [MessageHandler(FILTER, question_37)],
            QUESTION_38: [MessageHandler(FILTER, question_38)],
            QUESTION_39: [MessageHandler(FILTER, question_39)],
            QUESTION_40: [MessageHandler(FILTER, question_40)],
            QUESTION_41: [MessageHandler(FILTER, question_41)],
            QUESTION_42: [MessageHandler(FILTER, question_42)],
            QUESTION_43: [MessageHandler(FILTER, question_43)],
            QUESTION_44: [MessageHandler(FILTER, question_44)],
            QUESTION_45: [MessageHandler(FILTER, question_45)],
            QUESTION_46: [MessageHandler(FILTER, question_46)],
            QUESTION_47: [MessageHandler(FILTER, question_47)],
            QUESTION_48: [MessageHandler(FILTER, question_48)],
            QUESTION_49: [MessageHandler(FILTER, question_49)],
            QUESTION_50: [MessageHandler(FILTER, question_50)],
            QUESTION_51: [MessageHandler(FILTER, question_51)],
            QUESTION_52: [MessageHandler(FILTER, question_52)],
            QUESTION_53: [MessageHandler(FILTER, question_53)],
            QUESTION_54: [MessageHandler(FILTER, question_54)],
            QUESTION_55: [MessageHandler(FILTER, question_55)],
            QUESTION_56: [MessageHandler(FILTER, question_56)],
            QUESTION_57: [MessageHandler(FILTER, question_57)],
            QUESTION_58: [MessageHandler(FILTER, question_58)],
            QUESTION_59: [MessageHandler(FILTER, question_59)],
            QUESTION_60: [MessageHandler(FILTER, question_60)],
            QUESTION_61: [MessageHandler(FILTER, question_61)],
            QUESTION_62: [MessageHandler(FILTER, question_62)],
            QUESTION_63: [MessageHandler(FILTER, question_63)],
            QUESTION_64: [MessageHandler(FILTER, question_64)],
            QUESTION_65: [MessageHandler(FILTER, question_65)],
            QUESTION_66: [MessageHandler(FILTER, question_66)],
            QUESTION_67: [MessageHandler(FILTER, question_67)],
            QUESTION_68: [MessageHandler(FILTER, question_68)],
            QUESTION_69: [MessageHandler(FILTER, question_69)],
            QUESTION_70: [MessageHandler(FILTER, question_70)],
            QUESTION_71: [MessageHandler(FILTER, question_71)],
            QUESTION_72: [MessageHandler(FILTER, question_72)],
            QUESTION_73: [MessageHandler(FILTER, question_73)],
            QUESTION_74: [MessageHandler(FILTER, question_74)],
            QUESTION_75: [MessageHandler(FILTER, question_75)],
            QUESTION_76: [MessageHandler(FILTER, question_76)],
            QUESTION_77: [MessageHandler(FILTER, question_77)],
            QUESTION_78: [MessageHandler(FILTER, question_78)],
            QUESTION_79: [MessageHandler(FILTER, question_79)],
            QUESTION_80: [MessageHandler(FILTER, question_80)],
            QUESTION_81: [MessageHandler(FILTER, question_81)],
            QUESTION_82: [MessageHandler(FILTER, question_82)],
            QUESTION_83: [MessageHandler(FILTER, question_83)],
            QUESTION_84: [MessageHandler(FILTER, question_84)],
            QUESTION_85: [MessageHandler(FILTER, question_85)],
            QUESTION_86: [MessageHandler(FILTER, question_86)],
            QUESTION_87: [MessageHandler(FILTER, question_87)],
            DESCRIPTION: [MessageHandler(FILTER, description)]
        },
        fallbacks=[CommandHandler(CANCEL_COMMAND, cancel)],
    )


if __name__ == "__main__":
    import os

    from dotenv import load_dotenv
    from telegram.ext import Application


    load_dotenv()
    TOKEN = os.getenv('TOKEN')


    application = Application.builder().token(TOKEN).build()
    application.add_handler(task_2_handler)
    application.run_polling(allowed_updates=Update.ALL_TYPES)
