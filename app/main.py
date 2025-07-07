from fastapi import FastAPI, HTTPException
from app import models, schemas, security, database

app = FastAPI()

@app.post("/register")
async def register(user: schemas.UserCreate):
    existing_email = await models.User.filter(email=user.email).first()
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    existing_username = await models.User.filter(username=user.username).first()
    if existing_username:
        raise HTTPException(status_code=400, detail="Username already taken")
    
    hashed_pw = security.hash_password(user.password)
    new_user = await models.User.create(
        email=user.email,
        username=user.username,
        password_hash=hashed_pw
    )
    return {"msg": "User created", "email": new_user.email, "username": new_user.username}

@app.post("/login")
async def login(user: schemas.UserLogin):
    db_user = await models.User.filter(email=user.email).first()
    if not db_user or not security.verify_password(user.password, db_user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"msg": "Login successful", "email": db_user.email, "username": db_user.username}

database.init_db(app)
