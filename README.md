# 🎯 BugHunterAI - Sistema Autônomo de Bug Bounty

O **BugHunterAI** é uma plataforma avançada de penetration testing que utiliza a inteligência artificial do **Google Gemini** para atuar como um pesquisador de segurança sênior. Ele automatiza o processo de reconhecimento, análise e exploração de vulnerabilidades, fornecendo insights em tempo real através de uma interface web moderna.

## 🚀 Funcionalidades

- **Cérebro de IA (Gemini):** Decisões autônomas baseadas em 15+ anos de experiência simulada em segurança.
- **Execução em Tempo Real:** Integração com ferramentas reais (subfinder, nmap, nuclei, etc.).
- **Interface Moderna:** Dashboard dark mode com logs de terminal, pensamentos da IA e visualização de findings.
- **Foco em Impacto:** Priorização automática de vulnerabilidades Críticas e Altas.
- **Compatibilidade:** Otimizado para rodar no **Kali Linux**.

## 🛠️ Tecnologias

- **Backend:** Python 3.11, FastAPI, WebSockets, SQLAlchemy.
- **IA:** Google Gemini Pro API.
- **Frontend:** HTML5, Tailwind CSS, JavaScript (Vanilla).
- **Segurança:** Integração com ferramentas líderes de mercado.

## ⚙️ Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/bughunter-ai.git
   cd bughunter-ai
   ```

2. Instale as dependências:
   ```bash
   pip install -r backend/requirements.txt
   ```

3. Configure sua API Key no arquivo `.env`:
   ```env
   GEMINI_API_KEY=Sua_Chave_Aqui
   ```

4. Inicie o sistema:
   ```bash
   python run.py
   ```

## 📂 Estrutura do Projeto

- `backend/`: Lógica do servidor, integração com IA e execução de ferramentas.
- `frontend/`: Interface web do usuário.
- `core/`: Motores de decisão e execução.
- `modules/`: Módulos específicos de recon e exploração.

## ⚠️ Aviso Legal

Este software foi desenvolvido apenas para fins educacionais e de segurança ética. O uso desta ferramenta contra alvos sem autorização prévia é ilegal. O desenvolvedor não se responsabiliza pelo uso indevido.
