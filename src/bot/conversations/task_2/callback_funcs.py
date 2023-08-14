import logging

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import ContextTypes, ConversationHandler

from templates import (
    DESCRIPTION_MESSAGE, START, STOP,
    MESSAGE_18, MESSAGE_19, MESSAGE_20, MESSAGE_21, MESSAGE_22, MESSAGE_23,
    MESSAGE_24, MESSAGE_25, MESSAGE_26, MESSAGE_27, MESSAGE_28, MESSAGE_29,
    MESSAGE_30, MESSAGE_31, MESSAGE_32, MESSAGE_33, MESSAGE_34, MESSAGE_35,
    MESSAGE_36, MESSAGE_37, MESSAGE_38, MESSAGE_39, MESSAGE_40, MESSAGE_41,
    MESSAGE_42, MESSAGE_43, MESSAGE_44, MESSAGE_45, MESSAGE_46, MESSAGE_47,
    MESSAGE_48, MESSAGE_49, MESSAGE_50, MESSAGE_51, MESSAGE_52, MESSAGE_53,
    MESSAGE_54, MESSAGE_55, MESSAGE_56, MESSAGE_57, MESSAGE_58, MESSAGE_59,
    MESSAGE_60, MESSAGE_61, MESSAGE_62, MESSAGE_63, MESSAGE_64, MESSAGE_65,
    MESSAGE_66, MESSAGE_67, MESSAGE_68, MESSAGE_69, MESSAGE_70, MESSAGE_71,
    MESSAGE_72, MESSAGE_73, MESSAGE_74, MESSAGE_75, MESSAGE_76, MESSAGE_77,
    MESSAGE_78, MESSAGE_79, MESSAGE_80, MESSAGE_81, MESSAGE_82, MESSAGE_83,
    MESSAGE_84, MESSAGE_85, MESSAGE_86, MESSAGE_87
)
from keyboards import (
    NEXT_PLACEHOLDER, NEXT_KEYBOARD, REPLY_KEYBOARD, INPUT_PLACEHOLDER,
    ANSWER, CANSEL
)


(
    QUESTION_18,
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
) = range(18, 89)


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)


