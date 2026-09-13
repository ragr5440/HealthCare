query_cache = {}

retrieval_call_count = 0


def normalize_query(
    query: str,
) -> str:

    return query.strip().lower()


def get_cached_answer(
    query: str,
):

    key = normalize_query(query)

    return query_cache.get(key)


def store_cached_answer(
    query: str,
    answer: str,
):

    key = normalize_query(query)

    query_cache[key] = answer


def increment_retrieval_count():

    global retrieval_call_count

    retrieval_call_count += 1


def get_retrieval_count():

    return retrieval_call_count