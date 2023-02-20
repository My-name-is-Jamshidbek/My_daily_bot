from datetime import datetime
from aiogram import types
from loader import dp
from config import ADMIN_ID
from aiogram.dispatcher.filters import CommandStart, CommandHelp
from loader import bot
from aiogram.dispatcher import FSMContext
from buttons.keyboardbuttons import *                                                          
from buttons.inlinekeyboardbuttons import *
from database.database import *
from states import *

#start
@dp.message_handler(CommandStart())
async def start(message:types.Message):
    if str(message.from_user.id) == str(ADMIN_ID):
        await message.answer('salomadmin botga hush kelibsiz!', reply_markup=keyboard_admin_menu_1, )
        await Admin_states.main_menu.set()
    else:
        await message.answer(f"Salom {message.from_user.full_name} botga hush kelibsiz!\nBot ishlashi uchun "
                             f"kontaktingizni ulashing!!",reply_markup=keyboard_kontakt)
        await User.user_contact.set()

# Admin
@dp.message_handler(state=Admin_states.main_menu, content_types=types.ContentType.TEXT)
async def admin_main_menu(message:types.Message, state:FSMContext):
    if "Reklama" == message.text:
        await message.answer("Reklama habarni kiriting:")
        await Admin_states.reklama.set()
    elif "Foydalanuvchilar" == message.text:
        await message.answer(text=f"Foydalanuvchilar soni: {count_users()}")


@dp.message_handler(state = Admin_states.reklama, content_types=types.ContentType.TEXT)
async def admin_reklama(message:types.Message, state:FSMContext):
    await state.update_data(reklam = message.text)
    await message.answer("Habarni tasdiqlang!",reply_markup=keyboard_admin_rozibolish)
    await Admin_states.rozi_bolish.set()

@dp.message_handler(state = Admin_states.rozi_bolish, content_types=types.ContentType.TEXT)
async def admin_rozi_bolishi(message:types.Message, state:FSMContext):
    if message.text == "Tasdiqlash":
        ids = get_all_telegram_ids()
        n = 0
        for i in ids:
            try:
                await bot.send_message(chat_id = i,text = 'text')
                n+=1
            except:
                pass
        await message.answer(f"Reklama jo'natildi foydalanuvchilar soni: {n}",reply_markup=keyboard_admin_menu_1)
        await Admin_states.main_menu.set()

#royxatdan otish
@dp.message_handler(state=User.user_contact,content_types=types.ContentType.CONTACT)
async def sendcontact(message:types.Message,state:FSMContext):
    try:
        ba = message.values
        full_name = message.contact.full_name
        user_id = message.from_user.id
        tel_number = message.contact.phone_number
        add_user(tel_number,user_id,)
        # await state.finish()
        await bot.send_message(user_id,text='Tabriklayman siz muvaffaqiyatli ro\'yxatdan o\'tdingiz',
                               reply_markup=keyboard_user_menu_1)
        await User.main_menu.set()
    except:
        await state.finish()
        await bot.send_message(user_id, text='Tabriklayman siz muvaffaqiyatli ro\'yxatdan o\'tmadingiz',
                               reply_markup=keyboard_kontakt)

#users
@dp.message_handler(state = User.main_menu, content_types=[types.ContentType.TEXT,types.ContentType.CONTACT])
async def uthers_main_menu(message:types.Message, state:FSMContext):
    if message.text == "👨‍💻Dasturchi malumoti👨‍💻":
        await message.answer("Dasturchi malumoti")
    elif message.text == "Reja qo\'shish":
        await message.answer("Kunni tanlang:",reply_markup=get_week_menu())
        await state.update_data(main_menu = 'qoshish')
        await User.reja.set()
    elif message.text == "Rejalar":
        await message.answer("Kunni tanlang:",reply_markup=get_week_menu())
        await state.update_data(main_menu = 'korish')
        await User.reja.set()

#menyu
@dp.message_handler(state=User.reja, content_types=[types.ContentType.TEXT])
async def uthers_reja(m:types.Message,state:FSMContext):
    data = await state.get_data()
    reja = data.get("main_menu")
    if m.text == "Chiqish":
        await m.answer("Chiqildi.",reply_markup=keyboard_user_menu_1)
        await User.main_menu.set()
    elif reja == "qoshish":
        t,year,month,day = get_date_by_day_of_week(m.text.split()[0])
        if t:
            await m.answer("reja nomini kiriting:",reply_markup=get_btn(['Bekor qilish']))
            await state.update_data(reja = f"{year}_{month}_{day}")
            await User.reja_nomi.set()
    elif reja == "korish":
        t,year,month,day = get_date_by_day_of_week(m.text.split()[0])
        if t:
            btns = get_rejalarni_korish(yil=year,oy=month,kun=day, telegram_id=m.from_user.id)
            btns.append("Chiqish")
            await m.answer("Rejalar:",reply_markup=get_btn(btns))
            await state.update_data(reja = f"{year}_{month}_{day}")
            await User.reja_malumoti.set()


