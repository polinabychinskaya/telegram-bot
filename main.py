from aiogram import Bot, Dispatcher, executor, types, filters
import mcfq_db as db
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from background import keep_alive

TOKEN = '6388868345:AAGx6ZscZGS6aJnrCePmE3rbyh6KJUZlMF4'
GROUP_ID = -1001943459915
ADMIN_ID = 850399809
storage = MemoryStorage()
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=storage)


#-------------ONSTART-------------#
async def on_startup(_):
  await db.db_start()
  print('Bot has started')


#-------------KEY BOARD-------------#
keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
hello_list = [
  types.KeyboardButton(text='Да', callback_data='shop'),
  types.KeyboardButton(text='Другое', callback_data='other')
]
keyboard.add(*hello_list)

alt = types.ReplyKeyboardMarkup(resize_keyboard=True)
buttonlist = [
  types.KeyboardButton(text='Наша локация', callback_data='loction'),
  types.KeyboardButton(text='Связаться со мной',
                       callback_data='rechme',
                       request_contact=True),
  types.KeyboardButton(text='Вопрос/Ответ (FAQ)', callback_data='faq'),
  types.KeyboardButton(text='Назад', callback_data='back')
]
alt.add(*buttonlist)

yes = types.ReplyKeyboardMarkup(resize_keyboard=True)
yes_kb = [
  types.KeyboardButton(text='Ассортимент', callback_data='ассортимент'),
  types.KeyboardButton(text='Оформить заказ', callback_data='Оформить заказ'),
  types.KeyboardButton(text='Назад', callback_data='back')
]
yes.add(*yes_kb)

admin_board = types.ReplyKeyboardMarkup(resize_keyboard=True)
adm_btn = [
  types.KeyboardButton(text='Ассортимент', callback_data='ассортимент'),
  types.KeyboardButton(text='Добавить товар', callback_data='other'),
  types.KeyboardButton(text='Все заказы', callback_data='other')
]
admin_board.add(*adm_btn)
#-------------CATALOG INLINE KEY BOARD-------------#
inline_catalog = types.InlineKeyboardMarkup()
type1 = types.InlineKeyboardButton(text='Букеты', callback_data='bouquet')
type2 = types.InlineKeyboardButton(text='Розы одноголовые',
                                   callback_data='rosesing')
type3 = types.InlineKeyboardButton(text='Розы кустовые',
                                   callback_data='rosebush')
type4 = types.InlineKeyboardButton(text='Хризантемы',
                                   callback_data='goldendaisy')
type5 = types.InlineKeyboardButton(text='Тюльпаны', callback_data='tulip')
type6 = types.InlineKeyboardButton(text='Эустома', callback_data='eustoma')
type7 = types.InlineKeyboardButton(text='Другие цветы',
                                   callback_data='othertypes')
inline_catalog.add(type1)
inline_catalog.row(type2)
inline_catalog.row(type3)
inline_catalog.row(type4)
inline_catalog.row(type5)
inline_catalog.row(type6)
inline_catalog.row(type7)

inline_location = types.InlineKeyboardMarkup()
location_but = types.InlineKeyboardButton(
  text='📍',
  url=
  'https://www.google.by/maps/place/Minsk/@53.8429103,27.8469451,9z/data=!4m6!3m5!1s0x46dbcfd35b1e6ad3:0xb61b853ddb570d9!8m2!3d53.9006011!4d27.558972!16zL20vMGRseGo?entry=ttu'
)
inline_location.add(location_but)

#-------------FAQ INLINE KEY BOARD-------------#
inline_q = types.InlineKeyboardMarkup()
q1 = types.InlineKeyboardButton(text='Как осуществляется доставка?',
                                callback_data='q1')
q2 = types.InlineKeyboardButton(text='Какие виды упаковки доступны?',
                                callback_data='q2')
inline_q.add(q1)
inline_q.row(q2)


