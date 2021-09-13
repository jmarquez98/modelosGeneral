import subprocess






"""modelosACorrer =[
["ewz","T10YIE",False,False,["2003-01-02","2009-03-06"],FALTASERIE],
["ewz","T5YIFR",False,False,["2003-01-02","2009-03-06"],FALTASERIE]]
"""


modelosACorrer =[
["ewz","DGS10",False,False,"1962-01-02","DGS10",'diario'],
["ewz","T10Y2Y",False,False,"1976-06-01","T10Y2Y",'diario'],
["ewz","T10Y3M",False,False,"1982-01-04","T10Y3M",'diario'],

["ewz","DGS5",False,False,"1962-01-02","DGS5",'diario'],

["ewz","DGS2",False,False,"1976-06-01","DGS2",'diario'],

["ewz","TB3MS",False,False,"1934-01-01","TB3MS","mensual"],

["ewz","DFII10",False,False,"2003-01-02","DFII10",'diario'],

["ewz","DFII5",False,False,"2003-01-02","DFII5",'diario']
]








for index in modelosACorrer:

	bmark         = index[0]
	name          = index[1]
	fred          = str(index[2])
	inv           = str(index[3])
	fecha         = index[4]
	serie         = index[5]
	numRes        = str(20)
	maximizar     = "retorno Anualizado"
	modelo        = "mediasmoviles"
	ultimaMedia   = str(10)
	superposicion = str(0.5)
	diff          = str(0)
	freq          = index[6]
	vacio         = "pache"
	subprocess.run(["python3", "main.py", bmark,name,serie,fred,fecha,numRes,freq,vacio,maximizar,modelo,ultimaMedia,superposicion,inv,diff])
