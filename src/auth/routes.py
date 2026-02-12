from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from src.auth.utils import create_access_token, verify_password
from src.db.main import get_session
from .schemas import UserCreateModel, UserModel, UserLoginModel
from src.auth.service import UserService
from fastapi.exceptions import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from datetime import timedelta, datetime
from .dependencies import AccessTokenBearer, RefreshTokenBearer
from src.db.redis import add_jti_to_blocklist

REFRESH_TOKEN_EXIPRY = 7


auth_router = APIRouter()
user_service = UserService()


@auth_router.post(
    "/signup", status_code=status.HTTP_201_CREATED, response_model=UserModel
)
async def create_user_account(
    user_data: UserCreateModel, session: AsyncSession = Depends(get_session)
):
    email = user_data.email
    user_exists = await user_service.user_exists(email, session)
    if user_exists:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User with this email already exists",
        )

    new_user = await user_service.create_user(user_data, session)

    return new_user


@auth_router.post("/login")
async def login_users(
    login_data: UserLoginModel, session: AsyncSession = Depends(get_session)
):
    email = login_data.email
    password = login_data.password

    user = await user_service.get_user_by_email(email, session)
    if user is not None:
        password_vaild = verify_password(password, user.password_hash)

        if password_vaild:
            access_token = create_access_token(
                user_data={"email": user.email, "user_uid": str(user.uid)}
            )

            refresh_token = create_access_token(
                user_data={"email": user.email, "user_uid": str(user.uid)},
                refresh=True,
                expiry=timedelta(days=REFRESH_TOKEN_EXIPRY),
            )

            return JSONResponse(
                content={
                    "message": "Login successful",
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "user": {"email": user.email, "uid": str(user.uid)},
                }
            )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Email or Password"
        )


@auth_router.post("/refresh_token")
async def get_new_access_token(token_details: dict = Depends(RefreshTokenBearer())):
    expiry_timestamp = token_details["exp"]
    if datetime.fromtimestamp(expiry_timestamp) > datetime.now():
        new_access_token = create_access_token(user_data=token_details["user"])
        return JSONResponse(
            content={
                "message": "New access token generated successfully",
                "access_token": new_access_token,
            }
        )
    print(expiry_timestamp)

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Invalid or expired refresh token",
    )


@auth_router.post("/logout")
async def revoke_token(token_details: dict = Depends(AccessTokenBearer())):
    jti = token_details["jti"]
    await add_jti_to_blocklist(jti)

    return JSONResponse(
        content={"message": "Logout successful. Token has been revoked."},
        status_code=status.HTTP_200_OK,
    )
