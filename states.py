from aiogram.dispatcher.filters.state import State, StatesGroup

class User(StatesGroup):
    user_id=State()
    user_contact=State()
    main_menu = State()
    reja = State()
    reja_nomi = State()
    reja_vaqti = State()
    reja_tavsifi = State()
    reja_ajratilgan_vaqt = State()
    reja_malumoti = State()

class Admin_states(StatesGroup):
    main_menu = State()
    reklama = set()
    rozi_bolish = State()