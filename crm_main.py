
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



def main(debug=False):
    if debug:
        with timer("Veri okunuyor..."):
            df_ = pd.read_excel("datasets/online_retail_II.xlsx",
                                sheet_name="Year 2010-2011")
            df = df_.copy()
            gc.collect()
        #
        #
        with timer("Veri Ön İşleme Yapılıyor..."):
            # Ham veri, ön işlemeden geçirildi
            df_prep = hlp.crm_data_prep(df)
            gc.collect()
        #
        #
        with timer("RFM Segmentasyonu Yapılıyor..."):
            # Normal olan RFM tablosu oluşturuldu
            rfm = hlp.create_rfm(df_prep)
            gc.collect()
        #
        #
        with timer("CLTV C (CLTV Calculate)Hesaplanıyor..."):
            rfm_cltv_c = hlp.create_cltv_c(rfm)

            gc.collect()
        with timer("CLTV Tahmini (CLTV Predict) Yapılıyor..."):
            rfm_cltv_p = hlp.create_cltv_p(df_prep)
            crm_final = rfm_cltv_c.merge(rfm_cltv_p, on="Customer ID", how="left")
            print("İlk 5 Gözlem : \n", crm_final.head())
            gc.collect()
    else:
        df_ = pd.read_excel("datasets/online_retail_II.xlsx",
                            sheet_name="Year 2010-2011")
        df = df_.copy()
        gc.collect()

        # Ham veri, ön işlemeden geçirildi
        df_prep = hlp.crm_data_prep(df)
        gc.collect()

        # Normal olan RFM tablosu oluşturuldu
        rfm = hlp.create_rfm(df_prep)
        gc.collect()

        rfm_cltv_c = hlp.create_cltv_c(rfm)

        gc.collect()

        rfm_cltv_p = hlp.create_cltv_p(df_prep)
        crm_final = rfm_cltv_c.merge(rfm_cltv_p, on="Customer ID", how="left")
        print("İlk 5 Gözlem : \n", crm_final.head())
        gc.collect()




if __name__ == "__main__":
    namespace = hlp.get_namespace()

    with timer("Full model run"):

        schedule.every(45).minutes.do(main)

        while 1:
            schedule.run_pending()
            time.sleep(1)
