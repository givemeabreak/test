def cache_page(view_func):
    def wrapper(request):
        response = view_func(request)
        print('======',request.get_full_path(),'======')
        return response
    return wrapper