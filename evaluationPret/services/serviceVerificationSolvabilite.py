# Service permettant de vérifier la solvabilité
import json, sqlite3

# Importation du service composite
import serviceComposite


class serviceVerificationSolvabilite:
    
    def creationDBBanque():
    
        lienJSON = "./evaluationPret/services/bdd/banque.json"
        
        banque = [
            {"idBanque": 11,"age": 25,"enfants": 0,"emploi": 0,"nbCreditsEnCours": 0,"antecedents": 0,"tauxEndettement": 0},
            {"idBanque": 22,"age": 50,"enfants": 4,"emploi": 1,"nbCreditsEnCours": 4,"antecedents": 1,"tauxEndettement": 45},
            {"idBanque": 33,"age": 20,"enfants": 1,"emploi": 0,"nbCreditsEnCours": 0,"antecedents": 0,"tauxEndettement": 0},
            {"idBanque": 44,"age": 33,"enfants": 1,"emploi": 1,"nbCreditsEnCours": 0,"antecedents": 0,"tauxEndettement": 0},
            {"idBanque": 55,"age": 75,"enfants": 5,"emploi": 0,"nbCreditsEnCours": 1,"antecedents": 0,"tauxEndettement": 20}
        ]

        json_string = json.dumps(banque, indent=4) 

        with open(lienJSON, "w") as json_file:
            json_file.write(json_string)

        return lienJSON
    
    
    def recupDonnees(lienJSON, idEvaluation):
        
        connexion = sqlite3.connect('evaluationPret.db')
        cursor = connexion.cursor()
        
        cursor.execute("SELECT idBanque, montantPret, dureePret, revenuMensuel, depenseMensuelle FROM EVALUATION WHERE idEvaluation = ?", (idEvaluation,))
        resultats = cursor.fetchone()

        donnees=[]
        test=-1
        
        for i in range(0,len(resultats)):
            donnees.append(resultats[i])
            
        with open(lienJSON, "r") as json_file:
            banque = json.load(json_file)

        for client in banque:
            if str(client["idBanque"]) == str(donnees[0]):
                donnees.append(int(client["age"]))
                donnees.append(int(client["enfants"]))
                donnees.append(int(client["emploi"]))
                donnees.append(int(client["nbCreditsEnCours"]))
                donnees.append(int(client["antecedents"]))
                donnees.append(int(client["tauxEndettement"]))
                test=0
        
        if test==-1 : 
                print("Compte bancaire non retrouvé")
            
        connexion.commit()
        connexion.close()

        return donnees
    
    
    def calculScoring(donnees, idEvaluation):
    
        #stockage des données
        idBanque = donnees[0]
        montantPret = donnees[1]
        dureePret = donnees[2]
        revenuMensuel = donnees[3]
        depenseMensuelle = donnees[4]
        age = donnees[5]
        enfants = donnees[6]
        emploi = donnees[7]
        nbCreditsEnCours = donnees[8]
        antecedents = donnees[9]
        tauxEndettement = donnees[10]
        
        score = -1
        capaciteEmprunt = (int(revenuMensuel) * 33) / 100
        decision = "Pas de décision"
        
        
        #calcul scoring
        if age < 18 or tauxEndettement >= 33 or (depenseMensuelle + capaciteEmprunt) > revenuMensuel:
            if age < 18: decision = 'Non Admissible'
            if tauxEndettement >= 33: decision = 'Non Admissible'
            if (depenseMensuelle + capaciteEmprunt) > revenuMensuel: decision = 'Non Admissible'
        
        else:
            
            score = 0
            
            if 18 <= age < 35:
                if enfants == 0:
                    if emploi == 0: score += 10
                    else: score += 5
                if enfants == 1:
                    if emploi == 0: score += 8
                    else: score += 3
                if enfants == 2:
                    if emploi == 0: score += 6
                    else: score = 2
                if enfants > 3:
                    if emploi == 0: score += 5
                    else: decision = 'Non Admissible'
                
                if dureePret < 10: score += 10
                elif 10 <= dureePret < 15: score += 8
                elif 15 <= dureePret < 20: score += 6
                elif 20 <= dureePret < 25: score += 4
                elif dureePret >= 25: score += 2
        
                if montantPret < 100000: score += 10
                elif 100000 <= montantPret < 150000: score += 8
                elif 150000 <= montantPret < 200000: score += 6
                elif 200000 <= montantPret < 250000: score += 4
                elif montantPret >= 250000: score += 2

                if antecedents == 0: score += 10
                elif antecedents == 1: score += 7
                elif antecedents == 2: score += 4
                elif antecedents == 3: score += 1
                elif antecedents >= 4: decision = 'Non Admissible'
                
            elif 35 <= age < 60:
                if enfants == 0:
                    if emploi == 0: score += 8
                    else: score += 5
                if enfants == 1:
                    if emploi == 0: score += 6
                    else: score += 3
                if enfants == 2:
                    if emploi == 0: score += 5
                    else: score += 2
                if enfants > 3:
                    if emploi == 0: score += 4
                    else: decision = 'Non Admissible'
                
                if dureePret < 10: score += 9
                elif 10 <= dureePret < 15: score += 7
                elif 15 <= dureePret < 20: score += 5
                elif 20 <= dureePret < 25: score += 3
                elif dureePret >= 25: score += 1
                
                if montantPret < 100000: score += 9
                elif 100000 <= montantPret < 150000: score += 7
                elif 150000 <= montantPret < 200000: score += 5
                elif 200000 <= montantPret < 250000: score += 3
                elif montantPret >= 250000: score += 1
                    
                if antecedents == 0: score += 8
                elif antecedents == 1: score += 5
                elif antecedents == 2: score += 2
                elif antecedents == 3: score += 0
                elif antecedents >= 4: decision = 'Non Admissible'
            
            elif 60 <= age:
                if enfants == 0:
                    if emploi == 0: score += 6
                    else: score += 5
                if enfants == 1:
                    if emploi == 0: score += 4
                    else: score += 3
                if enfants == 2:
                    if emploi == 0: score += 2
                    else: decision = 'Non Admissible'
                if enfants > 3:
                    if emploi == 0: score += 0
                    else: decision = 'Non Admissible'
                
                if dureePret < 10: score += 6
                elif 10 <= dureePret < 15: score += 4
                elif 15 <= dureePret < 20: score += 2
                elif 20 <= dureePret < 25: score += 1
                elif dureePret >= 25: decision = 'Non Admissible'
                
                if montantPret < 100000: score += 6
                elif 100000 <= montantPret < 150000: score += 4
                elif 150000 <= montantPret < 200000: score += 2
                elif 200000 <= montantPret < 250000: score += 1
                elif montantPret >= 250000: decision = 'Non Admissible'
                    
                if antecedents == 0: score += 6
                elif antecedents == 1: score += 4
                elif antecedents == 2: score += 1
                elif antecedents == 3: score += 0
                elif antecedents >= 4: decision = 'Non Admissible'
                
            if score != -1:       
                if 30 < score <= 40:
                    if decision != 'Non Admissible': decision = 'Tres favorable'
                elif 20 < score <= 30:
                    if decision != 'Non Admissible': decision = 'Sous conditions'
                elif 10 < score <= 20:
                    if decision != 'Non Admissible': decision = 'A defendre'
                elif 0 <= score <= 10:
                    if decision != 'Non Admissible': decision = 'Peu probable'
        
            
        #Ecriture dans la BD
        connexion = sqlite3.connect('evaluationPret.db')
        cursor = connexion.cursor()
        
        cursor.execute("UPDATE EVALUATION SET score = ?, decisionScore = ? WHERE idEvaluation = ?", (score, decision, idEvaluation))
        
        connexion.commit()
        connexion.close()
        
    
    
    def verifier(idEvaluation : int):
        lien = serviceVerificationSolvabilite.creationDBBanque()
        donnees = serviceVerificationSolvabilite.recupDonnees(lien, idEvaluation)
        ret=serviceVerificationSolvabilite.calculScoring(donnees, idEvaluation)
        