import pytest
from app.database_tools.jwt_token import create_access_token

@pytest.mark.anyio
async def test_change_folder_success(client):
    await client.post(
        "/api/user/1",
        json={
            "user_name": "owner",
            "is_admin": False,
            "time_zone": "Asia/Almaty"
        }
    )

    token = await create_access_token(data={"sub": "1"})

    folder_response = await client.post(
        "/api/folders",
        json={
            "name": "Old Folder"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    folder_id = folder_response.json()["folder_id"]

    response = await client.put(
        f"/api/folders/{folder_id}",
        json={
            "new_folder_name": "New Folder"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "success"
    assert data["new_folder_name"] == "New Folder"

@pytest.mark.anyio
async def test_change_folder_not_found(client):
    token = await create_access_token(data={"sub": "1"})
    response = await client.put(
        "/api/folders/999",
        json={
            "folder_id": 999,
            "new_folder_name": "New Folder"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Папка не найдена!"

@pytest.mark.anyio
async def test_change_folder_forbidden(client):
    await client.post(
        "/api/user/1",
        json={
            "user_name": "owner",
            "is_admin": False,
            "time_zone": "Asia/Almaty"
        }
    )
    
    await client.post(
        "/api/user/2",
        json={
            "user_name": "another_user",
            "is_admin": False,
            "time_zone": "Asia/Almaty"
        }
    )

    token_1 = await create_access_token(data={"sub": "1"})
    
    folder_response = await client.post(
        "/api/folders",
        json={
            "name": "Private Folder"
        },
        headers={"Authorization": f"Bearer {token_1}"}
    )
    
    folder_id = folder_response.json()["folder_id"]

    token_2 = await create_access_token(data={"sub": "2"})

    response = await client.put(
        f"/api/folders/{folder_id}",
        json={
            "new_folder_name": "Hack Folder"
        },
        headers={"Authorization": f"Bearer {token_2}"} 
    )
    
    assert response.status_code == 403

@pytest.mark.anyio
async def test_delete_folder_success(client):
    await client.post(
        "/api/user/1",
        json={
            "user_name": "owner",
            "is_admin": False,
            "time_zone": "Asia/Almaty"
        }
    )

    token = await create_access_token(
        data={"sub": "1"}
    )

    folder_response = await client.post(
        "/api/folders",
        json={
            "name": "Delete Folder"
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert folder_response.status_code == 200

    folder_id = folder_response.json()["folder_id"]

    response = await client.delete(
        f"/api/folders/{folder_id}",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "success"


@pytest.mark.anyio
async def test_delete_folder_not_found(client):
    token = await create_access_token(data={"sub": "1"})
    response = await client.request(
        "DELETE",
        "/api/folders/999",
        json={
            "folder_id": 999,
            "user_id": 1
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Папка не найдена!"

@pytest.mark.anyio
async def test_delete_folder_forbidden(client):
    await client.post(
        "/api/user/1",
        json={
            "user_name": "owner",
            "is_admin": False,
            "time_zone": "Asia/Almaty"
        }
    )

    await client.post(
        "/api/user/2",
        json={
            "user_name": "another_user",
            "is_admin": False,
            "time_zone": "Asia/Almaty"
        }
    )
    token_1 = await create_access_token(data={"sub": "1"})

    folder_response = await client.post(
        "/api/folders",
        json={
            "name": "Private Folder",
        },
        headers={"Authorization": f"Bearer {token_1}"}
    )

    folder_id = folder_response.json()["folder_id"]

    token_2 = await create_access_token(data={"sub": "2"})

    response = await client.request(
        "DELETE",
        f"/api/folders/{folder_id}",
        json={
            "folder_id": folder_id,
        },
        headers={"Authorization": f"Bearer {token_2}"}
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "У вас нет прав на удаление этой папки!"