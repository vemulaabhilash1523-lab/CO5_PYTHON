POSITIVE = {
    "good", "clean", "fast", "helpful", "improved"
}

NEGATIVE = {
    "bad", "dirty", "slow", "rude", "smoke", "broken"
}

NEGATORS = {
    "not", "never", "no"
}


def score(text):
    words = (
        text.lower()
        .replace(".", " ")
        .replace(",", " ")
        .split()
    )

    total = 0

    for index, word in enumerate(words):
        if word in POSITIVE:
            value = 1
        elif word in NEGATIVE:
            value = -1
        else:
            value = 0

        if index > 0 and words[index - 1] in NEGATORS:
            value = -value

        total += value

    return total


def label(text):
    value = score(text)

    if value > 0:
        return "positive"
    elif value < 0:
        return "negative"
    else:
        return "neutral"


complaints = [
    "Roads are clean and the bus was fast.",
    "Smoke from the factory, air is bad.",
    "The staff were not helpful.",
    "Not bad, service improved."
]

for complaint in complaints:
    print(f"{label(complaint):8} | {complaint}")
