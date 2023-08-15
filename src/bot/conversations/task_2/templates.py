from keyboards import MAGIC_WORD_FOR_START_THIS_HANDLER


DESCRIPTION_MESSAGE = (
    'Расшифровка: \n\n'
)
STOP = (
    'Диалог прерван. Если хотите начать его сначала, '
    f'то введите /{MAGIC_WORD_FOR_START_THIS_HANDLER}'
)
START = (
    'Ниже 70 вопросов, в каждом из них – два утверждения. Выбери то '
    'продолжение, которое свойственно тебе больше всего. Важно: подолгу не '
    'задумывайся над ответами!\n\n'
)
MESSAGES = [
    (
        'В компании (на вечеринке) ты:\n\n'
        'а) общаешься со многими, включая и незнакомцев\n'
        'б) общаешься с немногими – твоими знакомыми'
    ),
    (
        'Ты человек скорее:\n\n'
        'а) реалистичный, чем склонный теоретизировать\n'
        'б) склонный теоретизировать, чем реалистичный'
    ),
    (
        'По-твоему, что хуже:\n\n'
        'а) «витать в облаках»\n'
        'б) придерживаться проторенной дорожки'
    ),
    (
        'Ты более подвержен влиянию:\n\n'
        'а) принципов, законов\n'
        'б) эмоций, чувств'
    ),
    (
        'Ты более склонен:\n\n'
        'а) убеждать\n'
        'б) затрагивать чувства'
    ),
    (
        'Ты предпочитаешь работать:\n\n'
        'а) выполняя все точно в срок\n'
        '6) не связывая себя определенными сроками'
    ),
    (
        'Ты склонен делать выбор:\n\n'
        'а) довольно осторожно\n'
        '6) внезапно импульсивно'
    ),
    (
        'В компании (на вечеринке) ты:\n\n'
        'a) остаешься допоздна, не чувствуя усталости\n'
        'б) быстро утомляешься и предпочитаешь пораньше уйти'
    ),
    (
        'Тебя бoлee привлекают:\n\n'
        'а) здравомыслящие люди\n'
        'б) люди с богатым воображением'
    ),
    (
        'Тебе интереснее:\n\n'
        'а) то, что происходит в действительности\n'
        'б) те события, которые могут произойти'
    ),
    (
        'Оценивая поступки людей, ты больше учитываешь:\n\n'
        'а) требования закона, чем обстоятельства\n'
        'б) обстоятельства, чем требования закона'
    ),
    (
        'Обращаясь к другим, ты склонен:\n\n'
        'а) соблюдать формальности, этикет\n'
        'б) проявлять свои личные, индивидуальные качества'
    ),
    (
        'Ты человек скорее:\n\n'
        'а) точный, пунктуальный\n'
        'б) неторопливый, медленный'
    ),
    (
        'Тебя больше беспокоит необходимость:\n\n'
        'а) оставлять дела незаконченными\n'
        'б) непременно доводить дело до конца'
    ),
    (
        'В кругу знакомых ты, как правило:\n\n'
        'а) в куpce происходящих событий\n'
        'б) узнаешь о новостях с опозданием'
    ),
    (
        'Повседневные дела тебе нравится делать:\n\n'
        'а) общепринятым способом\n'
        'б) своим оригинальным способом'
    ),
    (
        'Предпочитаешь таких писателей, которые:\n\n'
        'а) выражаются буквально, напрямую\n'
        'б) пользуются аналогиями, иносказаниями'
    ),
    (
        'Что тебя больше привлекает:\n\n'
        'а) стройность мысли\n'
        'б) гармония человеческих отношений'
    ),
    (
        'Ты чувствуешь себя увереннее:\n\n'
        'а) в логических умозаключениях\n'
        'б) в практических оценках ситуаций'
    ),
    (
        'Ты предпочитаешь, когда дела:\n\n'
        'а) решены и устроены\n'
        'б) не решены и не устроены'
    ),
    (
        'Как по-твоему, ты человек:\n\n'
        'а) серьезный, определенный\n'
        'б) беззаботный, беспечный'
    ),
    (
        'При телефонных разговорах ты:\n\n'
        'а) заранее не продумываешь то, что надо сказать\n'
        'б) мысленно репетируешь то, что будет сказано'
    ),
    (
        'Как ты считаешь, факты:\n\n'
        'а) важны сами по себе\n'
        'б) ecть проявление общих закономерностей'
    ),
    (
        'Фантазеры, мечтатели:\n\n'
        'а) раздражают тебя\n'
        'б) довольно симпатичны тебе'
    ),
    (
        'Ты чаще действуешь как человек:\n\n'
        'а) хладнокровный\n'
        'б) вспыльчивый, горячий'
    ),
    (
        'По-твоему, хуже быть:\n\n'
        'а) несправедливым\n'
        'б) беспощадным'
    ),
    (
        'Обычно ты предпочитаешь действовать:\n\n'
        'а) тщательно оценив возможности\n'
        'б) полагаясь на волю случая'
    ),
    (
        'Тебе приятнее:\n\n'
        'а) покупать что-то\n'
        'б) иметь возможность купить'
    ),
    (
        'В компании ты как правило:\n\n'
        'а) первым заводишь беседу\n'
        'б) ждешь, когда с тобой заговорят'
    ),
    (
        'Здравый смысл:\n\n'
        'а) редко ошибается\n'
        'б) часто попадает впросак'
    ),
    (
        'Детям часто не хватает:\n\n'
        'а) практичности\n'
        'б) воображения'
    ),
    (
        'В принятии решений ты руководствуешься скорее:\n\n'
        'а) принятыми нормами\n'
        'б) своими чувствами, ощущениями'
    ),
    (
        'Ты человек скорее:\n\n'
        'а) твердый, чем мягкий\n'
        'б) мягкий, чем твердый'
    ),
    (
        'Что, по-твоему, больше впечатляет:\n\n'
        'а) умение методично организовывать\n'
        'б) умение приспособиться и довольствоваться достигнутым'
    ),
    (
        'Ты больше ценишь:\n\n'
        'а) определенность, законченность\n'
        'б) открытость, многовариантность'
    ),
    (
        'Новые и нестандартные отношении с людьми:\n\n'
        'а) стимулируют, придают тебе энергии\n'
        'б) утомляют'
    ),
    (
        'Ты чаще действуешь как:\n\n'
        'а) человек практического склада\n'
        'б) человек оригинальный, необычный'
    ),
    (
        'Ты более склонен:\n\n'
        'а) находить пользу в отношениях с людьми\n'
        'б) понимать мысли и чувства других'
    ),
    (
        'Что приносит тебе больше удовлетворения:\n\n'
        'а) тщательное всестороннее обсуждение спорного вопроса\n'
        'б) достижения соглашения по поводу спорного вопроса'
    ),
    (
        'Ты руководствуешься более:\n\n'
        'а) рассудком\n'
        'б) велениями сердца'
    ),
    (
        'Тебе удобнее выполнять работу:\n\n'
        'а) по предварительной договоренности\n'
        'б) которая подвернулась случайно'
    ),
    (
        'Ты обычно полагаешься:\n\n'
        'а) на организованность, порядок\n'
        'б) на случайность, неожиданность'
    ),
    (
        'Ты предпочитаешь иметь:\n\n'
        'а) много друзей на непродолжительный срок\n'
        'б) несколько старых друзей'
    ),
    (
        'Ты руководствуешься в большей степени:\n\n'
        'а) фактами, обстоятельствами\n'
        'б) общим положениями, принципами'
    ),
    (
        'Тебя больше интересуют:\n\n'
        'а) производство и сбыт продукции\n'
        'б) проектирование и исследования'
    ),
    (
        'Что ты скорее сочтешь за комплимент:\n\n'
        'а) «Ты очень логичный человек»\n'
        'б) «Ты тонко чувствующий человек»'
    ),
    (
        'Ты более ценишь в себе:\n\n'
        'а) невозмутимость\n'
        'б) увлеченность'
    ),
    (
        'Ты предпочитаешь высказывать:\n\n'
        'а) окончательные и определенные утверждения\n'
        'б) предварительные и неоднозначные утверждения'
    ),
    (
        'Ты лучше чувствуешь себя:\n\n'
        'а) после принятия решения\n'
        'б) не ограничивая себя решениями'
    ),
    (
        'Общаясь с незнакомыми ты:\n\n'
        'а) легко завязываешь продолжительные беседы\n'
        'б) не всегда находишь общие темы для разговора'
    ),
    (
        'Ты больше доверяешь:\n\n'
        'a) своему опыту\n'
        'б) своим предчувствиям'
    ),
    (
        'Ты чувствуешь себя человеком:\n\n'
        'а) более практичным, чем изобретательным\n'
        'б) более изобретательным, чем практичным'
    ),
    (
        'Кто заслуживает больше одобрения:\n\n'
        'а) рассудительный, здравомыслящий человек\n'
        'б) глубоко переживающий человек'
    ),
    (
        'Ты более склонен:\n\n'
        'а) быть прямым и беспристрастным\n'
        'б) сочувствовать людям'
    ),
    (
        'Что, по-твоему, предпочтительней:\n\n'
        'а) удостовериться, что все подготовлено и улажено\n'
        'б) предоставить событиям идти своим чередом'
    ),
    (
        'Отношения между людьми должны строиться:\n\n'
        'а) на предварительной взаимной договоренности\n'
        'б) в зависимости от обстоятельств'
    ),
    (
        'Когда звонит телефон, ты:\n\n'
        'а) торопишься подойти первым\n'
        'б) надеешься, что подойдет кто-нибудь другой'
    ),
    (
        'Что ты цените в себе больше:\n\n'
        'а) развитое чувство реальности\n'
        'б) пылкое воображение'
    ),
    (
        'Ты больше придаешь значение:\n\n'
        'а) тому, что сказано\n'
        'б) тому, как сказано'
    ),
    (
        'Что выглядит большим заблуждением:\n\n'
        'а) излишняя пылкость, горячность\n'
        'б) чрезмерная объективность, беспристрастность'
    ),
    (
        'Ты в основном считаешь себя:\n\n'
        'а) трезвым и практичным\n'
        'б) сердечным и отзывчивым'
    ),
    (
        'Какие ситуации привлекают тебя больше:\n\n'
        'а) регламентированные и упорядоченные\n'
        'б) неупорядоченные и нерегламентированные'
    ),
    (
        'Ты человек скорее:\n\n'
        'а) педантичный, чем капризный\n'
        'б) капризный, чем педантичный'
    ),
    (
        'Ты чаще склонен:\n\n'
        'a) быть открытым, доступным людям\n'
        'б) быть сдержанным, скрытным'
    ),
    (
        'В литературных произведениях ты предпочитаешь:\n\n'
        'а) буквальность, конкретность\n'
        'б) образность, переносный смысл'
    ),
    (
        'Что для тебя труднее:\n\n'
        'а) находить общий язык\n'
        'б) использовать других в своих интересах'
    ),
    (
        'Что бы ты себе больше пожелал:\n\n'
        'а) ясности размышлений\n'
        'б) умения сочувствовать'
    ),
    (
        'Что хуже:\n\n'
        'а) быть неприхотливым\n'
        'б) быть излишне привередливым'
    ),
    (
        'Ты предпочитаешь:\n\n'
        'а) запланированные события\n'
        'б) незапланированные события'
    ),
    (
        'Ты склонен поступать скорее:\n\n'
        'а) обдуманно, чем импульсивно\n'
        'б) импульсивно, чем обдуманно'
    )
]
