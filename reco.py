import os
import pandas as pd
import pathlib
path = str(pathlib.Path(__file__).parent.absolute())


def get_maximizing_mm(excel_file, col):
  info = pd.read_excel(excel_file)
  fila_max = info[info[col] == max(info[col])]
  param_max = fila_max["parametro"].iloc[0]
  #Transfomo de str a tupla de int
  if (type(param_max) == str):
    param_max = (int(param_max[1:param_max.find(",")]), int(param_max[param_max.find(",") + 1:param_max.find(")")]))
  return param_max

def collect_mm(path, max_col):
    dict_final = {}
    for root, _, file_list in os.walk(path):
        #print("In directory {}".format(root))
        nombre_activo = root[root.find("/") + 1: root.find("/", 2)]
        #print("Activo {}".format(nombre_activo))
        dict_tmp = {}
        list_tmp = [None] * 5
        i = 0
        for file_name in file_list:
            if file_name.startswith("res-"):
                #os.remove(os.path.join(root, file_name))
                print("File: {}".format(os.path.join(root, file_name)))
                dict_tmp[file_name] = get_maximizing_mm(os.path.join(root, file_name), max_col)
                list_tmp[i] = (get_maximizing_mm(os.path.join(root, file_name), max_col))
                i += 1

        dict_final[nombre_activo] = list_tmp
        #dict_final[nombre_activo] = dict_tmp

    return pd.DataFrame(dict_final).T


data = collect_mm(".", "ret_port")

data.to_excel(path + "/cruces-optimos.xlsx")

print(data)
