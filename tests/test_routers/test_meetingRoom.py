
import pytest
from fastapi.testclient import TestClient
from main import app
import httpx
from fastapi.testclient import TestClient
from firebase_admin import auth
from database.firebse import authUser


client = TestClient(app)

#test pour faire un get all sur les rooms
def test_get_all_meeting_rooms(cleanup):
    client.post("/auth/signup", json={"email": "test_adama@example.com", "password": "testpassword"})
    
    auth_token = authUser.sign_in_with_email_and_password(email="test_adama@example.com", password="testpassword")['idToken']
    auth_headers= {"Authorization": f"Bearer {auth_token}"}

    response = client.get("/meetingroom/", headers=auth_headers)
    assert response.status_code == 200

#test pour ajouter un nouveau room
def test_add_new_meeting_room(cleanup):
    client.post("/auth/signup", json={"email": "test_adama@example.com", "password": "testpassword"})
    
    #Creation les données de la salle de réunion
    auth_token = authUser.sign_in_with_email_and_password(email="test_adama@example.com", password="testpassword")['idToken']
    auth_headers = {"Authorization": f"Bearer {auth_token}"}
    
    meeting_room_data = {
        "title": "Nouvelle salle de réunion",
        "description": "Il s'agit d'une nouvelle salle de réunion d'une capacité de 20 personnes.",
        "location": "San Francisco, CA",
        "capacity": 20,
        "priceOnHours": 100,
        "is_available": True
    }
    response = client.post("/meetingroom/", headers=auth_headers, json=meeting_room_data)
    assert response.status_code == 201
    # Vérifier que la salle de réunion a été créée
    nouvelle_salle_de_reunion = response.json()
    assert nouvelle_salle_de_reunion["title"] == meeting_room_data["title"]
    assert nouvelle_salle_de_reunion["description"] == meeting_room_data["description"]
    assert nouvelle_salle_de_reunion["location"] == meeting_room_data["location"]
    assert nouvelle_salle_de_reunion["capacity"] == meeting_room_data["capacity"]
    assert nouvelle_salle_de_reunion["priceOnHours"] == meeting_room_data["priceOnHours"]

#test pour faire un get by id
def test_get_meeting_room_by_id(cleanup):
    # Créez un utilisateur de test
    client.post("/auth/signup", json={"email": "test_user@example.com", "password": "testpassword"})
    auth_token = authUser.sign_in_with_email_and_password(email="test_user@example.com", password="testpassword")['idToken']
    auth_headers = {"Authorization": f"Bearer {auth_token}"}
      
    # Créez une nouvelle salle de réunion pour le test
    meeting_room_data = {
        "title": "Nouvelle salle de réunion",
        "description": "Il s'agit d'une nouvelle salle de réunion d'une capacité de 20 personnes.",
        "location": "San Francisco, CA",
        "capacity": 20,
        "priceOnHours": 100,
        "is_available": True
    }

    # Envoyer la requête POST avec le paramètre json
    response = client.post("/meetingroom/", headers=auth_headers, json=meeting_room_data)
    assert response.status_code == 201
    meeting_id = response.json()["id"]

    # Appelez la fonction get_meeting_room_by_id pour obtenir les détails de la salle de réunion
    response = client.get(f"/meetingroom/{meeting_id}", headers=auth_headers)
    #requête a réussi (code de statut 200)
    assert response.status_code == 200

#test pour faire un delete 
def test_delete_meeting_room_by_id(cleanup):
    # Créez un utilisateur de test
    client.post("/auth/signup", json={"email": "test_user@example.com", "password": "testpassword"})
    auth_token = authUser.sign_in_with_email_and_password(email="test_user@example.com", password="testpassword")['idToken']
    auth_headers = {"Authorization": f"Bearer {auth_token}"}

    # Créez une nouvelle salle de réunion pour le test
    meeting_room_data = {
        "title": "Nouvelle salle de réunion",
        "description": "Il s'agit d'une nouvelle salle de réunion d'une capacité de 20 personnes.",
        "location": "San Francisco, CA",
        "capacity": 20,
        "priceOnHours": 100,
        "is_available": True
    }
    response = client.post("/meetingroom/", headers=auth_headers, json=meeting_room_data)
    assert response.status_code == 201
    meeting_id = response.json()["id"]

    # Supprimez la salle de réunion avec le meeting_id
    response = client.delete(f"/meetingroom/{meeting_id}", headers=auth_headers)

    # suppression aavec succès (code de statut 200)
    assert response.status_code == 200
    assert response.json() == {"message": "Meeting room deleted"}

#fai un update sur une donnée
def test_patch_meeting_room_by_id(cleanup):
    # Créez un utilisateur de test
    client.post("/auth/signup", json={"email": "test_user@example.com", "password": "testpassword"})
    auth_token = authUser.sign_in_with_email_and_password(email="test_user@example.com", password="testpassword")['idToken']
    auth_headers = {"Authorization": f"Bearer {auth_token}"}

    # Créez une nouvelle salle de réunion pour le test
    meeting_room_data = {
        "title": "Nouvelle salle de réunion",
        "description": "Il s'agit d'une nouvelle salle de réunion d'une capacité de 20 personnes.",
        "location": "San Francisco, CA",
        "capacity": 20,
        "priceOnHours": 100,
        "is_available": True
    }
    response = client.post("/meetingroom/", headers=auth_headers, json=meeting_room_data)
    assert response.status_code == 201
    meeting_id = response.json()["id"]

    # Mettez à jour partiellement la salle de réunion avec le meeting_id
    updated_meeting_room_data = {
        "title": "Salle de réunion mise à jour",
        "description": "Description mise à jour",
        "location": "New York, NY",
        "capacity": 25,
        "priceOnHours": 150,
        "is_available": True
    }
    response = client.patch(f"/meetingroom/{meeting_id}", headers=auth_headers, json=updated_meeting_room_data)

    # Vérifiez si la salle de réunion a été mise à jour avec succès (code de statut 200)
    assert response.status_code == 200
    #Vérifiez si les données de la salle de réunion ont été mises à jour correctement
    updated_meeting_room = response.json()
    assert updated_meeting_room["title"] == updated_meeting_room_data["title"]
    assert updated_meeting_room["description"] == updated_meeting_room_data["description"]
    assert updated_meeting_room["location"] == updated_meeting_room_data["location"]
    assert updated_meeting_room["capacity"] == updated_meeting_room_data["capacity"]
    assert updated_meeting_room["priceOnHours"] == updated_meeting_room_data["priceOnHours"]

