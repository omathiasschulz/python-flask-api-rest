def normalize_path_params(
    cidade=None,
    estrelas_min=0,
    estrelas_max=5,
    diaria_min=0,
    diaria_max=10000,
    limit=50,
    offset=0,
    **dados
):
    """Normaliza os parametros enviados no request"""
    if cidade:
        return {
            "estrelas_min": estrelas_min,
            "estrelas_max": estrelas_max,
            "diaria_min": diaria_min,
            "diaria_max": diaria_max,
            "cidade": cidade,
            "limit": limit,
            "offset": offset,
        }
    return {
        "estrelas_min": estrelas_min,
        "estrelas_max": estrelas_max,
        "diaria_min": diaria_min,
        "diaria_max": diaria_max,
        "limit": limit,
        "offset": offset,
    }


CONSULTA_SEM_CIDADE = "select * from hoteis \
    where (estrelas >= ? and estrelas <= ?) \
    and (diaria >= ? and diaria <= ?) \
    limit ? offset ? \
"

CONSULTA_COM_CIDADE = "select * from hoteis \
    where (estrelas >= ? and estrelas <= ?) \
    and (diaria >= ? and diaria <= ?) \
    and cidade = ? \
    limit ? offset ?"
