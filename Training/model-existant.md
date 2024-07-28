# Algorithmes de base en Machine Learning 
__________________
## 1. Apprentissage supervisé
Régression

- Régression linéaire
- Régression logistique
- Régression polynomiale
- Régression par arbres de décision

Classification

- K plus proches voisins (K-NN)
- Machines à vecteurs de support (SVM)
- Arbres de décision
- Forêts aléatoires
- Classificateur bayésien naïf

## 2. Apprentissage non supervisé
Clustering

- K-means
- DBSCAN (Density-Based Spatial Clustering of Applications with Noise)
- Clustering hiérarchique

Réduction de dimensionnalité

- Analyse en composantes principales (PCA)
- t-SNE (t-distributed Stochastic Neighbor Embedding)

## 3. Apprentissage par renforcement

- Q-Learning
- SARSA (State-Action-Reward-State-Action)

## 4. Réseaux de neurones et Deep Learning

- Perceptron multicouche
- Réseaux de neurones convolutifs (CNN)
- Réseaux de neurones récurrents (RNN)
- Long Short-Term Memory (LSTM)

## 5. Ensemble Learning

- Bagging
- Boosting (AdaBoost, Gradient Boosting)
- Stacking

## 6. Autres

- Algorithmes génétiques
- Machines de Boltzmann
- Processus gaussiens


--------------------------
> On va faire le choix d'algorithme par ce qui adapte vraiment au besoin du projet et les données, et après par  le meilleur scoring.
>
> Notre dataset est en fonction de temps donc on a besoin d'une algorithme temporelle pour la modélisation

## trois algorithmes sont particulièrement bien adaptés à notre jeu de données pour les raisons suivantes :

> Nature des données  :*On a des variables numériques continues (température, humidité) et des variables catégorielles (classes de température et d'humidité). Ces algorithmes peuvent gérer efficacement ce type de données mixtes.*
> 
> Taille du dataset 
> 
> Objectif de classification : *Une classification multi-classes, ou simple, la notre est la première.*
> 
> Interprétabilité : *Il est crucial de comprendre les facteurs influençant la classification des conditions environnementales.Notre modèles, en particulier la régression logistique et l'arbre de décision, offrent une bonne interprétabilité.*
> 
> Performances avec peu de caractéristiques : *Notre données n'ont que deux caractéristiques principales (température et humidité).*
>
> Donc notre choix sont :
> - Régression logistique multinomiale
> - Arbre de décision
> - K plus proches voisins (K-NN)