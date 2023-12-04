# Service permettant de prendre une décision en fonction du score et de l'évaluation de la propriété

import sqlite3
# Importation du service composite
import serviceComposite


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
        estimationValeur = int(donnees[7])
        raisons = donnees[8]
            
    
        # Refus sans plus d'analyses :
        motif = "inconnu"
        test = -1
        
        if score == -1:
            motif = "à cause de votre situation financière actuelle"
            test = 0
            
        if decisionConformite == 'Non admissible a un pret immobilier':
            motif = "pour cette adresse immobilière pour la/les raison.s suivante.s :" + raisons
            test = 0
            
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
            
        
        #Trouver le idDossier
        connexion = sqlite3.connect('evaluationPret.db')
        cursor = connexion.cursor()
        cursor.execute("SELECT idDossier FROM EVALUATION WHERE idEvaluation = ?", (idEvaluation,))
        idDossier = cursor.fetchone()
        
        
        #Créer le résultat
        acceptation = "Bonjour [nom],$ Félicitations, votre demande de prêt numéro [numeroDossier] a bien été <vert>approuvée</vert>. $Veuillez trouver les modalités suivantes à respecter: $- Montant de prêt accordé : [montantPret] $- Durée du prêt : [dureePret]"
        refus = "Bonjour [nom],$ Nous sommes dans le regret de vous annoncer que votre demande de prêt numéro [numeroDossier] a été <rouge>refusée</rouge> pour le/les motif(s) suivant(s): $[motifs]"
        
        #refus
        if (test == 0):
            resultat = refus
            resultat = resultat.replace("[nom]", str(nom))
            resultat = resultat.replace("[numeroDossier]", str(numDossier))
            resultat = resultat.replace("[motifs]", str(motif))
        
        #acceptation
        else :
            resultat = acceptation
            resultat = resultat.replace("[nom]", str(nom))
            resultat = resultat.replace("[numeroDossier]", str(numDossier))
            resultat = resultat.replace("[montantPret]", str(montantPret)+" euros")
            resultat = resultat.replace("[dureePret]", str(dureePret)+" ans")

        #Creation d'un nouveau tuple(idDossier, resultat) dans RESULTAT
        cursor.execute("INSERT INTO RESULTAT (idDossier, resultat) VALUES (?,?)",(idDossier[0], str(resultat),))
        
        connexion.commit()
        connexion.close()
        

    
    def decider(idEvaluation : int):
        donnees = serviceDecisionApprobation.recupBD(idEvaluation)
        serviceDecisionApprobation.decision(donnees, idEvaluation)