# Processamento de Imagens para Detecção de Contornos

Este projeto demonstra diferentes técnicas de processamento de imagem usando OpenCV e Python para identificar e destacar o contorno principal de objetos em diferentes imagens.

## Objetivo

O objetivo principal do script `main.py` é carregar imagens específicas (`GIRAFA.jpeg`, `SATELITE.jpeg`, `AVIAO.jpeg`) e aplicar um fluxo de processamento adequado para cada uma, visando isolar e desenhar o contorno do objeto de interesse principal.

## Imagens Processadas

O script é configurado para processar as seguintes imagens localizadas no diretório `figs/`:

1.  `GIRAFA.jpeg`
2.  `SATELITE.jpeg`
3.  `AVIAO.jpeg`

## Abordagens de Processamento

Devido às características distintas de cada imagem (contraste, iluminação, complexidade do fundo), duas abordagens principais são utilizadas, configuradas através de parâmetros no script:

1.  **Baseada em Thresholding (Limiarização)**
2.  **Baseada em Detecção de Bordas (Canny)**

### 1. Abordagem Baseada em Thresholding

Esta abordagem é usada para a `GIRAFA.jpeg` e `SATELITE.jpeg`. O objetivo é segmentar a imagem em primeiro plano (objeto) e fundo com base na intensidade dos pixels.

**Passos:**

1.  **Carregamento e Pré-processamento:**
    *   A imagem é carregada no formato BGR.
    *   Convertida para RGB (útil para exibição correta com Matplotlib, embora a exibição intermediária tenha sido removida na versão final).
    *   Convertida para **Escala de Cinza**, pois as operações de thresholding geralmente trabalham em um único canal.

2.  **Suavização (GaussianBlur):**
    *   Um filtro Gaussiano é aplicado para reduzir ruídos e suavizar a imagem. Isso ajuda a evitar que o thresholding crie muitos pequenos contornos indesejados devido a variações mínimas de intensidade. O tamanho do kernel (ex: `(5, 5)`) controla a intensidade do blur.

3.  **Limiarização (Thresholding):**
    *   Converte a imagem em escala de cinza para uma imagem **binária** (preto e branco). O objetivo é fazer o objeto de interesse ficar branco e o fundo preto (ou vice-versa).
    *   **Global (Otsu):** Usado para a `GIRAFA.jpeg`. O método `THRESH_BINARY + THRESH_OTSU` assume que o objeto é mais claro que o fundo e calcula automaticamente um limiar global ótimo para separar os dois.
    *   **Adaptativo:** Usado para a `SATELITE.jpeg`. O método `cv2.adaptiveThreshold` com `ADAPTIVE_THRESH_GAUSSIAN_C` calcula um limiar diferente para cada pequena região da imagem, baseado na média ponderada gaussiana da vizinhança. Isso é útil para imagens com iluminação não uniforme. `THRESH_BINARY` é usado para tornar as regiões claras (como o satélite) brancas. Parâmetros como `adaptive_blockSize` (tamanho da vizinhança) e `adaptive_C` (constante de ajuste) são cruciais.

4.  **Operações Morfológicas:**
    *   Aplicadas na imagem binária para limpar "ruídos" resultantes do thresholding.
    *   `cv2.MORPH_OPEN`: Remove pequenos pontos brancos isolados (ruído). Usado para o `SATELITE.jpeg` após o threshold adaptativo.
    *   `cv2.MORPH_CLOSE`: Preenche pequenos buracos pretos dentro de objetos brancos. (Não usado ativamente na configuração final, mas foi testado).
    *   O tamanho do `kernel` e o número de `iterations` controlam a intensidade da operação.

5.  **Detecção de Contornos (`cv2.findContours`):**
    *   Identifica os limites das formas brancas na imagem binária limpa. `RETR_EXTERNAL` busca apenas os contornos mais externos.

6.  **Seleção e Desenho:**
    *   Os contornos encontrados são geralmente ordenados por área.
    *   Para a `GIRAFA.jpeg`, o maior contorno é selecionado e desenhado na imagem original.
    *   Para o `SATELITE.jpeg` (com threshold adaptativo), os 3 maiores contornos são desenhados para aumentar a chance de visualizar o satélite, mesmo que não seja o maior objeto detectado.

### 2. Abordagem Baseada em Detecção de Bordas (Canny)

Esta abordagem é usada para a `AVIAO.jpeg`, onde o thresholding global ou adaptativo teve dificuldade em isolar o avião devido ao fundo complexo.

**Passos:**

1.  **Carregamento e Pré-processamento:**
    *   Similar à abordagem de thresholding (BGR -> RGB -> Cinza).

2.  **Suavização (GaussianBlur):**
    *   Aplicada antes do Canny para reduzir ruído que poderia ser interpretado como bordas falsas.

3.  **Detecção de Bordas (`cv2.Canny`):**
    *   Algoritmo que detecta uma ampla gama de bordas na imagem com base em gradientes de intensidade. Utiliza dois limiares (`canny_thresh1` e `canny_thresh2`) para classificar as bordas como fortes ou fracas.

4.  **Dilatação (`cv2.dilate`):**
    *   As bordas detectadas pelo Canny podem ser finas ou quebradas. A dilatação "engrossa" as linhas brancas das bordas, ajudando a conectar segmentos próximos e formar contornos mais fechados.

5.  **Detecção de Contornos (`cv2.findContours`):**
    *   Encontra os contornos nas bordas dilatadas.

6.  **Filtragem de Contornos:**
    *   Como Canny detecta muitas bordas (pista, árvore, nuvens), aplicamos filtros para selecionar apenas os contornos que provavelmente pertencem ao avião:
        *   **Área Mínima (`contour_min_area`):** Ignora contornos muito pequenos (ruído).
        *   **Posição Vertical (`contour_max_bottom_y_ratio`):** Ignora contornos cuja parte inferior esteja muito abaixo na imagem (ex: contornos da pista ou do horizonte baixo), assumindo que o avião estará mais acima.

7.  **Desenho dos Contornos Filtrados:**
    *   Todos os contornos que passam pelos filtros são desenhados na imagem original.

## Configuração por Imagem

O script `main.py` utiliza um dicionário chamado `parametros_por_imagem`. Cada chave é o nome de um arquivo de imagem, e o valor é outro dicionário contendo os parâmetros específicos para aquela imagem. Isso inclui:

*   `'metodo'`: Define qual abordagem usar (`'threshold'` ou `'canny'`).
*   Parâmetros específicos para cada método (kernels de blur/morfologia, método/limiares de thresholding, limiares Canny, parâmetros de dilatação, filtros de contorno, etc.).

Isso permite ajustar finamente o processamento para obter o melhor resultado possível para cada imagem individualmente.

## Execução

Para executar o script e ver os resultados finais para cada imagem:

```bash
python lab06/main.py
```

Certifique-se de ter as bibliotecas OpenCV (`opencv-python`), NumPy e Matplotlib instaladas (`pip install opencv-python numpy matplotlib`) e que as imagens estejam no diretório `lab06/figs`.
