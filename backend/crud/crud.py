# here all the CRUD(Db logic) operations will be defined, and then imported into the main.py file to be used in the API endpoints
# sqlalchemy imports
from sqlalchemy.exc import SQLAlchemyError, OperationalError
from sqlalchemy.orm import Session
# files imports
from models.models import GroupMembers, User, RefreshToken, Group
from schemas.auth_schemas import UserRegister, UserEmail, PasswordUpdate, UserLogin, VerifyOtp
from schemas.classroom_schemas import CreateClassroom, JoinClassroom
from utils.otp import generate_totp, generate_secret, verify_totp

# other imports
from pwdlib import PasswordHash
from datetime import  timedelta, timezone, datetime
import jwt

password_hash = PasswordHash.recommended() # creating a password hashing object 

def register_user(db: Session, user_data: UserRegister):
    # 1. Check if user already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        return None, "User with this email already exists."
    
    # 2. Hash the password
    hashed_password = password_hash.hash(user_data.password)
    
    # 3. Create new user object
    new_user = User(
        name=user_data.name,
        email=user_data.email,
        admin_secret_key= user_data.admin_secret_key , 
        password=hashed_password,
        otp_secret=generate_secret()  # Generate a unique OTP secret for the user
    )
    
    # 4. Save to database
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user, None
    except SQLAlchemyError as e:
        db.rollback()
        return None, str(e)
    

def login_user(db: Session, login_data: UserLogin):
    # 1. Fetch user
    user = db.query(User).filter(User.email == login_data.email).first()
    if not user:
        return None
    print(f"User {user.email} found in database.")
    # 2. Verify password
    if not password_hash.verify(login_data.password, user.password):
        return None
    print(f"Password for user {user.email} verified successfully.")
    
    # 3. Update modified_at (last login)
    try:
        print(f"User {user.email} logged in successfully.")
        user.modified_at = datetime.now(timezone.utc)
        db.commit()
        db.refresh(user)
        return user
    except SQLAlchemyError as e:
        db.rollback()
        return None, str(e) 
    


def logout_user(db: Session, email: UserEmail):
    user = db.query(User).filter(User.email == email.email).first()
    if not user:
        return None, "User not found."
    
    user.modified_at = datetime.now(timezone.utc) # update last login time
    try:
        db.commit() # save changes to database
        db.refresh(user)
        return user, None
    except SQLAlchemyError as e:
        db.rollback()
        return None, str(e)

def update_password(db: Session, data: PasswordUpdate):
    user = db.query(User).filter(User.email == data.email).first()
    if not user:
        return None, "User not found."
    
    user.password = password_hash.hash(data.new_password)
    user.modified_at = datetime.cnow(timezone.utc)
    valid_otp = verify_totp(user_input= data.otp, secret= user.otp_secret)
    if valid_otp: 
        user.password =  password_hash.hash(data.new_password)
        db.commit()
        db.refresh(user)
    
    try:
        db.commit()
        db.refresh(user)
        return user, None
    except SQLAlchemyError as e:
        db.rollback()
        return None, str(e)

def create_token_entry(db: Session, user_id: int, permanent_token: str, access_token: str):
    # Logic to save the token in your new refresh_tokens table
    # (As we discussed in the previous step)
    refresh_token = RefreshToken(
        permanent_token=permanent_token,
        access_token=access_token, 
        user_id=user_id,
        expires_at=datetime.now(timezone.utc) + timedelta(days=7) # Set expiry as needed
        )
    
    db.add(refresh_token)
    db.commit()
    db.refresh(refresh_token)
    return refresh_token


def create_classroom(db: Session, classroom_data: CreateClassroom):
    """ Logic to create a new classroom entry in the database """
    # Assuming classroom_data contains 'name' and 'code'
    user = db.query(RefreshToken).filter(RefreshToken.access_token == classroom_data.token_id).first()
    if not user:
        return None
    

    try:
       # 1. Create classroom first
        new_classroom = Group(
            group_name=classroom_data.name,
            class_code=classroom_data.code,
            owner_id=user.user_id,
            created_at=datetime.now(timezone.utc)
        )
        db.add(new_classroom)
        db.commit()
        db.refresh(new_classroom)  # now new_classroom.id is available

        # 2. Now add teacher as member
        teacher_member = GroupMembers(
            group_id=new_classroom.id,  # ← id is valid now
            user_id=user.user_id,
            joined_at=datetime.now(timezone.utc)
        )
        db.add(teacher_member)
        db.commit()

        return new_classroom, None

    except SQLAlchemyError as e:
        db.rollback()
        return None, str(e)


def join_classroom(db: Session, classroom_data: JoinClassroom):
    """ Logic to create a new classroom entry in the database """
    user = db.query(RefreshToken).filter(RefreshToken.access_token == classroom_data.token_id).first()
    if not user:
        return None, "user not found"

    classroom = db.query(Group).filter(Group.class_code == classroom_data.code).first()
    if not classroom:
        return None, "Classroom not found"
    
    # Check if user is the owner
    if classroom.owner_id == user.user_id:
        return None, "You are the owner of this classroom"

    # Check if user is already a member of the classroom
    group_member = db.query(GroupMembers).filter(GroupMembers.user_id == user.user_id, GroupMembers.group_id == classroom.id).first()

    if group_member:
        return None, "User is already a member of this classroom"

    try:
        new_group_member = GroupMembers(
            user_id=user.user_id,
            group_id=classroom.id,
            joined_at=datetime.now(timezone.utc)
        )
        db.add(new_group_member)
        db.commit()
        db.refresh(new_group_member)
        return new_group_member, None
    
    except SQLAlchemyError as e:
        db.rollback()
        return None, str(e)   

    