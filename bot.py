from datetime import datetime
import json
import os
import threading
import time
from zoneinfo import ZoneInfo  # Корректная работа с часовыми поясами
from telebot.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)
import telebot
import schedule

TOKEN = "8658031274:AAHN9rcIbxIXlHPTQHToDCr6TAeAInVDOYU"

try:
  temp_bot = telebot.TeleBot(TOKEN)
  temp_bot.stop_polling()
  temp_bot.remove_webhook()
  time.sleep(1.5)
except Exception as e:
  print(f"Предупреждение при сбросе сессии: {e}")

bot = telebot.TeleBot(TOKEN)

# Файл для постоянного хранения прогресса
PROGRESS_FILE = "user_progress.json"

def load_progress():
  if os.path.exists(PROGRESS_FILE):
    try:
      with open(PROGRESS_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
        return {int(k): set(v) for k, v in data.items()}
    except Exception as e:
      print(f"Ошибка загрузки прогресса: {e}")
  return {}

def save_progress():
  try:
    data = {str(k): list(v) for k, v in user_read_days.items()}
    with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
      json.dump(data, f, ensure_ascii=False, indent=4)
  except Exception as e:
    print(f"Ошибка сохранения прогресса: {e}")

user_read_days = load_progress()
user_day_progress = {}

# База данных контента для всех 21 дней
DAYS_CONTENT = {
    1: {
        "tag": "🔵 <b>Масштаб и Горизонты</b>",
        "title": "День 1",
        "wish": (
            "<i>С днем рождения, наш дорогой человек! 🎉Сегодня стартует твой"
            " личный трехнедельный адвент-календарь. Ты человек, который умеет"
            " покорять самые крутые вершины — будь то заснеженные горнолыжные"
            " склоны, новые масштабы в бизнесе или амбициозные проекты. Но"
            " самый красивый вид всегда открывается тем, кто умеет смотреть за"
            " горизонт с высоты птичьего полета. Мы желаем тебе сегодня"
            " почувствовать бескрайнюю свободу и масштаб. Пусть этот день"
            " подарит понимание, как много великого, интересного и"
            " вдохновляющего у тебя еще впереди! Мы все тобой очень гордимся и"
            " бесконечно любим.</i>"
        ),
        "quote": (
            "«Чем выше поднимаешься, тем дальше видишь. А чем дальше видишь, тем"
            " проще проложить правильный путь.»\n— <b>Омар Хайям</b>,"
            " персидский математик, астроном, философ и поэт."
        ),
        "teaser": (
            "В массовом сознании Омар Хайям известен прежде всего своими"
            " поэтическими четверостишиями. Однако в истории он остался в"
            " первую очередь как выдающийся ученый, возглавлявший крупнейшую"
            " обсерваторию мира и мысливший категориями галактического"
            " масштаба.\n\nВ сегодняшней статье мы разбираем, как великому"
            " математику XI века удавалось сочетать точность расчетов с"
            " масштабом стратегического видения, и как этот принцип помогает"
            " строить крупные бизнес-системы сегодня. \n\n<i>Открой контент дня,"
            " чтобы узнать что-то новое.</i>"
        ),
        "article_title": (
            "Мудрость обсерваторий: Как Омар Хайям совмещал масштаб науки,"
            " точность математики и визионерский подход"
        ),
        "article_text": (
            "В 1074 году, когда Хайяму было всего 26 лет, визирь Сельджукской"
            " империи Низам аль-Мульк и султан Малик-шах призвали его в столицу"
            " Исфахан. Перед молодой учеными поставили грандиозную задачу —"
            " возглавить крупнейшую астрономическую обсерваторию мира и"
            " реформировать действующий календарь империи.\n\n<b>1. Проект"
            " длиной в 5 000 лет: Масштаб системного мышления</b>\n\nКалендарь,"
            " созданный Хайямом (получивший название «Джалали»), требовал"
            " фундаментального переосмысления того, как человек взаимодействует"
            " со временем. Хайям произвел точнейшие астрономические наблюдения и"
            " вычисления. Созданный им солнечный календарь давал погрешность в"
            " один день лишь раз в 5 000 лет. Для сравнения: современный"
            " григорианский календарь дает погрешность в один день каждые 3"
            " 330 лет.\n\nЧтобы создать такую систему, Хайяму требовалось"
            " мыслить категориями, выходящими далеко за пределы человеческой"
            " жизни. В современном управленческом контексте это классический"
            " пример визионерского масштаба: умение проектировать"
            " бизнес-архитектуру и процессы так, чтобы они оставались"
            " устойчивыми спустя десятилетия.\n\n<b>2. Пространственное видение"
            " сложных бизнес-задач</b>\n\nМало кто знал, что Хайям написал"
            " фундаментальный «Трактат о доказательствах задач алгебры», где"
            " впервые в истории дал классификацию кубических уравнений и решил"
            " их с помощью геометрического метода — через пересечение"
            " конических сечений.\n\nВ этом проявляется ключевой навык"
            " масштабного лидера: умение переводить сухую алгебру бизнес-показателей"
            " в объемную пространственную модель, видя взаимосвязи там, где"
            " другие видят лишь набор разрозненных цифр."
        ),
        "recommendation": (
            "📚 <a"
            " href='https://music.yandex.ru/search?text=Омар+Хайям+аудиокнига'>Слушать"
            " аудиокнигу «Омар Хайям: Рубаи и философия» на Яндекс Музыке</a>"
        ),
    },
    2: {
        "tag": "🔴 <b>Сила и Мудрость</b>",
        "title": "День 2",
        "wish": (
            "<i>Пусть этот день принесет тебе глубокое чувство внутреннего мира"
            " и гармонии. Истинная мудрость и сила духа проявляются не в"
            " стремлении покорить весь внешний мир, а в умении сохранить"
            " абсолютную тишину, ясность и непреклонность внутри себя. Мы желаем"
            " тебе сегодня момента глубокого созерцания и внутренней свободы."
            " Пусть твоя душевная стойкость служит надежным якорем, а мудрость"
            " помогает видеть истинную суть вещей за любой внешней суетой.</i>"
        ),
        "quote": (
            "«Нигде человек не находит более спокойного и безмятежного убежища,"
            " чем в своей собственной душе.»\n— <b>Марк Аврелий</b>, римский"
            " император и философ-стоик."
        ),
        "teaser": (
            "Марк Аврелий писал свои личные дневники во время военных походов и"
            " эпидемий. В самые тяжелые моменты он обращался к философии не ради"
            " теории, а чтобы найти внутренний стержень и сохранить чистоту"
            " помыслов. \n\nСегодняшний материал посвящен философии стоицизма и"
            " учению о «Внутренней цитадели» — искусству обретения непреклонной"
            " силы духа и ментального спокойствия в мире постоянных изменений."
        ),
        "article_title": (
            "Внутренняя Цитадель: Стоицизм как философия силы духа и спокойствия"
            " ума"
        ),
        "article_text": (
            "В философии стоиков существует понятие «Внутренней цитадели» —"
            " ментального пространства внутри каждого из нас, куда не имеют"
            " доступа внешние обстоятельства, чужие оценки или жизненные"
            " штормы.\n\n<b>1. Дихотомия контроля: Освобождение ума</b>\n\nОснова"
            " стоической мудрости заключается в умении проводить чёткую границу"
            " между двумя сферами:\n\nТо, что вне нашей власти: смены эпох,"
            " поведение окружающих людей, прошлые события, экономические циклы и"
            " физиологическое старение. Беспокойство о них разрушает духовные"
            " силы.\n\nТо, что полностью в нашей власти: наши суждения, наши"
            " ценности, наши реакции, отношение к происходящему и чистота наших"
            " намерений. Мудрость начинается тогда, когда человек полностью"
            " забирает свое внимание из первой сферы и направляет его на"
            " взращивание второй.\n\n<b>2. Практика ментальной тишины</b>\n\nСтоики"
            " верили, что нас расстраивают не сами вещи и события, а наши"
            " представления о них. Между событием и нашей реакцией всегда есть"
            " секунда абсолютной свободы — именно там обитает сила духа. Когда"
            " человек овладевает искусством делать паузу, он перестает мгновенно"
            " вовлекаться в эмоциональные провокации внешнего мира. Это дает"
            " ему редкое качество — «тихую силу», которую окружающие считывают"
            " как глубокую надежность и авторитет.\n\n<b>3. Три правила"
            " сохранения внутреннего стержня</b>\n\n<b>1. Осознанность момента"
            " (Amor Fati):</b> Принимать текущие обстоятельства не с"
            " покорностью, а с достоинством созерцателя, который понимает, что"
            " любые испытания — это лишь материал для закалки характера.\n\n<b>2."
            " Гигиена мыслей:</b> Очищать сознание от лишнего информационного"
            " шума так же регулярно, как мы очищаем физическое пространство.\n\n<b>3."
            " Верность своим ценностям:</b> Иметь нерушимый кодекс чести,"
            " который остается неизменным независимо от того, хвалят тебя или"
            " критикуют."
        ),
        "recommendation": (
            "📚 <a"
            " href='https://music.yandex.ru/search?text=Марк+Аврелий+Наедине+с+собой'>Слушать"
            " аудиокнигу Марк Аврелий «Наедине с собой» на Яндекс Музыке</a>"
        ),
    },
}

for d in range(1, 22):
  if d not in DAYS_CONTENT:
    DAYS_CONTENT[d] = {
        "tag": "🟢 <b>Энергия, Движение и Баланс</b>",
        "title": f"День {d}",
        "wish": "<i>Прекрасного и вдохновляющего дня! Желаем отличного настроения.</i>",
        "quote": "«Каждый день — это шаг вперед.»",
        "teaser": "Краткое содержание темы этого дня.",
        "article_title": f"Полезный материал для Дня {d}",
        "article_text": "Подробный текст для этого дня.",
        "recommendation": "💡 <a href='https://music.yandex.ru'>Яндекс Музыка</a>",
    }

def get_reply_keyboard():
  keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
  keyboard.add(
      KeyboardButton("📅 Вернуться в календарь"), KeyboardButton("🚀 Старт")
  )
  keyboard.add(KeyboardButton("🔄 Начать сначала"))
  return keyboard

def get_calendar_markup(user_id):
  markup = InlineKeyboardMarkup(row_width=5)
  buttons = []
  read_days = user_read_days.get(user_id, set())

  if read_days:
    next_unlocked_day = max(read_days) + 1
  else:
    next_unlocked_day = 1

  for i in range(1, 22):
    if i in read_days:
      btn_text = f"✅ {i}"
    elif i == next_unlocked_day:
      btn_text = f"🎁 {i}"
    elif i < next_unlocked_day:
      btn_text = f"🎁 {i}"
    else:
      btn_text = f"🔒 {i}"
    buttons.append(InlineKeyboardButton(btn_text, callback_data=f"day_{i}"))
  markup.add(*buttons)
  return markup

@bot.message_handler(commands=["start"])
def send_welcome(message):
  user_id = message.from_user.id
  if user_id not in user_read_days:
    user_read_days[user_id] = set()
  bot.send_message(
      message.chat.id,
      "🎉 <b>Алешка, добро пожаловать в твой праздничный 21-дневный"
      " адвент-календарь-открытку!</b>\n\nОткрой свой первый день:\n\n🎁 -"
      " доступен, ✅ - просмотрен, 🔒 - заблокирован.",
      reply_markup=get_calendar_markup(user_id),
      parse_mode="HTML",
  )
  bot.send_message(
      message.chat.id, "⬇️ Меню навигации ниже:", reply_markup=get_reply_keyboard()
  )

@bot.message_handler(commands=["reset"])
def reset_progress_command(message):
  user_id = message.from_user.id
  if user_id in user_read_days:
    user_read_days[user_id] = set()
  if user_id in user_day_progress:
    user_day_progress[user_id] = {}
  save_progress()

  bot.send_message(
      message.chat.id,
      "🔄 <b>Прогресс успешно сброшен!</b> Бот запущен как впервые.",
      parse_mode="HTML"
  )
  send_welcome(message)

@bot.message_handler(
    func=lambda message: message.text
    in ["📅 Вернуться в календарь", "🚀 Старт", "🔄 Начать сначала"]
)
def handle_reply_menu(message):
  user_id = message.from_user.id

  if message.text == "🔄 Начать сначала":
    if user_id in user_read_days:
      user_read_days[user_id] = set()
    if user_id in user_day_progress:
      user_day_progress[user_id] = {}
    save_progress()

    bot.send_message(
        message.chat.id,
        "🔄 <b>Все данные и прогресс сброшены.</b> Календарь открывается заново!",
        parse_mode="HTML"
    )

  if user_id not in user_read_days:
    user_read_days[user_id] = set()

  bot.send_message(
      message.chat.id,
      "🎉 <b>Твоя адвент-открытка:</b>\n\n🎁 - доступно, ✅ - прочитано, 🔒 - ждет своей очереди.",
      reply_markup=get_calendar_markup(user_id),
      parse_mode="HTML",
  )

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
  user_id = call.from_user.id
  read_days = user_read_days.get(user_id, set())
  next_unlocked_day = max(read_days) + 1 if read_days else 1

  if call.data.startswith("day_"):
    parts = call.data.split("_")
    day_num = int(parts[1].split()[0])
    if day_num > next_unlocked_day:
      bot.answer_callback_query(
          call.id,
          text="🔒 Этот день пока заблокирован! Сначала открой предыдущие дни.",
          show_alert=True,
      )
      return
    data = DAYS_CONTENT.get(day_num)
    bot.answer_callback_query(call.id)
    text = (
        f"{data['tag']}\n\n"
        f"🌟 <b>{data['title']}</b>\n\n"
        f"<b>Пожелание дня:</b>\n{data['wish']}\n\n"
        f"<b>Цитата дня:</b>\n{data['quote']}\n\n"
        f"<b>Тизер:</b>\n{data['teaser']}"
    )
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton("📖 Контент дня", callback_data=f"read_art_{day_num}"),
        InlineKeyboardButton("💡 Рекомендация дня", callback_data=f"rec_day_{day_num}"),
        InlineKeyboardButton("⬅️ К календарю", callback_data="back_to_menu"),
    )
    bot.send_message(call.message.chat.id, text, reply_markup=markup, parse_mode="HTML")
  elif call.data.startswith("read_art_"):
    day_num = int(call.data.split("_")[2])
    data = DAYS_CONTENT.get(day_num)
    bot.answer_callback_query(call.id)
    if user_id not in user_read_days:
      user_read_days[user_id] = set()
    if user_id not in user_day_progress:
      user_day_progress[user_id] = {}
    if day_num not in user_day_progress[user_id]:
      user_day_progress[user_id][day_num] = {"art": False, "rec": False}
    user_day_progress[user_id][day_num]["art"] = True
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton("📌 Рекомендация дня", callback_data=f"rec_day_{day_num}"),
        InlineKeyboardButton("📅 К календарю", callback_data="back_to_menu"),
    )
    bot.send_message(
        call.message.chat.id,
        f"📜 <b>{data['article_title']}</b>\n\n{data['article_text']}",
        reply_markup=markup,
        parse_mode="HTML",
        disable_web_page_preview=False,
    )
    if user_day_progress[user_id][day_num]["rec"]:
      user_read_days[user_id].add(day_num)
      save_progress()
  elif call.data.startswith("rec_day_"):
    day_num = int(call.data.split("_")[2])
    data = DAYS_CONTENT.get(day_num)
    bot.answer_callback_query(call.id)
    if user_id not in user_read_days:
      user_read_days[user_id] = set()
    if user_id not in user_day_progress:
      user_day_progress[user_id] = {}
    if day_num not in user_day_progress[user_id]:
      user_day_progress[user_id][day_num] = {"art": False, "rec": False}
    user_day_progress[user_id][day_num]["rec"] = True
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton("📖 Контент дня", callback_data=f"read_art_{day_num}"),
        InlineKeyboardButton("📅 К календарю", callback_data="back_to_menu"),
    )
    bot.send_message(
        call.message.chat.id,
        f"💡 <b>Рекомендация:</b>\n\n{data['recommendation']}",
        reply_markup=markup,
        parse_mode="HTML",
        disable_web_page_preview=False,
    )
    if user_day_progress[user_id][day_num]["art"]:
      user_read_days[user_id].add(day_num)
      save_progress()
  elif call.data == "back_to_menu":
    bot.answer_callback_query(call.id)
    bot.send_message(
        call.message.chat.id,
        "🎉 <b>Твоя адвент-открытка:</b>\n\n🎁 - доступно, ✅ - прочитано, 🔒 - заблокировано.",
        reply_markup=get_calendar_markup(user_id),
        parse_mode="HTML",
    )

