import re,sys,os
dataPath=sys.argv[1]
txtNames=[]

for txt in os.listdir(dataPath):
  txtNames.append(txt)

comisiones= {}

p = re.compile('.+COMI_([A-Z]+).*')
for txt in txtNames:
  result = p.search(txt)
  comision = result.group(1)
  if comision not in comisiones:
    comisiones[comision]=1
  else:
    value= comisiones.get(comision)
    comisiones[comision]=value+1

print(comisiones)

