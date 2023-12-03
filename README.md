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
Montant du pret : 160000 EUR  
Duree du pret : 10 ans  
Description de la propriete : Appartement a 6 etages avec un petit balcon  
Revenus mensuel : 12000 EUR  
Depenses mensuelles : 2000 EUR  
Compte bancaire : 33  
Identifiant propriété : 3  
```

#### Résultat

```
Score: 32 => Décision Très favorable
Valeur estimée : 148000
Décision conformité : Admissible a un pret immobilier
Visite virtuelle demandée et effectuée, Visite sur place concluante OU Visite virtuelle non demandée et non effectuée Visite sur place non demandée et non effectuée
Décision: Demande de prêt acceptée
```
### Profil emploi instable

#### Formulaire

```
Nom : Jack Daniel
Adresse : 52 Avenue de la gare, 91120 Palaiseau, France
Email : jack.daniel@email.com
Numéro de téléphone : 01 12 23 34 46
Montant du pret : 130000 EUR
Duree du pret : 15 ans
Description de la propriete : Appartement de 5 etages
Revenus mensuel : 7000 EUR
Depenses mensuelles : 3000 EUR
Compte bancaire : 44
Identifiant propriété : 4
```

#### Résultat
```
Score: 27 => Décision Sous condition
Valeur estimée: 135000
Décision conformité : Admissible a un pret immobilier
Visite virtuelle non demandée et non effectuée Visite sur place non demandée et non effectuée OU Visite virtuelle demandée et effectuée Visite sur place concluante
Decision: Demande de prêt acceptée
```

### Profil score trop faible

#### Formulaire
```
Nom : Victor Wolf
Adresse : 39 Rue Geais Padidee, 91120 Palaiseau, France
Email : victor.wolf@email.com
Numéro de téléphone : 01 12 23 34 47
Montant du pret : 25000 EUR
Duree du pret : 5 ans
Description de la propriete : Maison avec deux etages et un grand jardin
Revenus mensuel : 10000 EUR
Depenses mensuelles : 4000 EUR
Compte bancaire : 55
Identifiant propriété : 5
```
#### Résultat
```
Score: 12 => Décision Non Admissible
Valeur estimée: 200000
Décision conformité: Admissible a un pret immobilier
Visite virtuelle non demandée et non effectuée Visite sur place non demandée et non effectuée OU Visite virtuelle demandée et effectuée Visite sur place non demandée et non effectuée
Décision: Demande de prêt refusée - votre score n'est pas suffisant
```