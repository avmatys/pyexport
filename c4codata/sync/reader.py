import requests


def validate_auth(func):
    def wrapper(auth, *args):
        if auth is None or len(auth) == 0 or len(auth[0]) == 0:
            raise ValueError('Auth details are not provided')
        return func(auth, *args)
    return wrapper


def param_required_dict(parameter):
    def decorator(func):
        def wrapper(*args, **kwargs):
            odata_request = {}
            for arg in args:
                if isinstance(arg, dict):
                    odata_request = arg
                    break
            value = odata_request.get(parameter)
            if value is None:
                raise ValueError(f'{parameter.capitalize()} is mandatory')
            return func(*args, *kwargs)
        return wrapper
    return decorator


def param_not_empty_dict(parameter):
    def decorator(func):
        def wrapper(*args, **kwargs):
            odata_request = {}
            for arg in args:
                if isinstance(arg, dict):
                    odata_request = arg
                    break
            value = odata_request.get(parameter)
            if value is not None and len(value) == 0:
                raise ValueError(f'{parameter.capitalize()} should be not empty')
            return func(*args, *kwargs)
        return wrapper
    return decorator
    

def param_required_kwargs(parameter):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for key, value in kwargs:
                if key == parameter and value is None:
                     raise ValueError(f'{parameter.capitalize()} is mandatory')
            return func(*args, **kwargs)
        return wrapper
    return decorator


@param_required_kwargs('session')
@param_required_kwargs('url')
def __get_all_from_odata(session, url):
    result = {}
    iteration = 0
    while url is not None:
        response = session.get(url)
        next_url, status_code, content = (None, None, None)
        if response is not None:
            status_code = response.status_code
            if response.ok:
                content = response.json()
                next_url = content.get('__next') 
            else:
                content = response.reason
        result[iteration] = {
            'url' : url,
            'status_code' : status_code,
            'content' : content
        }
        iteration += 1
        url = next_url
    return result
          

@validate_auth
def read_from_odata(auth, url_list):
    with requests.session() as session:
        session.auth = auth
        session.headers.update({'x-csrf-token': 'fetch', 'Accept': 'application/json'})
        data = []
        for url in url_list:
            url_data = __get_all_from_odata(session, url)
            url_entry = {'url' : url, 'data' : url_data}
            data.append(url_entry)
    return data


@param_required_kwargs('session')
@param_required_kwargs('url')
def __get_chunk_from_odata(session, url):
    result = {}
    while url is not None:
        response = session.get(url)
        next_url, status_code, content = (None, None, None)
        if response is not None:
            status_code = response.status_code
            if response.ok:
                content = response.json()
                next_url = content.get('__next') 
            else:
                content = response.reason
        result = {
            'url' : url,
            'status_code' : status_code,
            'content' : content
        }
        yield result
        url = next_url



@validate_auth
def read_all_chunks_from_odata(auth, url_list):
    with requests.session() as session:
        session.auth = auth
        session.headers.update({'x-csrf-token': 'fetch', 'Accept': 'application/json'})
        data = []
        for url in url_list:
            generator = __get_chunk_from_odata(session, url)
            iteration = 0
            url_data = {}
            while True:
                try:
                    url_data[iteration] = next(generator)
                except StopIteration:
                    break
                iteration += 1
            url_entry = {'url' : url, 'data' : url_data}
            data.append(url_entry)
    return data