# -*- coding: utf-8 -*-
######################################################################
from twokenize import emoticon, Hashtag, AtMention, url
from twokenize import tokenize as ark_tokenize
#from nltk.tokenize import TweetTokenizer
import freeling
import re

######################################################################

#============================ Freling Initialization ================================
# Modify this line to be your FreeLing installation directory
FREELINGDIR = "/usr";

DATA = FREELINGDIR+"/share/freeling/";
LANG="es";

freeling.util_init_locale("default");

# create language analyzer
#la=freeling.lang_ident(DATA+"common/lang_ident/ident.dat");

# create options set for maco analyzer. Default values are Ok, except for data files.
op= freeling.maco_options("es");
op.set_data_files( "", 
                   DATA + "common/punct.dat",
                   DATA + LANG + "/dicc.src",
                   DATA + LANG + "/afixos.dat",
                   "",
                   DATA + LANG + "/locucions.dat", 
                   DATA + LANG + "/np.dat",
                   DATA + LANG + "/quantities.dat",
                   DATA + LANG + "/probabilitats.dat");

# create analyzers
f_tk=freeling.tokenizer(DATA+LANG+"/tokenizer.dat");
#sp=freeling.splitter(DATA+LANG+"/splitter.dat");
#sid=sp.open_session();
f_mf=freeling.maco(op);

# activate mmorpho odules to be used in next call
f_mf.set_active_options(False, True, True, True,  # select which among created 
                      True, True, False, True,  # submodules are to be used. 
                      True, True, True, True ); # default: all created submodules are used

# create tagger, sense anotator, and parsers
#tg=freeling.hmm_tagger(DATA+LANG+"/tagger.dat",True,2);
#sen=freeling.senses(DATA+LANG+"/senses.dat");
#parser= freeling.chart_parser(DATA+LANG+"/chunker/grammar-chunk.dat");
#dep=freeling.dep_txala(DATA+LANG+"/dep_txala/dependences.dat", parser.get_start_symbol());

#============================ Freling Initialization ================================


#============================ Descripción del proyecto ==============================
# El procesamiento de lenguaje natural de textos comprende 3 etapas 
# 1) Preprocesamiento: Consiste en normalizar el texto de entrada, en algunos casos 
# se corrigen errores ortográficos, se eliminan espacios innecesarios y dependiendo 
# del tipo de analisis que se desee hacer se le dá un significado alternativo a los 
# emoticones, se elimian hash "#" haciendo que el resto del hash haga parte de la oración
# tambien se modifican urls y nicknames. 
# NOTA: Para este caso no se hace la etapa de preprocesado

# 2) Segmentación de frases y palabras
# Tras el preprocesado del texto ya se han normalizado algunos de los elementos que podián
# complicar la identificación y división de frases y palabras, como la incorrecta colocación de 
# signos de puntuación o la aparición de nombres de usuarios de twitter o hashtags, para la 
# segmenación de oraciones, se usa la biblioteca nltk.
# NOTA: Las estructuras de un parrafo son: 
#   Sentencias o Oraciones (componentes del parrafo).
#   Palabras hace parte de una sentencia u oración 
# NLTK primero lleva a cabo la segmentación de oraciones y luego la segmentación de palabras 

# 3) Análisis morfológico
# Dada una oracion S compuesta por un conjunto de palabras Wi, y un conjunto de etiquetas 
# T con etiquetas Ti, el proceso de análisis morfológico tambien conocido como etiquetación,
# consiste en asignar a cada palabra de la oración su etiqueta correspondiente, creando una 
# lista de tuplas (s,t) donde s partenece a S y t pertenece a T

#============================ Descripción del proyecto ==============================

#============================ Definición Etiquetas EAGLES ===========================

EAGLES_ADJETIVOS = {
  '1A':'Adjetivo',
  '2Q':'Calificativo',
  '3A':'Apreciativo',
  '4M':'Masculino',
  '4F':'Femenino',
  '4C':'Común',
  '5S':'Singular',
  '5P':'Plural',
  '5N':'Invariable',
  '60':'-',
  '7P':'Participio'
}

EAGLES_ADVERBIOS = {
  '1R':'Adverbio',
  '2G':'General',
  '30':'-',
  '40':'-',
  '50':'-'
}

EAGLES_ARTICULOS = {
  '1T':'Artículo',
  '2D':'Definido',
  '3M':'Masculino',
  '3F':'Femenino',
  '3C':'Común',
  '4S':'Singular',
  '4P':'Plural',
  '50':'-'
}

