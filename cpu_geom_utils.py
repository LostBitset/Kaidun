# Kaidun (by HktOverload)

# Manhattan (L1) distance
# [: Citation https://mathworld.wolfram.com/TaxicabMetric.html :]
def manhattan(a, b):
    return sum(
        abs(i - j)
        for i, j in zip(a, b)
    )

