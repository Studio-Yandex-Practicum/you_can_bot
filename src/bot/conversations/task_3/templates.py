DELIMITER_TEXT_FROM_URL = "DELIMITER"
RESULT_MESSAGE = "Твой тип личности: \n\n"
TASK_3_CANCELLATION_TEXT = (
    "Прохождение задания прервано. Если хочешь начать его сначала,"
    ' то ты можешь открыть меню, перейти в "Мои задания" и выбрать Задание 3.'
)
TEXT_OF_START_TASK_3 = (
    "Сейчас тебе будут представлены 42 пары различных видов деятельности. "
    "Если бы тебе пришлось выбирать лишь одну работу из каждой пары, "
    "что бы ты предпочёл?\n\n"
)
QUESTIONS = [
    (
        "\n"
        "а) инженер-конструктор\n"
        "б) инженер-технолог"
        f"{DELIMITER_TEXT_FROM_URL}"
        "https://www.rtl-sdr.com/wp-content/uploads/2023/08/V4_promo-1024x807.jpg"
        f"{DELIMITER_TEXT_FROM_URL}"
        "https://www.rtl-sdr.com/wp-content/uploads/2023/08/V4_promo-1024x807.jpg"
    ),
    (
        "\n"
        "а) терапевт\n"
        "б) радиотехник"
        f"{DELIMITER_TEXT_FROM_URL}"
        "https://www.rtl-sdr.com/wp-content/uploads/2023/08/V4_promo-1024x807.jpg"
        f"{DELIMITER_TEXT_FROM_URL}"
        "https://www.rtl-sdr.com/wp-content/uploads/2023/08/V4_promo-1024x807.jpg"
    ),
    (
        "\n"
        "а) кодировщик информации\n"
        "б) оператор станков с программным управлением"
        f"{DELIMITER_TEXT_FROM_URL}"
        "https://www.rtl-sdr.com/wp-content/uploads/2023/08/V4_promo-1024x807.jpg"
        f"{DELIMITER_TEXT_FROM_URL}"
        "https://www.rtl-sdr.com/wp-content/uploads/2023/08/V4_promo-1024x807.jpg"
    ),
    (
        "\n"
        "а) бизнесмен\n"
        "б) фотограф"
        f"{DELIMITER_TEXT_FROM_URL}"
        "https://www.rtl-sdr.com/wp-content/uploads/2023/08/V4_promo-1024x807.jpg"
        f"{DELIMITER_TEXT_FROM_URL}"
        "https://www.rtl-sdr.com/wp-content/uploads/2023/08/V4_promo-1024x807.jpg"
    ),
    (
        "\n"
        "а) дизайнер\n"
        "б) спасатель МЧС"
        f"{DELIMITER_TEXT_FROM_URL}"
        "https://www.rtl-sdr.com/wp-content/uploads/2023/08/V4_promo-1024x807.jpg"
        f"{DELIMITER_TEXT_FROM_URL}"
        "https://www.rtl-sdr.com/wp-content/uploads/2023/08/V4_promo-1024x807.jpg"
    ),
    (
        "\n"
        "а) психиатр\n"
        "б) политолог"
        f"{DELIMITER_TEXT_FROM_URL}"
        "https://www.rtl-sdr.com/wp-content/uploads/2023/08/V4_promo-1024x807.jpg"
        f"{DELIMITER_TEXT_FROM_URL}"
        "https://www.rtl-sdr.com/wp-content/uploads/2023/08/V4_promo-1024x807.jpg"
    ),
    (
        "\n"
        "а) бухгалтер\n"
        "б) ученый-химик"
        f"{DELIMITER_TEXT_FROM_URL}"
        "https://www.rtl-sdr.com/wp-content/uploads/2023/08/V4_promo-1024x807.jpg"
        f"{DELIMITER_TEXT_FROM_URL}"
        "https://www.rtl-sdr.com/wp-content/uploads/2023/08/V4_promo-1024x807.jpg"
    ),
    (
        "\n"
        "а) частный предприниматель\n"
        "б) философ"
        f"{DELIMITER_TEXT_FROM_URL}"
        "https://www.rtl-sdr.com/wp-content/uploads/2023/08/V4_promo-1024x807.jpg"
        f"{DELIMITER_TEXT_FROM_URL}"
        "https://www.rtl-sdr.com/wp-content/uploads/2023/08/V4_promo-1024x807.jpg"
    ),
    (
        "\n"
        "а) модельер\n"
        "б) лингвист"
        f"{DELIMITER_TEXT_FROM_URL}"
        "https://www.rtl-sdr.com/wp-content/uploads/2023/08/V4_promo-1024x807.jpg"
        f"{DELIMITER_TEXT_FROM_URL}"
        "https://www.rtl-sdr.com/wp-content/uploads/2023/08/V4_promo-1024x807.jpg"
    ),
    (
        "\n"
        "а) статист\n"
        "б) инспектор службы занятости населения"
        f"{DELIMITER_TEXT_FROM_URL}"
        "https://www.rtl-sdr.com/wp-content/uploads/2023/08/V4_promo-1024x807.jpg"
        f"{DELIMITER_TEXT_FROM_URL}"
        "https://www.rtl-sdr.com/wp-content/uploads/2023/08/V4_promo-1024x807.jpg"
    ),
    (
        "\n"
        "а) брокер\n"
        "б) социальный педагог"
        f"{DELIMITER_TEXT_FROM_URL}"
        "https://www.rtl-sdr.com/wp-content/uploads/2023/08/V4_promo-1024x807.jpg"
        f"{DELIMITER_TEXT_FROM_URL}"
        "https://www.rtl-sdr.com/wp-content/uploads/2023/08/V4_promo-1024x807.jpg"
    ),
    (
        "\n"
        "а) искусствовед\n"
        "б) тренер"
        f"{DELIMITER_TEXT_FROM_URL}"
        "https://www.rtl-sdr.com/wp-content/uploads/2023/08/V4_promo-1024x807.jpg"
        f"{DELIMITER_TEXT_FROM_URL}"
        "https://www.rtl-sdr.com/wp-content/uploads/2023/08/V4_promo-1024x807.jpg"
    ),
    (
        "\n"
        "а) менеджер\n"
        "б) нотариус"
        f"{DELIMITER_TEXT_FROM_URL}"
        "https://www.rtl-sdr.com/wp-content/uploads/2023/08/V4_promo-1024x807.jpg"
        f"{DELIMITER_TEXT_FROM_URL}"
        "https://www.rtl-sdr.com/wp-content/uploads/2023/08/V4_promo-1024x807.jpg"
    ),
    (
        "\n"
        "а) художник\n"
        "б) печатник"
        f"{DELIMITER_TEXT_FROM_URL}"
        "https://www.rtl-sdr.com/wp-content/uploads/2023/08/V4_promo-1024x807.jpg"
        f"{DELIMITER_TEXT_FROM_URL}"
        "https://www.rtl-sdr.com/wp-content/uploads/2023/08/V4_promo-1024x807.jpg"
    ),
    (
        "\n"
        "а) писатель\n"
        "б) лидер общественного движения"
        f"{DELIMITER_TEXT_FROM_URL}"
        "https://www.rtl-sdr.com/wp-content/uploads/2023/08/V4_promo-1024x807.jpg"
        f"{DELIMITER_TEXT_FROM_URL}"
        "https://www.rtl-sdr.com/wp-content/uploads/2023/08/V4_promo-1024x807.jpg"
    ),
    (
        "\n"
        "а) метеоролог\n"
        "б) модельер"
        f"{DELIMITER_TEXT_FROM_URL}"
        "https://www.rtl-sdr.com/wp-content/uploads/2023/08/V4_promo-1024x807.jpg"
        f"{DELIMITER_TEXT_FROM_URL}"
        "https://www.rtl-sdr.com/wp-content/uploads/2023/08/V4_promo-1024x807.jpg"
    ),
    (
        "\n"
        "а) работник пресс-службы\n"
        "б) водитель"
        f"{DELIMITER_TEXT_FROM_URL}"
        "https://www.rtl-sdr.com/wp-content/uploads/2023/08/V4_promo-1024x807.jpg"
        f"{DELIMITER_TEXT_FROM_URL}"
        "https://www.rtl-sdr.com/wp-content/uploads/2023/08/V4_promo-1024x807.jpg"
    ),
    (
        "\n"
        "а) чертежник\n"
        "б) риелтор"
        f"{DELIMITER_TEXT_FROM_URL}"
        "https://www.rtl-sdr.com/wp-content/uploads/2023/08/V4_promo-1024x807.jpg"
        f"{DELIMITER_TEXT_FROM_URL}"
        "https://www.rtl-sdr.com/wp-content/uploads/2023/08/V4_promo-1024x807.jpg"
    ),
    (
        "\n"
        "а) специалист по ремонту компьютеров и оргтехники\n"
        "б) секретарь-референт"
        f"{DELIMITER_TEXT_FROM_URL}"
        "https://www.rtl-sdr.com/wp-content/uploads/2023/08/V4_promo-1024x807.jpg"
        f"{DELIMITER_TEXT_FROM_URL}"
        "https://www.rtl-sdr.com/wp-content/uploads/2023/08/V4_promo-1024x807.jpg"
    ),
    (
        "\n"
        "а) микробиолог\n"
        "б) психолог"
        f"{DELIMITER_TEXT_FROM_URL}"
        "https://www.rtl-sdr.com/wp-content/uploads/2023/08/V4_promo-1024x807.jpg"
        f"{DELIMITER_TEXT_FROM_URL}"
        "https://www.rtl-sdr.com/wp-content/uploads/2023/08/V4_promo-1024x807.jpg"
    ),
    (
        "\n"
        "а) видеооператор\n"
        "б) режиссер"
        f"{DELIMITER_TEXT_FROM_URL}"
        "https://www.rtl-sdr.com/wp-content/uploads/2023/08/V4_promo-1024x807.jpg"
        f"{DELIMITER_TEXT_FROM_URL}"
        "https://www.rtl-sdr.com/wp-content/uploads/2023/08/V4_promo-1024x807.jpg"
    ),
    (
        "\n"
        "а) экономист\n"
        "б) провизор"
        f"{DELIMITER_TEXT_FROM_URL}"
        "https://www.rtl-sdr.com/wp-content/uploads/2023/08/V4_promo-1024x807.jpg"
        f"{DELIMITER_TEXT_FROM_URL}"
        "https://www.rtl-sdr.com/wp-content/uploads/2023/08/V4_promo-1024x807.jpg"
    ),
    (
        "\n"
        "а) зоолог\n"
        "б) главный инженер"
        f"{DELIMITER_TEXT_FROM_URL}"
        "https://www.rtl-sdr.com/wp-content/uploads/2023/08/V4_promo-1024x807.jpg"
        f"{DELIMITER_TEXT_FROM_URL}"
        "https://www.rtl-sdr.com/wp-content/uploads/2023/08/V4_promo-1024x807.jpg"
    ),
    (
        "\n"
        "а) программист\n"
        "б) архитектор"
        f"{DELIMITER_TEXT_FROM_URL}"
        "https://www.rtl-sdr.com/wp-content/uploads/2023/08/V4_promo-1024x807.jpg"
        f"{DELIMITER_TEXT_FROM_URL}"
        "https://www.rtl-sdr.com/wp-content/uploads/2023/08/V4_promo-1024x807.jpg"
    ),
    (
        "\n"
        "а) работник инспекции по делам несовершеннолетних\n"
        "б) маркетолог"
        f"{DELIMITER_TEXT_FROM_URL}"
        "https://www.rtl-sdr.com/wp-content/uploads/2023/08/V4_promo-1024x807.jpg"
        f"{DELIMITER_TEXT_FROM_URL}"
        "https://www.rtl-sdr.com/wp-content/uploads/2023/08/V4_promo-1024x807.jpg"
    ),
    (
        "\n"
        "а) преподаватель\n"
        "б) трейдер"
        f"{DELIMITER_TEXT_FROM_URL}"
        "https://www.rtl-sdr.com/wp-content/uploads/2023/08/V4_promo-1024x807.jpg"
        f"{DELIMITER_TEXT_FROM_URL}"
        "https://www.rtl-sdr.com/wp-content/uploads/2023/08/V4_promo-1024x807.jpg"
    ),
    (
        "\n"
        "а) воспитатель\n"
        "б) декоратор"
        f"{DELIMITER_TEXT_FROM_URL}"
        "https://www.rtl-sdr.com/wp-content/uploads/2023/08/V4_promo-1024x807.jpg"
        f"{DELIMITER_TEXT_FROM_URL}"
        "https://www.rtl-sdr.com/wp-content/uploads/2023/08/V4_promo-1024x807.jpg"
    ),
    (
        "\n"
        "а) реставратор\n"
        "б) заведующий отделом предприятия"
        f"{DELIMITER_TEXT_FROM_URL}"
        "https://www.rtl-sdr.com/wp-content/uploads/2023/08/V4_promo-1024x807.jpg"
        f"{DELIMITER_TEXT_FROM_URL}"
        "https://www.rtl-sdr.com/wp-content/uploads/2023/08/V4_promo-1024x807.jpg"
    ),
    (
        "\n"
        "а) корректор\n"
        "б) литератор и кинокритик"
        f"{DELIMITER_TEXT_FROM_URL}"
        "https://www.rtl-sdr.com/wp-content/uploads/2023/08/V4_promo-1024x807.jpg"
        f"{DELIMITER_TEXT_FROM_URL}"
        "https://www.rtl-sdr.com/wp-content/uploads/2023/08/V4_promo-1024x807.jpg"
    ),
    (
        "\n"
        "а) фермер\n"
        "б) визажист"
        f"{DELIMITER_TEXT_FROM_URL}"
        "https://www.rtl-sdr.com/wp-content/uploads/2023/08/V4_promo-1024x807.jpg"
        f"{DELIMITER_TEXT_FROM_URL}"
        "https://www.rtl-sdr.com/wp-content/uploads/2023/08/V4_promo-1024x807.jpg"
    ),
    (
        "\n"
        "а) парикмахер\n"
        "б) социолог"
        f"{DELIMITER_TEXT_FROM_URL}"
        "https://www.rtl-sdr.com/wp-content/uploads/2023/08/V4_promo-1024x807.jpg"
        f"{DELIMITER_TEXT_FROM_URL}"
        "https://www.rtl-sdr.com/wp-content/uploads/2023/08/V4_promo-1024x807.jpg"
    ),
    (
        "\n"
        "а) экспедитор\n"
        "б) редактор"
        f"{DELIMITER_TEXT_FROM_URL}"
        "https://www.rtl-sdr.com/wp-content/uploads/2023/08/V4_promo-1024x807.jpg"
        f"{DELIMITER_TEXT_FROM_URL}"
        "https://www.rtl-sdr.com/wp-content/uploads/2023/08/V4_promo-1024x807.jpg"
    ),
    (
        "\n"
        "а) ветеринар\n"
        "б) финансовый директор"
        f"{DELIMITER_TEXT_FROM_URL}"
        "https://www.rtl-sdr.com/wp-content/uploads/2023/08/V4_promo-1024x807.jpg"
        f"{DELIMITER_TEXT_FROM_URL}"
        "https://www.rtl-sdr.com/wp-content/uploads/2023/08/V4_promo-1024x807.jpg"
    ),
    (
        "\n"
        "а) автомеханик\n"
        "б) стилист"
        f"{DELIMITER_TEXT_FROM_URL}"
        "https://www.rtl-sdr.com/wp-content/uploads/2023/08/V4_promo-1024x807.jpg"
        f"{DELIMITER_TEXT_FROM_URL}"
        "https://www.rtl-sdr.com/wp-content/uploads/2023/08/V4_promo-1024x807.jpg"
    ),
    (
        "\n"
        "а) археолог\n"
        "б) эксперт"
        f"{DELIMITER_TEXT_FROM_URL}"
        "https://www.rtl-sdr.com/wp-content/uploads/2023/08/V4_promo-1024x807.jpg"
        f"{DELIMITER_TEXT_FROM_URL}"
        "https://www.rtl-sdr.com/wp-content/uploads/2023/08/V4_promo-1024x807.jpg"
    ),
    (
        "\n"
        "а) библиограф\n"
        "б) корреспондент"
        f"{DELIMITER_TEXT_FROM_URL}"
        "https://www.rtl-sdr.com/wp-content/uploads/2023/08/V4_promo-1024x807.jpg"
        f"{DELIMITER_TEXT_FROM_URL}"
        "https://www.rtl-sdr.com/wp-content/uploads/2023/08/V4_promo-1024x807.jpg"
    ),
    (
        "\n"
        "а) эколог\n"
        "б) актер"
        f"{DELIMITER_TEXT_FROM_URL}"
        "https://www.rtl-sdr.com/wp-content/uploads/2023/08/V4_promo-1024x807.jpg"
        f"{DELIMITER_TEXT_FROM_URL}"
        "https://www.rtl-sdr.com/wp-content/uploads/2023/08/V4_promo-1024x807.jpg"
    ),
    (
        "\n"
        "а) логопед\n"
        "б) контролер"
        f"{DELIMITER_TEXT_FROM_URL}"
        "https://www.rtl-sdr.com/wp-content/uploads/2023/08/V4_promo-1024x807.jpg"
        f"{DELIMITER_TEXT_FROM_URL}"
        "https://www.rtl-sdr.com/wp-content/uploads/2023/08/V4_promo-1024x807.jpg"
    ),
    (
        "\n"
        "а) адвокат\n"
        "б) директор организации"
        f"{DELIMITER_TEXT_FROM_URL}"
        "https://www.rtl-sdr.com/wp-content/uploads/2023/08/V4_promo-1024x807.jpg"
        f"{DELIMITER_TEXT_FROM_URL}"
        "https://www.rtl-sdr.com/wp-content/uploads/2023/08/V4_promo-1024x807.jpg"
    ),
    (
        "\n"
        "а) кассир\n"
        "б) продюсер"
        f"{DELIMITER_TEXT_FROM_URL}"
        "https://www.rtl-sdr.com/wp-content/uploads/2023/08/V4_promo-1024x807.jpg"
        f"{DELIMITER_TEXT_FROM_URL}"
        "https://www.rtl-sdr.com/wp-content/uploads/2023/08/V4_promo-1024x807.jpg"
    ),
    (
        "\n"
        "а) поэт, писатель\n"
        "б) продавец"
        f"{DELIMITER_TEXT_FROM_URL}"
        "https://www.rtl-sdr.com/wp-content/uploads/2023/08/V4_promo-1024x807.jpg"
        f"{DELIMITER_TEXT_FROM_URL}"
        "https://www.rtl-sdr.com/wp-content/uploads/2023/08/V4_promo-1024x807.jpg"
    ),
    (
        "\n"
        "а) криминалист\n"
        "б) композитор"
        f"{DELIMITER_TEXT_FROM_URL}"
        "https://www.rtl-sdr.com/wp-content/uploads/2023/08/V4_promo-1024x807.jpg"
        f"{DELIMITER_TEXT_FROM_URL}"
        "https://www.rtl-sdr.com/wp-content/uploads/2023/08/V4_promo-1024x807.jpg"
    ),
]
