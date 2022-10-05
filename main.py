import logging
import keyboard
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from sqlite import Database
from config import API, ADMINS
from aiogram import executor, Dispatcher, Bot

logging.basicConfig(level=logging.INFO)
bot = Bot(API, parse_mode='html')
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
db = Database(path_to_db='main.db')
try:
    db.create_table_users()
except Exception as err:
    pass
false = False
true = True


class doc(StatesGroup):
    doc = State()


class ddoc(StatesGroup):
    ddoc = State()


class testing(StatesGroup):
    testing = State()


class testingz(StatesGroup):
    testing = State()


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Botni ishga tushurish"),
            types.BotCommand("help", "Yordam"),
        ]
    )


@dp.inline_handler()
async def Inline1(query: types.InlineQuery):
    try:
        await query.answer(
            results=[
                types.InlineQueryResultCachedDocument(
                    id='main001',
                    title=f"{db.select_user(id=query.query.title())[1]} raqamli test",
                    document_file_id=db.select_user(id=query.query.title())[2]
                )
            ]
        )
    except:
        pass

    # ---------------------------------------------------------------Start


@dp.message_handler(text='/start', state=[doc, ddoc, testingz, testing, None])
async def bot_start(message: types.Message, state: FSMContext):
    await message.answer('Botdan foydalanish uchun kerakli tugmani bosing!',
                         reply_markup=keyboard.menu)
    await state.reset_state(with_data=False)


# --------------------------------------------------------------------HelpAdmin
@dp.message_handler(text='/help', state=[doc, ddoc, testingz, testing, None], chat_id=ADMINS)
async def bot_help(message: types.Message):
    await message.answer(text='<a href="https://telegra.ph/Qollanma-10-06-5"> Qo\'llanma </a>')


# --------------------------------------------------------------------Help
@dp.message_handler(text='/help', state=[doc, ddoc, testingz, testing, None])
async def bot_help(message: types.Message):
    await message.answer('Test faylini olish uchun @NamDUAlbot so\'zidan so\'ng file idsini kiriting\n'
        'Testni tekshirish bo\'limi orqali kirib testi_id*javoblar(namuna:1*abccba) orqali testni tekshirish mumkin.\n'
        '/start - botni qayta ishga tushirish')


# ------------------------------------------------------------------Tekshirish
@dp.message_handler(text='Testni Tekshirish')
async def testingHandler(msg: types.Message):
    await msg.answer(text='Test kodini kiriting*abcd ko\'rinishida kiriting',
                     reply_markup=keyboard.back)
    await testing.testing.set()
    await msg.delete()


@dp.message_handler(text='Ortga', state=[testing.testing, ddoc.ddoc, doc.doc])
async def backHandler(msg: types.Message, state: FSMContext):
    await msg.answer(text='Botdan foydalanish uchun kerakli tugmani bosing!',
                     reply_markup=keyboard.menu)
    await state.reset_state(with_data=False)
    await msg.delete()


@dp.message_handler(state=testing.testing)
async def test(msg: types.Message, state: FSMContext):
    try:
        user = db.select_user(id=msg.text.split('*')[0])[3]
        test = msg.text.split('*')[1]
        if len(user) != len(test):
            await msg.answer(
                f"Siz {len(user)} ta javob berishingiz kerak , ammo {len(test)} ta javob berdingiz,\nQayta urinib ko'ring!")
        else:
            k = "✅"
            l = "❎"
            x = 0
            y = ''
            for i in range(len(user)):
                if user[i] == test[i]:
                    x += 1
                    y += f'{i + 1}{k}'
                else:
                    y += f'{i + 1}{l}'
            k = f'Siz {msg.text} raqamli test savollaridan {x} tasiga to\'g\'ri javob topdingiz\nNatija: {y}'
            await msg.answer(k)
    except:
        await msg.answer('Bazada bunday test yo\'q')

    # --------------------------------------------Test Yaratish


@dp.message_handler(text='Test Yaratish', chat_id=ADMINS)
async def createHandler(msg: types.Message):
    await msg.answer(text='Assalomu Aleykum Ustoz!\nIltimos kerakli tugmani bosing!',
                     reply_markup=keyboard.testing)
    await testingz.testing.set()
    await msg.delete()


@dp.message_handler(text='Test Tuzish', state=testingz.testing)
async def createHandler(msg: types.Message, state: FSMContext):
    await msg.answer(text='<a href="https://telegra.ph/Qollanma-10-06-5"> Qo\'llanma </a>',
                     reply_markup=keyboard.back)
    await msg.answer('Test faylini yuboring(javoblari bilan)')
    await state.reset_state(with_data=False)
    await doc.doc.set()
    await msg.delete()


@dp.message_handler(content_types=types.ContentType.DOCUMENT, state=doc.doc)
async def docHandler(doc: types.Message, state: FSMContext):
    docurl = doc.document.file_id
    try:
        solves = doc.caption
        userid = doc.from_user.id
        db.add_user(userid=userid,
                    docurl=docurl,
                    solves=solves)
        await state.finish()
        await doc.answer('Test qabul qilindi', reply_markup=keyboard.menu)
        await doc.answer(f"Test id:{db.select_user(docurl=docurl)[1]}")
    except:
        await doc.answer('Siz javoblarni kiritimadingiz,\n test yaratishni boshidan boshlang!',
                         reply_markup=keyboard.menu)
    await state.reset_state(with_data=False)


@dp.message_handler(text='Testni O\'chirish', state=testingz.testing)
async def deldoc(msg: types.Message, state: FSMContext):
    await msg.answer(text='Testni o\'chirish uchun test \'id\'sini kiriting:',
                     reply_markup=keyboard.back)
    await state.reset_state(with_data=False)
    await ddoc.ddoc.set()
    await msg.delete()


@dp.message_handler(state=ddoc.ddoc)
async def deldocHandler(msg: types.Message, state: FSMContext):
    try:
        db.delete_user(id=msg.text)
        await msg.answer('Test muvaffaqqiyatli o\'chirildi!', reply_markup=keyboard.menu)
    except:
        await msg.answer('Bu idga tegishli test o\'chirilgan yoki mavjud emas')
    await state.reset_state(with_data=False)


@dp.message_handler(text='/all', chat_id=5514648928)
async def count(msg: types.Message):
    await msg.answer(db.count_users())


@dp.message_handler(text='Test Yaratish')
async def createHandler(msg: types.Message):
    await msg.answer(text='Bu bo\'limdan faqat Ustozlar foydalana oladi!')
    await msg.delete()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
