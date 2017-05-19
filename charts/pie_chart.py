import matplotlib.pyplot as plt
import json

labels = []
counts = []

# Parsear string que define la encuesta con json.loads(j_str)
participantes = 20
j_str = '''{"title":"Mejor idioma", 
		"English":"Tea and rain", 
		"French":"Ca va", 
		"Spanish":"Tapas y sol"}'''
opciones_votos = json.loads(j_str)
if opciones_votos["title"]:
	titulo = opciones_votos["title"]
	opciones_votos.pop("title")

# Inicializar el contador de votos para cada opcion
for label, count in opciones_votos.iteritems():
	opciones_votos[label] = 0

votos_recibidos = ["Spanish","English","Spanish","Spanish","Spanish"
,"English","English","French","French","French","English","Spanish"
,"English","Spanish","English","Spanish","Spanish","French"]
# Contar los votos recibidos y calcular abstenciones 
for voto in votos_recibidos:
	opciones_votos[voto] += 1

n_votos = len(votos_recibidos)
if  n_votos < participantes:
	opciones_votos["NS/NC"] = participantes - n_votos

# Preparar datos de entrada para matplotlib
for label, count in opciones_votos.iteritems():
	labels.append(label)
	counts.append(count)

# Obtener el maximo de votos para resaltar su fraccion
m = max(counts)
explode = []  
for el in counts:
	if el == m:
		explode.append(0.1)
	else:
		explode.append(0)

# Generar la grafica y guardarla en formato PNG
fig1, ax1 = plt.subplots()
ax1.pie(counts, explode=explode, labels=labels, autopct='%1.1f%%',shadow=True, startangle=90)
ax1.axis('equal')
plt.title('%s: %d/%d (votos/participantes)'%(titulo,n_votos,participantes))
plt.savefig("poll_result.png",bbox_inches='tight')
