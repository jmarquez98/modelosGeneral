from  matplotlib.colors import LinearSegmentedColormap
import os
import dataframe_image as dfi
import pandas as pd
import pathlib
path = str(pathlib.Path(__file__).parent.absolute())



def get_tablas(path):
    path_modelos = path + "/resultadosModelos"
    etfs = os.listdir(path_modelos)
    tablas = {}

    for etf in etfs:
        tablas[etf] = {}
        if "news_sentiment_data" in etf: path_etf = path_modelos + "/" + etf + "/" + "un umbral"
        else: path_etf = path_modelos + "/" + etf + "/" + "mediasmoviles"
        fechas = os.listdir(path_etf)
        max_fecha = max(fechas)

        path_etf_fecha = path_etf + "/" + max_fecha
        files = os.listdir(path_etf_fecha)
        files = [file for file in files if file[-4:]=="xlsx"]
        for file in files:
            file_name = file[:-4]
            df = pd.read_excel(path_etf_fecha + "/" + file, index_col=0)
            df.set_index("parametro", inplace=True)
            tablas[etf][file_name] = df
    return tablas


tablas = get_tablas(path=path)

for etf in tablas:
    for fecha in tablas[etf]:
        df = tablas[etf][fecha]
        cols = df.columns
        ret_cols = [col for col in cols if col[:3]=="ret"]
        vol_cols = [col for col in cols if col[:3]=="vol"]
        sharpe_cols = [col for col in cols if col[:3]=="sha"]
        draw_cols = [col for col in cols if col[:3]=="dra"]
        port_cols = [col for col in cols if col[-4:]=="port"]
        etf_cols = [col for col in cols if ((col[:3] in ["ret", "vol", "sha", "dra"]) and (col[-4:]!="port"))]
        month_cols = [col for col in cols if col[:5]=="month"]
        sign_cols = [col for col in cols if col[:3] == "num"]

        pct_cols = ret_cols + sharpe_cols + draw_cols + month_cols
        df[pct_cols] = df[pct_cols] * 100
        month_below_cols = [col for col in cols if (("Below" in col) or ("Sold" in col))]

        neg_cols = vol_cols + sign_cols + month_below_cols
        pos_cols = [col for col in cols if col not in neg_cols]
        neg_etf = [col for col in neg_cols if col in etf_cols]
        pos_etf = [col for col in pos_cols if col in etf_cols]

        cols_no_etf = [col for col in cols if col not in etf_cols]
        df = df[cols_no_etf + etf_cols]

        cmap_default = LinearSegmentedColormap.from_list('rg', ["r", "w", "g"], N=256)
        cmap_default2 = LinearSegmentedColormap.from_list('rg', ["g", "w", "r"], N=256)
        cmap_default3 = LinearSegmentedColormap.from_list('Blues', ["darkblue", "white"], N=256)
        cmap_default4 = LinearSegmentedColormap.from_list('Blues', ["white", "darkblue"], N=256)


        df = df.style \
            .background_gradient(axis=0, cmap=cmap_default, subset=pos_cols) \
            .background_gradient(axis=0, cmap=cmap_default2, subset=neg_cols) \
            .background_gradient(axis=0, cmap=cmap_default3, subset=pos_etf) \
            .background_gradient(axis=0, cmap=cmap_default4, subset=neg_etf) \
            .format("{:.1f}")

        dfi.export(df, path + "/gradientes/" + etf + "/" + fecha + ".png")
        #df.to_excel(path + "/gradientes/" + etf + "/" + fecha)