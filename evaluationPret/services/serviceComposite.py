# serviceComposite.py : service permettant d'orchestrer les communications avec les autres services

# Importation des librairies extérieures
from flask import Flask, render_template, request
import sqlite3
import requests



CHEMIN_RACINE = "./evaluationPret/services/"



class serviceComposite:

    def creerBD():

        connexion = sqlite3.connect('evaluationPret.db')
        curseur = connexion.cursor()
        
        curseur.execute('DROP TABLE IF EXISTS DEMANDE')
        curseur.execute('''
                        CREATE TABLE IF NOT EXISTS DEMANDE (
                        idDossier INTEGER PRIMARY KEY,
                        formulaire TEXT)
                        ''')
        
        curseur.execute('DROP TABLE IF EXISTS EVALUATION')
        curseur.execute('''
                        CREATE TABLE IF NOT EXISTS EVALUATION (
                        idEvaluation INTEGER PRIMARY KEY,
                        idDossier INTEGER,
                        nom TEXT,
                        adresse TEXT,
                        email TEXT,
                        telephone TEXT,
                        montantPret INTEGER,
                        dureePret INTEGER,
                        descriptionPropriete TEXT,
                        revenuMensuel INTEGER,
                        depenseMensuelle INTEGER,
                        idBanque INTEGER,
                        idPropriete INTEGER,
                        score INTEGER,
                        decisionScore TEXT,
                        decisionConformite TEXT,
                        raison TEXT,
                        estimationValeur INTEGER)
                        ''')
        
        curseur.execute('DROP TABLE IF EXISTS RESULTAT')
        curseur.execute('''
                        CREATE TABLE IF NOT EXISTS RESULTAT (
                        idDossier INTEGER PRIMARY KEY,
                        resultat TEXT)
                        ''')
        

        connexion.commit()
        connexion.close()

        
    def lancerEvaluationPret(idDossier, formulaire):

        print("\n\n*****************************Nouvelle demande n°"+str(idDossier)+"*****************************")

        # Envoi de l'idDossier et formulaire à Extraction
        print("-- Service Extraction commencée --")
        
        serviceExtractionUrl = "http://127.0.0.1:8000/serviceExtraction"
        jsonPost = {"idDossier": idDossier, "formulaire": formulaire}
        headers = {"Content-Type":"application/json"}
        reponse = requests.post(serviceExtractionUrl, json=jsonPost, headers=headers)
        
        if reponse.status_code != 200:
            print("Endpoint serviceExtraction non OK")
    
        
        # Reception de l'idEvaluation d'Extraction
        serviceCompositeEvalUrl = "http://127.0.0.1:8000/serviceCompositeEval"
        reponse = requests.get(serviceCompositeEvalUrl, headers=headers)
        
        if reponse.status_code != 200:
            print("Endpoint serviceComposite non OK") 

        idEvaluationReponse = reponse.json()
        idEvaluation = idEvaluationReponse.get('idEvaluation')
        
        print("-- Service Extraction terminée --")
        
        
        # Envoi de l'idEvaluation à Verification Solvabilité
        print("-- Service Verification Solvabilité commencée --")

        serviceVerificationSolvabiliteUrl = "http://127.0.0.1:8000/serviceVerificationSolvabilite"
        jsonPost = {"idEvaluation": idEvaluation}
        reponse = requests.post(serviceVerificationSolvabiliteUrl, json=jsonPost, headers=headers)
        
        if reponse.status_code != 200:
            print("Endpoint serviceVerificationSolvabilite non OK")
        
        print("-- Service Verification Solvabilité terminée --")
        
        
        # Envoi de l'idEvaluation à Evaluation Proprieté
        print("-- Service Evaluation Propriete commencée --")
        
        serviceEvaluationProprieteUrl = "http://127.0.0.1:8000/serviceEvaluationPropriete"
        jsonPost = {"idEvaluation": idEvaluation}
        reponse = requests.post(serviceEvaluationProprieteUrl, json=jsonPost, headers=headers)
        
        if reponse.status_code != 200:
            print("Endpoint serviceEvaluationPropriete non OK")
        
        print("-- Service Evaluation Propriété terminée --")
        
        
        # Envoi de l'idEvaluation à Decision
        print("-- Service Décision commencée --")
        
        serviceDecisionApprobationUrl = "http://127.0.0.1:8000/serviceDecisionApprobation"
        jsonPost = {"idEvaluation": idEvaluation}
        reponse = requests.post(serviceDecisionApprobationUrl, json=jsonPost, headers=headers)
        
        if reponse.status_code != 200:
            print("Endpoint serviceDecision non OK")
        
        print("-- Service Décision terminée --")


    def recupererDossier(idDossier):

        connexion = sqlite3.connect('evaluationPret.db')
        curseur = connexion.cursor()
        curseur.execute('SELECT formulaire FROM DEMANDE WHERE idDossier = ?', (idDossier,))
        resultat = curseur.fetchone()
        connexion.close()

        if resultat:
            serviceComposite.lancerEvaluationPret(idDossier, resultat[0])
