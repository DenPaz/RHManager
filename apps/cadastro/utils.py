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
    }
    words = field.lower().split()
    capitalized_words = [
        word.capitalize() if word not in prepositions_set else word for word in words
    ]
    return " ".join(capitalized_words)
