Este repositório contém o projeto de um programa de Otimização Multidisciplinar desenvolvido para a equipe Minerva Aerodesign da UFRJ para o projeto de aeronaves destinadas à competição SAE Aerodesign.

O início do desenvolvimento se deu na fase inicial da competição de 2023, porém com o intuito de servir ao futuro da equipe.

A função do programa é otimizar a geometria de uma aeronave de modo a obter uma maior pontuação e satisfazendo as restrições necessárias.

O programa tem base em 2 pacotes:

    Avlwrapper: Traz uma interface em python para o uso do Avl, um software de análise de aerodinâmica e estabilidade que utiliza o método de malha de painéis (VLM).
    OpemMDAO: Um frmework que possibilita a realização simples e rápida de otimizações customizadas.

A geometria é definida no código "prototype.py", que recebe os parâmetros desejados e constrói um modelo de geometria do AVL.

No arquivo "simulator.py", se inserem todos os métodos para rodar, a partir de um indivíduo prototype(), todas as simulações necessárias e calcular todos os coeficientes de aerodinâmica, estabilidade e desempenho, incluindo a pontuação pela qual se deseja avaliar cada indivíduo.

Os arquivos "individual.py" e "optimizer.py" adaptam toda a construção e simulação para a otimização

"performance.py" e "stability.py" são bibliotecas que contém todas as funções, cálculos e verificações das suas respectivas áreas.

Diferentes conceitos de aeronaves precisarão de alterações nos inputs dos arquivos de protótipo, indivíduo e otimizador. Portanto serão forkeadas desse repositório provavelmente. A utilização de branches também pode ser considerada.

Da mesma forma, adaptar o código de um ano para o outro também deve requerer alterações nesses mesmos arquivos, na parte de cálculos de propriedades e restrições.

O fluxograma junto do repositório mostra o básico do funcionamento na versão 03 (pré release).

MSG.: Olá! Tentei documentar o suficiente para que com alguma pesquisa qualquer um com entendimento em python e aerodesign pudesse conseguir entender os códigos, mas não sou nenhum programador (dá pra perceber) e esse programa foi um pouco fruto de um experimento, em colaboração claro com alguns membros de aerodinâmica, desempenho e controle e estabilidade. A equipe já teve um MDO antes cujo domínio sobre se perdeu ao longo dos anos (depois de um tempo ninguém entendia mais como funcionava), então essa foi uma preocupação constante. Qualquer coisa só me contatar, devem haver as infos no GitHub, mas aí vai:

Autor: Lucas Alves da Rosa (lucas.rosa@poli.ufrj.br)

Sinta-se livre para mexer nesses códigos e incluir seu nome aqui ou copiar o que quiser para desenvolver um programa novo!