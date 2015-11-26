#**************************************************************************#
#**                                                                      **#
#**   Core: Adaptação de  Adaptado de um execício de programação da USP  **#
#**   Exercício-Programa 3                                               **#
#**   Professor: Carlos Eduardo Ferreira                                 **#
#**   Turma: 7                                                           **#
#**                                                                      **#
#**************************************************************************#


# Módulo necessário para as funções exp (exponencial) e sqrt (raiz quadrada).
import math
import sys

# Este é o módulo com as funções gráficas. Em especial, este módulo contém a função 
#    exibe_grafico(titulo, rotulos, medias, desvios, y0, y1).


# Constantes para a fase de teste do programa.
TESTE_COLUNAS_AUXILIARES = True # Se quiser ver as colunas para filtragem, mude para True.

# Constantes para tornar o seu programa mais legível. 
# Cada coluna da tabela se refere a uma medição:
DATA = 0
PREC = 1 # Precipitação
TEMP = 2 # Temperatura
UMID = 3 # Umidade
VENT = 4 # Velocidade do vento

# Coluna extra que calcularemos a partir dos dados
TAPA = 5 # Temperatura aparente

# Colunas auxiliares para filtragem
MES  = 6 # coluna auxiliar para ajudar na filtragem por mês
ANO  = 7 # coluna auxiliar para ajudar na filtragem por ano
AEM  = 8 # coluna auxiliar para ajudar na filtragem por mês/ano
# Lista com os títulos das diferentes medidas e colunas da tabela. 
NOMES = ['data', 'precipitação', 'temperatura', 'umidade', 'velocidade do vento', 'temperatura aparente']

#processa os dados com as informações recebidas do cliente. 
#Essa lista a definição dos dados que serão utilizados, entre outras coisas
def processa_dados(dado):
  
  tabela = criaTabela(dado['dados'])
  abcissas=[]
  medias=[]
  desvios=[]


  if(int(dado['tempoDivisao'])==1 and not bool(dado['filtro'])):
    
    lista = preparaLista(medias_e_desvios_de_medida(tabela, int(dado['medida']), ANO))
    abcissas=lista[0]
    medias=lista[1]
    desvios=lista[2]

  elif(int(dado['tempoDivisao'])==2 and not bool(dado['filtro'])):

    tabelaOrdenada = ordenaTabela(tabela, MES)
    lista = medias_e_desvios_de_medida(tabelaOrdenada, int(dado['medida']), MES)
    abcissas=lista[0]
    medias=lista[1]
    desvios=lista[2]

  elif(int(dado['tempoDivisao'])==1 and bool(dado['filtro'])):

    print('Entrou')

    v1=(int((dado['ano_ini']))*100)+int(dado['mes_ini'])
    v2=(int((dado['ano_fim']))*100)+int(dado['mes_fim'])


    print(dado['ano_ini'])
    print(dado['ano_fim'])

    tab=filtro_de_intervalo(tabela,AEM, AEM, v1,v2)
    lista = preparaLista(medias_e_desvios_de_medida(tab, int(dado['medida']), ANO))
    abcissas=lista[0]
    medias=lista[1]
    desvios=lista[2]

  elif(int(dado['tempoDivisao'])==2 and bool(dado['filtro'])):


    print(dado['ano_ini'])
    print(dado['ano_fim'])


    v1=(int((dado['ano_ini']))*100)+int(dado['mes_ini'])
    v2=(int((dado['ano_fim']))*100)+int(dado['mes_fim'])
    #print(v1)
    #print(v2)

    tab=filtro_de_intervalo(tabela,AEM, AEM, v1,v2)
    tab = ordenaTabela(tab, MES)
    lista = preparaLista(medias_e_desvios_de_medida(tab, int(dado['medida']), MES))
    abcissas=lista[0]
    medias=lista[1]
    desvios=lista[2]

  return {'abcissas': abcissas, 'medias': medias, 'desvios': desvios}