async def start(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Вступление."""
    await update.message.reply_text(
        START,
        reply_markup=ReplyKeyboardMarkup(
            NEXT_KEYBOARD,
            one_time_keyboard=True,
            resize_keyboard=True,
            input_field_placeholder=NEXT_PLACEHOLDER
        ),
    )
    return QUESTION_18

async def question_18(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """18 вопрос."""
    await update.message.reply_text(
        MESSAGE_18,
        reply_markup=ReplyKeyboardMarkup(
            REPLY_KEYBOARD,
            one_time_keyboard=True,
            resize_keyboard=True,
            input_field_placeholder=INPUT_PLACEHOLDER
        ),
    )
    return QUESTION_19

async def question_19(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """19 вопрос."""
    logger.info(
        ANSWER, update.message.from_user.username, 18, update.message.text
    )
    await update.message.reply_text(
        MESSAGE_19,
        reply_markup=ReplyKeyboardMarkup(
            REPLY_KEYBOARD,
            one_time_keyboard=True,
            resize_keyboard=True,
            input_field_placeholder=INPUT_PLACEHOLDER
        ),
    )
    return QUESTION_20

async def question_20(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """20 вопрос."""
    logger.info(
        ANSWER, update.message.from_user.username, 19, update.message.text
    )
    await update.message.reply_text(
        MESSAGE_20,
        reply_markup=ReplyKeyboardMarkup(
            REPLY_KEYBOARD,
            one_time_keyboard=True,
            resize_keyboard=True,
            input_field_placeholder=INPUT_PLACEHOLDER
        ),
    )
    return QUESTION_21

async def question_21(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """21 вопрос."""
    logger.info(
        ANSWER, update.message.from_user.username, 20, update.message.text
    )
    await update.message.reply_text(
        MESSAGE_21,
        reply_markup=ReplyKeyboardMarkup(
            REPLY_KEYBOARD,
            one_time_keyboard=True,
            resize_keyboard=True,
            input_field_placeholder=INPUT_PLACEHOLDER
        ),
    )
    return QUESTION_22


async def question_22(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """22 вопрос."""
    logger.info(
        ANSWER, update.message.from_user.username, 21, update.message.text
    )
    await update.message.reply_text(
        MESSAGE_22,
        reply_markup=ReplyKeyboardMarkup(
            REPLY_KEYBOARD,
            one_time_keyboard=True,
            resize_keyboard=True,
            input_field_placeholder=INPUT_PLACEHOLDER
        ),
    )
    return QUESTION_23

async def question_23(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """23 вопрос."""
    logger.info(
        ANSWER, update.message.from_user.username, 22, update.message.text
    )
    await update.message.reply_text(
        MESSAGE_23,
        reply_markup=ReplyKeyboardMarkup(
            REPLY_KEYBOARD,
            one_time_keyboard=True,
            resize_keyboard=True,
            input_field_placeholder=INPUT_PLACEHOLDER
        ),
    )
    return QUESTION_24

async def question_24(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """24 вопрос."""
    logger.info(
        ANSWER, update.message.from_user.username, 23, update.message.text
    )
    await update.message.reply_text(
        MESSAGE_24,
        reply_markup=ReplyKeyboardMarkup(
            REPLY_KEYBOARD,
            one_time_keyboard=True,
            resize_keyboard=True,
            input_field_placeholder=INPUT_PLACEHOLDER
        ),
    )
    return QUESTION_25

async def question_25(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """25 вопрос."""
    logger.info(
        ANSWER, update.message.from_user.username, 24, update.message.text
    )
    await update.message.reply_text(
        MESSAGE_25,
        reply_markup=ReplyKeyboardMarkup(
            REPLY_KEYBOARD,
            one_time_keyboard=True,
            resize_keyboard=True,
            input_field_placeholder=INPUT_PLACEHOLDER
        ),
    )
    return QUESTION_26

async def question_26(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """26 вопрос."""
    logger.info(
        ANSWER, update.message.from_user.username, 25, update.message.text
    )
    await update.message.reply_text(
        MESSAGE_26,
        reply_markup=ReplyKeyboardMarkup(
            REPLY_KEYBOARD,
            one_time_keyboard=True,
            resize_keyboard=True,
            input_field_placeholder=INPUT_PLACEHOLDER
        ),
    )
    return QUESTION_27

async def question_27(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """27 вопрос."""
    logger.info(
        ANSWER, update.message.from_user.username, 26, update.message.text
    )
    await update.message.reply_text(
        MESSAGE_27,
        reply_markup=ReplyKeyboardMarkup(
            REPLY_KEYBOARD,
            one_time_keyboard=True,
            resize_keyboard=True,
            input_field_placeholder=INPUT_PLACEHOLDER
        ),
    )
    return QUESTION_28

async def question_28(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """28 вопрос."""
    logger.info(
        ANSWER, update.message.from_user.username, 27, update.message.text
    )
    await update.message.reply_text(
        MESSAGE_28,
        reply_markup=ReplyKeyboardMarkup(
            REPLY_KEYBOARD,
            one_time_keyboard=True,
            resize_keyboard=True,
            input_field_placeholder=INPUT_PLACEHOLDER
        ),
    )
    return QUESTION_29

async def question_29(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """29 вопрос."""
    logger.info(
        ANSWER, update.message.from_user.username, 28, update.message.text
    )
    await update.message.reply_text(
        MESSAGE_29,
        reply_markup=ReplyKeyboardMarkup(
            REPLY_KEYBOARD,
            one_time_keyboard=True,
            resize_keyboard=True,
            input_field_placeholder=INPUT_PLACEHOLDER
        ),
    )
    return QUESTION_30

async def question_30(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """30 вопрос."""
    logger.info(
        ANSWER, update.message.from_user.username, 29, update.message.text
    )
    await update.message.reply_text(
        MESSAGE_30,
        reply_markup=ReplyKeyboardMarkup(
            REPLY_KEYBOARD,
            one_time_keyboard=True,
            resize_keyboard=True,
            input_field_placeholder=INPUT_PLACEHOLDER
        ),
    )
    return QUESTION_31

async def question_31(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """31 вопрос."""
    logger.info(
        ANSWER, update.message.from_user.username, 30, update.message.text
    )
    await update.message.reply_text(
        MESSAGE_31,
        reply_markup=ReplyKeyboardMarkup(
            REPLY_KEYBOARD,
            one_time_keyboard=True,
            resize_keyboard=True,
            input_field_placeholder=INPUT_PLACEHOLDER
        ),
    )
    return QUESTION_32

async def question_32(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """32 вопрос."""
    logger.info(
        ANSWER, update.message.from_user.username, 31, update.message.text
    )
    await update.message.reply_text(
        MESSAGE_32,
        reply_markup=ReplyKeyboardMarkup(
            REPLY_KEYBOARD,
            one_time_keyboard=True,
            resize_keyboard=True,
            input_field_placeholder=INPUT_PLACEHOLDER
        ),
    )
    return QUESTION_33

async def question_33(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """33 вопрос."""
    logger.info(
        ANSWER, update.message.from_user.username, 32, update.message.text
    )
    await update.message.reply_text(
        MESSAGE_33,
        reply_markup=ReplyKeyboardMarkup(
            REPLY_KEYBOARD,
            one_time_keyboard=True,
            resize_keyboard=True,
            input_field_placeholder=INPUT_PLACEHOLDER
        ),
    )
    return QUESTION_34

async def question_34(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """34 вопрос."""
    logger.info(
        ANSWER, update.message.from_user.username, 33, update.message.text
    )
    await update.message.reply_text(
        MESSAGE_34,
        reply_markup=ReplyKeyboardMarkup(
            REPLY_KEYBOARD,
            one_time_keyboard=True,
            resize_keyboard=True,
            input_field_placeholder=INPUT_PLACEHOLDER
        ),
    )
    return QUESTION_35

async def question_35(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """35 вопрос."""
    logger.info(
        ANSWER, update.message.from_user.username, 34, update.message.text
    )
    await update.message.reply_text(
        MESSAGE_35,
        reply_markup=ReplyKeyboardMarkup(
            REPLY_KEYBOARD,
            one_time_keyboard=True,
            resize_keyboard=True,
            input_field_placeholder=INPUT_PLACEHOLDER
        ),
    )
    return QUESTION_36

async def question_36(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """36 вопрос."""
    logger.info(
        ANSWER, update.message.from_user.username, 35, update.message.text
    )
    await update.message.reply_text(
        MESSAGE_36,
        reply_markup=ReplyKeyboardMarkup(
            REPLY_KEYBOARD,
            one_time_keyboard=True,
            resize_keyboard=True,
            input_field_placeholder=INPUT_PLACEHOLDER
        ),
    )
    return QUESTION_37

async def question_37(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """37 вопрос."""
    logger.info(
        ANSWER, update.message.from_user.username, 36, update.message.text
    )
    await update.message.reply_text(
        MESSAGE_37,
        reply_markup=ReplyKeyboardMarkup(
            REPLY_KEYBOARD,
            one_time_keyboard=True,
            resize_keyboard=True,
            input_field_placeholder=INPUT_PLACEHOLDER
        ),
    )
    return QUESTION_38

async def question_38(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """38 вопрос."""
    logger.info(
        ANSWER, update.message.from_user.username, 37, update.message.text
    )
    await update.message.reply_text(
        MESSAGE_38,
        reply_markup=ReplyKeyboardMarkup(
            REPLY_KEYBOARD,
            one_time_keyboard=True,
            resize_keyboard=True,
            input_field_placeholder=INPUT_PLACEHOLDER
        ),
    )
    return QUESTION_39

async def question_39(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """39 вопрос."""
    logger.info(
        ANSWER, update.message.from_user.username, 38, update.message.text
    )
    await update.message.reply_text(
        MESSAGE_39,
        reply_markup=ReplyKeyboardMarkup(
            REPLY_KEYBOARD,
            one_time_keyboard=True,
            resize_keyboard=True,
            input_field_placeholder=INPUT_PLACEHOLDER
        ),
    )
    return QUESTION_40

async def question_40(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """40 вопрос."""
    logger.info(
        ANSWER, update.message.from_user.username, 39, update.message.text
    )
    await update.message.reply_text(
        MESSAGE_40,
        reply_markup=ReplyKeyboardMarkup(
            REPLY_KEYBOARD,
            one_time_keyboard=True,
            resize_keyboard=True,
            input_field_placeholder=INPUT_PLACEHOLDER
        ),
    )
    return QUESTION_41

async def question_41(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """41 вопрос."""
    logger.info(
        ANSWER, update.message.from_user.username, 40, update.message.text
    )
    await update.message.reply_text(
        MESSAGE_41,
        reply_markup=ReplyKeyboardMarkup(
            REPLY_KEYBOARD,
            one_time_keyboard=True,
            resize_keyboard=True,
            input_field_placeholder=INPUT_PLACEHOLDER
        ),
    )
    return QUESTION_42

async def question_42(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """42 вопрос."""
    logger.info(
        ANSWER, update.message.from_user.username, 41, update.message.text
    )
    await update.message.reply_text(
        MESSAGE_42,
        reply_markup=ReplyKeyboardMarkup(
            REPLY_KEYBOARD,
            one_time_keyboard=True,
            resize_keyboard=True,
            input_field_placeholder=INPUT_PLACEHOLDER
        ),
    )
    return QUESTION_43

async def question_43(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """43 вопрос."""
    logger.info(
        ANSWER, update.message.from_user.username, 42, update.message.text
    )
    await update.message.reply_text(
        MESSAGE_43,
        reply_markup=ReplyKeyboardMarkup(
            REPLY_KEYBOARD,
            one_time_keyboard=True,
            resize_keyboard=True,
            input_field_placeholder=INPUT_PLACEHOLDER
        ),
    )
    return QUESTION_44

async def question_44(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """44 вопрос."""
    logger.info(
        ANSWER, update.message.from_user.username, 43, update.message.text
    )
    await update.message.reply_text(
        MESSAGE_44,
        reply_markup=ReplyKeyboardMarkup(
            REPLY_KEYBOARD,
            one_time_keyboard=True,
            resize_keyboard=True,
            input_field_placeholder=INPUT_PLACEHOLDER
        ),
    )
    return QUESTION_45

async def question_45(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """45 вопрос."""
    logger.info(
        ANSWER, update.message.from_user.username, 44, update.message.text
    )
    await update.message.reply_text(
        MESSAGE_45,
        reply_markup=ReplyKeyboardMarkup(
            REPLY_KEYBOARD,
            one_time_keyboard=True,
            resize_keyboard=True,
            input_field_placeholder=INPUT_PLACEHOLDER
        ),
    )
    return QUESTION_46

async def question_46(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """46 вопрос."""
    logger.info(
        ANSWER, update.message.from_user.username, 45, update.message.text
    )
    await update.message.reply_text(
        MESSAGE_46,
        reply_markup=ReplyKeyboardMarkup(
            REPLY_KEYBOARD,
            one_time_keyboard=True,
            resize_keyboard=True,
            input_field_placeholder=INPUT_PLACEHOLDER
        ),
    )
    return QUESTION_47

async def question_47(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """47 вопрос."""
    logger.info(
        ANSWER, update.message.from_user.username, 46, update.message.text
    )
    await update.message.reply_text(
        MESSAGE_47,
        reply_markup=ReplyKeyboardMarkup(
            REPLY_KEYBOARD,
            one_time_keyboard=True,
            resize_keyboard=True,
            input_field_placeholder=INPUT_PLACEHOLDER
        ),
    )
    return QUESTION_48

async def question_48(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """48 вопрос."""
    logger.info(
        ANSWER, update.message.from_user.username, 47, update.message.text
    )
    await update.message.reply_text(
        MESSAGE_48,
        reply_markup=ReplyKeyboardMarkup(
            REPLY_KEYBOARD,
            one_time_keyboard=True,
            resize_keyboard=True,
            input_field_placeholder=INPUT_PLACEHOLDER
        ),
    )
    return QUESTION_49

async def question_49(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """49 вопрос."""
    logger.info(
        ANSWER, update.message.from_user.username, 48, update.message.text
    )
    await update.message.reply_text(
        MESSAGE_49,
        reply_markup=ReplyKeyboardMarkup(
            REPLY_KEYBOARD,
            one_time_keyboard=True,
            resize_keyboard=True,
            input_field_placeholder=INPUT_PLACEHOLDER
        ),
    )
    return QUESTION_50

async def question_50(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """50 вопрос."""
    logger.info(
        ANSWER, update.message.from_user.username, 49, update.message.text
    )
    await update.message.reply_text(
        MESSAGE_50,
        reply_markup=ReplyKeyboardMarkup(
            REPLY_KEYBOARD,
            one_time_keyboard=True,
            resize_keyboard=True,
            input_field_placeholder=INPUT_PLACEHOLDER
        ),
    )
    return QUESTION_51

async def question_51(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """51 вопрос."""
    logger.info(
        ANSWER, update.message.from_user.username, 50, update.message.text
    )
    await update.message.reply_text(
        MESSAGE_51,
        reply_markup=ReplyKeyboardMarkup(
            REPLY_KEYBOARD,
            one_time_keyboard=True,
            resize_keyboard=True,
            input_field_placeholder=INPUT_PLACEHOLDER
        ),
    )
    return QUESTION_52

async def question_52(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """52 вопрос."""
    logger.info(
        ANSWER, update.message.from_user.username, 51, update.message.text
    )
    await update.message.reply_text(
        MESSAGE_52,
        reply_markup=ReplyKeyboardMarkup(
            REPLY_KEYBOARD,
            one_time_keyboard=True,
            resize_keyboard=True,
            input_field_placeholder=INPUT_PLACEHOLDER
        ),
    )
    return QUESTION_53

async def question_53(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """53 вопрос."""
    logger.info(
        ANSWER, update.message.from_user.username, 52, update.message.text
    )
    await update.message.reply_text(
        MESSAGE_53,
        reply_markup=ReplyKeyboardMarkup(
            REPLY_KEYBOARD,
            one_time_keyboard=True,
            resize_keyboard=True,
            input_field_placeholder=INPUT_PLACEHOLDER
        ),
    )
    return QUESTION_54

async def question_54(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """54 вопрос."""
    logger.info(
        ANSWER, update.message.from_user.username, 53, update.message.text
    )
    await update.message.reply_text(
        MESSAGE_54,
        reply_markup=ReplyKeyboardMarkup(
            REPLY_KEYBOARD,
            one_time_keyboard=True,
            resize_keyboard=True,
            input_field_placeholder=INPUT_PLACEHOLDER
        ),
    )
    return QUESTION_55

async def question_55(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """55 вопрос."""
    logger.info(
        ANSWER, update.message.from_user.username, 54, update.message.text
    )
    await update.message.reply_text(
        MESSAGE_55,
        reply_markup=ReplyKeyboardMarkup(
            REPLY_KEYBOARD,
            one_time_keyboard=True,
            resize_keyboard=True,
            input_field_placeholder=INPUT_PLACEHOLDER
        ),
    )
    return QUESTION_56

async def question_56(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """56 вопрос."""
    logger.info(
        ANSWER, update.message.from_user.username, 55, update.message.text
    )
    await update.message.reply_text(
        MESSAGE_56,
        reply_markup=ReplyKeyboardMarkup(
            REPLY_KEYBOARD,
            one_time_keyboard=True,
            resize_keyboard=True,
            input_field_placeholder=INPUT_PLACEHOLDER
        ),
    )
    return QUESTION_57

async def question_57(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """57 вопрос."""
    logger.info(
        ANSWER, update.message.from_user.username, 56, update.message.text
    )
    await update.message.reply_text(
        MESSAGE_57,
        reply_markup=ReplyKeyboardMarkup(
            REPLY_KEYBOARD,
            one_time_keyboard=True,
            resize_keyboard=True,
            input_field_placeholder=INPUT_PLACEHOLDER
        ),
    )
    return QUESTION_58

async def question_58(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """58 вопрос."""
    logger.info(
        ANSWER, update.message.from_user.username, 57, update.message.text
    )
    await update.message.reply_text(
        MESSAGE_58,
        reply_markup=ReplyKeyboardMarkup(
            REPLY_KEYBOARD,
            one_time_keyboard=True,
            resize_keyboard=True,
            input_field_placeholder=INPUT_PLACEHOLDER
        ),
    )
    return QUESTION_59

async def question_59(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """59 вопрос."""
    logger.info(
        ANSWER, update.message.from_user.username, 58, update.message.text
    )
    await update.message.reply_text(
        MESSAGE_59,
        reply_markup=ReplyKeyboardMarkup(
            REPLY_KEYBOARD,
            one_time_keyboard=True,
            resize_keyboard=True,
            input_field_placeholder=INPUT_PLACEHOLDER
        ),
    )
    return QUESTION_60

async def question_60(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """60 вопрос."""
    logger.info(
        ANSWER, update.message.from_user.username, 59, update.message.text
    )
    await update.message.reply_text(
        MESSAGE_60,
        reply_markup=ReplyKeyboardMarkup(
            REPLY_KEYBOARD,
            one_time_keyboard=True,
            resize_keyboard=True,
            input_field_placeholder=INPUT_PLACEHOLDER
        ),
    )
    return QUESTION_61

async def question_61(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """61 вопрос."""
    logger.info(
        ANSWER, update.message.from_user.username, 60, update.message.text
    )
    await update.message.reply_text(
        MESSAGE_61,
        reply_markup=ReplyKeyboardMarkup(
            REPLY_KEYBOARD,
            one_time_keyboard=True,
            resize_keyboard=True,
            input_field_placeholder=INPUT_PLACEHOLDER
        ),
    )
    return QUESTION_62

async def question_62(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """62 вопрос."""
    logger.info(
        ANSWER, update.message.from_user.username, 61, update.message.text
    )
    await update.message.reply_text(
        MESSAGE_62,
        reply_markup=ReplyKeyboardMarkup(
            REPLY_KEYBOARD,
            one_time_keyboard=True,
            resize_keyboard=True,
            input_field_placeholder=INPUT_PLACEHOLDER
        ),
    )
    return QUESTION_63

async def question_63(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """63 вопрос."""
    logger.info(
        ANSWER, update.message.from_user.username, 62, update.message.text
    )
    await update.message.reply_text(
        MESSAGE_63,
        reply_markup=ReplyKeyboardMarkup(
            REPLY_KEYBOARD,
            one_time_keyboard=True,
            resize_keyboard=True,
            input_field_placeholder=INPUT_PLACEHOLDER
        ),
    )
    return QUESTION_64

async def question_64(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """64 вопрос."""
    logger.info(
        ANSWER, update.message.from_user.username, 63, update.message.text
    )
    await update.message.reply_text(
        MESSAGE_64,
        reply_markup=ReplyKeyboardMarkup(
            REPLY_KEYBOARD,
            one_time_keyboard=True,
            resize_keyboard=True,
            input_field_placeholder=INPUT_PLACEHOLDER
        ),
    )
    return QUESTION_65

async def question_65(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """65 вопрос."""
    logger.info(
        ANSWER, update.message.from_user.username, 64, update.message.text
    )
    await update.message.reply_text(
        MESSAGE_65,
        reply_markup=ReplyKeyboardMarkup(
            REPLY_KEYBOARD,
            one_time_keyboard=True,
            resize_keyboard=True,
            input_field_placeholder=INPUT_PLACEHOLDER
        ),
    )
    return QUESTION_66

async def question_66(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """66 вопрос."""
    logger.info(
        ANSWER, update.message.from_user.username, 65, update.message.text
    )
    await update.message.reply_text(
        MESSAGE_66,
        reply_markup=ReplyKeyboardMarkup(
            REPLY_KEYBOARD,
            one_time_keyboard=True,
            resize_keyboard=True,
            input_field_placeholder=INPUT_PLACEHOLDER
        ),
    )
    return QUESTION_67

async def question_67(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """67 вопрос."""
    logger.info(
        ANSWER, update.message.from_user.username, 66, update.message.text
    )
    await update.message.reply_text(
        MESSAGE_67,
        reply_markup=ReplyKeyboardMarkup(
            REPLY_KEYBOARD,
            one_time_keyboard=True,
            resize_keyboard=True,
            input_field_placeholder=INPUT_PLACEHOLDER
        ),
    )
    return QUESTION_68

async def question_68(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """68 вопрос."""
    logger.info(
        ANSWER, update.message.from_user.username, 67, update.message.text
    )
    await update.message.reply_text(
        MESSAGE_68,
        reply_markup=ReplyKeyboardMarkup(
            REPLY_KEYBOARD,
            one_time_keyboard=True,
            resize_keyboard=True,
            input_field_placeholder=INPUT_PLACEHOLDER
        ),
    )
    return QUESTION_69

async def question_69(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """69 вопрос."""
    logger.info(
        ANSWER, update.message.from_user.username, 68, update.message.text
    )
    await update.message.reply_text(
        MESSAGE_69,
        reply_markup=ReplyKeyboardMarkup(
            REPLY_KEYBOARD,
            one_time_keyboard=True,
            resize_keyboard=True,
            input_field_placeholder=INPUT_PLACEHOLDER
        ),
    )
    return QUESTION_70

async def question_70(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """70 вопрос."""
    logger.info(
        ANSWER, update.message.from_user.username, 69, update.message.text
    )
    await update.message.reply_text(
        MESSAGE_70,
        reply_markup=ReplyKeyboardMarkup(
            REPLY_KEYBOARD,
            one_time_keyboard=True,
            resize_keyboard=True,
            input_field_placeholder=INPUT_PLACEHOLDER
        ),
    )
    return QUESTION_71

async def question_71(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """71 вопрос."""
    logger.info(
        ANSWER, update.message.from_user.username, 70, update.message.text
    )
    await update.message.reply_text(
        MESSAGE_71,
        reply_markup=ReplyKeyboardMarkup(
            REPLY_KEYBOARD,
            one_time_keyboard=True,
            resize_keyboard=True,
            input_field_placeholder=INPUT_PLACEHOLDER
        ),
    )
    return QUESTION_72

async def question_72(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """72 вопрос."""
    logger.info(
        ANSWER, update.message.from_user.username, 71, update.message.text
    )
    await update.message.reply_text(
        MESSAGE_72,
        reply_markup=ReplyKeyboardMarkup(
            REPLY_KEYBOARD,
            one_time_keyboard=True,
            resize_keyboard=True,
            input_field_placeholder=INPUT_PLACEHOLDER
        ),
    )
    return QUESTION_73

async def question_73(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """73 вопрос."""
    logger.info(
        ANSWER, update.message.from_user.username, 72, update.message.text
    )
    await update.message.reply_text(
        MESSAGE_73,
        reply_markup=ReplyKeyboardMarkup(
            REPLY_KEYBOARD,
            one_time_keyboard=True,
            resize_keyboard=True,
            input_field_placeholder=INPUT_PLACEHOLDER
        ),
    )
    return QUESTION_74

async def question_74(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """74 вопрос."""
    logger.info(
        ANSWER, update.message.from_user.username, 73, update.message.text
    )
    await update.message.reply_text(
        MESSAGE_74,
        reply_markup=ReplyKeyboardMarkup(
            REPLY_KEYBOARD,
            one_time_keyboard=True,
            resize_keyboard=True,
            input_field_placeholder=INPUT_PLACEHOLDER
        ),
    )
    return QUESTION_75

async def question_75(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """75 вопрос."""
    logger.info(
        ANSWER, update.message.from_user.username, 74, update.message.text
    )
    await update.message.reply_text(
        MESSAGE_75,
        reply_markup=ReplyKeyboardMarkup(
            REPLY_KEYBOARD,
            one_time_keyboard=True,
            resize_keyboard=True,
            input_field_placeholder=INPUT_PLACEHOLDER
        ),
    )
    return QUESTION_76

async def question_76(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """76 вопрос."""
    logger.info(
        ANSWER, update.message.from_user.username, 75, update.message.text
    )
    await update.message.reply_text(
        MESSAGE_76,
        reply_markup=ReplyKeyboardMarkup(
            REPLY_KEYBOARD,
            one_time_keyboard=True,
            resize_keyboard=True,
            input_field_placeholder=INPUT_PLACEHOLDER
        ),
    )
    return QUESTION_77

async def question_77(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """77 вопрос."""
    logger.info(
        ANSWER, update.message.from_user.username, 76, update.message.text
    )
    await update.message.reply_text(
        MESSAGE_77,
        reply_markup=ReplyKeyboardMarkup(
            REPLY_KEYBOARD,
            one_time_keyboard=True,
            resize_keyboard=True,
            input_field_placeholder=INPUT_PLACEHOLDER
        ),
    )
    return QUESTION_78

async def question_78(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """78 вопрос."""
    logger.info(
        ANSWER, update.message.from_user.username, 77, update.message.text
    )
    await update.message.reply_text(
        MESSAGE_78,
        reply_markup=ReplyKeyboardMarkup(
            REPLY_KEYBOARD,
            one_time_keyboard=True,
            resize_keyboard=True,
            input_field_placeholder=INPUT_PLACEHOLDER
        ),
    )
    return QUESTION_79

async def question_79(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """79 вопрос."""
    logger.info(
        ANSWER, update.message.from_user.username, 78, update.message.text
    )
    await update.message.reply_text(
        MESSAGE_79,
        reply_markup=ReplyKeyboardMarkup(
            REPLY_KEYBOARD,
            one_time_keyboard=True,
            resize_keyboard=True,
            input_field_placeholder=INPUT_PLACEHOLDER
        ),
    )
    return QUESTION_80

async def question_80(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """80 вопрос."""
    logger.info(
        ANSWER, update.message.from_user.username, 79, update.message.text
    )
    await update.message.reply_text(
        MESSAGE_80,
        reply_markup=ReplyKeyboardMarkup(
            REPLY_KEYBOARD,
            one_time_keyboard=True,
            resize_keyboard=True,
            input_field_placeholder=INPUT_PLACEHOLDER
        ),
    )
    return QUESTION_81

async def question_81(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """81 вопрос."""
    logger.info(
        ANSWER, update.message.from_user.username, 80, update.message.text
    )
    await update.message.reply_text(
        MESSAGE_81,
        reply_markup=ReplyKeyboardMarkup(
            REPLY_KEYBOARD,
            one_time_keyboard=True,
            resize_keyboard=True,
            input_field_placeholder=INPUT_PLACEHOLDER
        ),
    )
    return QUESTION_82

async def question_82(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """82 вопрос."""
    logger.info(
        ANSWER, update.message.from_user.username, 81, update.message.text
    )
    await update.message.reply_text(
        MESSAGE_82,
        reply_markup=ReplyKeyboardMarkup(
            REPLY_KEYBOARD,
            one_time_keyboard=True,
            resize_keyboard=True,
            input_field_placeholder=INPUT_PLACEHOLDER
        ),
    )
    return QUESTION_83

async def question_83(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """83 вопрос."""
    logger.info(
        ANSWER, update.message.from_user.username, 82, update.message.text
    )
    await update.message.reply_text(
        MESSAGE_83,
        reply_markup=ReplyKeyboardMarkup(
            REPLY_KEYBOARD,
            one_time_keyboard=True,
            resize_keyboard=True,
            input_field_placeholder=INPUT_PLACEHOLDER
        ),
    )
    return QUESTION_84

async def question_84(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """84 вопрос."""
    logger.info(
        ANSWER, update.message.from_user.username, 83, update.message.text
    )
    await update.message.reply_text(
        MESSAGE_84,
        reply_markup=ReplyKeyboardMarkup(
            REPLY_KEYBOARD,
            one_time_keyboard=True,
            resize_keyboard=True,
            input_field_placeholder=INPUT_PLACEHOLDER
        ),
    )
    return QUESTION_85

async def question_85(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """85 вопрос."""
    logger.info(
        ANSWER, update.message.from_user.username, 84, update.message.text
    )
    await update.message.reply_text(
        MESSAGE_85,
        reply_markup=ReplyKeyboardMarkup(
            REPLY_KEYBOARD,
            one_time_keyboard=True,
            resize_keyboard=True,
            input_field_placeholder=INPUT_PLACEHOLDER
        ),
    )
    return QUESTION_86

async def question_86(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """86 вопрос."""
    logger.info(
        ANSWER, update.message.from_user.username, 85, update.message.text
    )
    await update.message.reply_text(
        MESSAGE_86,
        reply_markup=ReplyKeyboardMarkup(
            REPLY_KEYBOARD,
            one_time_keyboard=True,
            resize_keyboard=True,
            input_field_placeholder=INPUT_PLACEHOLDER
        ),
    )
    return QUESTION_87

async def question_87(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """87 вопрос."""
    logger.info(
        ANSWER, update.message.from_user.username, 86, update.message.text
    )
    await update.message.reply_text(
        MESSAGE_87,
        reply_markup=ReplyKeyboardMarkup(
            REPLY_KEYBOARD,
            one_time_keyboard=True,
            resize_keyboard=True,
            input_field_placeholder=INPUT_PLACEHOLDER
        ),
    )
    return DESCRIPTION

async def description(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Расшифровка."""
    logger.info(
        ANSWER, update.message.from_user.username, 87, update.message.text
    )
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=DESCRIPTION_MESSAGE
    )
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Конец диалога."""
    logger.info(CANSEL, update.message.from_user.first_name)
    # context.user_data.clear()
    await update.message.reply_text(
        STOP,
        reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END