EAGLES_DETERMINANTES = {
  '1D':'Determinante',
  '2D':'Demostrativo',
  '2P':'Posesivo',
  '2T':'Interrogativo',
  '2E':'Exclamativo',
  '2I':'Indefinido',
  '31':'Primera',
  '32':'Segunda',
  '33':'Tercera',
  '4M':'Masculino',
  '4F':'Femenino',
  '4C':'Común',
  '5S':'Singular',
  '5P':'Plural',
  '5N':'Invariable',
  '6O':'-',
  '71':'1 Persona-sg',
  '72':'2 Persona-sg',
  '70':'3 Persona',
  '74':'1 Persona-pl',
  '75':'2 Persona-pl'
}

EAGLES_NOMBRES = {
  '1N':'Nombre',
  '2C':'Común',
  '2P':'Propio',
  '3M':'Masculino',
  '3F':'Femenino',
  '3C':'Común',
  '4S':'Singular',
  '4P':'Plural',
  '4N':'Invariable',
  '50':'-',
  '60':'-',
  '7A':'Apreciativo'
}

EAGLES_VERBOS = {
  '1V':'Verbo',
  '2M':'Principal',
  '2A':'Auxiliar',
  '3I':'Indicativo',
  '3S':'Subjuntivo',
  '3M':'Imperactivo',
  '3C':'Condicional',
  '3N':'Infinitivo',
  '3G':'Gerundio',
  '3P':'Participio',
  '4P':'Presente',
  '4I':'Imperfecto',
  '4F':'Futuro',
  '4S':'Pasado',
  '51':'Primera',
  '52':'Segunda',
  '53':'Tercera',
  '6S':'Singular',
  '6P':'Plural',
  '7M':'Masculino',
  '7F':'Femenino'
}

EAGLES_PRONOMBRES = {
  '1P':'Pronombre',
  '2P':'Personal',
  '2D':'Demostrativo',
  '2X':'Posesivo',
  '2I':'Indefinido',
  '2T':'Interrogativo',
  '2R':'Relativo',
  '31':'Primera',
  '32':'Segunda',
  '33':'Tercera',
  '4M':'Masculino',
  '4F':'Femenino',
  '4C':'Común',
  '5S':'Singular',
  '5P':'Plural',
  '5N':'Invariable',
  '6N':'Normativo',
  '6A':'Acusativo',
  '6D':'Dativo',
  '6O':'Oblicuo',
  '71':'1 Persona-sg',
  '72':'2 Persona-sg',
  '70':'3 Persona',
  '74':'1 Persona-pl',
  '75':'2 Persona-pl',
  '8P':'Polite'
}

EAGLES_CONJUNCIONES = {
  '1C':'Conjunción',
  '2C':'Coordinada',
  '2S':'Subordinada',
  '30':'-',
  '40':'-'
}

EAGLES_NUMERALES = {
  '1M':'Numeral',
  '2C':'Cardinal',
  '2O':'Ordinal',
  '3M':'Masculino',
  '3F':'Femenino',
  '3C':'Común',
  '4S':'Singular',
  '4P':'Plural',
  '50':'-',
  '6P':'Pronominal',
  '6D':'Determinante',
  '6A':'Adjetivo'
}

EAGLES_INTERJECCIONES = {
  '1I':'Interjección'
}

EAGLES_ABREVIATURAS = {
  '1Y':'Abreviratura'
}

EAGLES_PREPOSICIONES = {
  '1S':'Adposición',
  '2P':'Preposición',
  '3S':'Simple',
  '3C':'Contraída',
  '3M':'Masculino',
  '4S':'Singular'
}

EAGLES_SIGNOS_DE_PUNTUACION = {
  '1F':'Puntuación'
}

#============================ Definición Etiquetas EAGLES ===========================

#============================ Algoritmo Propuesto ===================================
""" 
    Iterar el arreglo que devuelve TweetTokenizer (lista de strings) y cada palabra
    a word usando freeling.word() al finalizar crear un list<word>
    
    Parte dificil?:
    Hacer a mano tagueo set_tag() de símbolos, nicknames, hashtags, urls y para
    cada uno setear lock_analysis() para que sean ignorados por el analyze()

    Convertir el list<word> a sentence, aplicar el análisis morfológico, 
    crear estructura de datos para enviar a la aplicación web (interpretar etiquetas)
    y mostrar

 """

def procesar_texto_nltk_freeling(texto):
  # Segmentación de frases (sentencias) y palabras con nltk
  # Tokenización
  tknzr = TweetTokenizer()
  tkn_mensaje = tknzr.tokenize(texto)