def leitura_dos_dados(arquivo_input):
  """(None) -> tabela
   Lê os dados de um arquivo e os coloca em uma tabela. Devolve a tabela.
     Cada linha da tabela corresponde às medições de um dia.
  """
  # Lê o nome do arquivo de dados e o abre para leitura.
  ok = False
  while not ok:
    nome_do_arquivo = arquivo_input
    try: 
      f = open(nome_do_arquivo, 'r', encoding='utf8')
    except FileNotFoundError:
      print(nome_do_arquivo, " não encontrado. Você digitou direito?")
    else:
      ok = True

  # Ignora a primeira linha do arquivo, que tem um cabeçalho.
  linha = f.readline()

  # Monta e devolve a tabela com os dados do arquivo.
  tabela = []
  for linha in f:
    lista = linha.split(";") # cada valor vem seguido por ; no arquivo
    medicoes_de_um_dia = [lista[0], None, None, None, None] # data, precipitacao, temperatura, umidade, velocidade
    for i in range(1, 5):
      if lista[i] != '':
        medicoes_de_um_dia[i] = float(lista[i])
    tabela.append(medicoes_de_um_dia)
  f.close()
  return tabela

def temperatura_aparente(tabela):
  """ (tabela) --> None 
      Recebe uma matriz tabela e acrescenta à matriz uma coluna com a temperatura aparente, 
      calculada das colunas da tabela que contêm a temperatura, a umidade e a velocidade do vento, 
      pela fórmula dada em http://www.bom.gov.au/info/thermal_stress/, que reproduzimos abaixo:
        temperatura_aparente = temperatura + 0.33*e − 0.70*velocidade_do_vento − 4.00, 
      onde e = (umidade / 100) * 6.105 * exp(17.27 * temperatura / (237.7 + temperatura)).
      Se uma das medidas necessárias não estiver disponível na tabela (for None), coloque None 
      na entrada da temperatura aparente.
      Para o arquivo teste.txt, seu programa deve obter a seguinte tabela:

        Data        Prec    Temp    Umid   Vento  TempApar
      01/01/1990   15.50   22.24   88.00    1.77   24.77  
      02/01/1991   35.90   21.20   89.75    2.33   23.00  
      03/02/1992   16.30   19.00   89.00    3.37   19.08  
      04/02/1993    5.20   19.58   92.50    1.67   21.35  
      05/03/1994   11.90   21.62   86.25    1.00   24.25  
      06/03/1995    9.40   22.98   85.50    1.53   25.80  
      07/03/1996   15.70   23.64   78.50    1.43   26.18  
      08/04/1997    5.90   24.06   70.00    3.00   24.86  
      09/04/1998    0.00   21.98   86.50    0.93   24.84  
      10/04/1999    9.30   22.54   79.75    1.20   24.87  
      11/04/1999                   79.75    1.20        
  """
  # Passo 1: escreva o corpo desta função.
  for i in range(len(tabela)):
    for j in range(1,4):
      if tabela[i][j]==None: #inserção de None nos espaços vazios da tabela
        tabela[i][j]=None
  y=0
  while y<(len(tabela)):
    if tabela[y][1]!=None and tabela[y][2]!=None and tabela[y][3]!=None and tabela[y][4]!=None: #calculo da tempApar apenas onde há todos os dados disponiveis
      temp=tabela[y][2]
      e=(tabela[y][3]/100)*6.105*math.exp(17.27*tabela[y][2]/(237.7+tabela[y][2]))
      vel=tabela[y][4]
      tabela[y].append(temp+(0.33*e)-(0.70*vel)-4.00) #calculo da tempApar
    else:
      tabela[y].append(None) #inserção de None onde nao é possivel calcular a tempApar
    y=y+1

  return tabela
         
