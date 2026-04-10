import json

CONFIG_PATH = "config/config_client.json"

# 🔹 Charger la config
def load_config():
    with open(CONFIG_PATH, "r") as f:
        return json.load(f)

# 🔹 Sauvegarder la config
def save_config(config):
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=4)

# 🔹 Afficher les clients
def list_clients():
    config = load_config()
    clients = config.get("clients", [])

    print("\n👥 === CLIENTS / FOURNISSEURS ===")

    if not clients:
        print("Aucun client enregistré.")
        return

    for i, client in enumerate(clients, 1):
        print(f"{i}. {client}")

# 🔹 Ajouter un client
def add_client(name):
    config = load_config()
    clients = config.get("clients", [])

    if name in clients:
        print("⚠️ Ce client existe déjà.")
        return

    clients.append(name)
    config["clients"] = clients
    save_config(config)

    print("✅ Client ajouté avec succès.")