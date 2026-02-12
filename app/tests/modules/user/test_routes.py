import pytest

from app.modules.user.models import User

# @pytest.mark.anyio
# async def test_get_user(async_client, user):
#     response = await async_client.get(f"/users")
#     assert response.status_code == 200

#     response = response.json()

#     assert response["id"] == user.id
#     assert response["email"] == user.email
#     assert response["full_name"] == user.full_name
#     assert response["is_superuser"] is False


@pytest.mark.anyio
async def test_delete_user(async_client, async_session, user):
    user_id = user.id

    response = await async_client.delete(f"/users/")
    assert response.status_code == 200

    response = response.json()

    assert response["id"] == user_id

    async_session.expire_all()

    deleted_user = await async_session.get(User, user_id)

    assert deleted_user is not None
    assert deleted_user.is_active is False
    assert deleted_user.deleted_at is not None


@pytest.mark.anyio
async def test_create_user(async_client):
    response = await async_client.post(
        "/users/",
        json={
            "full_name": "Test User",
            "email": "tester@example.com",
            "password": "password12335",
        },
    )

    assert response.status_code == 201

    response = response.json()

    assert response["email"] == "tester@example.com"
    assert response["full_name"] == "Test User"

    assert "id" in response.keys()


@pytest.mark.anyio
async def test_update_user(async_client, user):
    user_id = user.id

    assert user.full_name != "Updated Name"
    assert user.email != "updated@email.com"

    response = await async_client.put(
        f"/users/",
        json={"full_name": "Updated Name", "email": "updated@email.com"},
    )

    assert response.status_code == 200

    response = response.json()

    assert response["id"] == user_id
    assert response["full_name"] == "Updated Name"
    assert response["email"] == "updated@email.com"
