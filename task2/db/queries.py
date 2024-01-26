from .conn import AsyncSession
from .models import User


async def create_user(user_id, user_name):
    try:
        async with AsyncSession() as session:
            user = User(user_id=user_id, user_name=user_name)
            session.add(user)
            await session.commit()
    except Exception as e:
        print(e)
