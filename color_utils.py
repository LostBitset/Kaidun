# Kaidun (by HktOverload)

def unhexify(x):
    r = x >> 0o20 & 0xFF
    g = x >> 0o10 & 0xFF
    b = x >> 0o00 & 0xFF
    r /= 0xFF
    g /= 0xFF
    b /= 0xFF
    return (r, g, b)

