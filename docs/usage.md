# Instruções de Uso

## 1. Pré-requisitos

Antes de começar a usar o robô seguidor de pessoa, certifique-se de que o ambiente está devidamente configurado e que todas as dependências necessárias foram instaladas. Verifique os pré-requisitos abaixo:

### Hardware
- **iRobot Create 2** conectado à **Orange Pi 3B**.
- **Câmera USB** conectada à Orange Pi.
- **Sensores Ultrassônicos** conectados à Orange Pi (opcional para prevenção de colisões).

### Software
- **Sistema Operacional:** Armbian (ou outra distribuição Linux compatível com Orange Pi).
- **Python 3.7+** instalado.
- **YOLOv5s** (ou outra versão compacta do YOLO) instalado para detecção de objetos.

Para garantir que todos os pacotes Python necessários estão instalados, você pode executar o comando:

```bash
pip install -r requirements.txt
```

## 2. Iniciando o Sistema

### 2.1. Conectando o iRobot Create 2

Certifique-se de que o iRobot Create 2 está ligado e conectado via USB à Orange Pi na porta `/dev/ttyUSB0`. 

### 2.2. Executando o Código

Para iniciar o sistema e colocar o robô em operação, siga estas etapas:

1. **Suba o servidor Flask para a interface de controle web:**

   No terminal da Orange Pi, navegue até o diretório do projeto e execute:

   ```bash
   python3 main.py
   ```

2. **Acesse a interface web de controle:**

   A interface pode ser acessada pelo navegador através do endereço:
   
   ```bash
   http://<ip_da_orange_pi>:5000
   ```

   Substitua `<ip_da_orange_pi>` pelo IP real da Orange Pi na rede. 

   Na interface web, você poderá monitorar a câmera em tempo real, controlar a movimentação do robô e visualizar os dados dos sensores.

### 2.3. Comandos via Interface Web

#### Controles de Movimentação

- **Cima (`Up`)**: O robô se move para frente.
- **Baixo (`Down`)**: O robô recua.
- **Esquerda (`Left`)**: O robô gira à esquerda.
- **Direita (`Right`)**: O robô gira à direita.

#### Outros Comandos

- **Buzina (`Beep`)**: O robô emitirá um som de alerta.
- **Reset (`Reset`)**: O robô será reinicializado.
- **Parada Automática**: O robô para automaticamente quando um obstáculo é detectado.

## 3. Parâmetros Configuráveis

### 3.1. Ajuste de Velocidade

A velocidade de movimentação do robô pode ser ajustada nos parâmetros `VELOCITYCHANGE` e `ROTATIONCHANGE` no arquivo `config.py`.

Exemplo:

```python
VELOCITYCHANGE = 150  # Ajuste a velocidade para frente e para trás
ROTATIONCHANGE = 120  # Ajuste a velocidade de rotação
```

### 3.2. YOLOv5s - Sensibilidade de Detecção

O modelo YOLOv5s pode ser ajustado para alterar a sensibilidade da detecção da pessoa a ser seguida. Isso pode ser feito modificando o parâmetro de confiança mínima no arquivo de configuração:

```python
CONFIDENCE_THRESHOLD = 0.5  # Ajuste a confiança mínima para detectar uma pessoa
```

Aumente esse valor para aumentar a precisão e diminuir detecções falsas, ou reduza para permitir mais detecções.

## 4. Diagnóstico e Solução de Problemas

### 4.1. O robô não está se movendo

- Verifique se a conexão com o iRobot Create 2 foi estabelecida corretamente. Use o comando `dmesg` para verificar se o dispositivo está conectado à porta `/dev/ttyUSB0`.
- Certifique-se de que o robô está no **modo passivo** e depois no **modo seguro**. Isso é feito automaticamente ao iniciar o código, mas você pode verificar os logs no terminal.

### 4.2. O vídeo da câmera não está sendo exibido

- Certifique-se de que a câmera está corretamente conectada à Orange Pi. Use o comando `lsusb` para verificar se a câmera está listada.
- Verifique se o OpenCV está configurado corretamente e que a câmera está sendo inicializada no código.

### 4.3. Detecção de pessoa falhando

- Verifique se o modelo YOLOv5s foi carregado corretamente e se o caminho para o modelo está correto no código.
- Experimente ajustar o parâmetro de confiança mínima (`CONFIDENCE_THRESHOLD`) no arquivo `config.py` para aumentar a sensibilidade de detecção.

## 5. Atualizando o Sistema

Sempre que houver atualizações no repositório, faça o **pull** das mudanças mais recentes e atualize as dependências:

```bash
git pull origin main
pip install -r requirements.txt
```

## 6. Desligando o Sistema

Para desligar o sistema com segurança:

1. Acesse o terminal e pressione `Ctrl+C` para interromper a execução do servidor Flask.
2. Desligue o iRobot Create 2 manualmente ou desconecte-o da Orange Pi.