def procesar_texto_nltk(texto):
  print ("Usando tokenizacion de nltk: ")
  # tokenizacion con TweetTokenizer
  tknzr = TweetTokenizer()
  tkn_mensaje = tknzr.tokenize(mensaje)
  print (tkn_mensaje)
  # crear list<word> y sentence
  msg = to_freeling_lword(tkn_mensaje)
  msg = freeling.sentence(msg)
  # aplicar análisis morfo
  msg = f_mf.analyze(msg)
  #show_mf(msg)
  for w in sentence:
    print("Análisis de: ", w.get_form())
  for w_a in w.get_analysis():
    print (w_a.get_lemma())
    print (w_a.get_tag())

def procesar_texto_freeling(texto):
  # análisis morfológico solamente sobre las palabras del Español
  print ("Usando tokenizacion de freeling: ")

  # tokenize() de freeling retorna un list<word>
  tk_msg = f_tk.tokenize(texto)
  # En este caso sentence recibe un list<word> y devuelve un sentence
  s_msg = freeling.sentence(tk_msg)
  # analyze recibe un sentence y me retorna un sentence analizado :P
  s_msg = f_mf.analyze(s_msg)

  # retorna vector<word>
  ws = s_msg.get_words()
  # iterar sobre las word
  for w in ws:
    print("Análisis de: ", w.get_form())
    #print (w.get_lemma())
    #print (w.get_tag())
    for a in w.get_analysis():
      print (a.get_lemma())
      print (a.get_tag())

######################################################################
# Funciones internas 

def list2tuple(lis):
  """
  Recibe una lista y devuelve una tupla con los mismos elementos
  """
  tup = ()
  for item in lis:
    tup += (item,)
  return tup

def taggear(w,tag):
  """
  A una palabra freeling "w" le asigna un "tag", lema="" y bloquea el
  análisis respectivo
  """
  analisis = freeling.analysis()
  analisis.set_tag(tag)
  analisis.set_lemma("")
  w.set_analysis(analisis)
  w.lock_analysis()

######################################################################
#

def pre_mf_analyze(tokens):
  """
  :param lis: lista de strings
  
  Hace el casting de los elementos a <word> y si es una expresión
  especial (emoticon, nickname, hashtag o url) le asigna una
  anotación morfológica
  
  :retorna: tupla de words list<word>
  """
  re_emoticon = re.compile(emoticon)
  re_hashtag = re.compile(Hashtag)
  re_nickname = re.compile(AtMention)
  re_url = re.compile(url)
  for i, tk in enumerate(tokens):
    tokens[i] = freeling.word(tk)
    if re_emoticon.match(tk):
      taggear(tokens[i], "E")
    elif re_nickname.match(tk):
      taggear(tokens[i], "@")
    elif re_hashtag.match(tk):
      taggear(tokens[i], "#")
    elif re_hashtag.match(tk):
      taggear(tokens[i], "#")
  return list2tuple(tokens)

def analisis_morfologico(lword):
  """
  Recibe una tupla list<word>, aplica análisis morfológico, por cada
  elemento retorna el elemento y una lista con sublistas de parejas
  lema, tag

  Ejemplo para toca:
  [ toca, [[tocar, VMIP3S0],[toca,NCFS000],[tocar,VMM02S0]] ]
  """
  sentencia = freeling.sentence(lword)
  sentencia = f_mf.analyze(sentencia)

  for w in sentencia:
    print("Análisis de: ", w.get_form())
  for w_a in w.get_analysis():
    print (w_a.get_lemma())
    print (w_a.get_tag())

  return 

######################################################################
# Funciones para interacción externa
def obtener_tk(texto):
  pass

def obtener_mf(texto):
  pass
######################################################################

######################################################################
if __name__ == '__main__':
  mensaje = "El músico bajo toca el bajo"
  mensaje1 = "Mi #Tbt hoy es con @MarcAnthony  y seguro les gustara quiero que continúen \
  ustedes con la letra. Cuando nos volvamos a encontrar :)"
  mensaje2 = "Por fin!! de nuevo en Twitter! =D se me daño mi celular pero ya tengo uno \
  nuevo =D @rosariomeneses1 creo que es igual al tuyo #emoticones XD <3 ^_^!"
  m_emojis = "Hola si =D entonces o.O 12:30 O.o (: jeje :v 1, 2, 3.5 1,2"

  
  # Tokenizar con Twokenize
  tokens = ark_tokenize(m_emojis)
  
######################################################################