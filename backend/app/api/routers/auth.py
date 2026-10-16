from fastapi import APIRouter, Depends, Response, status

from app.api.dependencies import get_auth_service, require_authenticated_account
from app.api.schemas.auth import (
    LoginRequest,
    MessageResponse,
    PasswordRecoveryRequest,
    PasswordResetRequest,
    RegisterRequest,
    UserResponse,
)
from app.application.auth_service import AuthService, AuthenticatedAccount


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(payload: RegisterRequest, service: AuthService = Depends(get_auth_service)):
    return service.register(payload.display_name, str(payload.email), payload.password)


@router.post("/login", status_code=status.HTTP_204_NO_CONTENT)
def login(payload: LoginRequest, service: AuthService = Depends(get_auth_service)) -> Response:
    token = service.login(str(payload.email), payload.password)
    response = Response(status_code=status.HTTP_204_NO_CONTENT)
    response.set_cookie(
        "access_token",
        token,
        max_age=30 * 60,
        httponly=True,
        secure=service.settings.secure_cookies,
        samesite="lax",
        path="/api",
    )
    return response


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(
    authenticated: AuthenticatedAccount = Depends(require_authenticated_account),
    service: AuthService = Depends(get_auth_service),
) -> Response:
    service.logout(authenticated)
    response = Response(status_code=status.HTTP_204_NO_CONTENT)
    response.delete_cookie("access_token", path="/api", samesite="lax")
    return response


@router.get("/me", response_model=UserResponse)
def current_user(
    authenticated: AuthenticatedAccount = Depends(require_authenticated_account),
):
    return authenticated.user


@router.post(
    "/password-recovery",
    response_model=MessageResponse,
    status_code=status.HTTP_202_ACCEPTED,
)
def request_password_recovery(
    payload: PasswordRecoveryRequest,
    service: AuthService = Depends(get_auth_service),
):
    service.request_password_recovery(str(payload.email))
    return MessageResponse(
        message="Si la cuenta existe, recibirás instrucciones para recuperar el acceso"
    )


@router.post("/password-reset", status_code=status.HTTP_204_NO_CONTENT)
def reset_password(
    payload: PasswordResetRequest,
    service: AuthService = Depends(get_auth_service),
) -> Response:
    service.reset_password(payload.token, payload.new_password)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
