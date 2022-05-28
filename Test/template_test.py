import json


def test_create_template(client, token):
    """
    Tests template creation endpoint
    """

    data = {
        "template_name": "temp_test",
        "subject": "testing",
        "body": "testing the api",
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token[0]}",
    }
    response = client.post("/api/v1/template", headers=headers, data=json.dumps(data))
    assert response.status_code == 201
    response = json.loads(response.get_data(as_text=True))
    assert "success" == response["status"]


def test_get_templates(client, token, default_template):
    """
    Tests template fetching endpoint
    """

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token[0]}",
    }
    response = client.get("/api/v1/template", headers=headers)
    assert response.status_code == 200
    response = json.loads(response.get_data(as_text=True))
    assert "success" == response["status"]
    assert len(response["templates"]) == 1


def test_get_template(client, token, default_template):
    """
    Tests single template fetching endpoint
    """

    temp_id = default_template[0]
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token[0]}",
    }
    response = client.get(f"/api/v1/template/{temp_id}", headers=headers)
    assert response.status_code == 200
    response = json.loads(response.get_data(as_text=True))
    assert "success" == response["status"]


def test_unpermitted_template(client, token, default_template):
    """
    Tests single template fetching endpoint for unauthorized
    """

    temp_id = default_template[1]
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token[0]}",
    }
    response = client.get(f"/api/v1/template/{temp_id}", headers=headers)
    assert response.status_code == 403
    response = json.loads(response.get_data(as_text=True))
    assert "failed" == response["status"]


def test_put_template(client, token, default_template):
    """
    Tests template update endpoint
    """

    temp_id = default_template[0]
    data = {
        "template_name": "temporary_test",
        "subject": "testing101",
        "body": "testing the api",
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token[0]}",
    }
    response = client.put(
        f"/api/v1/template/{temp_id}", headers=headers, data=json.dumps(data)
    )
    assert response.status_code == 200
    response = json.loads(response.get_data(as_text=True))
    assert "success" == response["status"]


def test_delete_template(client, token, default_template):
    """
    Tests template deletion endpoint
    """

    temp_id = default_template[0]
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token[0]}",
    }
    response = client.delete(f"/api/v1/template/{temp_id}", headers=headers)
    assert response.status_code == 200
    response = json.loads(response.get_data(as_text=True))
    assert "success" == response["status"]
