from io import BytesIO
from unittest.mock import patch
import pytest

from app.database_tools.jwt_token import create_access_token


@pytest.mark.anyio
@patch("cloudinary.uploader.upload")
async def test_get_photo_success(mock_upload, client):

    mock_upload.return_value = {
        "secure_url": "https://cloudinary.com/test.jpg"
    }

    await client.post(
        "/api/user/1",
        json={
            "user_name": "photo_owner",
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
            "name": "Photo Folder"
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert folder_response.status_code == 200

    folder_id = folder_response.json()["folder_id"]

    photo_response = await client.post(
        "/api/photos",
        data={
            "folder_id": str(folder_id)
        },
        files={
            "file": (
                "test.jpg",
                BytesIO(b"fake image content"),
                "image/jpeg"
            )
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert photo_response.status_code == 200

    photo_id = photo_response.json()["photo_id"]

    response = await client.get(
        f"/api/photos/{photo_id}",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "success"
    assert data["photo_id"] == photo_id
    assert data["folder_id"] == folder_id
    assert data["file_path"] == "https://cloudinary.com/test.jpg"

@pytest.mark.anyio
async def test_get_photo_not_found(client):
    await client.post(
        "/api/user/1",
        json={
            "user_name": "photo_owner",
            "is_admin": False,
            "time_zone": "Asia/Almaty"
        }
    )
    token = await create_access_token(data={"sub": "1"})

    response = await client.get(
        "/api/photos/99999",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Фото не найдено!"

@pytest.mark.anyio
@patch("cloudinary.uploader.upload")
async def test_delete_photo_success(mock_upload, client):

    mock_upload.return_value = {
        "secure_url": "https://cloudinary.com/test.jpg"
    }

    await client.post(
        "/api/user/1",
        json={
            "user_name": "photo_owner",
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

    folder_id = folder_response.json()["folder_id"]

    photo_response = await client.post(
        "/api/photos",
        data={
            "folder_id": str(folder_id)
        },
        files={
            "file": (
                "test.jpg",
                BytesIO(b"fake image"),
                "image/jpeg"
            )
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    photo_id = photo_response.json()["photo_id"]

    response = await client.delete(
        f"/api/photos/{photo_id}",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "success"
    assert data["photo_id"] == photo_id

from io import BytesIO
from unittest.mock import patch


@pytest.mark.anyio
@patch("cloudinary.uploader.upload")
async def test_delete_photo_then_get_404(mock_upload, client):

    mock_upload.return_value = {
        "secure_url": "https://cloudinary.com/test.jpg"
    }

    await client.post(
        "/api/user/1",
        json={
            "user_name": "photo_owner",
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

    folder_id = folder_response.json()["folder_id"]

    photo_response = await client.post(
        "/api/photos",
        data={
            "folder_id": str(folder_id)
        },
        files={
            "file": (
                "test.jpg",
                BytesIO(b"fake image"),
                "image/jpeg"
            )
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    photo_id = photo_response.json()["photo_id"]

    delete_response = await client.delete(
        f"/api/photos/{photo_id}",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert delete_response.status_code == 200

    response = await client.get(
        f"/api/photos/{photo_id}",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 404

@pytest.mark.anyio
async def test_delete_photo_not_found(client):
    await client.post(
        "/api/user/1",
        json={
            "user_name": "photo_owner",
            "is_admin": False,
            "time_zone": "Asia/Almaty"
        }
    )
    token = await create_access_token(data={"sub": "1"})

    response = await client.delete(
        "/api/photos/99999",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Фото не найдено!"