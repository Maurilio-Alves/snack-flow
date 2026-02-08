import customtkinter as ctk
import sqlite3
from datetime import datetime
import os
import win32print
import win32api

# ===================== TELA DE LOGIN =====================
class LoginScreen(ctk.CTk):
    def __init__(self, on_login_success):
        super().__init__()
        self.title("LOGIN - BILU BURGER")
        self.geometry("400x500")
        self.on_login_success = on_login_success
        self.frame = ctk.CTkFrame(self, corner_radius=15)
        self.frame.pack(pady=40, padx=40, fill="both", expand=True)
        ctk.CTkLabel(self.frame, text="🍔 BILU LOGIN", font=ctk.CTkFont(size=24, weight="bold")).pack(pady=(30, 20))
        self.user_entry = ctk.CTkEntry(self.frame, placeholder_text="Usuário", width=250, height=40)
        self.user_entry.pack(pady=10)
        self.user_entry.insert(0, "admin")
        self.pass_entry = ctk.CTkEntry(self.frame, placeholder_text="Senha", show="*", width=250, height=40)
        self.pass_entry.pack(pady=10)
        self.btn_login = ctk.CTkButton(self.frame, text="ENTRAR", command=self.verificar_login, width=200, height=45, fg_color="#27ae60")
        self.btn_login.pack(pady=30)
        self.label_erro = ctk.CTkLabel(self.frame, text="", text_color="#e74c3c")
        self.label_erro.pack()

    def verificar_login(self):
        if self.user_entry.get() == "admin" and self.pass_entry.get() == "1234":
            self.destroy()
            self.on_login_success()
        else:
            self.label_erro.configure(text="Usuário ou Senha Inválidos!")

