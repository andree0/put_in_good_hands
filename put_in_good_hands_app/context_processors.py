def metadata(request):
    return {
        'user': request.user,
        'author': 'Andrzej Jończy',
        'github': 'https://github.com/andree0',
        'ip_address': request.META['REMOTE_ADDR']
    }
