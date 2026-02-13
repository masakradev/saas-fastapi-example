from fastapi import APIRouter

from app.modules.auth.router import router as auth_router
from app.modules.company.router import router as company_router
from app.modules.membership.router import router as membership_router
from app.modules.user.router import router as user_router

router = APIRouter()
router.include_router(auth_router, prefix="/auth")
router.include_router(user_router, prefix="/users")
router.include_router(membership_router, prefix="/memberships")
router.include_router(company_router, prefix="/companies")
