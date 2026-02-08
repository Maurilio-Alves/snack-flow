# 🍔 Snack Flow - Bilu Burger v7.0 (Final Edition)

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)
![CustomTkinter](https://img.shields.io/badge/UI-CustomTkinter-blue?style=for-the-badge)

O **Snack Flow** é um sistema completo de PDV (Ponto de Venda) e Gestão de Produção desenvolvido especificamente para hamburguerias e lanchonetes. O foco principal é a agilidade no monitor de preparo e a facilidade na gestão financeira diária.

---

## 🚀 Funcionalidades Principais

* **📺 Monitor de Produção Ativo:** Acompanhamento de pedidos em tempo real com cronômetro de espera e alertas visuais de prioridade (Amarelo/Vermelho).
* **👥 Gestão de Clientes:** Cadastro completo com banco de dados SQLite para agilizar entregas e histórico.
* **📊 Painel Financeiro:** Relatórios de faturamento diário, ticket médio e histórico detalhado de vendas.
* **⚙️ Ajuste Dinâmico de Preços:** Interface administrativa para alteração de valores do cardápio sem necessidade de mexer no código.
* **📱 Integração WhatsApp:** Gerador automático de cardápio formatado para cópia e envio rápido via WhatsApp.
* **🧾 Impressão de Ticket:** Emissão de cupons de pedido para a cozinha e entrega via `win32print`.

---

## 🛠️ Tecnologias Utilizadas

* **Linguagem:** Python 3.x
* **Interface Gráfica:** CustomTkinter (Modern Dark Theme)
* **Banco de Dados:** SQLite3
* **Manipulação de Data/Hora:** Datetime (Cálculo de tempo de espera em tempo real)
* **Impressão:** Bibliotecas Win32 para integração com Windows Spooler.

---

## 📦 Como rodar o projeto

1. **Clone o repositório:**
   ```bash
   git clone [https://github.com/Maurilio-Alves/snack-flow/upload](https://github.com/Maurilio-Alves/snack-flow.git)

Instale as dependências:

Bash
pip install customtkinter sqlite3 pywin32
Inicie o sistema:

Bash
python interface.py

📝 Licença
Este projeto foi desenvolvido para fins de gestão comercial e portfólio. Desenvolvido por Maurilio.