# Service permettant d'extraire les informations utiles
import re, sqlite3, random, requests

# Importation du service composite
import serviceComposite


class serviceExtraction:

    def extraire(idDossier: int, formulaire: str):
        
        connexion = sqlite3.connect('evaluationPret.db')
        cursor = connexion.cursor()
        
        # random int idEvaluation
        exist = 1
        while(exist):
            idEvaluation = random.randint(0,1000000)
            cursor.execute("SELECT * FROM EVALUATION WHERE idEvaluation = ?", (idEvaluation,))
            resultats = cursor.fetchall()

            if(len(resultats) == 0) :
                break
        
        # parse formulaire 
        infosExtraites = re.findall(r'(?<=:\s)[a-zA-ZàéÉ0-9\'\,\-\sA-Z@.]+\n', formulaire)
        for i in range(0,len(infosExtraites)):
            infosExtraites[i] = infosExtraites[i].replace("\n",'')
        
        # INSERT INTO EVALUATION
        cursor.execute("INSERT INTO EVALUATION (idEvaluation, idDossier, nom, adresse, email, telephone, montantpret, dureepret, descriptionpropriete, revenumensuel, depensemensuelle, idbanque, idpropriete) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",(idEvaluation, idDossier, infosExtraites[0], infosExtraites[1], infosExtraites[2], infosExtraites[3], infosExtraites[4], infosExtraites[5], infosExtraites[6], infosExtraites[7], infosExtraites[8], infosExtraites[9], infosExtraites[10]))
        
        connexion.commit()
        connexion.close()
        
        serviceCompositeEvalUrl = "http://127.0.0.1:8000/serviceCompositeEval"
        jsonPost = {"idEvaluation": idEvaluation}
        headers = {"Content-Type":"application/json"}
        reponse = requests.post(serviceCompositeEvalUrl, json=jsonPost, headers=headers)
        
        if reponse.status_code != 200:
            print("Endpoint serviceCompositeEval non OK")

        return
