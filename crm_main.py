
import schedule

from scripts import helpers as hlp
import pandas as pd
import time
import gc
from contextlib import contextmanager

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.float_format', lambda x: '%.3f' % x)
pd.set_option('display.expand_frame_repr', False)



@contextmanager
def timer(title):
    t0 = time.time()
    yield
    print("{} - done in {:.0f}s".format(title, time.time() - t0))





if __name__ == "__main__":
    namespace = hlp.get_namespace()

    with timer("Full model run"):

        schedule.every(45).minutes.do(main)

        while 1:
            schedule.run_pending()
            time.sleep(1)