#-------------START-------------#
@dp.message_handler(commands=['start'])
async def cmd_handler(message: types.Message):
  if message.from_user.id == ADMIN_ID:
    await message.answer(
      f'Добро пожаловать, <b>{message.from_user.first_name}</b>. Вы авторизованы как администратор. Можете добавить товарную позицию и посмотреть обновленный ассортимент',
      reply_markup=admin_board,
      parse_mode='html')
  else:
    await message.answer(
      f'Добрый день, <b>{message.from_user.first_name}</b>! Вас приветствует Telegram бот McFlowersQueen! Я смогу ответить на Ваши вопросы и помогу опредделиться с выбором 🥰 Хотели бы посмотреть наш ассортимент?',
      reply_markup=keyboard,
      parse_mode='html')


@dp.message_handler(commands=['id'])
async def cmd_id(message: types.Message):
  await message.answer(f'{message.from_user.id}')


@dp.message_handler(filters.Text(contains='да', ignore_case=True))
async def category_handler(message: types.Message):
  await message.answer('Выберете действие 🤍', reply_markup=yes)


@dp.message_handler(filters.Text(contains='назад', ignore_case=True))
async def category_handler(message: types.Message):
  await message.answer(
    'Не нашли то, что искали? Свяжитесь с нашим флористом @Trofimovich_Vika (+375 25 713 56 72) или перейдите в раздел "другое" 🌿',
    reply_markup=keyboard)


@dp.message_handler(filters.Text(contains='другое', ignore_case=True))
async def category_handler(message: types.Message):
  await message.answer(
    'В этом разделе Вы сможете найти ответы на часто задаваемые вопросы или оставить свои контакты для дальнейшего взаимодействия',
    reply_markup=alt)


#-------------SHOP BUTTON-------------#
@dp.message_handler(filters.Text(contains='ассортимент', ignore_case=True))
async def category_handler(message: types.Message):
  await message.answer('Выберете категорию 🌿: ', reply_markup=inline_catalog)


#-------------LOCATION BUTTON-------------#
@dp.message_handler(filters.Text(contains='локация', ignore_case=True))
async def loc_handler(message: types.Message):
  await message.answer(text='Вы можете найти нас тут: ',
                       reply_markup=inline_location)


#-------------REACH ME BUTTON -> SEND TO MANAGER-------------#
@dp.message_handler(content_types=['contact'])
async def forward_message(message: types.Message):
  await bot.forward_message(ADMIN_ID, message.from_user.id, message.message_id)


#-------------FAQ-------------#
@dp.message_handler(
  filters.Text(contains='вопрос' or 'ответ', ignore_case=True))
async def category_handler(message: types.Message):
  await message.answer(
    'Перед Вами список наиболее часто задаваемых вопросов. Выберете инстересующий Вас вопрос 🌿: ',
    reply_markup=inline_q)


@dp.callback_query_handler(filters.Text(contains='q1'))
async def category_callback_handler(callback_query: types.CallbackQuery):
  await callback_query.message.answer(
    text=
    '<b>Как осуществляется доставка?</b> \nБЕСПЛАТНО призаказе от 80р (в пределах МКАД)\nПри заказе менее 80р - 9р\nБЕСПЛАТНО - самовывоз с ул. Полевая, 10 (г. Минск\nДоставка по Минской области (в пределах МКАД 2) - 15р)',
    parse_mode='html')
  await callback_query.answer()


@dp.callback_query_handler(filters.Text(contains='q2'))
async def category_callback_handler(callback_query: types.CallbackQuery):
  await callback_query.message.answer(
    text=
    '<b>Какие виды упаковки доступны?</b> \nКрафт ~ 3р\nЦветная/прозрачная пленка ~ 3-6р\nБез упаковки (только лента) - 0р \n*Просьба отбратить внимание, что на стоимость упаковки влияет размер букета',
    parse_mode='html')
  await callback_query.answer()


#-------------NEW ORDER-------------#
class NewOrder(StatesGroup):
  name = State()
  phone = State()
  items = State()
  time = State()
  delivery = State()
  pay = State()
  wrap = State()


@dp.message_handler(text='Оформить заказ')
async def add_order(message: types.Message):
  await NewOrder.name.set()
  await message.answer('Введите свое <b>имя</b>', parse_mode='html')


@dp.message_handler(state=NewOrder.name)
async def add_order_name(message: types.Message, state: FSMContext):
  async with state.proxy() as data:
    data['name'] = message.text
  await message.answer('Введите свой <b>номер телефона</b>', parse_mode='html')
  await NewOrder.next()