# ==================== ФОНОВАЯ РАССЫЛКА (SCHEDULE) ====================
def send_daily_notification():
  """Функция рассылки уведомлений пользователям."""
  print("\n[РАССЫЛКА]: Запуск автоматической утренней рассылки по Москве...")
  for user_id in user_read_days.keys():
    try:
      bot.send_message(
          user_id,
          (
              "⏰ <b>Твой новый день ждет, чтобы ты открыл его!</b>\n\nЗагляни в"
              " календарь, чтобы узнать что-то новое:"
          ),
          reply_markup=get_calendar_markup(user_id),
          parse_mode="HTML",
      )
      print(f"Уведомление успешно отправлено пользователю {user_id}")
    except Exception as e:
      print(f"Не удалось отправить уведомление пользователю {user_id}: {e}")

def run_scheduler():
  """Фоновый планировщик с учетом московского времени (Europe/Moscow)."""
  moscow_tz = ZoneInfo("Europe/Moscow")
  
  # ТЕСТОВОЕ ВРЕМЯ: Установите нужное время для теста (например, 18:43 по Москве)
  TARGET_TIME = "18:43"
  
  schedule.every().day.at(TARGET_TIME).do(send_daily_notification)
  print(f"Планировщик настроен на время {TARGET_TIME} по МСК.")

  while True:
    # Получаем текущее время именно по Московскому часовому поясу
    now_moscow = datetime.now(moscow_tz)
    # Проверяем запланированные задачи (schedule сравнивает локальное время машины, 
    # поэтому мы делаем сверку с учетом зоны или настраиваем запуск)
    # Альтернативный цикл проверки для точного срабатывания по МСК:
    
    # Более надежный метод проверки времени по МСК в цикле:
    current_time_str = now_moscow.strftime("%H:%M")
    if current_time_str == TARGET_TIME:
      # Запускаем рассылку один раз в эту минуту
      send_daily_notification()
      # Ждем 61 секунду, чтобы не запустить повторно в ту же минуту
      time.sleep(61)
      
    time.sleep(15)

if __name__ == "__main__":
  scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
  scheduler_thread.start()
  print("Фоновый планировщик рассылки успешно запущен в потоке!")
  print("Бот успешно запущен и работает!")
  bot.polling(none_stop=True)
