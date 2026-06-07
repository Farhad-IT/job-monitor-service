from os import getenv
from aiogram import Bot,Dispatcher,Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.state import State,StatesGroup

from app.api.dependencies import get_users_repository, get_subscribe_repository
from app.db.session import AsyncSessionLocal

load_dotenv()

TOKEN = getenv('BOT_TOKEN')
bot = Bot(token=TOKEN)
dp=Dispatcher(storage=MemoryStorage())
router=Router()
dp.include_router(router)



class SubscribeState(StatesGroup):
    waiting_keyword = State()

class UnsubscribeState(StatesGroup):
    waiting_keyword = State()



@router.message(Command("start"))
async def start(message: Message):
    async with AsyncSessionLocal() as session:
        user_repository = get_users_repository(session)

        user = await user_repository.get_by_telegram_id(telegram_id=message.from_user.id)

        if not user:
            await user_repository.create_user(telegram_id=message.from_user.id)

        await session.commit()
        await message.answer("Привет! Я бот для мониторинга вакансии. Введите команду /help для помоши.")


@router.message(Command("help"))
async def helper(message: Message):
    await message.answer(
        "Команды:\n"
        "<b>/start</b>-запустить бота.\n"
        "<b>/help</b>-список команд.\n"
        "<b>/subscribe</b>-оформить подписку.\n"
        "<b>/unsubscribe</b>-отменить подписку.\n"
        "<b>/list</b>-список оформленных подписок\n"
        , parse_mode="HTML"
    )


@router.message(Command("subscribe"))
async def subscribe(message: Message, state: FSMContext):
    await state.set_state(SubscribeState.waiting_keyword)
    await message.answer("Введите название подписки")


@router.message(SubscribeState.waiting_keyword)
async def save_subscribe(message: Message, state: FSMContext):
    async with AsyncSessionLocal() as session:
        user_repository = get_users_repository(session)
        subscribe_repository = get_subscribe_repository(session)

        user = await user_repository.get_by_telegram_id(telegram_id=message.from_user.id)

        await subscribe_repository.create_subscription(user_id=user.id, keyword=message.text)

        await session.commit()
        await message.answer(f"Подписка '{message.text}' сохранена")
        await state.clear()


@router.message(Command("unsubscribe"))
async def unsubscribe(message: Message, state: FSMContext):
    await state.set_state(UnsubscribeState.waiting_keyword)
    await message.answer("Введите ID подписки")


@router.message(UnsubscribeState.waiting_keyword)
async def delete_subscribe_by_id(message: Message, state: FSMContext):
    async with AsyncSessionLocal() as session:
        user_repository = get_users_repository(session)
        subscribe_repository = get_subscribe_repository(session)

        user = await user_repository.get_by_telegram_id(telegram_id=message.from_user.id)

        try:
            await subscribe_repository.delete_subscription(subscription_id=int(message.text), user_id=user.id)
        except ValueError:
            await message.answer("Введите корректный ID подписки")
            return

        await session.commit()
        await message.answer(f"Подписка '{message.text}' отменена")
        await state.clear()


@router.message(Command("list"))
async def show_subscriptions(message: Message):
    async with AsyncSessionLocal() as session:
        user_repository = get_users_repository(session)
        subscribe_repository = get_subscribe_repository(session)

        user = await user_repository.get_by_telegram_id(telegram_id=message.from_user.id)

        subscriptions = await subscribe_repository.get_subscriptions(user_id=user.id)

        if not subscriptions:
            await message.answer("Подписок нет.")
            return

        text = "Ваши подписки:\n\n"

        for sub in subscriptions:
            text += (
                f"ID: {sub.id} | "
                f"{sub.keyword}\n"
            )

        await message.answer(text)


#async def main():
#    await dp.start_polling(bot)


#if __name__ == '__main__':
#    asyncio.run(main())