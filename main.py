import customtkinter as ctk
import sqlite3
from datetime import datetime
import os

# Configurações Visuais
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class SnackFlowApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("SNACK FLOW - Gestão Bilu Burger v5.1")
        self.geometry("1250x800")
        
        self.carrinho_atual = []
        self.total_valor = 0.0

        # Layout Principal
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- BARRA LATERAL ---
        self.menu_frame = ctk.CTkFrame(self, width=220, corner_radius=0)
        self.menu_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        ctk.CTkLabel(self.menu_frame, text="BILU MENU", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=15)
        
        # Categorias
        categorias = ["Artesanal", "Tradicional", "Variados", "Bebidas", "Adicionais"]
        for cat in categorias:
            btn = ctk.CTkButton(self.menu_frame, text=cat, command=lambda c=cat: self.carregar_produtos(c))
            btn.pack(pady=5, padx=20, fill="x")
            
        ctk.CTkLabel(self.menu_frame, text="GESTÃO", font=ctk.CTkFont(size=14, weight="bold")).pack(pady=(20,5))
        
        # BOTÃO DE CLIENTES
        self.btn_clientes = ctk.CTkButton(self.menu_frame, text="👥 CLIENTES", fg_color="#8e44ad", hover_color="#9b59b6", command=self.janela_clientes)
        self.btn_clientes.pack(pady=5, padx=20, fill="x")

        self.btn_ver_monitor = ctk.CTkButton(self.menu_frame, text="📺 MONITOR ATIVO", fg_color="#34495e", hover_color="#2c3e50", command=self.mostrar_monitor)
        self.btn_ver_monitor.pack(side="bottom", pady=20, padx=20, fill="x")

        # --- CENTRO ---
        self.centro_frame = ctk.CTkFrame(self, corner_radius=10)
        self.centro_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        
        self.label_centro = ctk.CTkLabel(self.centro_frame, text="BILU BURGER", font=ctk.CTkFont(size=22, weight="bold"))
        self.label_centro.pack(pady=15)

        self.scroll_area = ctk.CTkScrollableFrame(self.centro_frame, width=600, height=550)
        self.scroll_area.pack(expand=True, fill="both", padx=20, pady=10)

        # --- DIREITA: CARRINHO ---
        self.carrinho_frame = ctk.CTkFrame(self, width=280)
        self.carrinho_frame.grid(row=0, column=2, sticky="nsew", padx=10, pady=10)

        ctk.CTkLabel(self.carrinho_frame, text="🛒 CARRINHO", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=10)
        
        ctk.CTkLabel(self.carrinho_frame, text="Cliente:").pack()
        self.entry_cliente = ctk.CTkEntry(self.carrinho_frame, placeholder_text="Nome do Cliente...")
        self.entry_cliente.pack(pady=5, padx=20, fill="x")

        self.txt_carrinho = ctk.CTkTextbox(self.carrinho_frame, width=250, height=300, font=("Consolas", 12))
        self.txt_carrinho.pack(padx=10, pady=10)

        self.label_total = ctk.CTkLabel(self.carrinho_frame, text="TOTAL: R$ 0.00", font=ctk.CTkFont(size=20, weight="bold"), text_color="#2ecc71")
        self.label_total.pack(pady=5)

        ctk.CTkButton(self.carrinho_frame, text="LIMPAR CARRINHO", fg_color="#c0392b", command=self.limpar_carrinho).pack(pady=5, padx=20, fill="x")
        ctk.CTkButton(self.carrinho_frame, text="ENVIAR PARA COZINHA", height=45, fg_color="#27ae60", command=self.salvar_pedido).pack(side="bottom", pady=20, padx=20, fill="x")

        self.mostrar_monitor()
        self.atualizar_loop()

    # ===================== SISTEMA DE CLIENTES =====================
    def janela_clientes(self):
        for widget in self.scroll_area.winfo_children(): widget.destroy()
        self.label_centro.configure(text="👥 CADASTRO DE CLIENTES")

        f_cad = ctk.CTkFrame(self.scroll_area)
        f_cad.pack(pady=10, padx=10, fill="x")
        
        self.c_nome = ctk.CTkEntry(f_cad, placeholder_text="Nome Completo", width=200)
        self.c_nome.grid(row=0, column=0, padx=5, pady=10)
        self.c_tel = ctk.CTkEntry(f_cad, placeholder_text="Telefone", width=150)
        self.c_tel.grid(row=0, column=1, padx=5, pady=10)
        
        self.c_end = ctk.CTkEntry(f_cad, placeholder_text="Endereço (Rua, Nº, Bairro)", width=400)
        self.c_end.grid(row=1, column=0, columnspan=2, padx=5, pady=10, sticky="ew")
        
        ctk.CTkButton(f_cad, text="SALVAR CLIENTE", fg_color="#8e44ad", command=self.salvar_cliente_db).grid(row=1, column=2, padx=10)

        # Label de Status (para sabermos se salvou)
        self.lbl_status_cliente = ctk.CTkLabel(self.scroll_area, text="", font=("Arial", 12))
        self.lbl_status_cliente.pack(pady=5)

        ctk.CTkLabel(self.scroll_area, text="Lista de Clientes:", font=("Arial", 14, "bold")).pack(pady=10)
        self.listar_clientes()

    def salvar_cliente_db(self):
        n, t, e = self.c_nome.get().strip(), self.c_tel.get().strip(), self.c_end.get().strip()
        if not n:
            self.lbl_status_cliente.configure(text="❌ Erro: O nome é obrigatório!", text_color="#e74c3c")
            return

        conn = sqlite3.connect('snackflow.db')
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO clientes (nome, telefone, endereco) VALUES (?, ?, ?)", (n, t, e))
            conn.commit()
            self.lbl_status_cliente.configure(text=f"✅ Cliente {n} salvo com sucesso!", text_color="#2ecc71")
            # Limpa os campos
            self.c_nome.delete(0, 'end'); self.c_tel.delete(0, 'end'); self.c_end.delete(0, 'end')
        except sqlite3.IntegrityError:
            self.lbl_status_cliente.configure(text="❌ Erro: Este nome já está cadastrado!", text_color="#e74c3c")
        except Exception as err:
            self.lbl_status_cliente.configure(text=f"❌ Erro: {err}", text_color="#e74c3c")
        conn.close()
        self.listar_clientes()

    def listar_clientes(self):
        # Frame para a lista (para podermos limpar apenas a lista sem apagar o formulário)
        if hasattr(self, 'lista_frame'):
            self.lista_frame.destroy()
        
        self.lista_frame = ctk.CTkFrame(self.scroll_area, fg_color="transparent")
        self.lista_frame.pack(fill="both", expand=True)

        conn = sqlite3.connect('snackflow.db')
        cursor = conn.cursor()
        cursor.execute("SELECT nome, telefone, endereco FROM clientes ORDER BY nome")
        clientes = cursor.fetchall()
        conn.close()

        if not clientes:
            ctk.CTkLabel(self.lista_frame, text="Nenhum cliente cadastrado ainda.").pack(pady=10)
        else:
            for nome, tel, end in clientes:
                card = ctk.CTkFrame(self.lista_frame, border_width=1)
                card.pack(pady=5, padx=10, fill="x")
                txt = f"👤 {nome} | 📞 {tel}\n📍 {end}"
                ctk.CTkLabel(card, text=txt, justify="left").pack(side="left", padx=10, pady=5)
                ctk.CTkButton(card, text="USAR", width=80, fg_color="#3498db", command=lambda n=nome: self.selecionar_cliente(n)).pack(side="right", padx=10)

    def selecionar_cliente(self, nome):
        self.entry_cliente.delete(0, "end")
        self.entry_cliente.insert(0, nome)

    # ===================== MONITOR E PEDIDOS =====================
    def mostrar_monitor(self):
        for widget in self.scroll_area.winfo_children(): widget.destroy()
        self.label_centro.configure(text="📺 MONITOR DE PRODUÇÃO")
        
        conn = sqlite3.connect('snackflow.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id, cliente, lanche, total, status, hora_entrada FROM pedidos WHERE status != 'FINALIZADO'")
        pedidos = cursor.fetchall()
        conn.close()

        for p_id, cliente, lanche, total, status, h_entrada in pedidos:
            try:
                entrada = datetime.strptime(h_entrada, '%Y-%m-%d %H:%M:%S.%f')
            except:
                entrada = datetime.strptime(h_entrada.split('.')[0], '%Y-%m-%d %H:%M:%S')
            
            minutos = int((datetime.now() - entrada).total_seconds() / 60)
            cor_tempo = "#e74c3c" if minutos >= 15 else ("#f1c40f" if minutos >= 10 else "#2ecc71")

            card = ctk.CTkFrame(self.scroll_area, border_width=2, border_color="#34495e")
            card.pack(pady=10, padx=20, fill="x")
            text_frame = ctk.CTkFrame(card, fg_color="transparent")
            text_frame.pack(side="left", fill="both", expand=True, padx=15, pady=10)
            ctk.CTkLabel(text_frame, text=f"#{p_id:03} | {cliente.upper()} | ⏳ {minutos}m", font=("Consolas", 14, "bold"), text_color=cor_tempo, anchor="w").pack(fill="x")
            ctk.CTkLabel(text_frame, text=lanche, font=("Consolas", 12), wraplength=450, justify="left", anchor="w").pack(fill="x")
            ctk.CTkLabel(text_frame, text=f"VALOR: R${total:.2f}", font=("Consolas", 11, "italic"), text_color="gray", anchor="w").pack(fill="x")
            ctk.CTkButton(card, text="CONCLUIR", fg_color="#27ae60", width=110, height=40, font=ctk.CTkFont(weight="bold"), command=lambda i=p_id: self.finalizar_pedido(i)).pack(side="right", padx=15, pady=10)

    def carregar_produtos(self, categoria):
        for widget in self.scroll_area.winfo_children(): widget.destroy()
        self.label_centro.configure(text=f"LANCHES: {categoria.upper()}")
        conn = sqlite3.connect('snackflow.db')
        cursor = conn.cursor()
        cursor.execute("SELECT nome, preco FROM produtos WHERE categoria = ?", (categoria,))
        for nome, preco in cursor.fetchall():
            ctk.CTkButton(self.scroll_area, text=f"{nome}\n R${preco:.2f}", height=70, command=lambda n=nome, p=preco: self.adicionar_ao_carrinho(n, p)).pack(pady=8, padx=15, fill="x")
        conn.close()

    def adicionar_ao_carrinho(self, nome, preco):
        self.carrinho_atual.append(nome)
        self.total_valor += preco
        self.txt_carrinho.insert("end", f"• {nome} - R${preco:.2f}\n")
        self.label_total.configure(text=f"TOTAL: R$ {self.total_valor:.2f}")

    def limpar_carrinho(self):
        self.carrinho_atual = []
        self.total_valor = 0.0
        self.txt_carrinho.delete("1.0", "end")
        self.label_total.configure(text="TOTAL: R$ 0.00")
        self.entry_cliente.delete(0, "end")

    def salvar_pedido(self):
        cliente = self.entry_cliente.get().strip() or "Balcão"
        if not self.carrinho_atual: return
        conn = sqlite3.connect('snackflow.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO pedidos (cliente, lanche, status, hora_entrada, total) VALUES (?, ?, ?, ?, ?)", (cliente, ", ".join(self.carrinho_atual), 'AGUARDANDO', datetime.now(), self.total_valor))
        conn.commit()
        conn.close()
        self.limpar_carrinho()
        self.mostrar_monitor()

    def finalizar_pedido(self, p_id):
        conn = sqlite3.connect('snackflow.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE pedidos SET status = 'FINALIZADO' WHERE id = ?", (p_id,))
        conn.commit()
        conn.close()
        self.mostrar_monitor()

    def atualizar_loop(self):
        if self.label_centro.cget("text") == "📺 MONITOR DE PRODUÇÃO": self.mostrar_monitor()
        self.after(10000, self.atualizar_loop)

if __name__ == "__main__":
    app = SnackFlowApp()
    app.mainloop()