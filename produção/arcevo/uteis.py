class ignorar():
    """Gerenciador de contexto que ignora os erros gerados.
    Equivalente a:
    try:
       código
    except Exception:
       pass
    """

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        return True