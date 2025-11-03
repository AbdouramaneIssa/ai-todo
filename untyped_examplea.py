"""Exemple de code NON typé - À NE PAS FAIRE !

Ce fichier montre ce qui se passe quand vous écrivez du code sans type hints.
Mypy et Flake8 vont le rejeter lors d'un commit.
"""


def add_numbers(a, b):
    """Additionne deux nombres SANS type hints."""
    return a + b


def process_list(items):
    """Traite une liste SANS type hints."""
    result = []
    for item in items:
        result.append(item * 2)
    return result


class DataHelper:
    """Classe SANS type hints."""

    def __init__(self, name):
        self.name = name
        self.data = []

    def add_item(self, value):
        """Ajoute un élément."""
        self.data.append(value)

    def get_data(self):
        """Retourne les données."""
        return self.data


def main():
    """Fonction principale SANS type hints."""
    helper = DataHelper("test")
    helper.add_item(10)
    helper.add_item(20)
    result = process_list(helper.get_data())
    print(result)


if __name__ == "__main__":
    main()
