
    
def test_create_item(test_client):
    response = test_client.post("/items/add_item", json={"name": "TestItem", "value":100})
    assert response.status_code == 200
    assert response.json()["name"] == "TestItem"
    assert response.json()["value"] == 100

def test_get_items(test_client):
    response = test_client.get("/items/")
    assert response.status_code == 200
     
def test_get_item(test_client):
    response = test_client.get("/items/get_item", params={"item_id": 1})
    print(f"response is {response.json()}")
    assert response.status_code == 200
    assert response.json()["name"] == "TestItem"
    assert response.json()["value"] == 100
    
def test_update_item(test_client):
    response = test_client.put("/items/update_item", params={"item_id": 1}, json={ "name": "UpdatedItem", "value":200})
    assert response.status_code == 200
    assert response.json()["name"] == "UpdatedItem"
    assert response.json()["value"] == 200

def test_delete_item(test_client):
    response = test_client.delete("/items/delete_item", params={"item_id":1})
    assert response.status_code == 200
    assert response.json()["name"] == "UpdatedItem"
    assert response.json()["value"] == 200
