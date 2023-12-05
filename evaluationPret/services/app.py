# Interface
from flask import Flask, render_template, request, jsonify
from flask_restful import Resource, Api
import sqlite3
import random
import threading
import os


# Importation des services
from serviceComposite import serviceComposite
from serviceExtraction import serviceExtraction
from serviceVerificationSolvabilite import serviceVerificationSolvabilite
from serviceEvaluationPropriete import serviceEvaluationPropriete
from serviceDecisionApprobation import serviceDecisionApprobation





CHEMIN_RACINE = "./evaluationPret/services/"




class App():

    # creation de l'interface web
    def creerInterfaceWeb():

        serviceComposite.creerBD()

        app = Flask(__name__)

        @app.route('/')
        def pageAccueil():
            return render_template('accueil.html')

        @app.route('/connexion.html')
        def pageConnexion():
            return render_template('connexion.html')

        @app.route('/formulaire.html')
        def pageFormulaire():
            return render_template('formulaire.html')

        @app.route('/confirmation.html')
        def pageConfirmation():
            return render_template('confirmation.html')

        @app.route('/disponible.html')
        def pageDisponible():
            return render_template('disponible.html')

        @app.route('/traitement.html')
        def pageTraitement():
            return render_template('traitement.html')

        @app.route('/introuvable.html')
        def pageIntrouvable():
            return render_template('introuvable.html')



        @app.route('/enregistrer', methods=['POST'])
        def enregistrer():
            # connexion à la BD
            connexion = sqlite3.connect('evaluationPret.db')
            cursor = connexion.cursor()

            # recuperation du formulaire
            nom = request.form['nom']
            adresse = request.form['adresse']
            email = request.form['email']
            telephone = request.form['telephone']
            montantpret = request.form['montantpret']
            dureepret = request.form['dureepret']
            descriptionpropriete = request.form['descriptionpropriete']
            revenumensuel = request.form['revenumensuel']
            depensemensuelle = request.form['depensemensuelle']
            idbanque = request.form['idbanque']
            idpropriete = request.form['idpropriete']

            # trouver un id de dossier non existant
            exist = 1

            while(exist):

                idDossier = random.randint(0,1000000)

                cursor.execute("SELECT * FROM DEMANDE WHERE idDossier = ?", (idDossier,))
                resultats = cursor.fetchall()

                if(len(resultats) == 0) :
                    break


            # préparer le texte pour formulaire

            form = "Nom du Client: " + nom + "\nAdresse: " + adresse + "\nEmail: " + email + "\nNuméro de Téléphone: " + telephone + "\nMontant du Prêt Demandé: " + montantpret + "\nDurée du Prêt: " + dureepret + "\nDescription de la Propriété: " + descriptionpropriete + "\nRevenu Mensuel: " + revenumensuel + "\nDépenses Mensuelles: " + depensemensuelle + "\nNuméro de compte bancaire: " + idbanque + "\nRéférence de la propriété: " + idpropriete + "\n"

            # insertion du tuple avec idDossier et form dans DEMANDE
            cursor.execute("INSERT INTO DEMANDE (idDossier, formulaire) VALUES (?,?)",(idDossier,form))

            # affichage de la page de confirmation avec le numéro de dossier
            htmlResponse = open(CHEMIN_RACINE+"templates/confirmation.html","r",encoding="UTF-8")
            strHtmlResponse = htmlResponse.read()
            strHtmlResponse = strHtmlResponse.replace("123456789", str(idDossier))
            htmlResponse.close()


            # démarrage du serviceComposite pour la nouvelle demande
            thread = threading.Thread(target=serviceComposite.recupererDossier, args=(idDossier,))
            thread.start()

            #fermeture de la base de données
            connexion.commit()
            connexion.close()

            # Retourne la page web réponse à l'interface
            return strHtmlResponse



        @app.route('/resultat', methods=['POST'])
        def resultat():
            numerodossier = request.form['numerodossier']

            connexion = sqlite3.connect('evaluationPret.db')
            curseur = connexion.cursor()

            curseur.execute('SELECT formulaire FROM DEMANDE WHERE idDossier = ?', (numerodossier,))
            resultat = curseur.fetchone()

            #if(len(resultat) == 0):
            if(resultat == None):
                connexion.close()
                return open(str(CHEMIN_RACINE+"templates/introuvable.html"),"r", encoding="UTF-8").read()

            else:
                curseur.execute('SELECT resultat FROM RESULTAT WHERE idDossier = ?', (numerodossier,))
                resultat2 = curseur.fetchone()

                #if(len(resultat2) == 0):
                if(resultat2 == None):
                    connexion.close()
                    return open(str(CHEMIN_RACINE+"templates/traitement.html"),"r", encoding="UTF-8").read()

                else:
                    connexion.close()
                    valcat = ', '.join(map(str, resultat2))
                    valcat = valcat.replace("$","<br></br>")
                    return open(str(CHEMIN_RACINE+"templates/disponible.html"),"r", encoding="UTF-8").read().replace("REPONSE", valcat)

            return None


        @app.route('/serviceExtraction', methods=['POST'])
        def getDemande():
            recuServiceComposite = request.get_json()
            serviceExtraction.extraire(recuServiceComposite.get('idDossier'), recuServiceComposite.get('formulaire'))

            return jsonify(recuServiceComposite)

        @app.route('/serviceCompositeEval', methods=['GET', 'POST'])
        def getEvaluation():
            if request.method == 'POST':
                recupServiceExtraction = request.get_json()
                idEvaluation = recupServiceExtraction.get('idEvaluation')

                with open(CHEMIN_RACINE+"tmp/idEval.txt", "w") as f:
                    f.write(f'{idEvaluation}')
                f.close()
                
            elif request.method == 'GET':
                
                with open(CHEMIN_RACINE+"tmp/idEval.txt", "r") as f:
                    idEvaluation = f.read()
                f.close()
                return {"idEvaluation" : idEvaluation}

            else:
                print("Méthode non autorisée")

            return jsonify(recupServiceExtraction)
        
        @app.route('/serviceVerificationSolvabilite', methods=['POST'])
        def getEvaluation1():
            recuServiceComposite = request.get_json()
            serviceVerificationSolvabilite.verifier(recuServiceComposite.get('idEvaluation'))

            return jsonify(recuServiceComposite)
        
        @app.route('/serviceEvaluationPropriete', methods=['POST'])
        def getEvaluation2():
            recuServiceComposite = request.get_json()
            serviceEvaluationPropriete.evaluer(recuServiceComposite.get('idEvaluation'))

            return jsonify(recuServiceComposite)
        
        @app.route('/serviceDecisionApprobation', methods=['POST'])
        def getEvaluation3():
            recuServiceComposite = request.get_json()
            serviceDecisionApprobation.decider(recuServiceComposite.get('idEvaluation'))

            return jsonify(recuServiceComposite)

        return app




if __name__ == '__main__':

    app = App.creerInterfaceWeb()
    app.run(debug=True, port=8000)
