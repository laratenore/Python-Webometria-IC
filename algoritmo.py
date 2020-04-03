import sys
import shutil
import fileinput
import unicodedata

def indicePagina(url, vertices, host):
    url = url.strip()
    for i in range(0,len(vertices)):
        if url==vertices[i][0]:
            return i
    if (not host in url):
        url = url.replace('http:/',"")
        url = url.replace('https:/',"")
        url = url.replace('www.',"")
        url = url.split("/")[0]

        for i in range(0,len(vertices)):
            if vertices[i][1]=='externo' and url==vertices[i][0]:
                return i

    elif url.endswith(".pdf"):
        return "pdf"
    elif url.endswith(".htm") or url.endswith(".html") or url.endswith(".oth") or url.endswith(".php") :
        return "htm"
    elif url.endswith(".doc") or url.endswith(".docx") or url.endswith(".rtf") or url.endswith(".odt"):
        return "doc"
    elif url.endswith(".xls") or url.endswith(".xlsx") or url.endswith(".ods") or url.endswith(".odp"):
        return "xls"
    elif url.endswith(".ppt") or url.endswith(".pptx") or url.endswith(".odp"):
        return "ppt"
    elif url.endswith(".zip") or url.endswith(".rar") or url.endswith(".tgr") or url.endswith(".tar.gz") or url.endswith(".7z") or url.endswith(".tar") or url.endswith(".xz")  :
        return "zip"
    elif url.endswith(".txt"):
        return "txt"
    elif url.endswith(".jpg") or url.endswith(".jpeg") or url.endswith(".bmp") or url.endswith(".png") or url.endswith(".gif") or url.endswith(".tif") :
        return "jpg"
    elif url.endswith(".mp3") or url.endswith(".wma") or url.endswith(".aac") or url.endswith(".wav") or url.endswith(".ac3"):
        return "mp3"
    elif url.endswith(".mp4") or url.endswith(".avi") or url.endswith(".mpeg") or url.endswith(".mov") or url.endswith(".rmvb"):
        return "mp4"
    elif url.endswith(".exe") or url.endswith(".bin") or url.endswith(".sh"):
        return "exe"

    else:
        return -1
    


# --------------------------------------------
# Programa principal
# --------------------------------------------
if __name__ == "__main__":
    print("Iniciando leitura do arquivo...")

    arquivoEntrada = "cecs.txt"
    host = "ufabc.edu.br"

    # ========================================
    # FASE 1
    # Criacao de lista de vertices
    count    = 0
    vertices = list([])
    arestas  = list([])

    listaDeExtensoes =  ['pdf', 'htm', 'doc', 'xls', 'ppt', 'zip', 'txt', 'jpg', 'mp3', 'mp4', 'exe']
    

    for line in fileinput.input(arquivoEntrada):
        line = line.strip('\n')
        line = line.replace("//","/")
        if ("main_html" in line):
            line = line[10:]
            count = count+1

            contadorDeArquivos = dict([])
            for ext in listaDeExtensoes:
                contadorDeArquivos[ext] = 0

            vertices.append((line, 'interno', contadorDeArquivos))
        else: 
            if line.startswith("\t") and (not host in line):
                line = line.strip()
                line = line.replace("http:/", "")
                line = line.replace("https:/", "")
                line = line.replace("www.", "")
                line = line.replace("wwws.","")
                line = line.replace("www1.","")
                line = line.split("/")[0]
                if(not (line, 'externo', []) in vertices):
                    vertices.append((line, 'externo', []))

    print(count)
    print (len(vertices))
    for vext in vertices:
        if vext[1]=='externo':
            print(vext)


    # ========================================
    # FASE 2
    # Criacao de lista de arestas
    for line in fileinput.input(arquivoEntrada):
        line = line.strip('\n')
        line = line.replace("//","/")
        if ("main_html" in line):
            line = line[10:]
            indiceOrigem = indicePagina(line, vertices, host)
        elif line.startswith("\t"): 
            line = line.replace("\t","")
            indiceDestino = indicePagina(line, vertices, host)

            if indiceDestino in listaDeExtensoes:
                vertices[indiceOrigem][2][indiceDestino] += 1
            elif not indiceDestino==-1:
                print ("aresta int->ext", [indiceOrigem, indiceDestino] )
                arestas.append([indiceOrigem, indiceDestino])

    
    print(len(arestas))

    # ========================================
    # FASE 3
    # Criacao do grafo
    arquivoSaida = arquivoEntrada+".gdf"
    s = "nodedef>name VARCHAR, label VARCHAR, tipo VARCHAR, numeropdfs DOUBLE, numerohtm DOUBLE, numerodoc DOUBLE, numeroxls DOUBLE, numeroppt DOUBLE, numerozip DOUBLE, numerotxt DOUBLE, numerojpg DOUBLE, numeromp3 DOUBLE, numeromp4 DOUBLE, numeroexe DOUBLE"
    for i in range(0,len(vertices)):
        s += "\n" + str(i) + "," + vertices[i][0]+ "," + vertices[i][1]
        for  ext in listaDeExtensoes:
            if vertices[i][1]=='interno':
                s +=  "," + str(vertices[i][2][ext])
            else:
                s +=  ",0"  


    s += "\nedgedef>node1 VARCHAR,  node2 VARCHAR, directed BOOLEAN"

    for i in range(0,len(arestas)):
        s += "\n" + str(arestas[i][0]) + "," + str(arestas[i][1]) + ", true"

    output = open(arquivoSaida, 'w')
    output.write(s)
    output.close