@dp.message_handler(state=User.reja_nomi,content_types=types.ContentType.TEXT)
async def user_reja_nomi(m:types.Message,state:FSMContext):
    if m.text == 'Bekor qilish':
        await m.answer("Bekor qilindi")
        await m.answer("Kunni tanlang:", reply_markup=get_week_menu())
        await User.reja.set()
    else:
        await m.answer("Reja haqida batafsil malumot kiriting:")
        await state.update_data(reja_nomi = m.text)
        await User.reja_tavsifi.set()



@dp.message_handler(state=User.reja_tavsifi,content_types=types.ContentType.TEXT)
async def user_reja_tavsifi(m:types.Message,state:FSMContext):
    if m.text == 'Bekor qilish':
        await m.answer("Bekor qilindi")
        await m.answer("Kunni tanlang:", reply_markup=get_week_menu())
        await User.reja.set()
    else:
        await m.answer("Reja boshlanadigan vaqtni kiriting kiriting:\nMasalan: 12:45")
        await state.update_data(reja_tavsifi = m.text)
        await User.reja_vaqti.set()


@dp.message_handler(state=User.reja_vaqti,content_types=types.ContentType.TEXT)
async def user_reja_vaqti(m:types.Message,state:FSMContext):
    if m.text == 'Bekor qilish':
        await m.answer("Bekor qilindi")
        await m.answer("Kunni tanlang:", reply_markup=get_week_menu())
        await User.reja.set()
    else:
        await m.answer("Rejaga ajratilgan vaqtni kiriting kiriting:\nMasalan: 1:45")
        await state.update_data(reja_vaqti = m.text)
        await User.reja_ajratilgan_vaqt.set()


@dp.message_handler(state=User.reja_ajratilgan_vaqt,content_types=types.ContentType.TEXT)
async def user_reja_ajratilgan_vaqt(m:types.Message,state:FSMContext):
    if m.text == 'Bekor qilish':
        await m.answer("Bekor qilindi")
        await m.answer("Kunni tanlang:", reply_markup=get_week_menu())
        await User.reja.set()
    else:
        data = await state.get_data()
        year, month, day = str(data.get("reja")).split("_")
        try:
            add_reja(
                telegram_id=m.from_user.id,
                reja_nomi=data.get('reja_nomi'),
                reja_tavsifi=data.get("reja_tavsifi"),
                reja_mojallangan_vaqt=f"{year}_{month}_{day}_{data.get('reja_vaqti')}",
                ajratilgan_vaqt=m.text,
                yil=year,
                oy=month,
                kun=day,
                soat=data.get('reja_vaqti').split(':')[0],
                daqiqa=data.get('reja_vaqti').split(':')[1]
            )
            t = True
        except:
            t = False
        if t:
            await m.answer("Reja muvaffaqiyatli qo'shildi.")
        else:
            await m.answer("Kiritilgan malumotlarni kiritishni iloji bo'lmadi iltimos tekshirib qaytadan kiriting!")
        await m.answer("Kunni tanlang:", reply_markup=get_week_menu())
        await User.reja.set()


@dp.message_handler(state=User.reja_malumoti, content_types=types.ContentType.TEXT)
async def users_reja_malumoti(m:types.Message,state:FSMContext):
    data = await state.get_data()
    year,month,day = str(data.get("reja")).split("_")
    btns = get_rejalarni_korish(yil=year, oy=month, kun=day, telegram_id=m.from_user.id)
    if m.text == "Chiqish":
        await m.answer("Kunni tanlang:", reply_markup=get_week_menu())
        await User.reja.set()
    elif m.text in btns:
        data = get_reja_malumotlari(
            yil=year,
            oy=month,
            kun=day,
            reja_nomi=m.text,
            telegram_id=m.from_user.id
        )
        await m.answer(text = f"Reja nomi: {data[0]}\nTavsif: {data[1]}\nSana: {data[2].split('_')[0]}-"
                              f"{data[2].split('_')[1]}-{data[2].split('_')[2]} {data[2].split('_')[3]}\nAjratilgan "
                              f"vaqt: {data[3].split(':')[0]} soat {data[3].split(':')[1]} daqiqa"
        )