from ipyparallel import Client
import os


def get_parallel_view():
    c = Client()
    dview = c.direct_view()
    dview.execute('%reset')
    dview.execute('import sys')
    dview.execute(f'sys.path.append("{os.getcwd()}")', block=True)
    return c.load_balanced_view()

