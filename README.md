# Projet Evaluation des demandes de prêts immobiliers 

## Configurer l'environnement virtuel et ajouter les dépendances nécessaires

`chmod 774 ./configure`

`./configure`

## Lancer le serveur Flask et l'interface web

`chmod 774 ./run`

`./run`

L'interface est accessible à `http://localhost:8000`

## Interface

### Dépôt d'un dossier de prêt

![](https://github.com/Clem0908/Usefull_bash_scripts/blob/main/depot_dossier.gif)

### Récupération des résultats : acceptation de demande de prêt

![](https://github.com/Clem0908/Usefull_bash_scripts/blob/main/recup_dossier.gif)

### Récupération des résultats : refus de demande de prêt

![](https://github.com/Clem0908/Usefull_bash_scripts/blob/main/refus.gif)

## Scénario 

### Profil parfait

#### Formulaire
```
Nom : Paul Gauthier  
Adresse : 12 Rue du Pont Neuf, 91120 Palaiseau, France  
Email : paul.gauthier@email.com  
Numéro de téléphone : 01 12 23 34 45  
Montant du pret : 160000  
Duree du pret : 10  
Description de la propriete : Appartement a 6 etages avec un petit balcon  
Revenus mensuel : 12000  
Depenses mensuelles : 2000  
Compte bancaire : 33  
Identifiant propriété : 3  
```

#### Résultat

```
Score : 32
Decision Score : Très favorable
Decision Conformité : Admissible a un pret immobilier
Raisons : /
EstimationValeur: 148000
=> DEMANDE DE PRÊT ACCEPTEE
```
### Profil emploi instable

#### Formulaire

```
Nom : Jack Daniel  
Adresse : 52 Avenue de la gare, 91120 Palaiseau, France  
Email : jack.daniel@email.com  
Numéro de téléphone : 01 12 23 34 46  
Montant du pret : 130000  
Duree du pret : 15  
Description de la propriete : Appartement de 5 etages  
Revenus mensuel : 7000  
Depenses mensuelles : 3000  
Compte bancaire : 44  
Identifiant propriété : 4  
```

#### Résultat
```
Score : 27
Decision Score : Sous condition
Decision Conformité : Admissible a un pret immobilier
Raisons : /
EstimationValeur: 135000
=> DEMANDE DE PRÊT ACCEPTEE
```

### Profil score trop faible

#### Formulaire
```
Nom : Victor Wolf  
Adresse : 39 Rue Geais Padidee, 91120 Palaiseau, France  
Email : victor.wolf@email.com  
Numéro de téléphone : 01 12 23 34 47  
Montant du pret : 70000  
Duree du pret : 25    
Description de la propriete : Maison avec deux etages et un grand jardin  
Revenus mensuel : 10000  
Depenses mensuelles : 6000   
Compte bancaire : 55  
Identifiant propriété : 5  
```
#### Résultat
```
Score : 12
Decision Score : Non Admissible
Decision Conformité : Admissible a un pret immobilier
Raisons : Score pas suffisant
EstimationValeur: 200000
=> DEMANDE DE PRÊT REFUSEE
```