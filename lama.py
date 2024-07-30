import requests
import time
import json

API_TOKEN = "r8_USSnW9a9gBQ2NikEQcR7imePfHrUNex2JnpS3"
MODEL_VERSION = "2796ee9483c3fd7aa2e171d38f4ca12251a30609463dcfd4cd76703f22e96cdf"


def create_prediction(prompt):
    url = "https://api.replicate.com/v1/predictions"
    headers = {
        "Authorization": f"Token {API_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "version": MODEL_VERSION,
        "input": {
            "prompt": prompt,
            "max_new_tokens": 500,
            "temperature": 0.75,
            "top_p": 0.9,
            "top_k": 50
        }
    }
    response = requests.post(url, headers=headers, json=data)

    if response.status_code not in [200, 201]:
        print(f"Erreur HTTP: {response.status_code}")
        print(response.text)
        return None

    return response.json()


def get_prediction(prediction_id):
    url = f"https://api.replicate.com/v1/predictions/{prediction_id}"
    headers = {"Authorization": f"Token {API_TOKEN}"}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Erreur HTTP: {response.status_code}")
        print(response.text)
        return None

    return response.json()


def ask_question(prompt):
    prediction = create_prediction(prompt)
    if not prediction:
        print("Erreur: La prédiction n'a pas pu être créée.")
        return None

    prediction_id = prediction["id"]
    print(f"Prédiction créée avec l'ID: {prediction_id}")

    while True:
        prediction_status = get_prediction(prediction_id)
        if not prediction_status:
            print("Erreur: Impossible de récupérer le statut de la prédiction.")
            return None

        current_status = prediction_status["status"]
        print(f"Statut actuel: {current_status}")

        if current_status == "succeeded":
            print("Prédiction terminée avec succès!")
            output = prediction_status.get("output", [])
            return ''.join(output).strip() if isinstance(output, list) else str(output)
        elif current_status in ["failed", "canceled"]:
            print(f"Prédiction terminée avec le statut: {current_status}")
            return None
        elif current_status in ["starting", "processing"]:
            print("La prédiction est en cours de traitement...")
            time.sleep(2)
        else:
            print(f"Statut inattendu: {current_status}")
            return None


def main():
    prompt = input("Entrez votre prompt pour LLaMA : ")
    response = ask_question(prompt)

    if response:
        print("\nRéponse du modèle:")
        print(response)
    else:
        print("Aucune réponse n'a pu être obtenue.")


main()