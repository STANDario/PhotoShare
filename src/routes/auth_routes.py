from fastapi import APIRouter, HTTPException, Depends, Security, status, BackgroundTasks, Request
from fastapi.security import HTTPAuthorizationCredentials, OAuth2PasswordRequestForm, HTTPBearer
from sqlalchemy.orm import Session

from src.services.email_service import send_email
from src.entity.models import Role
from src.database.db import get_db
from src.repository import users as repository_users
from src.schemas.user_schemas import RequestEmail, UserSchema, TokenSchema, UserResponse
from src.services.auth_service import auth_service


router = APIRouter(prefix='/auth', tags=['auth'])

get_refresh_token = HTTPBearer()


@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED, name="Create new user")
async def signup(body: UserSchema, bt: BackgroundTasks, request: Request, db: Session = Depends(get_db)):
    """
    Endpoint to sign up a new user.

    Args:
        body (UserSchema): User data.
        bt (BackgroundTasks): Background tasks.
        request (Request): Request object.
        db (Session, optional): Database session. Defaults to Depends(get_db).

    Returns:
        UserResponse: Created user.
    """
    num_users = await repository_users.get_total_users_count(db)
    if num_users == 0:
        body.role = Role.admin
    elif num_users == 1:
        body.role = Role.moderator
    else:
        body.role = Role.user

    exist_user = await repository_users.get_user_by_email(body.email, db)
    exist_username = await repository_users.get_user_by_username(body.username, db)

    if exist_user or exist_username:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Account is already exist")
    body.password = auth_service.get_password_hash(body.password)
    new_user = await repository_users.create_user(body, db)
    bt.add_task(send_email, new_user.email, new_user.username, str(request.base_url))

    return new_user


@router.post("/login", response_model=TokenSchema, status_code=status.HTTP_202_ACCEPTED, name="Login")
async def login(body: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Endpoint to log in a user.

    Args:
        body (OAuth2PasswordRequestForm, optional): Login form data. Defaults to Depends().
        db (Session, optional): Database session. Defaults to Depends(get_db).

    Returns:
        TokenSchema: Access and refresh tokens.
    """
    user = await repository_users.get_user_by_email(body.username, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email")
    if not user.confirmed:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Email not confirmed")

    if not auth_service.verify_password(body.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password")
    # Generate JWT
    access_token = await auth_service.create_access_token(data={"sub": user.email, "test": "My token"})  # payload
    refresh_token = await auth_service.create_refresh_token(data={"sub": user.email})
    await repository_users.update_token(user, refresh_token, db)

    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


@router.get('/refresh_token', response_model=TokenSchema, status_code=status.HTTP_202_ACCEPTED, name="Update token")
async def refresh_token(credentials: HTTPAuthorizationCredentials = Security(get_refresh_token),
                        db: Session = Depends(get_db)):
    """
    Endpoint to refresh an access token.

    Args:
        credentials (HTTPAuthorizationCredentials, optional): Token credentials. Defaults to Security(get_refresh_token).
        db (Session, optional): Database session. Defaults to Depends(get_db).

    Returns:
        TokenSchema: New access and refresh tokens.
    """

    token = credentials.credentials
    email = await auth_service.decode_refresh_token(token)
    user = await repository_users.get_user_by_email(email, db)
    if user.refresh_token != token:
        await repository_users.update_token(user=user, db=db, token=None)
        user.refresh_token = None
        db.commit()
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

    access_token = await auth_service.create_access_token(data={"sub": email})
    refresh_token = await auth_service.create_refresh_token(data={"sub": email})
    await repository_users.update_token(user, refresh_token, db)
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


@router.get('/confirmed_email/{token}', name="Email confirmation with token")
async def confirmed_email(token: str, db: Session = Depends(get_db)):
    """
    Endpoint to confirm user email using a token.

    Args:
        token (str): Confirmation token.
        db (Session, optional): Database session. Defaults to Depends(get_db).

    Returns:
        dict: Confirmation message.
    """
    email = await auth_service.get_email_from_token(token)
    user = await repository_users.get_user_by_email(email, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Verification error")
    if user.confirmed:
        return {"message": "Your email is already confirmed"}
    await repository_users.confirmed_email(email, db)
    return {"message": "Email confirmed"}


@router.post('/request_email', name="Request email confirmation")
async def request_email(body: RequestEmail, background_tasks: BackgroundTasks, request: Request,
                        db: Session = Depends(get_db)):
    """
    Endpoint to request email confirmation.

    Args:
        body (RequestEmail): Email request data.
        background_tasks (BackgroundTasks): Background tasks.
        request (Request): Request object.
        db (Session, optional): Database session. Defaults to Depends(get_db).

    Returns:
        dict: Confirmation message.
    """
    user = await repository_users.get_user_by_email(body.email, db)

    if user.confirmed:
        return {"message": "Your email is already confirmed"}
    if user:
        background_tasks.add_task(send_email, user.email, user.username, str(request.base_url))
    return {"message": "Check your email for confirmation"}