@dp.message_handler(state=NewOrder.phone)
async def add_order_phone(message: types.Message, state: FSMContext):
  async with state.proxy() as data:
    data['phone'] = message.text
  await message.answer(
    'Введите <b>товарные позиции</b> и их <b>количество</b>',
    parse_mode='html')
  await NewOrder.next()


@dp.message_handler(state=NewOrder.items)
async def add_order_items(message: types.Message, state: FSMContext):
  async with state.proxy() as data:
    data['items'] = message.text
  await message.answer(
    'Введите <b>время</b> и <b>дату</b> доставки или самовывоза',
    parse_mode='html')
  await NewOrder.next()


@dp.message_handler(state=NewOrder.time)
async def add_order_items(message: types.Message, state: FSMContext):
  async with state.proxy() as data:
    data['time'] = message.text
  await message.answer(
    'Введите <b>способ доставки</b> \nБЕСПЛАТНО при заказе от 80р (в пределах МКАД)\nПри заказе менее 80р - 9р\nБЕСПЛАТНО - самовывоз с ул. Полевая, 10 (г. Минск\nДоставка по Минской области (в пределах МКАД 2) - 15р)',
    parse_mode='html')
  await NewOrder.next()


@dp.message_handler(state=NewOrder.delivery)
async def add_order_items(message: types.Message, state: FSMContext):
  async with state.proxy() as data:
    data['delivery'] = message.text
  await message.answer(
    'Введите <b>способ оплаты</b>\n<b>Доступные виды оплаты:</b>\nОплата по реквизитам\nНаличными при получении',
    parse_mode='html')
  await NewOrder.next()


@dp.message_handler(state=NewOrder.pay)
async def add_order_delivery(message: types.Message, state: FSMContext):
  async with state.proxy() as data:
    data['pay'] = message.text
  await message.answer(
    'Введите вид упаковки\n<b>Доступные виды упаковки:</b>\nКрафт ~ 3р\nЦветная/прозрачная пленка ~ 3-6р\nБез упаковки (только лента) - 0р \n*Просьба отбратить внимание, что на стоимость упаковки влияет размер букета',
    parse_mode='html')
  await NewOrder.next()


@dp.message_handler(state=NewOrder.wrap)
async def add_order_delivery(message: types.Message, state: FSMContext):
  async with state.proxy() as data:
    data['wrap'] = message.text
  await db.add_order(state)
  db.cur.execute("SELECT * FROM items")
  rows = db.cur.fetchall()
  data = []
  for row in rows:
    rec = {}
    rec['id'] = row[0]
    rec['name'] = row[1]
    rec['phone'] = row[2]
    rec['items'] = row[3]
    rec['time'] = row[4]
    rec['delivery'] = row[5]
    rec['pay'] = row[6]
    rec['wrap'] = row[7]
    data.append(rec)
  for rec in data:
    text = f"ID: {rec['id']}\nИмя: {rec['name']}\nТелефон: {rec['phone']}\nТовары: {rec['items']}\nВремя получения: {rec['time']}\nДоставка: {rec['delivery']}\nОплата: {rec['pay']}\nУпаковка: {rec['wrap']}"
  await bot.send_message(chat_id=ADMIN_ID, text=text)
  await message.answer('Заказ создан!', reply_markup=keyboard)
  await message.answer(
    '*<b>Внимание!</b> Заказ является подтвержденным только после связи с нашим специалистом',
    parse_mode='html')
  await state.finish()


@dp.message_handler(filters.Text(contains='Все заказы', ignore_case=True))
async def handle_get_data(message: types.Message):
  db.cur.execute("SELECT * FROM items")
  rows = db.cur.fetchall()
  data = []
  for row in rows:
    rec = {}
    rec['id'] = row[0]
    rec['name'] = row[1]
    rec['phone'] = row[2]
    rec['items'] = row[3]
    rec['time'] = row[4]
    rec['delivery'] = row[5]
    rec['pay'] = row[6]
    rec['wrap'] = row[7]
    data.append(rec)
  for rec in data:
    text = f"ID: {rec['id']}\nИмя: {rec['name']}\nТелефон: {rec['phone']}\nТовары: {rec['items']}\nВремя получения: {rec['time']}\nДоставка: {rec['delivery']}\nОплата: {rec['pay']}\nУпаковка: {rec['wrap']}"
    await bot.send_message(chat_id=ADMIN_ID, text=text)


