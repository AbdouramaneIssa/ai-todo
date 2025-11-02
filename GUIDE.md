# Guide d'Utilisation - To-Do List avec Qualité de Code

## 📋 Vue d'Ensemble

Ceci est une application **To-Do List** complète avec :
- Backend Python/Flask typé (Mypy)
- Frontend HTML/CSS/JavaScript moderne
- Base de données SQLite
- Vérification de qualité de code (Flake8, Mypy)
- Hooks pre-commit pour les vérifications locales

## 🚀 Installation sur Windows

### 1. Créer un Environnement Virtuel

```bash
python -m venv venv
.\venv\Scripts\activate
```

Vous devez voir `(venv)` au début de votre ligne de commande.

### 2. Installer les Dépendances

```bash
pip install -r requirements.txt
```

### 3. Configurer Pre-commit (Optionnel)

```bash
pre-commit install
```

## ▶️ Lancer l'Application

```bash
python app.py
```

Ouvrez votre navigateur et allez à : **http://localhost:5000**

## 🧪 Tester l'API avec curl

### Récupérer toutes les tâches

```bash
curl http://localhost:5000/api/todos
```

### Créer une tâche

```bash
curl -X POST http://localhost:5000/api/todos ^
  -H "Content-Type: application/json" ^
  -d "{\"title\": \"Ma tâche\", \"description\": \"Description\"}"
```

### Marquer comme complétée

```bash
curl -X PUT http://localhost:5000/api/todos/1 ^
  -H "Content-Type: application/json" ^
  -d "{\"completed\": true}"
```

### Supprimer une tâche

```bash
curl -X DELETE http://localhost:5000/api/todos/1
```

## ✅ Vérifier la Qualité du Code

### Mypy (Typage)

```bash
mypy app.py models.py database.py --config-file=mypy.ini
```

Résultat attendu : `Success: no issues found in 3 source files`

### Flake8 (Style)

```bash
flake8 app.py models.py database.py --config=setup.cfg
```

Résultat attendu : Aucune sortie (tout est bon)

## 📁 Structure du Projet

```
todo_app/
├── app.py                 # Application Flask
├── models.py              # Modèles typés
├── database.py            # Gestion SQLite
├── requirements.txt       # Dépendances
├── setup.cfg              # Config Flake8
├── mypy.ini               # Config Mypy
├── .pre-commit-config.yaml # Hooks locaux
├── templates/
│   └── index.html         # Interface web
└── static/
    ├── css/
    │   └── style.css      # Styles
    └── js/
        └── app.js         # Logique JavaScript
```

## 🎯 Fonctionnalités

- ✅ Ajouter une tâche avec titre et description
- ✅ Marquer une tâche comme complétée
- ✅ Supprimer une tâche
- ✅ Voir toutes les tâches en temps réel
- ✅ Persistance en base de données SQLite

## 🔧 Dépannage

**Erreur : "python n'est pas reconnu"**
- Réinstallez Python en cochant "Add Python to PATH"

**Erreur : "Module not found"**
- Assurez-vous que l'environnement virtuel est activé
- Réinstallez les dépendances : `pip install -r requirements.txt`

**Port 5000 déjà utilisé**
- Modifiez le port dans `app.py` : `app.run(port=5001)`

## 📚 Ressources

- Flask : https://flask.palletsprojects.com/
- Mypy : https://mypy.readthedocs.io/
- Flake8 : https://flake8.pycqa.org/

Bon développement ! 🚀
