import sys
import time
from functools import wraps

import numpy as np



def timeit(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        tic = time.time()
        result = f(*args, **kwargs)
        print("{}({}): {}".format(f.__name__, ", ".join([str(a) for a in args]),time.time() - tic))
        return result
    return wrapper

@timeit
def coefficients(n_dims, step):
    x = []

    def go(ws):
        d = 1 - sum(ws)
        if len(ws) == n_dims - 1:
            return ws + (d,)
        for w in np.arange(0, d + step - sys.float_info.epsilon, step):
            x.append(go(ws + (w,)))

    go(())

    return filter(None, x)

def iter_coefficients(n_dims, step):
    def go(ws):
        d = 1 - sum(ws)
        if len(ws) == n_dims - 1:
            yield ws + (d,)
        if len(ws) < n_dims:
            for w in np.arange(0, d + step - sys.float_info.epsilon, step):
                for x in go(ws + (w,)):
                    yield x

    return go(())

if __name__ == '__main__':
    n_dims = 10
    step = 0.1

    coefficients(n_dims, step)

    @timeit
    def time_iter(n_dims, step):
        return list(iter_coefficients(n_dims, step))
    time_iter(n_dims, step)