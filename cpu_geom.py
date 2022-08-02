# Kaidun (by HktOverload)

def triNormal(tri):
    a1 = tri[3] - tri[0]
    a2 = tri[4] - tri[1]
    a3 = tri[5] - tri[2]
    b1 = tri[6] - tri[0]
    b2 = tri[7] - tri[1]
    b3 = tri[8] - tri[2]
    return (
        (a2*b3) - (a3*b2),
        (a3*b1) - (a1*b3),
        (a1*b2) - (a2*b1),
    )
