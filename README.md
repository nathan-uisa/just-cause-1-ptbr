# Tradução 100% PT-BR para Just Cause (2006) 🇧🇷

[![Just Cause](https://img.shields.io/badge/Game-Just%20Cause%20(2006)-orange.svg)](https://store.steampowered.com/app/6880/Just_Cause/)
[![Status](https://img.shields.io/badge/Status-100%25%20Traduzido-brightgreen.svg)]()
[![Platform](https://img.shields.io/badge/Plataforma-PC%20(Windows%20%2F%20Linux)-blue.svg)]()
[![Python](https://img.shields.io/badge/Python-3.6%2B-blue.svg)]()
[![License](https://img.shields.io/badge/Licen%C3%A7a-MIT-green.svg)]()

Tradução completa e definitiva para Português do Brasil do primeiro **Just Cause (2006)** para PC (Steam / GOG / DVD).

Diferente de versões parciais ou traduções incompletas, este projeto traduz **100% de todo o conteúdo de texto do jogo** diretamente nos contêineres originais dos arquivos de dados (`.arc` / `.tab`), com instalador automatizado para Windows e Linux.

---

## 🌟 O Que Foi Traduzido:

- **Menus & Interface Geral:**
  - Menu Principal, Novo Jogo, Carregar Jogo, Perfis, Créditos, Menu de Pausa.
  - Menus completos de Configurações de Vídeo, Áudio, Jogabilidade e Controles.
  - Telas de PDA, Mapa Político, status das províncias e vilarejos.
  - Telas de carregamento (*loading screens*) e telas de *Game Over*.
- **Campanha Principal Completa (Atos 1, 2 e 3):**
  - Todas as 21 missões da história traduzidas.
  - Legendas completas de todas as *cutscenes* com os marcadores de tempo de áudio (`{t:min:seg}`) rigorosamente preservados.
  - Todos os diálogos via rádio com Tom Sheldon, Maria Kane, Presidente Salvador Mendoza e José Caramicas.
- **Missões Secundárias & Mundo Aberto:**
  - Todas as missões dos contatos: Benito, Roberto, Tomas, Jimenez e Agência Sheldon.
  - Todas as missões mundiais (*World Side Missions*): assassinatos, sequestro de comboios, resgates de reféns e suporte aéreo.
  - Missões de tomada e libertação de vilarejos e províncias por toda a ilha de San Esperito.
  - Nomes de vilarejos, esconderijos (*safehouses*), pontos de entrega de veículos e drogas.
- **Tutoriais & HUD:**
  - Dicas de jogabilidade na tela, manobras acrobáticas, uso de gancho, paraquedas, mira e direção.
  - Mapeamento e comandos de Teclado e Mouse em português.

---

## 💡 Sobre os Acentos:

O motor gráfico original de Just Cause (lançado em 2006) possui mapas de caracteres de fonte que não suportam certos caracteres especiais do português (como o **ç** e o til **~**), gerando caixas brancas ilegíveis (`[]`). 

Para proporcionar uma experiência 100% limpa, estável e agradável, todos os textos foram tratados sem acentos gráficos (`Configuracoes`, `Creditos`, `Missao`, `Voce`), garantindo exibição perfeita em qualquer resolução e sem nenhum erro visual na tela.

---

## 🚀 Como Instalar

### Requisitos:
- O jogo **Just Cause (2006)** instalado no seu computador (Steam, GOG ou versão física).
- **Python 3.6 ou superior** instalado. (No Windows, certifique-se de marcar a opção *"Add Python to PATH"* durante a instalação).

---

### Instalação Automática (Windows ou Linux):

1. **Baixe ou clone este repositório:**
   ```bash
   git clone https://github.com/nathan-uisa/just-cause-1-ptbr.git
   cd just-cause-1-ptbr
   ```
   *(Ou baixe o arquivo ZIP da página do repositório e extraia em qualquer pasta).*

2. **Execute o instalador:**
   - **No Linux:**
     ```bash
     python3 instalar_ptbr.py
     ```
   - **No Windows:**
     Dê um duplo clique no arquivo `instalar_ptbr.py` ou abra o Prompt de Comando (CMD) na pasta e execute:
     ```cmd
     python instalar_ptbr.py
     ```

3. **Pronto!** O instalador detectará automaticamente a pasta do Just Cause na sua Steam, criará um backup de segurança (`pc.tab.orig`) e injetará a tradução em menos de 2 segundos.

> **Dica:** Se o jogo estiver instalado em uma pasta personalizada ou diferente, basta informar o caminho quando o instalador solicitar, ou passar o parâmetro:
> ```bash
> python instalar_ptbr.py --game-dir "C:\Caminho\Para\Just Cause"
> ```

---

## 🔄 Como Desinstalar (Restaurar Original)

Caso queira voltar o jogo ao idioma original em inglês a qualquer momento:

Execute o desinstalador:
```bash
python desinstalar_ptbr.py
```
Ele restaurará instantaneamente o arquivo de índice original `pc.tab.orig` e reverterá o jogo ao estado de fábrica da Steam.

---

## 🔬 Detalhes Técnicos da Engenharia Reversa

Just Cause utiliza a engine proprietária da **Avalanche Software**:
- O arquivo `pc.tab` é uma tabela de índice de 12 bytes por entrada: `(uint32 hash, uint32 block_offset, uint32 size)`.
- Os arquivos `.arc` contêm os blocos alinhados em múltiplos de 2048 bytes.
- Os textos do jogo ficam organizados em arquivos `.csv` dentro de 179 contêineres do tipo `SARC`.
- O instalador deste projeto lê a tabela de blocos, descompacta os contêineres SARC, injeta os textos traduzidos em todas as colunas de idioma do CSV mantendo a estrutura delimitadora `#D#,#D#`, reconstrói os cabeçalhos SARC com os novos offsets e anexa os blocos ao arquivo `pc4.arc`, atualizando o `pc.tab` de forma 100% não-destrutiva.

---

## 📜 Licença

Distribuído sob a licença MIT. Consulte o arquivo [LICENSE](LICENSE) para mais detalhes.

---

*Criado para a comunidade brasileira de jogadores de Just Cause!* 🇧🇷🎮
