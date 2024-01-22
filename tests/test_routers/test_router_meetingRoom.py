
import pytest
from fastapi.testclient import TestClient
from main import app
from firebase_admin import auth

client = TestClient(app)

@pytest.fixture
def cleanup(request):
    # Nettoyer la base de données une fois les tests terminés
    def remove_test_users():
        users = auth.list_users().iterate_all()
        for user in users:
            # Ajoutez votre logique de filtrage pour identifier les utilisateurs de test
            if user.email.startswith("test_"):
                auth.delete_user(user.uid)
    
    # Ajouter la fonction de nettoyage pour qu'elle soit appelée à la fin des tests
    request.addfinalizer(remove_test_users)

# Exemple de test avec nettoyage
def test_create_account_success(cleanup):
    # Effectuez vos actions de test ici
    response = client.post("/auth/signup", json={"email": "test_adama@example.com", "password": "testpassword"})
    assert response.status_code == 201
    assert "message" in response.json()
    assert "id" in response.json()["message"]
    # Le nettoyage se fera automatiquement à la fin du test grâce au décorateur @pytest.fixture

# Exemple de test avec nettoyage
def test_create_account_conflict(cleanup):
    # Effectuez vos actions de test ici
    response = client.post("/auth/signup", json={"email": "adama@example.com", "password": "testpassword"})
    assert response.status_code == 409  # Conflict
    # Le nettoyage se fera automatiquement à la fin du test grâce au décorateur @pytest.fixture

def test_login(cleanup):
    # Créer un utilisateur pour le test de connexion
    response_create = client.post("/auth/signup", json={"email": "test_test@example.com", "password": "testpassword"})
    assert response_create.status_code == 201

    # Effectuer le test de connexion avec les informations de l'utilisateur créé
    response_login = client.post("/auth/login", data={"username": "test_test@example.com", "password": "testpassword"})
    assert response_login.status_code == 200
    assert "access_token" in response_login.json()

def test_login_user_not_exists():
    # Effectuez vos actions de test ici en utilisant un utilisateur qui n'existe pas
    response = client.post("/auth/login", data={"username": "utilisateur_inconnu@example.com", "password": "mot_de_passe_incorrect"})

    # Assurez-vous que le code d'état est 401 (Non autorisé)
    assert response.status_code == 401
    # Assurez-vous que le message d'erreur est conforme à vos attentes
    assert "Invalid Credentials" in response.json()["detail"]

@pytest.fixture
def auth_token():
    # Effectuer le test de connexion avec les informations de l'utilisateur créé
    response_login = client.post("/auth/login", data={"username": "counttest@gmail.com", "counttest": "testpassword"})
    assert response_login.status_code == 200
    assert "access_token" in response_login.json()
    return response_login.json()["access_token"]

















'''
1. Identification des Cas de Test :
    Test d'ajout de salle de réunion (POST)
    Test de récupération de toutes les salles de réunion (GET)
    Test de récupération d'une salle de réunion spécifique (GET/{meeting_id})
    Test de mise à jour d'une salle de réunion (PATCH/{meeting_id})
    Test de suppression d'une salle de réunion (DELETE/{meeting_id}) 
    
2. Création des Scénarios de Test :
    Scénario 1 - Ajout de Salle de Réunion :
        Créez une nouvelle salle de réunion et vérifiez si elle est correctement ajoutée.
    Scénario 2 - Récupération de Toutes les Salles de Réunion :
        Ajoutez plusieurs salles de réunion, puis récupérez-les toutes et vérifiez si la liste correspond aux salles ajoutées.
    Scénario 3 - Récupération d'une Salle de Réunion Spécifique :
        Ajoutez une salle de réunion, récupérez-la par ID et vérifiez si les données correspondent.
    Scénario 4 - Mise à Jour d'une Salle de Réunion :
        Ajoutez une salle de réunion, effectuez une mise à jour et vérifiez si les modifications sont correctement enregistrées.
    Scénario 5 - Suppression d'une Salle de Réunion :
        Ajoutez une salle de réunion, supprimez-la et assurez-vous qu'elle n'est plus présente dans la liste.
    Scénario 6 - Tester le cas où une salle n'existe pas :
        Essayer teste le cas ou recuper une salle qui n'existe pas


'''