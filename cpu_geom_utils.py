# Kaidun (by HktOverload)

# Manhattan (L1) distance
def manhattan(a, b):
    return sum(
        abs(i - j)
        for i, j in zip(a, b)
    )

