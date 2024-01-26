import asyncio

from aiogram import Router
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from db.queries import create_user
from states.states import UserStates
from utils import parsing

router = Router()


@router.message(CommandStart())
async def process_start(message: Message, state: FSMContext):
    await message.answer("Введите имя")
    await state.set_state(UserStates.ask_name)


@router.message(StateFilter(UserStates.ask_name))
async def enter_name(message: Message, state: FSMContext):
    name = message.text
    # save to db
    await create_user(message.from_user.id, name)
    await state.set_state(UserStates.main_menu)
    await message.answer("Теперь вы можете ввести ссылку для парсинга")


@router.message(StateFilter(UserStates.main_menu))
async def parse_link(message: Message, state: FSMContext):
    parse_link = message.text
    await message.answer("Ждите ответа")
    asyncio.create_task(parsing.parse_and_send_file(parse_link, message))
