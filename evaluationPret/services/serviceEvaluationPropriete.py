# Service permettant d'évaluer la propriété

#Importation 
import json
import sqlite3
import random
import re

#Importation du service composite
import serviceComposite



#Struct pour convertir les nombres en texte
nombres_en_texte = {
    "un": "1",
    "deux": "2",
    "trois": "3",
}



class serviceEvaluationPropriete:
    
    def creationDBImmobilier():
    
        connexion = sqlite3.connect("immobilier.db")
        curseur = connexion.cursor()

        curseur.execute('DROP TABLE IF EXISTS IMMOBILIER')
        curseur.execute('''
            CREATE TABLE IF NOT EXISTS IMMOBILIER (
                idImmobilier INTEGER PRIMARY KEY,
                adresse TEXT,
                age INTEGER,
                normeLegal INTEGER,
                normeReglementaire INTEGER,
                litigesEnCours INTEGER,
                normeElectricite TEXT,
                normeGaz TEXT
            )
        ''')

        donnees_json = [
            {
                "idImmobilier": 1,
                "adresse": "123 Rue de la Liberte, 75001 Paris, France",
                "age": 9,
                "normeLegal": 0,
                "normeReglementaire": 0,
                "litigesEnCours": 0,
                "normeElectricite": "NF C 15-100",
                "normeGaz": "NF P 45-500"
            },
            {
                "idImmobilier": 2,
                "adresse": "45 avenue des Etats-Unis, 78000 Versailles, France",
                "age": 23,
                "normeLegal": 1,
                "normeReglementaire": 1,
                "litigesEnCours": 1,
                "normeElectricite": "NF C 14-100",
                "normeGaz": ""
            },
            {
                "idImmobilier": 3,
                "adresse": "12 Rue du Pont Neuf, 91120 Palaiseau, France",
                "age": 9,
                "normeLegal": 0,
                "normeReglementaire": 0,
                "litigesEnCours": 0,
                "normeElectricite": "NF C 15-100",
                "normeGaz": "NF P 45-500"
            },
            {
                "idImmobilier": 4,
                "adresse": "2 Avenue de la gare, 91120 Palaiseau, France",
                "age": 9,
                "normeLegal": 0,
                "normeReglementaire": 0,
                "litigesEnCours": 0,
                "normeElectricite": "NF C 15-100",
                "normeGaz": ""
            },
            {
                "idImmobilier": 5,
                "adresse": "39 Rue Geais Padidee, 91120 Palaiseau, France",
                "age": 20,
                "normeLegal": 0,
                "normeReglementaire": 0,
                "litigesEnCours": 0,
                "normeElectricite": "NF C 15-100",
                "normeGaz": ""
            }
        ]

        for immobilier in donnees_json:
            curseur.execute('''
                INSERT INTO immobilier (idImmobilier, adresse, age, normeLegal, normeReglementaire, litigesEnCours, normeElectricite, normeGaz)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                immobilier["idImmobilier"],
                immobilier["adresse"],
                immobilier["age"],
                immobilier["normeLegal"],
                immobilier["normeReglementaire"],
                immobilier["litigesEnCours"],
                immobilier["normeElectricite"],
                immobilier["normeGaz"]
            ))

        connexion.commit()
        connexion.close()
        
        print("La table IMMOBILIER a été crée.")
    
    
    def creationDBMarcheImmobilier():
    
        connexion = sqlite3.connect("marcheImmobilier.db")
        curseur = connexion.cursor()

        curseur.execute('DROP TABLE IF EXISTS MARCHEIMMOBILIER')
        curseur.execute('''
            CREATE TABLE IF NOT EXISTS MARCHEIMMOBILIER(
                idMarche INTEGER PRIMARY KEY,
                adresse TEXT,
                codePostal INTEGER,
                batiment TEXT,
                nbEtage TEXT,
                valeur INTEGER
            )
        ''')

        donnees_json = [
            {
                "adresse": "1 Rue Gpasdidee",
                "codePostal": 75001,
                "batiment": "Maison",
                "nbEtage": "2",
                "valeur": 190000
            },
            {
                "adresse": "36 Rue LaFayette",
                "codePostal": 75001,
                "batiment": "Maison",
                "nbEtage": "2",
                "valeur": 230000
            },
            {
                "adresse": "25 Avenue Victor Hugo",
                "codePostal": 75001,
                "batiment": "Maison",
                "nbEtage": "1",
                "valeur": 140000
            },
            {
                "adresse": "12 Rue Jp",
                "codePostal": 75001,
                "batiment": "Maison",
                "nbEtage": "2",
                "valeur": 210000
            },
            {
                "adresse": "1 Rue Jesaispas",
                "codePostal": 78000,
                "batiment": "Maison",
                "nbEtage": "6",
                "valeur": 150000
            },
            {
                "adresse": "3 Rue Truc",
                "codePostal": 78000,
                "batiment": "Maison",
                "nbEtage": "7",
                "valeur": 180000
            },
            {
                "adresse": "27 Avenue Bidule",
                "codePostal": 78000,
                "batiment": "Maison",
                "nbEtage": "5",
                "valeur": 100000
            },
            {
                "adresse": "42 Rue Mj",
                "codePostal": 78000,
                "batiment": "Maison",
                "nbEtage": "6",
                "valeur": 120000
            },


            {
                "adresse": "33 Rue Gaspard",
                "codePostal": 91120,
                "batiment": "Maison",
                "nbEtage": "2",
                "valeur": 190000
            },
            {
                "adresse": "26 Rue LaFayette",
                "codePostal": 91120,
                "batiment": "Maison",
                "nbEtage": "0",
                "valeur": 100000
            },
            {
                "adresse": "25 Avenue Victor Hugo",
                "codePostal": 91120,
                "batiment": "Maison",
                "nbEtage": "1",
                "valeur": 140000
            },
            {
                "adresse": "12 Rue Jp",
                "codePostal": 91120,
                "batiment": "Maison",
                "nbEtage": "2",
                "valeur": 210000
            },
            {
                "adresse": "25 Rue Gaspard",
                "codePostal": 91120,
                "batiment": "Appartement",
                "nbEtage": "6",
                "valeur": 150000
            },
            {
                "adresse": "26 Rue Gaspard",
                "codePostal": 91120,
                "batiment": "Appartement",
                "nbEtage": "6",
                "valeur": 150000
            },
            {
                "adresse": "27 Rue Gaspard",
                "codePostal": 91120,
                "batiment": "Appartement",
                "nbEtage": "6",
                "valeur": 150000
            },
            {
                "adresse": "26 Rue LaFayette",
                "codePostal": 91120,
                "batiment": "Appartement",
                "nbEtage": "6",
                "valeur": 120000
            },
            {
                "adresse": "12 Rue Truc",
                "codePostal": 91120,
                "batiment": "Appartement",
                "nbEtage": "7",
                "valeur": 180000
            },
            {
                "adresse": "27 Avenue Bidule",
                "codePostal": 91120,
                "batiment": "Appartement",
                "nbEtage": "5",
                "valeur": 100000
            },
            {
                "adresse": "42 Avenue Jean Paul",
                "codePostal": 91120,
                "batiment": "Appartement",
                "nbEtage": "6",
                "valeur": 170000
            },
            {
                "adresse": "29 Avenue Sartres",
                "codePostal": 91120,
                "batiment": "Appartement",
                "nbEtage": "5",
                "valeur": 170000
            }
        ]

        for marcheImmobilier in donnees_json:
            curseur.execute('''
                INSERT INTO marcheImmobilier (adresse, codePostal, batiment, nbEtage, valeur)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                marcheImmobilier["adresse"],
                marcheImmobilier["codePostal"],
                marcheImmobilier["batiment"],
                marcheImmobilier["nbEtage"],
                marcheImmobilier["valeur"]
            ))

        connexion.commit()
        connexion.close()
        print("La table MARCHEIMMOBILIER a été crée.")
    
    
    def recupDonneesImmobilier(idEvaluation):
        
        donnees=[]
    
        connexion1 = sqlite3.connect('evaluationPret.db')
        curseur1 = connexion1.cursor()
        curseur1.execute("SELECT idPropriete, adresse, descriptionPropriete FROM EVALUATION WHERE idEvaluation = ?", (idEvaluation,))
        evaluation = curseur1.fetchone()
        print("$Recup evaluation: "+str(evaluation))
        
        for i in range(0,len(evaluation)):
            donnees.append(evaluation[i])
            
        connexion1.commit()
        connexion1.close()
        
        connexion2 = sqlite3.connect('immobilier.db')
        curseur2 = connexion2.cursor()
        curseur2.execute("SELECT age, normeLegal, normeReglementaire, litigesEnCours, normeElectricite, normeGaz FROM immobilier WHERE idImmobilier = ?", (donnees[0],))
        immobilier = curseur2.fetchone()
        print("$Recup immobilier: "+str(immobilier))

        connexion2.commit()
        connexion2.close()
        
        if(immobilier != None):
            
            for i in range(0,len(immobilier)):
                donnees.append(immobilier[i])
                
            return donnees
        
        else:        
            return -1
    
    
    def verificationConformite(donnees, idEvaluation): 
        
        print("$Donnees Verif : "+str(donnees))
        
        age=donnees[3]
        normeLegal=donnees[4]
        normeReglementaire=donnees[5]
        litigesEnCours=donnees[6]
        normeElectricite=donnees[7]
        normeGaz=donnees[8]
        
        
        #Initialisation
        decision = 'Admissible a un pret immobilier'
        facteur1 = ''
        facteur2 = ''
        facteur3 = '' 
        facteur4 = '' 
        facteur5 = ''
        raison = ''
        
        #Attribution aléatoire des visites (virtuelles et sur place)
        random_number = random.randint(0, 1)
        
        if random_number == 0:
            visitevirutelle = "Visite virtuelle non demandée et non effectuée"
            visitesurplace = "Visite sur place non demandée et non effectuée"
        else:
            visitevirutelle = "Visite virtuelle demandée et effectuée"
            visitesurplace = "Visite sur place non demandée et non effectuée"

        #Decision
        if int(age) < 10:
            if normeElectricite not in ['NFC 15-100', 'NF C 15-100', 'C 15-100']:
                facteur1 = 'Non conforme : Electricite'
                decision = 'Non admissible a un pret immobilier'               

                if visitevirutelle == "Visite virtuelle demandée et effectuée": visitesurplace = "Visite sur place non concluante"                 
                elif visitevirutelle == "Visite virtuelle demandée et effectuée": visitesurplace = "Visite sur place concluante"
                
                if normeGaz == '':
                    if visitevirutelle == "Visite virtuelle demandée et effectuée" and visitesurplace != "Visite sur place non concluante": visitesurplace = "Visite sur place concluante"
                elif normeGaz != 'NF P 45-500':
                    facteur2 = 'Non conforme : Gaz '
                    decision = 'Non admissible a un pret immobilier'

                    if visitevirutelle == "Visite virtuelle demandée et effectuée": visitesurplace = "Visite sur place non concluante"                 
                    elif visitevirutelle == "Visite virtuelle demandée et effectuée" and visitesurplace != "Visite sur place non concluante": visitesurplace = "Visite sur place concluante"

        if normeLegal != 0:
            facteur3 = 'Normes non legales!'
            decision = 'Non admissible a un pret immobilier'
            
        if normeReglementaire != 0:
            facteur4 = 'Normes non reglementaires !'
            decision = 'Non admissible a un pret immobilier'
            
        if litigesEnCours != 0:
            facteur5 = 'Il y a au moins 1 litige en cours'
            decision = 'Non admissible a un pret immobilier'
            
            
        if decision == 'Non admissible a un pret immobilier':
            # Liste les raisons du refus
            if facteur1 == 'Non conforme : Electricite':
                raison += facteur1
            if facteur2 == 'Non conforme : Gaz':
                raison += facteur2
            if facteur3 == 'Normes non legales !':
                raison += facteur3
            if facteur4 == 'Normes non reglementaires !':
                raison_ += facteur4
            if facteur5 == 'Il y a au moins 1 litige en cours':
                raison += facteur5
                
                
        #Ecriture dans la BD
        connexion = sqlite3.connect('evaluationPret.db')
        cursor = connexion.cursor()
        
        print("$Decision Conformite: "+decision)
        print("$Raisons: "+raison)
        
        cursor.execute("UPDATE EVALUATION SET decisionConformite = ?, raison = ? WHERE idEvaluation = ?", (decision, raison, idEvaluation))
        
        connexion.commit()
        connexion.close()
  
    
    def valeurMarche(donnees, idEvaluation):
        print("Donnees: "+str(donnees))
        adresse = donnees[1]
        print("Adresse: "+str(adresse))
        descriptionPropriete = str(donnees[2])
        print("Description propriete: "+str(descriptionPropriete))
        codePostal = int(re.search(r'\b\d{5}\b', adresse).group())
        print("Code postal: "+str(codePostal))
        #modeleRegex = r"(Maison|Appartement)|(maison|appartement)(?:.*?(\b\w+\b)?\s?[ée]tage[s])?"
        modeleRegex = r"(Maison|Appartement)(?:.*?(\b\w+\b)?\s?etage[s])?"
        resultat = re.search(modeleRegex, descriptionPropriete, re.IGNORECASE)
        print("Resultat: "+str(resultat))
        print("Resultat1: "+str(resultat.group(1)))
        print("Resultat2: "+str(resultat.group(2)))
        
        if resultat:
            batiment = resultat.group(1)
            nbEtageExtrait = resultat.group(2) if resultat.group(2) else None
            nbEtage = nombres_en_texte.get(nbEtageExtrait.lower(), nbEtageExtrait) if nbEtageExtrait else None
        else:
            print("Aucun match trouvé")
            
        print("Batiment: "+str(batiment))
        print("Nombre d'étages: "+str(nbEtage))
            
        connexion1 = sqlite3.connect("marcheImmobilier.db")
        curseur1 = connexion1.cursor()
        
        if nbEtage == None:
            curseur1.execute("SELECT AVG(valeur) FROM MARCHEIMMOBILIER WHERE codePostal = ? AND batiment = ?", (codePostal, batiment))
        else:
            curseur1.execute("SELECT AVG(valeur) FROM MARCHEIMMOBILIER WHERE codePostal = ? AND batiment = ? AND nbEtage = ?", (codePostal, batiment, nbEtage))
        
        marcheImmobilier = curseur1.fetchone()
        
        connexion1.commit()
        connexion1.close()
        
        print("Marche Immobilier: "+str(marcheImmobilier))

        if marcheImmobilier is not None and marcheImmobilier[0] is not None:
            moyenneValeur = int(marcheImmobilier[0])
            print("Moyenne : "+str(moyenneValeur))
        else:
            print("Aucun résultat trouvé pour le code_postal", codePostal, ", le batiment", batiment, "et le nombre d'etages", nbEtage)
        
        connexion2 = sqlite3.connect('evaluationPret.db')
        curseur2 = connexion2.cursor()
        
        curseur2.execute("UPDATE EVALUATION SET estimationValeur = ? WHERE idEvaluation = ?", (moyenneValeur, idEvaluation))
        
        connexion2.commit()
        connexion2.close()
        
    
    
    def evaluer(idEvaluation : int):
        serviceEvaluationPropriete.creationDBImmobilier()
        serviceEvaluationPropriete.creationDBMarcheImmobilier()
        donnees1=serviceEvaluationPropriete.recupDonneesImmobilier(idEvaluation)
        if (donnees1 == -1):
            print("Propriété non existante dans l'Immobilier")
        else:
            serviceEvaluationPropriete.verificationConformite(donnees1, idEvaluation)
            serviceEvaluationPropriete.valeurMarche(donnees1, idEvaluation)
        