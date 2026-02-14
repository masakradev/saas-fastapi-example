from fastapi import APIRouter, Depends

from app.core.deps import AccountDep, UserAccountDep

router = APIRouter(tags=["membership"], prefix="/c/{company_id}/memberships")


@router.get("/")
async def get_memberships(account: AccountDep):
    """Get all memberships for a company."""
    return {"message": f"Get all memberships for company {account.company}"}


@router.delete("/{id}")
async def delete_membership(id: int, account: AccountDep):
    """Delete a membership."""
    return {"message": f"Delete a membership {id} for company {account.company}"}


@router.get("/invites")
async def get_invites(account: AccountDep):
    """Get all invites for a company."""
    return {"message": f"Get all invites for company {account.company}"}


@router.get("/invites/{id}")
async def get_invite(id: int, account: AccountDep):
    """Get a membership invite."""
    return {"message": f"Get a membership invite {id} for company {account.company}"}


@router.post("/invites")
async def invite_member(email: str, account: AccountDep):
    """Invite a member to a company."""
    return {"message": f"Invite {email} to company {account.company}"}


@router.put("/invites/{id}")
async def update_invite(id: int, account: AccountDep):
    """Update invite."""
    return {"message": f"Update invite {id} for company {account.company}"}


@router.delete("/invites/{id}")
async def delete_invite(id: int, account: AccountDep):
    """Delete invite."""
    return {"message": f"Delete invite {id} for company {account.company}"}


@router.post("/accept-invite/{id}")
async def accept_invite(id: int, account: UserAccountDep):
    """Accept invite."""
    return {"message": f"Accept invite {id} for user {account.user}"}
