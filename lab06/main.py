import math
import numpy as np
import cv2
import matplotlib.pyplot as plt
import os

def processar_threshold(caminho_imagem, parametros):
    """Processa usando thresholding e exibe apenas o resultado final."""
    print(f"Processando (Threshold): {caminho_imagem}")
    img_bgr = cv2.imread(caminho_imagem)
    if img_bgr is None: return
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    img_cinza = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)

    # Parâmetros com defaults
    tamanho_kernel_blur = parametros.get('blur_kernel', (5, 5))
    metodo_threshold = parametros.get('metodo_threshold', cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    tamanho_kernel_morf = parametros.get('morph_kernel', (5, 5))
    morph_op = parametros.get('morph_op', cv2.MORPH_OPEN)
    iteracoes_morf = parametros.get('morph_iter', 1)

    # Processamento
    img_blur = cv2.GaussianBlur(img_cinza, tamanho_kernel_blur, 0)
    _, thresh = cv2.threshold(img_blur, 0, 255, metodo_threshold)
    kernel_morf = np.ones(tamanho_kernel_morf, np.uint8)
    thresh_limpa = cv2.morphologyEx(thresh, morph_op, kernel_morf, iterations=iteracoes_morf)
    contornos, _ = cv2.findContours(thresh_limpa, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Desenhar contorno
    img_contorno_final = img_rgb.copy()
    if contornos:
        contornos = sorted(contornos, key=cv2.contourArea, reverse=True)
        cv2.drawContours(img_contorno_final, [contornos[0]], -1, (0, 255, 0), 3)
    else:
        print("Nenhum contorno (threshold) encontrado.")

    # Exibir apenas resultado final
    nome_imagem = os.path.basename(caminho_imagem)
    plt.figure(figsize=(8, 6))
    plt.imshow(img_contorno_final)
    plt.title(f"Resultado Final (Threshold): {nome_imagem}", fontsize=14)
    plt.axis('off')
    plt.show()

def processar_canny(caminho_imagem, parametros):
    """Processa usando Canny e exibe apenas o resultado final."""
    print(f"Processando (Canny): {caminho_imagem}")
    img_bgr = cv2.imread(caminho_imagem)
    if img_bgr is None: return
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    img_cinza = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)

    # Parâmetros com defaults
    blur_kernel = parametros.get('blur_kernel', (5, 5))
    canny_thresh1 = parametros.get('canny_thresh1', 50)
    canny_thresh2 = parametros.get('canny_thresh2', 150)
    dilate_ksize = parametros.get('dilate_kernel_size', (5, 5))
    dilate_iter = parametros.get('dilate_iter', 1)
    min_area = parametros.get('contour_min_area', 1000)
    max_bottom_y_ratio = parametros.get('contour_max_bottom_y_ratio', 0.6)

    # Processamento
    img_blur = cv2.GaussianBlur(img_cinza, blur_kernel, 0)
    bordas = cv2.Canny(img_blur, canny_thresh1, canny_thresh2)
    kernel_dilate = np.ones(dilate_ksize, np.uint8)
    bordas_dilatadas = cv2.dilate(bordas, kernel_dilate, iterations=dilate_iter)
    contornos, _ = cv2.findContours(bordas_dilatadas, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Filtrar e Desenhar contornos
    img_contorno_final = img_rgb.copy()
    altura_img = img_cinza.shape[0]
    max_y_permitido = int(altura_img * max_bottom_y_ratio)
    contornos_filtrados = []

    for cnt in contornos:
        area = cv2.contourArea(cnt)
        x, y, w, h = cv2.boundingRect(cnt)
        y_inferior = y + h
        if area > min_area and y_inferior < max_y_permitido:
            contornos_filtrados.append(cnt)
            cv2.drawContours(img_contorno_final, [cnt], -1, (0, 255, 0), 2)

    if not contornos_filtrados:
        print("Nenhum contorno (canny) encontrado após filtragem.")

    # Exibir apenas resultado final
    nome_imagem = os.path.basename(caminho_imagem)
    plt.figure(figsize=(8, 6))
    plt.imshow(img_contorno_final)
    plt.title(f"Resultado Final (Canny): {nome_imagem}", fontsize=14)
    plt.axis('off')
    plt.show()

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    diretorio_imagens = os.path.join(script_dir, 'figs')

    if not os.path.exists(diretorio_imagens):
        print(f"Erro: Diretório de imagens não encontrado em {diretorio_imagens}")
        exit()

    # Parâmetros ainda necessários para flexibilidade
    parametros_padrao = {
        'metodo': 'threshold', 'blur_kernel': (5, 5), 'metodo_threshold': cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU,
        'morph_kernel': (5, 5), 'morph_op': cv2.MORPH_OPEN, 'morph_iter': 1
    }
    parametros_por_imagem = {
        'GIRAFA.jpeg': { 'metodo': 'threshold', 'metodo_threshold': cv2.THRESH_BINARY + cv2.THRESH_OTSU },
        'SATELITE.jpeg': { 'metodo': 'threshold', 'metodo_threshold': cv2.THRESH_BINARY + cv2.THRESH_OTSU, 'blur_kernel': (5, 5), 'morph_op': cv2.MORPH_OPEN, 'morph_kernel': (7, 7) },
        'AVIAO.jpeg': { 'metodo': 'canny', 'blur_kernel': (5, 5), 'canny_thresh1': 50, 'canny_thresh2': 150, 'dilate_kernel_size': (5, 5), 'dilate_iter': 1, 'contour_min_area': 1000, 'contour_max_bottom_y_ratio': 0.6 }
    }
    arquivos_imagem = ['GIRAFA.jpeg', 'SATELITE.jpeg', 'AVIAO.jpeg']

    for img_arquivo in arquivos_imagem:
        caminho = os.path.join(diretorio_imagens, img_arquivo)
        if os.path.exists(caminho):
            params_atuais = parametros_padrao.copy()
            if img_arquivo in parametros_por_imagem:
                params_atuais.update(parametros_por_imagem[img_arquivo])

            metodo = params_atuais.get('metodo', 'threshold')
            print(f"--> Usando método '{metodo}' para '{img_arquivo}'")

            if metodo == 'canny':
                processar_canny(caminho, params_atuais)
            else:
                processar_threshold(caminho, params_atuais)
        else:
            print(f"Aviso: Arquivo de imagem não encontrado em {caminho}")
