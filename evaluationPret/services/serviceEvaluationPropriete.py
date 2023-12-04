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
    
        lienJSON = "./evaluationPret/services/bdd/immobilier.json"
        
        immobilier = [
            {"idImmobilier": 1,"adresse": "123 Rue de la Liberte, 75001 Paris, France","age": 9,"normeLegal": 0,"normeReglementaire": 0,"litigesEnCours": 0,"normeElectricite": "NF C 15-100","normeGaz": "NF P 45-500"},
            {"idImmobilier": 2,"adresse": "45 avenue des Etats-Unis, 78000 Versailles, France","age": 23,"normeLegal": 1,"normeReglementaire": 1,"litigesEnCours": 1,"normeElectricite": "NF C 14-100","normeGaz": ""},
            {"idImmobilier": 3,"adresse": "12 Rue du Pont Neuf, 91120 Palaiseau, France","age": 9,"normeLegal": 0,"normeReglementaire": 0,"litigesEnCours": 0,"normeElectricite": "NF C 15-100","normeGaz": "NF P 45-500"},
            {"idImmobilier": 4,"adresse": "2 Avenue de la gare, 91120 Palaiseau, France","age": 9,"normeLegal": 0,"normeReglementaire": 0,"litigesEnCours": 0,"normeElectricite": "NF C 15-100","normeGaz": ""},
            {"idImmobilier": 5,"adresse": "39 Rue Geais Padidee, 91120 Palaiseau, France","age": 20,"normeLegal": 0,"normeReglementaire": 0,"litigesEnCours": 0,"normeElectricite": "NF C 15-100","normeGaz": ""}
        ]
        
        json_string = json.dumps(immobilier, indent=4) 

        with open(lienJSON, "w") as json_file:
            json_file.write(json_string)
            
        return lienJSON
    
    
    def creationDBMarcheImmobilier():
    
        lienJSON = "./evaluationPret/services/bdd/marcheImmobilier.json"
        
        marcheImmobilier = [
            {"adresse": "1 Rue Gpasdidee","codePostal": 75001,"batiment": "Maison","nbEtage": "2","valeur": 190000},
            {"adresse": "36 Rue LaFayette","codePostal": 75001,"batiment": "Maison","nbEtage": "2","valeur": 230000},
            {"adresse": "25 Avenue Victor Hugo","codePostal": 75001,"batiment": "Maison","nbEtage": "1","valeur": 140000},
            {"adresse": "12 Rue Jp","codePostal": 75001,"batiment": "Maison","nbEtage": "2","valeur": 210000},
            {"adresse": "1 Rue Jesaispas","codePostal": 78000,"batiment": "Maison","nbEtage": "6","valeur": 150000},
            {"adresse": "3 Rue Truc","codePostal": 78000,"batiment": "Maison","nbEtage": "7","valeur": 180000},
            {"adresse": "27 Avenue Bidule","codePostal": 78000,"batiment": "Maison","nbEtage": "5","valeur": 100000},
            {"adresse": "42 Rue Mj","codePostal": 78000,"batiment": "Maison","nbEtage": "6","valeur": 120000},
            {"adresse": "33 Rue Gaspard","codePostal": 91120,"batiment": "Maison","nbEtage": "2","valeur": 190000},
            {"adresse": "26 Rue LaFayette","codePostal": 91120,"batiment": "Maison","nbEtage": "0","valeur": 100000},
            {"adresse": "25 Avenue Victor Hugo","codePostal": 91120,"batiment": "Maison","nbEtage": "1","valeur": 140000},
            {"adresse": "12 Rue Jp","codePostal": 91120,"batiment": "Maison","nbEtage": "2","valeur": 210000},
            {"adresse": "25 Rue Gaspard","codePostal": 91120,"batiment": "Appartement","nbEtage": "6","valeur": 150000},
            {"adresse": "26 Rue Gaspard","codePostal": 91120,"batiment": "Appartement","nbEtage": "6","valeur": 150000},
            {"adresse": "27 Rue Gaspard","codePostal": 91120,"batiment": "Appartement","nbEtage": "6","valeur": 150000},
            {"adresse": "26 Rue LaFayette","codePostal": 91120,"batiment": "Appartement","nbEtage": "6","valeur": 120000},
            {"adresse": "12 Rue Truc","codePostal": 91120,"batiment": "Appartement","nbEtage": "7","valeur": 180000},
            {"adresse": "27 Avenue Bidule","codePostal": 91120,"batiment": "Appartement","nbEtage": "5","valeur": 100000},
            {"adresse": "42 Avenue Jean Paul","codePostal": 91120,"batiment": "Appartement","nbEtage": "6","valeur": 170000},
            {"adresse": "29 Avenue Sartres","codePostal": 91120,"batiment": "Appartement","nbEtage": "5","valeur": 170000}
        ]
        
        json_string = json.dumps(marcheImmobilier, indent=4) 

        with open(lienJSON, "w") as json_file:
            json_file.write(json_string)
            
        return lienJSON
    
    
    def recupDonneesImmobilier(lienJSONImmobilier, idEvaluation):
    
        connexion = sqlite3.connect('evaluationPret.db')
        cursor = connexion.cursor()
        
        cursor.execute("SELECT idPropriete, adresse FROM EVALUATION WHERE idEvaluation = ?", (idEvaluation,))
        resultats = cursor.fetchone()

        donnees=[]
        test=-1
        
        for i in range(0,len(resultats)):
            donnees.append(resultats[i])
    
        with open(lienJSONImmobilier, "r") as json_file:
            immobilier = json.load(json_file)
        
        for propriete in immobilier:
            if str(propriete["idImmobilier"]) == str(donnees[0]):
                donnees.append(propriete["age"])
                donnees.append(propriete["normeLegal"])
                donnees.append(propriete["normeReglementaire"])
                donnees.append(propriete["litigesEnCours"])
                donnees.append(propriete["normeElectricite"])
                donnees.append(propriete["normeGaz"])
                test=0
        
        if test==-1 : 
                print("Propriete non existante")
            
        connexion.commit()
        connexion.close()
                
        return donnees
    
    
    def recupDonneesMarcheImmobilier(idEvaluation):

        connexion = sqlite3.connect('evaluationPret.db')
        cursor = connexion.cursor()
        
        cursor.execute("SELECT adresse, idPropriete FROM EVALUATION WHERE idEvaluation = ?", (idEvaluation,))
        resultats = cursor.fetchone()

        donnees=[]
        
        for i in range(0,len(resultats)):
            donnees.append(resultats[i])
            
        connexion.commit()
        connexion.close()
        
        return donnees
    
    
    def verificationConformite(donnees, idEvaluation): 
    
        idImmobilier=donnees[0]
        adresse=donnees[1]
        age=donnees[2]
        normeLegal=donnees[3]
        normeReglementaire=donnees[4]
        litigesEnCours=donnees[5]
        normeElectricite=donnees[6]
        normeGaz=donnees[7]
        
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
        if age < 10:
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
        
        cursor.execute("UPDATE EVALUATION SET decisionConformite = ?, raison = ? WHERE idEvaluation = ?", (decision, raison, idEvaluation))
        
        connexion.commit()
        connexion.close()
  
    
    def valeurMarche(donnees, idEvaluation, lienJSONMarcheImmobilier):
        print("Donnees: "+str(donnees))
        adresse = donnees[0]
        print("Adresse: "+str(adresse))
        descriptionPropriete = str(donnees[1])
        print("Description propriete: "+str(descriptionPropriete))
        codePostal = int(re.search(r'\b\d{5}\b', adresse).group())
        print("Code postal: "+str(codePostal))
        modeleRegex = r"(Maison|Appartement)|(maison|appartement)(?:.*?(\b\w+\b)?\s?[ée]tage[s])?"
        print("Regex: "+str(modeleRegex))
        resultat = re.search(modeleRegex, descriptionPropriete, re.IGNORECASE)
        print("Resultat: "+str(resultat))
        
        nbEtage = None
        batiment = None
        moyenne_valeur = 0
        
        if resultat:
            batiment = resultat.group(1)
            nbEtageExtrait = resultat.group(2) if resultat.group(2) else None
            nbEtage = nombres_en_texte.get(nbEtageExtrait.lower(), nbEtageExtrait) if nbEtageExtrait else None
        else:
            print("Aucun match trouvé")
            
            
        with open(lienJSONMarcheImmobilier, "r") as json_file:
            marcheImmobilier = json.load(json_file)
            
        somme = 0
        nbElements = 1

        if nbEtage == None:
            for propriete in marcheImmobilier:
                if (str(propriete["codePostal"]) == str(codePostal)) and (str(propriete['batiment']) == str(batiment)):
                    somme+=propriete["valeur"]
                    nbElements+=1
        else:
            for propriete in marcheImmobilier:
                if (str(propriete["codePostal"]) == str(codePostal)) and (str(propriete['batiment']) == str(batiment)) and (str(propriete["nbEtage"]) == str(nbEtage)):
                    somme+=propriete["valeur"]
                    nbElements+=1

        if resultat is not None and resultat[0] is not None:
            moyenne_valeur = int(somme/nbElements)
            
        else:
            print("Aucun résultat trouvé pour le code_postal", codePostal, ", le batiment", batiment, "et le nombre d'etages", nbEtage)

        
        #Ecriture dans la BD
        connexion = sqlite3.connect('evaluationPret.db')
        cursor = connexion.cursor()
        
        cursor.execute("UPDATE EVALUATION SET estimationValeur = ? WHERE idEvaluation = ?", (moyenne_valeur, idEvaluation))
        
        connexion.commit()
        connexion.close()
        
    
    
    def evaluer(idEvaluation : int):
        lien1=serviceEvaluationPropriete.creationDBImmobilier()
        lien2=serviceEvaluationPropriete.creationDBMarcheImmobilier()
        donnees1=serviceEvaluationPropriete.recupDonneesImmobilier(lien1, idEvaluation)
        donnees2=serviceEvaluationPropriete.recupDonneesMarcheImmobilier(idEvaluation)
        serviceEvaluationPropriete.verificationConformite(donnees1, idEvaluation)
        serviceEvaluationPropriete.valeurMarche(donnees2, idEvaluation, lien2)
        