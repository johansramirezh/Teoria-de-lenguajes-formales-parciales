class Nodo:
    def __init__(self, simbolo):
        self.simbolo = simbolo
        self.hijos = []


class GeneradorArbol:
    def __init__(self):
        self.reglas = {}
        self.simbolo_inicial = ""

    def leer_reglas(self, nombre_archivo):
        archivo = open(nombre_archivo, "r", encoding="utf-8")
        lineas = archivo.readlines()
        archivo.close()
        for linea in lineas:
            linea = linea.strip()
            if linea == "":
                continue
          
            partes = linea.split("->")
            cabeza = partes[0].strip()
           
            if self.simbolo_inicial == "":
                self.simbolo_inicial = cabeza
           
            alternativas = []
            for texto_alternativa in partes[1].split("|"):
                alternativas.append(texto_alternativa.split())
           
            self.reglas[cabeza] = alternativas
       

    def leer_pasos(self, nombre_archivo):
        archivo = open(nombre_archivo, "r", encoding="utf-8")
        lineas = archivo.readlines()
        archivo.close()
        modo = lineas[0].strip()
        pasos = []
        for i in range(1, len(lineas)):
            linea = lineas[i].strip()
            if linea == "":
                continue
            partes = linea.split("->")
            cabeza = partes[0].strip()
            cuerpo = partes[1].split()
            pasos.append([cabeza, cuerpo])
        return modo, pasos

    def es_no_terminal(self, simbolo):
        return simbolo in self.reglas

    def buscar_posicion(self, frase, modo):
        if modo == "izquierda":
            for i in range(len(frase)):
                if self.es_no_terminal(frase[i].simbolo):
                    return i

        else:
            for i in range(len(frase) - 1, -1, -1):
                if self.es_no_terminal(frase[i].simbolo):
                    return i

        return -1

    def mostrar_frase(self, frase):
        texto = ""
        for nodo in frase:
            texto = texto + nodo.simbolo + " "
        
        return texto

    def construir_arbol(self, modo, pasos):
        raiz = Nodo(self.simbolo_inicial)
        frase = [raiz]
        print("Paso 0 :", self.mostrar_frase(frase))
        numero_paso = 0
        for paso in pasos:
            numero_paso = numero_paso + 1
            cabeza = paso[0]
            cuerpo = paso[1]

            if cabeza not in self.reglas or cuerpo not in self.reglas[cabeza]:
                print("ERROR en el paso", numero_paso, ": la producción no existe en la gramática.")
                return None

            posicion = self.buscar_posicion(frase, modo)
            if posicion == -1:
                print("ERROR en el paso", numero_paso, ": ya no quedan no terminales.")
                return None

            nodo = frase[posicion]

            if nodo.simbolo != cabeza:
                print("ERROR en el paso", numero_paso, ": en la derivación por la", modo,
                      "toca reemplazar", nodo.simbolo, "y no", cabeza)
                return None

            for simbolo in cuerpo:
                nodo.hijos.append(Nodo(simbolo))

            frase.pop(posicion)
            lugar = posicion
            for hijo in nodo.hijos:
                frase.insert(lugar, hijo)
                lugar = lugar + 1
  
            print("Paso", numero_paso, ":", self.mostrar_frase(frase))
  
        print("Frase obtenida:", self.mostrar_frase(frase))
        return raiz

    def imprimir_arbol(self, nodo, nivel):

        if nivel == 0:
            print(nodo.simbolo)
        else:
            print("    " * (nivel - 1) + "|-- " + nodo.simbolo)

        for hijo in nodo.hijos:
            self.imprimir_arbol(hijo, nivel + 1)



def main():
    nombre_reglas = input("Archivo de reglas (ejemplo: reglas): ")
    nombre_pasos = input("Archivo de pasos (ejemplo: pasos): ")
    generador = GeneradorArbol()
    generador.leer_reglas(nombre_reglas)
    modo, pasos = generador.leer_pasos(nombre_pasos)
    print("Derivación por la", modo)
    raiz = generador.construir_arbol(modo, pasos)
    if raiz is not None:
        print("")
        print("Árbol de derivación:")
        generador.imprimir_arbol(raiz, 0)



main()