#-------------NEW GOOD-------------#
class NewGood(StatesGroup):
  good_type = State()
  good_name = State()
  good_desc = State()
  good_price = State()
  good_photo = State()


@dp.message_handler(text='Добавить товар')
async def add_new_good(message: types.Message):
  if message.from_user.id == ADMIN_ID:
    await NewGood.good_type.set()
    await message.answer('Выберете категорию товара: ',
                         reply_markup=inline_catalog)


@dp.callback_query_handler(state=NewGood.good_type)
async def add_good_type(call: types.CallbackQuery, state: FSMContext):
  async with state.proxy() as data:
    data['good_type'] = call.data
  await call.message.answer('Введите название товара')
  await NewGood.next()


@dp.message_handler(state=NewGood.good_name)
async def add_good_name(message: types.Message, state: FSMContext):
  async with state.proxy() as data:
    data['good_name'] = message.text
  await message.answer('Введите описание товара')
  await NewGood.next()


@dp.message_handler(state=NewGood.good_desc)
async def add_good_desc(message: types.Message, state: FSMContext):
  async with state.proxy() as data:
    data['good_desc'] = message.text
  await message.answer('Введите цену товара')
  await NewGood.next()


@dp.message_handler(state=NewGood.good_price)
async def add_good_price(message: types.Message, state: FSMContext):
  async with state.proxy() as data:
    data['good_price'] = message.text
  await message.answer('Отправьте фотографию товара')
  await NewGood.next()


@dp.message_handler(lambda message: not message.photo,
                    state=NewGood.good_photo)
async def add_item_photo_check(message: types.Message):
  await message.answer('This is not an image!')


@dp.message_handler(content_types=['photo'], state=NewGood.good_photo)
async def add_good_photo(message: types.Message, state: FSMContext):
  async with state.proxy() as data:
    data['good_photo'] = message.photo[0].file_id
  await db.add_good(state)
  await message.answer('Товар успешно создан!', reply_markup=admin_board)
  await state.finish()


@dp.callback_query_handler(filters.Text(contains='bouquet'))
async def send_ord_data(callback_query: types.CallbackQuery):
  db.cur.execute("SELECT * FROM goods WHERE good_category=?", ('bouquet', ))
  ord_rows = db.cur.fetchall()
  ord = []
  for i in ord_rows:
    record = {}
    record['i_id'] = i[0]
    record['good_name'] = i[1]
    record['good_desc'] = i[2]
    record['good_price'] = i[3]
    record['good_photo'] = i[4]
    record['good_category'] = i[5]
    ord.append(record)
  for record in ord:
    id_photo = record['good_photo']
    cap_text = f"Название: {record['good_name']}\nСостав/Описание: {record['good_desc']}\nЦена: {record['good_price']}"
    await callback_query.message.answer_photo(photo=id_photo, caption=cap_text)
    await callback_query.answer()


@dp.callback_query_handler(filters.Text(contains='rosesing'))
async def send_ord_data(callback_query: types.CallbackQuery):
  db.cur.execute("SELECT * FROM goods WHERE good_category=?", ('rosesing', ))
  rose_rows = db.cur.fetchall()
  rose = []
  for rs in rose_rows:
    rosesing = {}
    rosesing['i_id'] = rs[0]
    rosesing['good_name'] = rs[1]
    rosesing['good_desc'] = rs[2]
    rosesing['good_price'] = rs[3]
    rosesing['good_photo'] = rs[4]
    rosesing['good_category'] = rs[5]
    rose.append(rosesing)
  for rosesing in rose:
    id_photo = rosesing['good_photo']
    cap_text = f"Название: {rosesing['good_name']}\nСостав/Описание: {rosesing['good_desc']}\nЦена: {rosesing['good_price']}"
    await callback_query.message.answer_photo(photo=id_photo, caption=cap_text)
    await callback_query.answer()