def acrescenta_colunas_para_filtragem(tabela):
  """ (tabela) --> None
      Recebe uma matriz tabela, que contém, em sua primeira coluna, strings no formato dd/mm/aaaa,
      representando a data de cada medição, e acrescenta à matriz três colunas: 
      uma coluna com um inteiro que representa o mês extraído de cada data, 
      uma coluna com um inteiro que representa o ano extraído de cada data, e 
      uma coluna com um inteiro no formato aaaamm com o ano e o mês juntos.
      Para o arquivo teste.txt, com TESTE_COLUNAS_AUXILIARES = True, seu programa 
      deve obter a seguinte tabela:

        Data        Prec    Temp    Umid   Vento  TempApar
      01/01/1990   15.50   22.24   88.00    1.77   24.77   1  1990  199001
      02/01/1991   35.90   21.20   89.75    2.33   23.00   1  1991  199101
      03/02/1992   16.30   19.00   89.00    3.37   19.08   2  1992  199202
      04/02/1993    5.20   19.58   92.50    1.67   21.35   2  1993  199302
      05/03/1994   11.90   21.62   86.25    1.00   24.25   3  1994  199403
      06/03/1995    9.40   22.98   85.50    1.53   25.80   3  1995  199503
      07/03/1996   15.70   23.64   78.50    1.43   26.18   3  1996  199603
      08/04/1997    5.90   24.06   70.00    3.00   24.86   4  1997  199704
      09/04/1998    0.00   21.98   86.50    0.93   24.84   4  1998  199804
      10/04/1999    9.30   22.54   79.75    1.20   24.87   4  1999  199904
      11/04/1999                   79.75    1.20           4  1999  199904
  """
  # Passo 1: escreva o corpo desta função.
  memo=[]
  palavra=''
  for i in range(len(tabela)):
    sdia = ""
    smes = ""
    sano = ""
    edia = True
    emes = False
    for k in tabela[i][0]:
      if k!='/' and edia:            #cria uma lista com as strings de dia, mes e ano
        sdia = sdia + k
      elif k!= '/' and emes:
        smes = smes + k
      elif k != '/' and not edia and not emes: 
        sano = sano + k
      elif k == '/' and edia : 
        emes = True
        edia = False
      else:
        emes = False
    tabela[i].append(int(smes))
    tabela[i].append(int(sano))
    tabela[i].append(int(sano)*100 + int(smes))

  return tabela

def criaTabela(arquivo_input):
  return acrescenta_colunas_para_filtragem(temperatura_aparente(leitura_dos_dados(arquivo_input)))



###################################################
# Funções obrigatórias
###################################################


            
def imprime_estatisticas(abcissas, medias, desvios):
  """ (lista, lista, lista) --> None
      Recebe três listas do mesmo comprimento, e as imprime em três colunas. A lista abcissas pode conter strings ou inteiros. 
      As listas medias e desvios são de valores reais, com algumas entradas eventualmente valendo None. 
      A media deve ser impressa com duas casas decimais, ocupando 6 colunas (ou seja, com o formato %6.2f), 
      enquanto que o desvio padrão deve ser impresso com três casas decimais (formato %.3f).
      No lugar das entradas None deve ser impresso um traço (-).
  """
  # Passo 2: escreva o corpo desta função.
  y=0
  while y<(len(medias)):
    if medias[y] == None:
      if  desvios[y] == None:
        print("%4s    -    -" %(str(abcissas[y])))
      else:
        print("%4s - (%.3f)"%(str(abcissas[y]),desvios[y]))
    else:
      if  desvios[y] == None:
        print("%4s %6.2f (-)"%(str(abcissas[y]),medias[y]))
      
      else:
        print("%4s %6.2f (%.3f)"%(str(abcissas[y]),medias[y],desvios[y]))
    if y<(len(medias)):
      y+=1
          
def medias_e_desvios_de_medida(tabela, medida, coluna_de_referencia):
  """ (tabela, int, int) --> (lista, lista, lista)
      Constrói lista de valores distintos da tabela na coluna_de_referência (que pode ser MES, ANO ou AEM). 
      Para cada valor distinto na coluna_de_referência, calcula a média e o desvio padrão da coluna medida da tabela.
      Se o número de entradas válidas para algum dos valores da coluna_de_referencia for nulo, usa-se None como média e desvio, 
      e se houver uma única entrada válida para algum valor da coluna_de_referencia, usa-se None como desvio padrão.
      Devolve três listas: a lista dos valores na coluna_de_referência, a lista das médias e a lista dos desvios correspondentes.
  """
  listaMedida=[]
  listaColRef=[]
  soma=0
  abcissas=[]
  medias=[]  #listas a serem preenchidas e devolvidas
  desvios=[]
  ini=0

  #preencher listamedida e listacoluna
  for i in range(len(tabela)):
    listaMedida.append(tabela[i][medida])
    listaColRef.append(tabela[i][coluna_de_referencia])
  
  #realizar soma dos valores de coluna_de_referencia iguais
  for i in range(len(listaColRef)):
    if i==0: #primeiro elemento 
      ini=i
      if listaMedida[i]!=None:
        soma=listaMedida[i] #adiciona o valor somente se a entrada for diferente de None
      else:
        soma=0
    else: #se não for o primeiro elemento
      if listaColRef[i]==listaColRef[i-1]: #se é igual ao de cima
        if listaMedida[i]!=None:
            soma+=listaMedida[i]                   
      else: #se NÃO for igual ao de cima
        abcissas.append(listaColRef[i-1])
        if soma==0:
            medias.append(None)
            desvios.append(None)
        else:
            medias.append(media(soma,i-ini))
            desvios.append(desvio(listaMedida[ini:i]))
        if listaMedida[i]!=None:
          soma = listaMedida[i]
        else:
          soma = 0
        ini=i

      #tratamento para último elemento
      if i==(len(listaColRef)-1):
        abcissas.append(listaColRef[i-1])
        if soma==0:
          medias.append(None)
          desvios.append(None)
        else:
          medias.append(media(soma,i-ini))
          desvios.append(desvio(listaMedida[ini:i]))

  saida=[]
  saida.append(abcissas)
  saida.append(medias)
  saida.append(desvios)
  return saida
                        
