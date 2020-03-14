import math

# template decorator nowhere using at this moment
# converts pixels to percentage by axis
def dimensions(resolution):
    def decorator(function):
        def wrapper(*args, **kwargs):
            def getPercentage(axisize, size):
                perc = math.trunc(100/(axisize/size))
                perc = 1 if not perc else perc
                return perc
            dims = list()
            radius = None
            color = args[-1]
            exclnames = ['drawCircle', 'drawCircleFilled']
            if function.__name__ not in exclnames:
                predims = args[1:-1]
            else:
                predims = args[1:-2]
                radius = args[-2]
            i = 0
            for dim in predims:
                if isinstance(dim, int):
                    perc = getPercentage(resolution[i], dim)
                elif isinstance(dim, str):
                    perc = dim[:-1] if dim.endswith("%") else None
                else:
                    raise ValueError("Wrong Value. Value must be an int or perc str")
                if str(perc).isdigit():
                    dims.append(perc)
                else: raise ValueError("Wrong Value")
                i = 1 if i < 1 else 0
            if radius: dims.append(radius)
            dims.append(color)
            # for now decorator just prints all args and kwargs:
            print(dims, kwargs)
            return function(*args, **kwargs)
        #wrapper.__name__ = function.__name__
        #wrapper.__doc__  = function.__doc__
        return wrapper
    return decorator
