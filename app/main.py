from fastapi import FastAPI, HTTPException, APIRouter
from app.models import User
from app.schemas import UserCreate, UserLogin, PayloadEncrypt
from app import security
from app.db import init_db
from app.security import encrypt_return_data_submit
from config import SECRET_KEY

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
    try:
        decrypted_data = security.decrypt_payload({
            "payload": user.payload,
            "nonce": user.nonce,
            "tag": user.tag
        })
        username = decrypted_data["username"]
        password = decrypted_data["password"]
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid encrypted data")

    users = await User.all()
    for u in users:
        try:
            decrypted_username = security.decrypt_text(u.username)
            if decrypted_username == username:
                if security.verify_password(password, u.password_hash):
                    return encrypt_return_data_submit({
                        "msg": "Login successful",
                        "email": u.email
                    })
        except Exception:
            continue

    raise HTTPException(status_code=404, detail="User not found")


app = FastAPI()
init_db(app)
app.include_router(router)
