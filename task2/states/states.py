from aiogram.fsm.state import State, StatesGroup


class UserStates(StatesGroup):
    ask_name = State()
    main_menu = State()