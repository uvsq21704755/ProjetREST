# serviceDecisionApprobation.py : service permettant de générer une décision en fonction du score de Verification Solvabilité et de la décision de Evaluation Propriété

# Importation des librairies extérieures
import sqlite3



class serviceDecisionApprobation:
    
    def recupBD(idEvaluation):
        
        connexion = sqlite3.connect('evaluationPret.db')
        cursor = connexion.cursor()
        
        cursor.execute("SELECT idDossier, nom, montantPret, dureePret, score, decisionScore, decisionConformite, estimationValeur, raison FROM EVALUATION WHERE idEvaluation = ?", (idEvaluation,))
        resultats = cursor.fetchone()

        donnees=[]
        
        for i in range(0,len(resultats)):
            donnees.append(resultats[i])
            
        connexion.commit()
        connexion.close()
                
        return donnees
    
    
    def decision(donnees,idEvaluation):
        
        numDossier = donnees[0]
        nom = donnees[1]
        montantPret = int(donnees[2])
        dureePret = donnees[3]
        score = donnees[4]
        decisionScore = donnees[5]
        decisionConformite = donnees[6]
        estimationValeur = donnees[7]
        raisons = donnees[8]
            
        motif = "inconnu"
        test = -1
        
        if score == -1:
            motif = "à cause de votre situation financière actuelle"
            test = 0
            
        if decisionConformite == 'Non admissible a un pret immobilier':
            motif = "pour cette adresse immobilière pour la/les raison.s suivante.s :" + raisons
            test = 0
        
        if estimationValeur != None:    
            if montantPret > (int(estimationValeur) + 10000):
                motif = "votre demande est supérieure à la moyenne du marché pour un batiment du même type et dans le même secteur"
                test = 0
        
        if decisionScore == 'Tres favorable' and decisionConformite == 'Admissible a un pret immobilier':
            test = 1
            
        elif decisionScore == 'Sous conditions' and decisionConformite == 'Admissible a un pret immobilier' :
            test = 1

        elif decisionScore == 'A defendre' and decisionConformite == 'Admissible a un pret immobilier':
            test = 1
            
        else:
            motif = "votre score n'est pas suffisant"
            test = 0
            
        connexion = sqlite3.connect('evaluationPret.db')
        cursor = connexion.cursor()
        cursor.execute("SELECT idDossier FROM EVALUATION WHERE idEvaluation = ?", (idEvaluation,))
        idDossier = cursor.fetchone()
        
        acceptation = "Bonjour [nom],$ Félicitations, votre demande de prêt numéro [numeroDossier] a bien été <vert>approuvée</vert>. $Veuillez trouver les modalités suivantes à respecter: $- Montant de prêt accordé : [montantPret] $- Durée du prêt : [dureePret]"
        refus = "Bonjour [nom],$ Nous sommes dans le regret de vous annoncer que votre demande de prêt numéro [numeroDossier] a été <rouge>refusée</rouge> pour le/les motif(s) suivant(s): $[motifs]"
        
        if (test == 0):
            resultat = refus
            resultat = resultat.replace("[nom]", str(nom))
            resultat = resultat.replace("[numeroDossier]", str(numDossier))
            resultat = resultat.replace("[motifs]", str(motif))
        
        else :
            resultat = acceptation
            resultat = resultat.replace("[nom]", str(nom))
            resultat = resultat.replace("[numeroDossier]", str(numDossier))
            resultat = resultat.replace("[montantPret]", str(montantPret)+" euros")
            resultat = resultat.replace("[dureePret]", str(dureePret)+" ans")

        cursor.execute("INSERT INTO RESULTAT (idDossier, resultat) VALUES (?,?)",(idDossier[0], str(resultat),))
        
        connexion.commit()
        connexion.close()
        

    def decider(idEvaluation : int):
        donnees = serviceDecisionApprobation.recupBD(idEvaluation)
        serviceDecisionApprobation.decision(donnees, idEvaluation)