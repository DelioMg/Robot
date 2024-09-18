# Robô Seguidor de Pessoa com iRobot Create 2 e YOLOv5s

### Introdução
Este projeto desenvolve um robô seguidor de pessoa utilizando a plataforma **iRobot Create 2**, integrado com um modelo de detecção de objetos baseado em **YOLOv5s**. A inteligência do robô é implementada em Python e roda em uma **Orange Pi 3B**, que utiliza a câmera para detectar e seguir uma pessoa em tempo real. O projeto também usa sensores ultrassônicos para evitar colisões enquanto o robô segue seu alvo.

### Etapas do Projeto:

#### 1. Configuração do Hardware:

1. Instalação do sistema operacional na Orange Pi 3B.
2. Conexão da câmera e sensores ultrassônicos à Orange Pi.
3. Configuração da comunicação serial entre a Orange Pi e o iRobot Create 2.

#### 2. Desenvolvimento do Software:

1. **Aquisição de dados:** Captura de imagens em tempo real da câmera e leitura dos dados dos sensores ultrassônicos.
   
2. **Detecção de pessoas:** Utilização do **YOLOv5s** para detectar e rastrear a pessoa na imagem.
   
3. **Controle de movimentação:** Cálculo da trajetória para que o robô siga a pessoa enquanto evita obstáculos detectados pelos sensores ultrassônicos.

4. **Integração dos componentes:** Coordenação da visão computacional, controle de obstáculos e movimentação dos motores do robô via comandos seriais.

5. **Controle de segurança:** Implementação de mecanismos para garantir que o robô evite colisões enquanto segue a pessoa.

### Especificação Detalhada:

#### Hardware:

- **Orange Pi 3B:** Computador principal para processamento de visão computacional e controle do robô.
- **iRobot Create 2:** Base robótica com motores e sensores.
- **Câmera USB:** Captura de vídeo para a detecção de pessoas.
- **Sensores ultrassônicos:** Usados para detecção de obstáculos e prevenção de colisões.
- **Bateria:** Fonte de alimentação para a Orange Pi e seus periféricos.

#### Software:

- **Sistema Operacional:** Linux (Armbian para Orange Pi).
- **Linguagem de Programação:** Python 3.
- **Bibliotecas:**
  - **YOLOv5s**: Framework para detecção de objetos.
  - **OpenCV**: Processamento de imagens em tempo real.
  - **PySerial**: Comunicação serial com o iRobot Create 2.
  - **Numpy**: Cálculos matemáticos.
  - **Eventlet/Flask-SocketIO**: Comunicação em tempo real e controle remoto via interface web.
  
#### Fluxo do Sistema:

1. **Captura de vídeo:** A câmera captura o vídeo em tempo real.
2. **Processamento com YOLOv5s:** O vídeo é processado para detectar a pessoa que será seguida.
3. **Movimentação do robô:** O robô calcula e executa o movimento necessário para seguir a pessoa, enquanto monitora os sensores ultrassônicos para evitar colisões.
4. **Correção de trajetória:** O robô ajusta sua trajetória conforme a posição da pessoa muda.

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
│   ├── yolo-detection.py
│   ├── robot-control.py
│   └── obstacle-avoidance.py
│
├── docs/
│   ├── installation.md
│   ├── usage.md
│   ├── contributing.md
│   └── license.md
│
└── README.md
```

### Estrutura do Código

- **Descrição dos Arquivos Principais**:
  - `data-acquisition.py`: Captura de vídeo da câmera e leitura dos sensores ultrassônicos.
  - `yolo-detection.py`: Utilização do YOLOv5s para detectar a pessoa que o robô irá seguir.
  - `robot-control.py`: Controle da movimentação do robô para seguir a pessoa.
  - `obstacle-avoidance.py`: Algoritmo para evitar obstáculos usando sensores ultrassônicos.

### Como Usar:

1. **Instalar dependências:**
   - Siga as instruções no arquivo `docs/installation.md` para instalar as dependências necessárias.
   
2. **Executar o robô:**
   - Use o comando para iniciar o sistema:
     ```bash
     python3 main.py
     ```

3. **Monitorar e Controlar:**
   - A interface de controle web pode ser acessada para monitorar e ajustar o comportamento do robô em tempo real.
   - Acesse a página web via `http://<ip_da_orange_pi>:5000` para visualização ao vivo e controle.

### Parâmetros Configuráveis:

Os parâmetros configuráveis, como velocidade do robô, sensibilidade do YOLO, e distância mínima para evitar obstáculos, podem ser ajustados no arquivo `config.py`.

### Contribuições

1. **Como Contribuir**:
   - Faça um fork do repositório.
   - Crie uma branch para sua modificação (`git checkout -b feature/nova-funcionalidade`).
   - Commit suas mudanças (`git commit -am 'Adiciona nova funcionalidade'`).
   - Push para a branch (`git push origin feature/nova-funcionalidade`).
   - Abra um Pull Request.

2. **Guia de Estilo**:
   - Utilize o guia de estilo PEP 8 para Python.

### Licença

Este projeto está licenciado sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

### Autores

- [Seu Nome](https://github.com/DelioMg)
