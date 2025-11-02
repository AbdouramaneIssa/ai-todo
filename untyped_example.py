"""Exemple de code typé - C'est la bonne pratique !"""

from typing import List


def add_numbers(a: int, b: int ) -> int:
    """Additionne deux nombres avec type hints."""
    return a + b


def process_list(items: List[int]) -> List[int]:
    """Traite une liste avec type hints."""
    result: List[int] = []
    for item in items:
        result.append(item * 2)
    return result


class DataHelper:
    """Classe avec type hints."""

    def __init__(self, name: str) -> None:
        """Initialise la classe."""
        self.name: str = name
        self.data: List[int] = []

    def add_item(self, value: int) -> None:
        """Ajoute un élément."""
        self.data.append(value)

    def get_data(self) -> List[int]:
        """Retourne les données."""
        return self.data


def main() -> None:
    """Fonction principale avec type hints."""
    helper: DataHelper = DataHelper("test")
    helper.add_item(10)
    helper.add_item(20)
    result: List[int] = process_list(helper.get_data())
    print(result)


if __name__ == "__main__":
    main()