@dp.callback_query_handler(filters.Text(contains='rosebush'))
async def send_ord_data(callback_query: types.CallbackQuery):
  db.cur.execute("SELECT * FROM goods WHERE good_category=?", ('rosebush', ))
  rose_rows = db.cur.fetchall()
  rose = []
  for rs in rose_rows:
    rosesing = {}
    rosesing['i_id'] = rs[0]
    rosesing['good_name'] = rs[1]
    rosesing['good_desc'] = rs[2]
    rosesing['good_price'] = rs[3]
    rosesing['good_photo'] = rs[4]
    rosesing['good_category'] = rs[5]
    rose.append(rosesing)
  for rosesing in rose:
    id_photo = rosesing['good_photo']
    cap_text = f"Название: {rosesing['good_name']}\nСостав/Описание: {rosesing['good_desc']}\nЦена: {rosesing['good_price']}"
    await callback_query.message.answer_photo(photo=id_photo, caption=cap_text)
    await callback_query.answer()


@dp.callback_query_handler(filters.Text(contains='goldendaisy'))
async def send_ord_data(callback_query: types.CallbackQuery):
  db.cur.execute("SELECT * FROM goods WHERE good_category=?",
                 ('goldendaisy', ))
  ord_rows = db.cur.fetchall()
  ord = []
  for i in ord_rows:
    record = {}
    record['i_id'] = i[0]
    record['good_name'] = i[1]
    record['good_desc'] = i[2]
    record['good_price'] = i[3]
    record['good_photo'] = i[4]
    record['good_category'] = i[5]
    ord.append(record)
  for record in ord:
    id_photo = record['good_photo']
    cap_text = f"Название: {record['good_name']}\nСостав/Описание: {record['good_desc']}\nЦена: {record['good_price']}"
    await callback_query.message.answer_photo(photo=id_photo, caption=cap_text)
    await callback_query.answer()


@dp.callback_query_handler(filters.Text(contains='tulip'))
async def send_ord_data(callback_query: types.CallbackQuery):
  db.cur.execute("SELECT * FROM goods WHERE good_category=?", ('tulip', ))
  ord_rows = db.cur.fetchall()
  ord = []
  for i in ord_rows:
    record = {}
    record['i_id'] = i[0]
    record['good_name'] = i[1]
    record['good_desc'] = i[2]
    record['good_price'] = i[3]
    record['good_photo'] = i[4]
    record['good_category'] = i[5]
    ord.append(record)
  for record in ord:
    id_photo = record['good_photo']
    cap_text = f"Название: {record['good_name']}\nСостав/Описание: {record['good_desc']}\nЦена: {record['good_price']}"
    await callback_query.message.answer_photo(photo=id_photo, caption=cap_text)
    await callback_query.answer()


@dp.callback_query_handler(filters.Text(contains='eustoma'))
async def send_ord_data(callback_query: types.CallbackQuery):
  db.cur.execute("SELECT * FROM goods WHERE good_category=?", ('eustoma', ))
  ord_rows = db.cur.fetchall()
  ord = []
  for i in ord_rows:
    record = {}
    record['i_id'] = i[0]
    record['good_name'] = i[1]
    record['good_desc'] = i[2]
    record['good_price'] = i[3]
    record['good_photo'] = i[4]
    record['good_category'] = i[5]
    ord.append(record)
  for record in ord:
    id_photo = record['good_photo']
    cap_text = f"Название: {record['good_name']}\nСостав/Описание: {record['good_desc']}\nЦена: {record['good_price']}"
    await callback_query.message.answer_photo(photo=id_photo, caption=cap_text)
    await callback_query.answer()


@dp.callback_query_handler(filters.Text(contains='othertypes'))
async def send_ord_data(callback_query: types.CallbackQuery):
  db.cur.execute("SELECT * FROM goods WHERE good_category=?", ('othertypes', ))
  ord_rows = db.cur.fetchall()
  ord = []
  for i in ord_rows:
    record = {}
    record['i_id'] = i[0]
    record['good_name'] = i[1]
    record['good_desc'] = i[2]
    record['good_price'] = i[3]
    record['good_photo'] = i[4]
    record['good_category'] = i[5]
    ord.append(record)
  for record in ord:
    id_photo = record['good_photo']
    cap_text = f"Название: {record['good_name']}\nСостав/Описание: {record['good_desc']}\nЦена: {record['good_price']}"
    await callback_query.message.answer_photo(photo=id_photo, caption=cap_text)
    await callback_query.answer()


keep_alive()

if __name__ == '__main__':
  executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
