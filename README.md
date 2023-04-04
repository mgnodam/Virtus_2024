############################### INSTRUÇÕES DE INSTALAÇÃO.:
Aqui estarão as instruções recomendadas para rodar o programa de otimização. Pode ser um pouco complicado e diferente para cada máquina baseado no que já havia instalado na máquina anteriormente. Talvez falte algo aqui que requeira um pouco de investigação, se descobrir coloque aqui.

1. Instalar o Anaconda, para gerenciar o ambiente virtuais e instalar os pacotes
2. Instalar o VSCode, para editar e rodar os códigos
3. Instalar os seguintes pacotes:
    pip install openmdao;
    pip install pyDOE2;
    pip install avlwrapper;
    pip install mpi4py;

    o avlwrapper do pip provavelmente estará desatualizado, use: git clone https://github.com/jbussemaker/AVLWrapper.git; e substitua o conteúdo do avlwrapper no C:/Users/"SeuUsuário"/anaconda3/Lib/site-packages/avlwrapper pelo que você acabou de clonar do git
4. Baixar o executável do avl na versão 3.36 e copiar para dentro dessa pasta do avlwrapper (se não achar o executável tente especificar mais o caminho do diretório no arquivo config)
5. Abrir o vscode pelo ambiente do anaconda, tentar rodar e ir consertando os erros que vão dar...

############################### DESCRIÇÃO.:
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

Diferentes conceitos de aeronaves precisarão de alterações nos inputs dos arquivos de protótipo, indivíduo e otimizador. O melhor é criar diretórios diferentes para diferentes configurações. Da mesma forma, adaptar o código de um ano para o outro também deve requerer alterações nesses mesmos arquivos, na parte de cálculos de propriedades e restrições além de outras melhorias.

O fluxograma junto do repositório mostra a estrutura básica do funcionamento.

O notebook "viewer.ipynb" possibilita a visualização gráfica da evolução dos indivíduos em termos de objetivos e restrições.

O script "post_processing" foi criado para incluir todas as funções de pós processamento além da simples visualização do arquivo "viewer.ipynb". Uma das funções por exemplo é filtrar as melhores aeronaves que se adequem totalmente a todas as restrições fornecendo as variáveis de design adotadas e organizar em um log.


############################### MSG.:
Olá! Tentei documentar o suficiente para que com alguma pesquisa qualquer um com entendimento em python e aerodesign pudesse conseguir entender os códigos, mas não sou nenhum programador (dá pra perceber) e esse programa foi um pouco fruto de um experimento, em colaboração claro com alguns membros de aerodinâmica, desempenho e controle e estabilidade. A equipe já teve um MDO antes cujo domínio sobre se perdeu ao longo dos anos (depois de um tempo ninguém entendia mais como funcionava), então essa foi uma preocupação constante. Qualquer coisa só me contatar, devem haver as infos no GitHub, mas aí vai:

Autor: Lucas Alves da Rosa (lucas.rosa@poli.ufrj.br)

Sinta-se livre para mexer nesses códigos e incluir seu nome aqui ou copiar o que quiser para desenvolver um programa novo!