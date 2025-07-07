from fastapi import APIRouter, HTTPException
from app.models import User
from app.schemas import UserCreate, UserLogin, PayloadEncrypt
from app import security
from app.security import encrypt_return_data_submit

router = APIRouter()


@router.post("/register", response_model=PayloadEncrypt)
async def register(user: UserCreate):
    if await User.filter(email=user.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    existing_users = await User.all()
    for existing_user in existing_users:
        try:
            decrypted_username = security.decrypt_text(existing_user.username)
            if decrypted_username == user.username:
                raise HTTPException(status_code=400, detail="Username already exists")
        except Exception:
            continue

    encrypted_username = security.encrypt_text(user.username)
    hashed_password = security.hash_password(user.password)

    await User.create(
        email=user.email,
        username=encrypted_username,
        password_hash=hashed_password
    )

    return encrypt_return_data_submit(user.model_dump())


@router.post("/login", response_model=PayloadEncrypt)
async def login(user: UserLogin):
    users = await User.all()

    for u in users:
        try:
            decrypted_username = security.decrypt_text(u.username)
            if decrypted_username == user.username:
                if security.verify_password(user.password, u.password_hash):
                    return encrypt_return_data_submit({
                        "msg": "Login successful",
                        "email": u.email
                    })
        except Exception:
            continue

    raise HTTPException(status_code=404, detail="User not found")
