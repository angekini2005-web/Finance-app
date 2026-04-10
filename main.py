from scripts.accounts import add_transaction, check_balances
from scripts.clients import add_client, list_clients
from scripts.projects import add_project, list_projects
from scripts.dashboard import show_bar_chart, show_pie_chart, get_projects
from scripts.export import export_transactions_to_excel
from scripts.projects import analyze_projects
from scripts.projects import project_alerts
from scripts.projects import forecast_projects
from scripts.projects import project_alerts


def main_menu():
    while True:
        print("\n=== MENU PRINCIPAL ===")
        print("1. Voir les soldes")
        print("2. Ajouter une transaction")
        print("3. Ajouter un client")
        print("4. Voir les clients")
        print("5. Ajouter un projet")
        print("6. Voir les projets")
        print("8. Dashboard (barres)")
        print("9. Export Excel")
        print("10. Diagramme circulaire")
        print("11. Analyse des projets")
        print("12. Alertes intelligentes")
        print("13. Prévisions financières")
        print("14. Alertes intelligentes")
        print("0. Quitter")

        choice = input("Choix: ")

        # 💰 SOLDES
        if choice == "1":
            check_balances()

        # 💸 TRANSACTION
        elif choice == "2":
            type_ = input("Type (income/expense): ")
            amount = float(input("Montant: "))
            description = input("Description: ")
            project = input("Projet (optionnel): ")

            add_transaction(type_, amount, description, project)

        # 👤 CLIENT
        elif choice == "3":
            name = input("Nom du client: ")
            add_client(name)

        elif choice == "4":
            list_clients()

        # 📁 PROJET
        elif choice == "5":
            name = input("Nom du projet: ")
            add_project(name)

        elif choice == "6":
            list_projects()

        # 📊 DASHBOARD BARRES (PRO + FILTRE)
        elif choice == "8":
            print("1. Global")
            print("2. Par projet")

            sous_choix = input("Choix: ")

            if sous_choix == "1":
                titre = input("Titre du graphique: ")
                show_bar_chart(titre)

            elif sous_choix == "2":
                projets = get_projects()

                if not projets:
                    print("❌ Aucun projet trouvé")
                else:
                    print("Projets disponibles :")
                    for i, p in enumerate(projets):
                        print(f"{i+1}. {p}")

                    choix_projet = int(input("Choisis un projet: ")) - 1
                    projet = projets[choix_projet]

                    titre = input("Titre du graphique: ")
                    show_bar_chart(titre, projet)

        # 📄 EXPORT
        elif choice == "9":
            export_transactions_to_excel()

        # 🥧 DIAGRAMME CIRCULAIRE
        elif choice == "10":
            titre = input("Titre du graphique: ")
            show_pie_chart(titre)

        elif choice == "11":
            analyze_projects()   

        elif choice == "12":
            project_alerts() 

        elif choice == "13":
            forecast_projects()   

        elif choice == "14":
            project_alerts()         

        # ❌ QUITTER
        elif choice == "0":
            print("👋 Au revoir")
            break

        else:
            print("❌ Choix invalide")


# 🔥 LANCEMENT DU PROGRAMME
if __name__ == "__main__":
    main_menu()