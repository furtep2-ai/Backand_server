import pytest
from app.database_tools.jwt_token import create_access_token

@pytest.mark.anyio
async def test_create_folder_success(client):
    await client.post(
        "/api/user/1",
        json={
            "user_name": "folder_owner",
            "is_admin": False,
            "time_zone": "Asia/Almaty"
        }
    )
    
    token = await create_access_token(data={"sub": "1"}) 
    
    response = await client.post(
        "/api/folders",
        json={
            "name": "My Folder"},
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Папка успешно создана!"

from unittest.mock import patch

@pytest.mark.anyio
@patch("cloudinary.uploader.upload") 
async def test_add_photo_success(mock_cloudinary_upload, client):
    mock_cloudinary_upload.return_value = {
        "secure_url": "https://res.cloudinary.com/demo/image/upload/test.jpg"
    }

    await client.post(
        "/api/user/1",
        json={
            "user_name": "photo_owner",
            "is_admin": False,
            "time_zone": "Asia/Almaty"
        }
    )
    
    token = await create_access_token(data={"sub": "1"})
    
    folder_response = await client.post(
        "/api/folders",
        json={
            "name": "Photos"
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    
    folder_id = folder_response.json()["folder_id"]
    
    response = await client.post(
        "/api/photos",
        data={
            "folder_id": folder_id
        },
        files={
            "file": ("test.jpg", b"fake-image-bytes", "image/jpeg")
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["image_url"] == "https://res.cloudinary.com/demo/image/upload/test.jpg"

@pytest.mark.anyio
@patch("cloudinary.uploader.upload")
async def test_add_photo_folder_not_found(mock_cloudinary_upload, client):
    # 1. Қолданушыны тіртейміз
    await client.post(
        "/api/user/1",
        json={
            "user_name": "photo_owner",
            "is_admin": False,
            "time_zone": "Asia/Almaty"
        }
    )

    token = await create_access_token(data={"sub": "1"})

    response = await client.post(
        "/api/photos",
        data={
            "folder_id": 99999
        },
        files={
            "file": ("test.jpg", b"fake-image-bytes", "image/jpeg")
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 404