#funcao que calcula os minimos quadrados
def minimos_quadrados(x, y):
  """ (lista, lista) --> (float, float)
      Recebe duas listas do mesmo tamanho, x e y. A lista x contém números, e a lista y contém números e eventualmente algumas 
      entradas None. Devolve uma lista com dois números [y0, y1] calculados da seguinte maneira. Aplique o método dos mínimos 
      quadrados sobre os pontos dados por x e y, para as entradas válidas de y (diferentes de None), para obter valores a e b 
      que aproximem os pontos dados por x e y por uma reta. Devolva y0 = a + b*x_min e y1 = a + b*x_max, onde x_min e x_max 
      são respectivamente o menor e o maior valor na lista x (independente do correspondente valor de y ser None ou não). 
      Caso não haja nenhum valor válido em y, devolva [None, None].
  """
  # Passo 3: escreva o corpo desta função.
  lista=[]
  if len(tiraNone(x))==0:
    print("A tabela de dados não contém dados suficientes para análise")
    sys.exit(0)      
  lista.append(funcA(x,y)+(funcB(x,y)*min(tiraNone(x))))
  lista.append(funcA(x,y)+(funcB(x,y)*max(tiraNone(x))))
  return lista
    

def imprime_estatisticas_e_mostra_grafico(titulo, coluna_de_referencia, abcissas, medias, desvios):
  """ (str, int, lista, lista, lista) --> None
      Recebe na string titulo o nome da medida cujas estatísticas serão impressas. Recebe também a coluna de referência, 
      a lista abcissas dos valores inteiros distintos da coluna de referência, a lista das médias e a lista dos desvios correspondentes, 
      e imprime, usando a função imprime_estatísticas, a tabela das médias e desvios, calcula a aproximação linear das médias 
      dada pelo método dos mínimos quadrados, e mostra o gráfico com as médias e desvio correspondente, e a aproximação linear obtida.
  """
  # Passo 3: escreva o corpo desta função.
  lista=minimos_quadrados(desvios,medias)
  y0=lista[0]
  y1=lista[1]
  graficos.exibe_grafico(titulo, abcissas, medias, desvios, y0, y1)
  imprime_estatisticas(abcissas,medias,desvios)
  
  
#retorna um intervalo de uma tabela, ja ordenada pela coluna j 
def filtro_de_intervalo(tabela, j, k, v1, v2):
  """ (tabela, int, int, int) --> tabela
      Constrói e devolve uma subtabela com as linhas i da tabela onde v1 <= tabela[i][j] <= v2.
  """  # Passo 4: escreva o corpo desta função.
  linhav1=0
  linhav2=0
  tabela=ordenaTabela(tabela,j)
  
  for i in range(len(tabela)):
    if tabela[i][k]==v1:
      linhav1=i
      break
  for i in range(len(tabela)):
    if tabela[i][k]==v2:
      linhav2=i

  return tabela[linhav1:linhav2]
  
  
  
  
#####################################
# Funções extras que você decida usar
#####################################

