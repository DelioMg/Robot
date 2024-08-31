# Navegação Autônoma com iRobot Create 2 e Visão Computacional

### Introdução
Este projeto visa desenvolver um robô autônomo baseado em um iRobot Create 2, capaz de navegar em ambientes desconhecidos e encontrar o melhor caminho para um objetivo predefinido. A inteligência do robô reside em uma Orange Pi 3B que processa dados de uma câmera e sensores ultrassônicos para construir um mapa do ambiente e planejar a trajetória. A programação é feita em Python, aproveitando as bibliotecas OpenCV para processamento de imagens e frameworks de robótica para controle do iRobot e planejamento de trajetória.

### Etapas do Projeto:

### 1.Configuração do Hardware:

1.Instalação do sistema operacional na Orange Pi 3B.
2.Conexão da câmera e dos sensores ultrassônicos à Orange Pi.
3.Configuração da comunicação serial entre a Orange Pi e o iRobot Create 2.

#### 2.Desenvolvimento do Software:

**1.Aquisição de dados:** Captura de imagens da câmera e leitura dos dados dos sensores ultrassônicos.

**2.Processamento de imagens:** Utilização de técnicas de visão computacional para extrair informações relevantes das imagens, como detecção de obstáculos, reconhecimento de marcadores ou estimativa de profundidade.

**3.strução de mapas:** Criação de um mapa do ambiente a partir dos dados da câmera e dos sensores, utilizando algoritmos de SLAM (Simultaneous Localization and Mapping).

**4.Planejamento de trajetória:** Cálculo da melhor rota para o objetivo, considerando o mapa do ambiente e as restrições do robô.

**5.Controle do robô:** Envio de comandos para o iRobot Create 2 para seguir a trajetória planejada, utilizando a comunicação serial.

#### 3.Integração dos Componentes:

1.Desenvolvimento de um loop principal que controla a execução das diferentes etapas do projeto.
- Capturar imagens.
- Processar imagens.
- Atualizar o mapa.
- Planejar a trajetória.
- Controlar o robô.
  
2.Implementação de mecanismos de segurança para evitar colisões e garantir a estabilidade do robô.

### Especificação Detalhada:

#### Hardware:

- **Orange Pi 3B:** Processador principal, NPU para aceleração da visão computacional, portas USB para comunicação e expansão.
- **iRobot Create 2:** Plataforma robótica com sensores e atuadores básicos.
- **Conversor de Nível USB:** Garante a compatibilidade de voltagem entre a Orange Pi (3.3V) e o iRobot (5V).
- **Bateria:** Fornece energia para a Orange Pi e seus periféricos.
- **ESP32:** Microcontrolador para tarefas de baixo nível, como leitura de sensores adicionais ou controle de atuadores.
- **Sensores:** Ultrassônicos, câmera, outros sensores conforme a necessidade da aplicação.

#### Software:

- **Sistema Operacional:** Raspberry Pi OS (ou outro sistema Linux compatível com a Orange Pi).
- **Linguagem de Programação:** Python 3.
- **Bibliotecas:**
- **PySerial:** Comunicação serial com o iRobot.
- **OpenCV:** Processamento de imagens, visão computacional.
- **TensorFlow/PyTorch:** Framework de deep learning para YOLO.
- **Numpy, SciPy:** Cálculos numéricos.
- **Modelo de Visão Computacional:** YOLO (You Only Look Once) para detecção de objetos em tempo real.
- **Algoritmos de Navegação:** SLAM, pathfinding (A*, RRT).


### Estrutura do Projeto
```
project-root/
│
├── hardware-setup/
│   ├── orange-pi-setup.md
│   ├── sensor-setup.md
│   └── camera-setup.md
│
├── software/
│   ├── data-acquisition.py
│   ├── image-processing.py
│   ├── slam-algorithm.py
│   ├── path-planning.py
│   └── robot-control.py
│
├── docs/
│   ├── installation.md
│   ├── usage.md
│   ├── contributing.md
│   └── license.md
│
└── README.md
```

3. **Parâmetros Configuráveis**:
   - Descrição de parâmetros configuráveis e suas funções está disponível no arquivo `docs/usage.md`.

### Estrutura do Código
- **Diagrama de Blocos**:
  ![Diagrama de Blocos](docs/block-diagram.png)

- **Descrição dos Arquivos Principais**:
  - `data-acquisition.py`: Captura de imagens da câmera e leitura dos dados dos sensores ultrassônicos.
  - `image-processing.py`: Utilização de técnicas de visão computacional para processamento de imagens.
  - `slam-algorithm.py`: Construção de mapas utilizando algoritmos de SLAM.
  - `path-planning.py`: Cálculo da melhor rota para o objetivo.
  - `robot-control.py`: Controle do robô e envio de comandos para o iRobot Create 2.

### Contribuições
1. **Como Contribuir**:
   - Faça um fork do repositório.
   - Crie uma branch para sua modificação (`git checkout -b feature/feature-name`).
   - Commit suas mudanças (`git commit -am 'Add some feature'`).
   - Push para a branch (`git push origin feature/feature-name`).
   - Abra um Pull Request.

2. **Guia de Estilo**:
   - Utilize o guia de estilo PEP 8 para Python.

### Licença
Este projeto está licenciado sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

### Autores
- [Delio](https://github.com/DelioMg)

### Agradecimentos
Agradecimentos a todos que contribuíram direta ou indiretamente para o desenvolvimento deste projeto.

