"""Script de vérification de code et notification par email via Gemini API.

Ce script exécute Mypy et Flake8, puis utilise l'API Gemini pour générer
un email HTML professionnel avec les résultats de l'analyse.
"""

import os
import sys
import smtplib
import subprocess
from typing import Tuple
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from google import genai


# Configuration - Récupération des secrets via les variables d'environnement
GEMINI_API_KEY: str = os.environ.get("GEMINI_API_KEY", "")
GMAIL_APP_PASSWORD: str = os.environ.get("GMAIL_APP_PASSWORD", "")
SENDER_EMAIL: str = os.environ.get("SENDER_EMAIL", "")

# Récupération des paramètres
if len(sys.argv) < 3:
    print("Erreur: L'email du destinataire et la liste des fichiers modifiés sont requis.")
    sys.exit(1)

RECIPIENT_EMAIL: str = sys.argv[1]
CHANGED_FILES: list = sys.argv[2].split()


def get_file_content(file_path: str) -> str:
    """Lit le contenu d'un fichier (max 100 lignes)."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content: str = "".join(f.readlines()[:100])
        return f"--- Contenu du fichier: {file_path} ---\n{content}\n"
    except Exception as e:
        return f"--- Impossible de lire le fichier: {file_path} (Erreur: {e}) ---\n"


def run_mypy_verification() -> Tuple[bool, str]:
    """Exécute la vérification Mypy et retourne le résultat."""
    print("Début de la vérification Mypy...")
    try:
        result = subprocess.run(
            ['mypy', 'app.py', 'models.py', 'database.py', 'untyped_example.py',
             '--config-file=mypy.ini'],
            capture_output=True,
            text=True,
            check=False
        )

        mypy_success: bool = result.returncode == 0
        mypy_report: str = result.stdout if result.stdout else result.stderr

        print(f"Vérification Mypy terminée. Succès: {mypy_success}")

        return mypy_success, mypy_report

    except FileNotFoundError:
        msg = "Erreur: La commande 'mypy' n'a pas été trouvée."
        return False, msg
    except Exception as e:
        msg = f"Erreur inattendue lors de l'exécution de Mypy: {e}"
        return False, msg


def run_flake8_verification() -> Tuple[bool, str]:
    """Exécute la vérification Flake8 et retourne le résultat."""
    print("Début de la vérification Flake8...")
    try:
        result = subprocess.run(
            ['flake8', 'app.py', 'models.py', 'database.py', 'untyped_example.py',
             '--config=setup.cfg'],
            capture_output=True,
            text=True,
            check=False
        )

        flake8_success: bool = result.returncode == 0
        flake8_report: str = result.stdout if result.stdout else "Aucune erreur"

        print(f"Vérification Flake8 terminée. Succès: {flake8_success}")

        return flake8_success, flake8_report

    except FileNotFoundError:
        msg = "Erreur: La commande 'flake8' n'a pas été trouvée."
        return False, msg
    except Exception as e:
        msg = f"Erreur inattendue lors de l'exécution de Flake8: {e}"
        return False, msg


def generate_prompt(
    changed_files: list,
    mypy_report: str,
    flake8_report: str
) -> str:
    """Génère le prompt pour l'IA Gemini."""

    mypy_section: str = (
        "--- Rapport de Vérification Mypy ---\n"
        f"{mypy_report}\n"
        "------------------------------------\n\n"
    )

    flake8_section: str = (
        "--- Rapport de Vérification Flake8 ---\n"
        f"{flake8_report}\n"
        "--------------------------------------\n\n"
    )

    prompt: str = (
        "Vous êtes un expert en revue de code Python. Analysez les résultats des vérifications "
        "Mypy (typage) et Flake8 (style) ci-dessous. "
        "Si des erreurs sont présentes, expliquez-les clairement et proposez des corrections. "
        "Si tout est bon, félicitez le développeur et proposez des bonnes pratiques. "
        "Générez une réponse UNIQUEMENT sous forme de code HTML complet et professionnel "
        "pour un email. Le HTML doit avoir un design moderne avec CSS en ligne, "
        "une palette de couleurs agréable (bleu, vert, gris), et être responsive. "
        "Utilisez des emojis pour améliorer la lisibilité. "
        "Le HTML doit commencer par <!DOCTYPE html> et être complet.\n\n"
        f"{mypy_section}"
        f"{flake8_section}"
        "--- Fichiers Modifiés ---\n"
    )

    for file in changed_files:
        if file.startswith('.github/') or file.endswith(('.png', '.jpg', '.gif')):
            continue
        prompt += get_file_content(file)

    return prompt


def get_ai_review(prompt: str) -> str:
    """Appelle l'API Gemini pour obtenir la revue de code HTML."""
    try:
        client = genai.Client(api_key=GEMINI_API_KEY)

        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=prompt
        )

        html_content: str = response.text.strip()
        if html_content.startswith("```html"):
            html_content = html_content.strip("```html").strip("```").strip()

        return html_content

    except Exception as e:
        error_msg = f"Impossible d'obtenir la revue de code. Erreur: {e}"
        return f"<h1>Erreur d'API Gemini</h1><p>{error_msg}</p>"


def send_email(recipient: str, subject: str, html_body: str) -> None:
    """Envoie l'email HTML via SMTP (Gmail)."""
    try:
        msg = MIMEMultipart('alternative')
        msg['From'] = SENDER_EMAIL
        msg['To'] = recipient
        msg['Subject'] = subject

        msg.attach(MIMEText(html_body, 'html'))

        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(SENDER_EMAIL, GMAIL_APP_PASSWORD)

        server.sendmail(SENDER_EMAIL, recipient, msg.as_string())
        server.close()

        print(f"Succès: Email envoyé à {recipient}")

    except Exception as e:
        print(f"Erreur: Échec de l'envoi de l'email. Erreur: {e}")
        print("\n--- Contenu HTML (pour débogage) ---\n")
        print(html_body)


# --- Logique principale ---

print(f"Début de l'analyse pour: {RECIPIENT_EMAIL}")
print(f"Fichiers modifiés: {', '.join(CHANGED_FILES)}")

# 1. Exécuter les vérifications
mypy_success, mypy_report = run_mypy_verification()
flake8_success, flake8_report = run_flake8_verification()

# Déterminer le succès global
global_success: bool = mypy_success and flake8_success

# 2. Préparer le prompt pour l'IA
review_prompt: str = generate_prompt(CHANGED_FILES, mypy_report, flake8_report)

# 3. Obtenir la revue de l'IA
if global_success:
    email_subject: str = "✅ Revue de Code Automatisée - Succès"
else:
    email_subject: str = "❌ Revue de Code Automatisée - Erreurs Détectées"

html_review: str = get_ai_review(review_prompt)

# 4. Envoyer l'email
send_email(RECIPIENT_EMAIL, email_subject, html_review)

# 5. Déterminer le code de sortie
if not global_success:
    print("Échec des vérifications. Le push est bloqué.")
    if not mypy_success:
        print("\n--- Rapport Mypy ---\n")
        print(mypy_report)
    if not flake8_success:
        print("\n--- Rapport Flake8 ---\n")
        print(flake8_report)
    sys.exit(1)
else:
    print("Vérifications réussies. Le push est accepté.")
    sys.exit(0)
