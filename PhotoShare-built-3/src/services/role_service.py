from typing import List

from fastapi import Depends, HTTPException, status, Request

from src.entity.models import User, Role
from src.services.auth_service import auth_service


class RoleAccess:
    def __init__(self, allowed_roles: List[Role]):
        self.allowed_roles = allowed_roles

    async def __call__(
        self,
        request: Request,
        current_user: User = Depends(auth_service.get_current_user),
    ):
        if current_user.role not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Operation forbidden"
            )


all_roles = RoleAccess([Role.admin, Role.moderator, Role.user])
admin_and_moder = RoleAccess([Role.admin, Role.moderator])
only_admin = RoleAccess([Role.admin])
