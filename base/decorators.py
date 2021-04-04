def allow_shares(view_func):
    def sharify(request, *args, **kwargs):
        shared = kwargs.get('__shared', None)
        if shared is not None:
            if '__shared' not in view_func.func_code.co_varnames[:view_func.func_code.co_argcount]:
                del kwargs["__shared"]
            return view_func(request, *args, **kwargs)
        else: return login_required(view_func)(request, *args, **kwargs)
    return sharify    

class SharifyError(Exception):pass