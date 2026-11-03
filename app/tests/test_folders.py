from app.database_tools.jwt_token import create_access_token
import pytest
from unittest.mock import patch

@pytest.mark.anyio
async def test_get_user_folders_success(client):
    await client.post(
        "/api/user/1",
        json={
            "user_name": "test_user",
            "is_admin": False,
            "time_zone": "Asia/Almaty"
        }
    )

    token = await create_access_token(data={"sub": "1"})

    await client.post(
        "/api/folders",
        json={
            "name": "Folder 1"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    await client.post(
        "/api/folders",
        json={
            "name": "Folder 2"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    response = await client.get(
        "/api/folders",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2
  
    assert data[0]["user_id"] == 1

@pytest.mark.anyio
async def test_get_user_folders_empty(client):
    await client.post(
        "/api/user/10",
        json={
            "user_name": "empty_user",
            "is_admin": False,
            "time_zone": "Asia/Almaty"
        }
    )
    token = await create_access_token(data={"sub": "1"})

    response = await client.get(
        "/api/folders",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert response.json() == []

@pytest.mark.anyio
@patch("cloudinary.uploader.upload")
async def test_get_folder_photos_success(mock_cloudinary_upload, client): 
    mock_cloudinary_upload.return_value = {
        "secure_url": "https://res.cloudinary.com/demo/image/upload/test.jpg"
    }

    await client.post(
        "/api/user/1",
        json={
            "user_name": "photo_user",
            "is_admin": False,
            "time_zone": "Asia/Almaty"
        }
    )

    token = await create_access_token(data={"sub": "1"})

    folder_response = await client.post(
        "/api/folders",
        json={
            "name": "Photos",
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    folder_id = folder_response.json()["folder_id"]

    await client.post(
        "/api/photos",
        data={
            "folder_id": folder_id
        },
        files={
            "file": ("test.jpg", b"fake-image-bytes", "image/jpeg")
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    response = await client.get(
        f"/api/folders/{folder_id}/photos",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["url"] == "https://res.cloudinary.com/demo/image/upload/test.jpg"

@pytest.mark.anyio
@patch("cloudinary.uploader.upload") 
async def test_get_folder_photos_empty(mock_cloudinary_upload, client):
    mock_cloudinary_upload.return_value = {
        "secure_url": "https://res.cloudinary.com/demo/image/upload/test.jpg"
    }
    await client.post(
        "/api/user/1",
        json={
            "user_name": "photo_user",
            "is_admin": False,
            "time_zone": "Asia/Almaty"
        }
    )
    token = await create_access_token(data={"sub": "1"})

    folder_response = await client.post(
        "/api/folders",
        json={
            "name": "Empty folder",
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    folder_id = folder_response.json()["folder_id"]

    response = await client.get(
        f"/api/folders/{folder_id}/photos",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.anyio
async def test_get_folder_not_found(client):
    # 1. Қолданушыны тіртейміз
    await client.post(
        "/api/user/1",
        json={
            "user_name": "test_user",
            "is_admin": False,
            "time_zone": "Asia/Almaty"
        }
    )

    token = await create_access_token(data={"sub": "1"})

    response = await client.get(
        "/api/folder/99999",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Папка не найдена!"

@pytest.mark.anyio
async def test_get_folder_forbidden(client):
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
            "user_name": "other_user",
            "is_admin": False,
            "time_zone": "Asia/Almaty"
        }
    )
    token = await create_access_token(data={"sub": "1"})
    token2 = await create_access_token(data={"sub": "2"})

    folder_response = await client.post(
        "/api/folders",
        json={
            "name": "Private Folder",
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    folder_id = folder_response.json()["folder_id"]

    response = await client.get(
        f"/api/folders/{folder_id}/photos",
        headers={"Authorization": f"Bearer {token2}"}
    )
    

    assert response.status_code == 404
    assert response.json()["detail"] == "Папка не найдена или у вас нет доступа!"