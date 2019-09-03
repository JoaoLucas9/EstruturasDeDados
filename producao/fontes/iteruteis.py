def tamanho(iteravel):
    """Retorna a o tamanho do iteravel."""
    return sum(1 for x in iteravel)

def vazio(iteravel):
    """Retorna true se o iterável estiver vazio, false caso contrário."""
    return tamanho(iteravel) is 0

