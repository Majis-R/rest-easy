import asyncio
import getpass
from app.core.database import async_session_maker
from app.modules.account_auth.models import User
from app.modules.account_auth.services import get_password_hash, get_user_by_username

async def create_superuser():
    print("--- Create Admin Account ---")
    username = input("Enter admin username: ")
    password = getpass.getpass("Enter admin password: ")
    confirm_password = getpass.getpass("Confirm admin password: ")

    if password != confirm_password:
        print("Error: Passwords do not match.")
        return

    #TODO Uncomment to enforce admin pass length
    #if len(password) < 8:
    #    print("Error: Password must be at least 8 characters long.")
    #    return

    async with async_session_maker() as db:
        existing_user = await get_user_by_username(db, username)
        if existing_user:
            print(f"Error: User '{username}' already exists.")
            return
        
        hashed_password = get_password_hash(password)
        admin_user = User(
            username=username,
            hashed_password=hashed_password,
            role="admin"
        )
        db.add(admin_user)
        await db.commit()
        print(f"Success: Admin user '{username}' created successfully.")

if __name__ == "__main__":
    asyncio.run(create_superuser())