# Configurações Visuais
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class SnackFlowApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("SNACK FLOW - Bilu Burger v7.0 (FINAL EDITION)")
        self.geometry("1250x800")
        self.carrinho_atual = []
        self.valor_lanches = 0.0
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- BARRA LATERAL ---
        self.menu_frame = ctk.CTkFrame(self, width=220, corner_radius=0)
        self.menu_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        ctk.CTkLabel(self.menu_frame, text="BILU MENU", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=15)
        for cat in ["Artesanal", "Tradicional", "Variados", "Bebidas", "Adicionais"]:
            ctk.CTkButton(self.menu_frame, text=cat, command=lambda c=cat: self.carregar_produtos(c)).pack(pady=5, padx=20, fill="x")
        ctk.CTkLabel(self.menu_frame, text="GESTÃO", font=ctk.CTkFont(size=14, weight="bold")).pack(pady=(20,5))
        ctk.CTkButton(self.menu_frame, text="👥 CLIENTES", fg_color="#8e44ad", command=self.janela_clientes).pack(pady=5, padx=20, fill="x")
        ctk.CTkButton(self.menu_frame, text="🍔 EDITAR PREÇOS", fg_color="#e67e22", hover_color="#d35400", command=self.janela_cardapio).pack(pady=5, padx=20, fill="x")
        ctk.CTkButton(self.menu_frame, text="📊 FINANCEIRO", fg_color="#d35400", hover_color="#a04000", command=self.acesso_administrativo).pack(pady=5, padx=20, fill="x")
        ctk.CTkButton(self.menu_frame, text="📱 CARDÁPIO WHATS", fg_color="#27ae60", hover_color="#1e8449", command=self.janela_cardapio_whats).pack(pady=5, padx=20, fill="x")
        self.btn_ver_monitor = ctk.CTkButton(self.menu_frame, text="📺 MONITOR ATIVO", fg_color="#34495e", command=self.mostrar_monitor)
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
        self.entry_cliente = ctk.CTkEntry(self.carrinho_frame, placeholder_text="Nome do Cliente...")
        self.entry_cliente.pack(pady=5, padx=20, fill="x")
        self.entry_taxa = ctk.CTkEntry(self.carrinho_frame, placeholder_text="Taxa Entrega", border_color="#e67e22")
        self.entry_taxa.pack(pady=5, padx=20, fill="x")
        self.entry_taxa.bind("<KeyRelease>", lambda e: self.atualizar_total_display())
        self.txt_carrinho = ctk.CTkTextbox(self.carrinho_frame, width=250, height=250, font=("Consolas", 12))
        self.txt_carrinho.pack(padx=10, pady=10)
        self.label_total = ctk.CTkLabel(self.carrinho_frame, text="TOTAL: R$ 0.00", font=ctk.CTkFont(size=20, weight="bold"), text_color="#2ecc71")
        self.label_total.pack(pady=5)
        ctk.CTkButton(self.carrinho_frame, text="LIMPAR", fg_color="#c0392b", command=self.limpar_carrinho).pack(pady=5, padx=20, fill="x")
        ctk.CTkButton(self.carrinho_frame, text="ENVIAR E IMPRIMIR", height=45, fg_color="#27ae60", command=self.salvar_pedido).pack(side="bottom", pady=20, padx=20, fill="x")

        self.mostrar_monitor()
        self.atualizar_loop()

    # ===================== CARDÁPIO WHATSAPP (RESTAURADO) =====================
    def janela_cardapio_whats(self):
        self.limpar_tela_central()
        self.label_centro.configure(text="📱 PRÉVIA CARDÁPIO WHATSAPP")
        conn = sqlite3.connect('snackflow.db'); cursor = conn.cursor()
        cursor.execute("SELECT nome, preco, categoria FROM produtos ORDER BY categoria, nome")
        produtos = cursor.fetchall(); conn.close()
        
        if not produtos: return
        
        texto = "🍔 *BILU BURGER - CARDÁPIO* 🍔\n------------------------------------------\n"
        cat_atual = ""
        for n, p, c in produtos:
            if c != cat_atual:
                cat_atual = c
                texto += f"\n🔹 *{cat_atual.upper()}*\n"
            texto += f"✅ {n} - _R$ {p:.2f}_\n"
        texto += "\n📍 *Mande seu Nome e Endereço para pedir!*"

        txt_p = ctk.CTkTextbox(self.scroll_area, width=500, height=400)
        txt_p.pack(pady=10)
        txt_p.insert("1.0", texto)
        
        ctk.CTkButton(self.scroll_area, text="COPIAR PARA O WHATSAPP", fg_color="#27ae60", 
                      command=lambda: self.copiar_texto_whats(texto)).pack(pady=20)

    def copiar_texto_whats(self, texto):
        self.clipboard_clear()
        self.clipboard_append(texto)
        self.update()
        self.label_centro.configure(text="✅ COPIADO! DÊ CTRL+V NO ZAP", text_color="#2ecc71")
        self.after(3000, lambda: self.label_centro.configure(text="📱 PRÉVIA CARDÁPIO WHATSAPP", text_color="white"))

    # ===================== CLIENTES (RESTAURADO) =====================
    def janela_clientes(self):
        self.limpar_tela_central()
        self.label_centro.configure(text="👥 GESTÃO DE CLIENTES")
        f = ctk.CTkFrame(self.scroll_area); f.pack(pady=10, padx=10, fill="x")
        self.c_nome = ctk.CTkEntry(f, placeholder_text="Nome"); self.c_nome.grid(row=0, column=0, padx=5, pady=5)
        self.c_tel = ctk.CTkEntry(f, placeholder_text="Tel"); self.c_tel.grid(row=0, column=1, padx=5, pady=5)
        self.c_end = ctk.CTkEntry(f, placeholder_text="Endereço", width=350); self.c_end.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="ew")
        ctk.CTkButton(f, text="SALVAR", fg_color="#8e44ad", command=self.salvar_cliente_db).grid(row=1, column=2, padx=10)
        
        conn = sqlite3.connect('snackflow.db'); cursor = conn.cursor()
        cursor.execute("SELECT nome, telefone, endereco FROM clientes ORDER BY nome")
        for n, t, e in cursor.fetchall():
            card = ctk.CTkFrame(self.scroll_area, border_width=1); card.pack(pady=5, padx=10, fill="x")
            ctk.CTkLabel(card, text=f"👤 {n} | 📞 {t}\n📍 {e}", justify="left").pack(side="left", padx=10, pady=5)
            ctk.CTkButton(card, text="USAR", width=60, command=lambda nm=n: self.selecionar_cliente(nm)).pack(side="right", padx=10)
        conn.close()

    def salvar_cliente_db(self):
        n, t, e = self.c_nome.get(), self.c_tel.get(), self.c_end.get()
        if n:
            conn = sqlite3.connect('snackflow.db'); cursor = conn.cursor()
            try: cursor.execute("INSERT INTO clientes (nome, telefone, endereco) VALUES (?, ?, ?)", (n, t, e)); conn.commit()
            except: pass
            conn.close(); self.janela_clientes()

    # ===================== MONITOR E FINALIZAÇÃO =====================
    def mostrar_monitor(self):
        self.limpar_tela_central()
        self.label_centro.configure(text="📺 MONITOR DE PRODUÇÃO")
        conn = sqlite3.connect('snackflow.db'); cursor = conn.cursor()
        cursor.execute("SELECT id, cliente, lanche, total, hora_entrada FROM pedidos WHERE status != 'FINALIZADO' ORDER BY hora_entrada ASC")
        for p_id, cli, lanch, tot, h_entrada in cursor.fetchall():
            try:
                entrada = datetime.strptime(h_entrada, '%Y-%m-%d %H:%M:%S.%f')
                minutos = int((datetime.now() - entrada).total_seconds() / 60)
                cor_t = "#e74c3c" if minutos >= 30 else "#f1c40f"; txt_t = f"⏳ {minutos} min"
            except: txt_t = "⏳ --"; cor_t = "white"
            card = ctk.CTkFrame(self.scroll_area, border_width=2, border_color="#34495e"); card.pack(pady=10, padx=20, fill="x")
            ctk.CTkButton(card, text="CONCLUIR", fg_color="#27ae60", width=100, height=40, command=lambda i=p_id: self.finalizar_pedido(i)).pack(side="right", padx=15, pady=10)
            info = ctk.CTkFrame(card, fg_color="transparent"); info.pack(side="left", padx=15, pady=10, expand=True, fill="both")
            header = ctk.CTkFrame(info, fg_color="transparent"); header.pack(fill="x", side="top")
            ctk.CTkLabel(header, text=f"#{p_id:03} | {cli.upper()}", font=("Arial", 14, "bold")).pack(side="left")
            ctk.CTkLabel(header, text=f"  |  {txt_t}", font=("Arial", 14, "bold"), text_color=cor_t).pack(side="left")
            ctk.CTkLabel(info, text=lanch, font=("Consolas", 11), justify="left", anchor="w", wraplength=400).pack(fill="x", side="top", pady=(5,0))
        conn.close()

    def finalizar_pedido(self, p_id):
        from tkinter import messagebox
        if messagebox.askyesno("CONFIRMAR", f"Finalizar pedido #{p_id:03}?"):
            conn = sqlite3.connect('snackflow.db'); cursor = conn.cursor()
            cursor.execute("UPDATE pedidos SET status = 'FINALIZADO' WHERE id = ?", (p_id,))
            conn.commit(); conn.close(); self.mostrar_monitor()

    # ===================== FINANCEIRO E PREÇOS =====================
    def acesso_administrativo(self):
        dialogo = ctk.CTkInputDialog(text="Senha:", title="Segurança")
        if dialogo.get_input() == "1234": self.janela_financeiro()

    def janela_financeiro(self):
        self.limpar_tela_central(); self.label_centro.configure(text="📊 PAINEL FINANCEIRO BILU")
        conn = sqlite3.connect('snackflow.db'); cursor = conn.cursor(); hoje = datetime.now().strftime('%Y-%m-%d')
        cursor.execute("SELECT SUM(total), COUNT(id) FROM pedidos WHERE status = 'FINALIZADO' AND hora_entrada LIKE ?", (f'{hoje}%',))
        res = cursor.fetchone(); fat = res[0] if res[0] else 0.0
        card = ctk.CTkFrame(self.scroll_area, fg_color="#27ae60", corner_radius=15); card.pack(pady=20, padx=30, fill="x")
        ctk.CTkLabel(card, text="FATURAMENTO HOJE", font=("Arial", 16, "bold")).pack(pady=(15,5))
        ctk.CTkLabel(card, text=f"R$ {fat:.2f}", font=("Arial", 45, "bold")).pack(pady=10)
        ctk.CTkLabel(self.scroll_area, text="Histórico de Hoje:", font=("Arial", 14, "bold")).pack(pady=10)
        cursor.execute("SELECT id, cliente, total, hora_entrada FROM pedidos WHERE status = 'FINALIZADO' AND hora_entrada LIKE ? ORDER BY id DESC LIMIT 15", (f'{hoje}%',))
        for v_id, cli, tot, data in cursor.fetchall():
            item = ctk.CTkFrame(self.scroll_area, border_width=1); item.pack(pady=2, padx=20, fill="x")
            ctk.CTkLabel(item, text=f"#{v_id:03} | {cli.upper()} | R$ {tot:.2f} | {data[11:16]}").pack(padx=15, pady=5)
        conn.close()

    def janela_cardapio(self):
        self.limpar_tela_central(); self.label_centro.configure(text="⚙️ AJUSTE DE PREÇOS")
        conn = sqlite3.connect('snackflow.db'); cursor = conn.cursor()
        cursor.execute("SELECT id, nome, preco FROM produtos ORDER BY categoria, nome")
        for i, n, p in cursor.fetchall():
            fr = ctk.CTkFrame(self.scroll_area); fr.pack(pady=5, padx=20, fill="x")
            ctk.CTkLabel(fr, text=n, width=200, anchor="w").pack(side="left", padx=10)
            en = ctk.CTkEntry(fr, width=80); en.insert(0, f"{p:.2f}"); en.pack(side="left", padx=10)
            ctk.CTkButton(fr, text="✅ SALVAR", width=80, fg_color="#27ae60", command=lambda idx=i, ent=en: self.atualizar_preco_db(idx, ent.get())).pack(side="right", padx=10)
        conn.close()

    def atualizar_preco_db(self, i, v):
        try:
            val = float(v.replace(',', '.')); conn = sqlite3.connect('snackflow.db'); cursor = conn.cursor()
            cursor.execute("UPDATE produtos SET preco = ? WHERE id = ?", (val, i)); conn.commit(); conn.close()
            self.label_centro.configure(text="✅ PREÇO ATUALIZADO!", text_color="#2ecc71")
        except: pass

    # ===================== FUNÇÕES DE APOIO =====================
    def selecionar_cliente(self, nome):
        self.entry_cliente.delete(0, "end"); self.entry_cliente.insert(0, nome)

    def adicionar_ao_carrinho(self, n, p):
        self.carrinho_atual.append(n); self.valor_lanches += p
        self.txt_carrinho.insert("end", f"• {n} - R${p:.2f}\n"); self.atualizar_total_display()

    def atualizar_total_display(self):
        try: tx = float(self.entry_taxa.get().replace(',', '.')) if self.entry_taxa.get() else 0.0
        except: tx = 0.0
        self.label_total.configure(text=f"TOTAL: R$ {self.valor_lanches + tx:.2f}")

    def limpar_carrinho(self):
        self.carrinho_atual = []; self.valor_lanches = 0.0
        self.txt_carrinho.delete("1.0", "end"); self.entry_cliente.delete(0, "end"); self.entry_taxa.delete(0, "end"); self.label_total.configure(text="TOTAL: R$ 0.00")

    def limpar_tela_central(self):
        for w in self.scroll_area.winfo_children(): w.destroy()

    def imprimir_ticket(self, arquivo):
        try: win32api.ShellExecute(0, "print", arquivo, None, ".", 0)
        except: pass

    def salvar_pedido(self):
        cli = self.entry_cliente.get().strip() or "Balcão"
        if not self.carrinho_atual: return
        dial = ctk.CTkInputDialog(text="1-DINHEIRO 2-PIX 3-CARTÃO", title="CAIXA")
        op = dial.get_input(); pag = {"1": "DINHEIRO", "2": "PIX", "3": "CARTÃO"}.get(op, "N/A")
        try: tx = float(self.entry_taxa.get().replace(',', '.')) if self.entry_taxa.get() else 0.0
        except: tx = 0.0
        total = self.valor_lanches + tx; conn = sqlite3.connect('snackflow.db'); cursor = conn.cursor()
        cursor.execute("INSERT INTO pedidos (cliente, lanche, status, hora_entrada, total) VALUES (?, ?, ?, ?, ?)", (f"{cli} ({pag})", ", ".join(self.carrinho_atual), 'AGUARDANDO', datetime.now(), total))
        p_id = cursor.lastrowid; conn.commit(); conn.close()
        with open(f"pedido_{p_id:03}.txt", "w", encoding="utf-8") as f: f.write(f"PEDIDO #{p_id:03}\nCLIENTE: {cli}\nTOTAL: R$ {total:.2f}")
        self.imprimir_ticket(f"pedido_{p_id:03}.txt"); self.limpar_carrinho(); self.mostrar_monitor()

    def atualizar_loop(self):
        if hasattr(self, 'label_centro') and self.label_centro.cget("text") == "📺 MONITOR DE PRODUÇÃO":
            try: self.mostrar_monitor()
            except: pass
        self.after(15000, self.atualizar_loop)

def iniciar_sistema_principal():
    app = SnackFlowApp(); app.mainloop()

if __name__ == "__main__":
    login = LoginScreen(on_login_success=iniciar_sistema_principal); login.mainloop()