#calcula a media dado um valor e a quantidade de elementos
def media(valor, qtd_elementos):
  if qtd_elementos>0:
    return valor/qtd_elementos
  else:
    return 0

#calcula o desvio de uma lista 
def desvio(lista):
  n=len(lista)
  soma=0
  somatorio=0
  if n==1:
      return '-'
  else:    
    for i in range(n):
      if lista[i]!='-' and lista[i]!=None:
        soma+=lista[i]  #soma de todos os valores da lista

    med=media(soma,n) #calculo da media dos valores da lista

    #calculo do somatorio do desvio
    for i in range(n):
      if lista[i]!='-' and lista[i]!=None:
        somatorio+=(lista[i]-med)**2

    desvio=math.sqrt(somatorio/(n-1)) #calculo do desvio

    return desvio

#retorna a media de uma lista
def medialista(lista):
  soma=0
  n=len(lista)
  for i in range(n):
    if lista[i]!=None and lista[i]!='-':
      soma+=lista[i]
  return(soma/n)

 #funcao utilizada na preparacao dos dados para estatisticas 
def funcB(lx,ly):
  xm=medialista(lx)
  ym=medialista(ly)
  somatorio1=0
  somatorio2=0
  for i in range(len(ly)):
    if ly[i]!=None and ly[i]!='-' and lx[i]!=None and lx[i]!='-':
      somatorio1+=lx[i]*(ly[i]-ym)
  for i in range(len(lx)):
    if lx[i]!='-' and lx[i]!=None:
      somatorio2+=lx[i]*(lx[i]-xm)
  if somatorio2!=0:
    return (somatorio1/somatorio2)
  return 0

#funcao utilizada na preparacao dos dados para estatisticas
def funcA(lx,ly):
  ym=medialista(ly)
  xm=medialista(lx)
  return ym-funcB(lx,ly)*xm

def preparaLista(lista):
  lista1=[]
  lista2=[]
  lista3=[]
  for i in range (len(lista[0])):
    if lista[1][i]!=None and lista[2][i]!=None:
      lista1.append(lista[0][i])
      lista2.append(lista[1][i])
      lista3.append(lista[2][i])
  saida=[]
  saida.append(lista1)
  saida.append(lista2)
  saida.append(lista3)
  return saida

#retorna uma lista sem valores nulos
def tiraNone(lista):
  limpa=[]
  for i in range(len(lista)):
    if lista[i]!=None and lista[i]!='-':
      limpa.append(lista[i])
  return limpa



#acha o mínimo de uma lista sem considerar os numeros da listaex
def getMinExp(lista,listaex):
  if len(lista)>0:
    minimo=lista[0]
  else:
    return -1
  
  for i in range(len(lista)):
    if(lista[i] not in listaex):
      minimo=lista[i]
      break
    
  if minimo in listaex:
    return -1
 
  for i in range(len(lista)):
    if lista[i]<minimo and lista[i] not in listaex:
      minimo=lista[i]
  return minimo


#ordena a tabela dada a coluna que se deseja ordenar
#utiliza algoritmo de contagem para tanto
def ordenaTabela(tabela,coluna):
  lista1=[]
  listaex=[]
  linhasOrdenadas=[]
  tabelaOrdenada = []
  
  #preencher uma lista com a coluna que desejo ordenar
  for i in range (len(tabela)):
    lista1.append(tabela[i][coluna])

  #tamanho da lista n
  n = len(lista1)
  
  while(True):
    minimo = getMinExp(lista1, listaex)
    if minimo == -1: #se não houver mais mínimos
      break
    else:
      listaex.append(minimo)

      #pego todas as linhas que contem esse mínimo encontrado
      for i in range(n):
        if lista1[i]==minimo: #se eu achei um dos mínimos da lista
          linhasOrdenadas.append(i) #salvo a linha que eu achei

  #agora eu tenho a ordem em que as linhas da tabela precisam estar
  for i in range(n):
    tabelaOrdenada.append(tabela[linhasOrdenadas[i]])

  return tabelaOrdenada
    
def arrumaAEM(abcissas):
  mes=0
  ano=0
  dataArrumada=[]

  for i in range(len(abcissas)):
    mes = str(abcissas[i])[-2:]
    ano = str(abcissas[i])[2:4]
    dataArrumada.append(mes+'/'+ano)

  return dataArrumada  











