def get_capitalized_words(field: str) -> str:
    prepositions_set = {
        "da",
        "de",
        "do",
        "das",
        "dos",
        "e",
        "em",
        "na",
        "no",
        "nas",
        "nos",
        "para",
        "pela",
        "pelo",
        "pelas",
        "pelos",
        "por",
        "com",
        "sem",
        "sob",
        "sobre",
        "a",
        "o",
        "as",
        "os",
        "à",
        "às",
        "ao",
        "aos",
        "após",
        "até",
        "sob",
        "sobre",
        "trás",
        "como",
        "entre",
        "que",
        "se",
    }

    words = field.lower().split()
    capitalized_words = [
        word.capitalize() if i == 0 or word not in prepositions_set else word
        for i, word in enumerate(words)
    ]
    return " ".join(capitalized_words)
