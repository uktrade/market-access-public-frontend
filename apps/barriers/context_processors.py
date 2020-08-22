def query_params(request):
    context = {
        "location": request.location,
        "sector": request.sector,
        "query_string": request.query_string
    }

    return context

