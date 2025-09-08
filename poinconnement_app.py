import customtkinter as ctk
import math
from tkinter import messagebox



def calculate_k_for_beta(c1, c2):
    if c2 == 0: return 0.8
    x = c1 / c2
    points = [(0.5, 0.45), (1.0, 0.60), (2.0, 0.70), (3.0, 0.80)]
    if x <= 0.5: return 0.45
    if x >= 3.0: return 0.80
    for (x1, k1), (x2, k2) in zip(points[:-1], points[1:]):
        if x1 <= x <= x2:
            pente = (k2 - k1) / (x2 - x1)
            return k1 + (x - x1) * pente
    return 0.8

def perform_punching_check(data, element_type):
    fck, gamma_c = data['fck'], data['gamma_c']
    B1_mm, B2_mm = data['B1'] * 10, data['B2'] * 10
    C1_mm, C2_mm = data['C1'] * 10, data['C2'] * 10
    dy_mm, dz_mm = data['dy'] * 10, data['dz'] * 10
    a_mm = data['a'] * 10
    VEd_N = data['VEd'] * 1000
    MEd_N_mm = data['MEd'] * 1000 * 1000
    
    results = {}
    
    results['e_cm'] = (data['MEd'] / data['VEd']) * 100 if data['VEd'] != 0 else 0
    d = (dy_mm + dz_mm) / 2
    results['d_cm'] = d / 10
    results['a_cm'] = a_mm / 10
    u = 2 * (C1_mm + C2_mm + math.pi * a_mm) if element_type.lower() == 'poteau' else 2 * (C1_mm + C2_mm)
    results['u_cm'] = u / 10
    S = 2 * a_mm * (C1_mm + C2_mm) + C1_mm * C2_mm + math.pi * a_mm**2
    results['S_m2'] = S / 1000**2
    delta_VEd = VEd_N * S / (B1_mm * B2_mm) if (B1_mm * B2_mm) > 0 else 0
    results['delta_VEd_kN'] = delta_VEd / 1000
    VEd_red = max(0, VEd_N - delta_VEd)
    results['VEd_red_kN'] = VEd_red / 1000
    W = C1_mm**2 / 2 + C1_mm * C2_mm + 2 * C2_mm * a_mm + 4 * a_mm**2 + math.pi * a_mm * C1_mm
    results['W_cm2'] = W / 100
    k_beta = calculate_k_for_beta(C1_mm, C2_mm)
    results['k_beta'] = k_beta
    beta = 1.0
    if VEd_red > 0 and W > 0: beta = 1 + k_beta * abs(MEd_N_mm / VEd_red) * (u / W)
    results['beta'] = beta
    vEd = (beta * VEd_red) / (u * d) if u > 0 and d > 0 else 0
    results['vEd_MPa'] = vEd
    rho_ly = data['Asy'] / (100 * data['dy']) if data['dy'] > 0 else 0
    rho_lz = data['Asz'] / (100 * data['dz']) if data['dz'] > 0 else 0
    results['rho_ly'] = rho_ly
    results['rho_lz'] = rho_lz
    rho_l = min(math.sqrt(rho_ly * rho_lz), 0.02) if (rho_ly * rho_lz) >= 0 else 0
    results['rho_l'] = rho_l
    k_resistance = min(1 + math.sqrt(200 / d), 2.0) if d > 0 else 1.0
    results['k_resistance'] = k_resistance
    CRd_c = 0.18 / gamma_c
    results['CRd_c'] = CRd_c
    v_min = 0.035 * k_resistance**(3/2) * math.sqrt(fck)
    results['v_min_MPa'] = v_min
    term_vrd = CRd_c * k_resistance * (100 * rho_l * fck)**(1/3)
    facteur_2d_a = (2 * d / a_mm) if a_mm > 0 else 1.0
    v_Rd = max(term_vrd, v_min) * facteur_2d_a
    results['v_Rd_MPa'] = v_Rd
    if v_Rd == 0:
        results['ratio'] = float('inf')
        results['verdict'] = "NON OK (résistance nulle)"
    else:
        results['ratio'] = vEd / v_Rd
        results['verdict'] = "OK" if results['ratio'] <= 1 else "NON OK"
    return results



class PunchingShearApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Calcul de Poinçonnement - Eurocode 2")
        self.geometry("900x850")
        
        ctk.set_appearance_mode("dark")

 
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1) 
        self.entries = {}
        self.result_labels = {}
        self.create_header_widgets()
        self.create_input_widgets()
        self.create_output_widgets()
        self.create_footer() 

    def create_header_widgets(self):
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, columnspan=2, padx=20, pady=(10, 0), sticky="ew")
        header_frame.grid_columnconfigure(0, weight=1)

        self.theme_switch_var = ctk.StringVar(value="on")
        theme_switch = ctk.CTkSwitch(header_frame, text="Mode Sombre", command=self.toggle_theme, variable=self.theme_switch_var, onvalue="on", offvalue="off")
        theme_switch.grid(row=0, column=1, padx=0, pady=0)

    def toggle_theme(self):
        ctk.set_appearance_mode("dark" if self.theme_switch_var.get() == "on" else "light")

    def create_input_widgets(self):
        self.input_frame = ctk.CTkFrame(self)
        self.input_frame.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")
        self.input_frame.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(self.input_frame, text="Données d'entrée", font=ctk.CTkFont(size=16, weight="bold")).grid(row=0, column=0, columnspan=2, padx=10, pady=(10, 20))
        ctk.CTkLabel(self.input_frame, text="Type d'élément:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.element_type_var = ctk.StringVar(value="Poteau")
        ctk.CTkSegmentedButton(self.input_frame, values=["Poteau", "Voile"], variable=self.element_type_var).grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        input_prompts = {
            'fck': "fck [MPa]", 'gamma_c': "γc", 'B1': "B1 [cm]", 'B2': "B2 [cm]",
            'C1': "C1 [cm]", 'C2': "C2 [cm]", 'dy': "dy [cm]", 'dz': "dz [cm]",
            'a': "a [cm]", 'Asy': "Asy [cm²/m]", 'Asz': "Asz [cm²/m]",
            'VEd': "VEd [kN]", 'MEd': "MEd [kN.m]"
        }
        for i, (key, prompt) in enumerate(input_prompts.items(), start=2):
            ctk.CTkLabel(self.input_frame, text=f"{prompt}:").grid(row=i, column=0, padx=10, pady=5, sticky="w")
            entry = ctk.CTkEntry(self.input_frame, placeholder_text=f"Valeur de {key}")
            entry.grid(row=i, column=1, padx=10, pady=5, sticky="ew")
            self.entries[key] = entry
        
        ctk.CTkButton(self.input_frame, text="Calculer", command=self.run_calculation, height=40).grid(row=len(input_prompts) + 2, column=0, columnspan=2, padx=10, pady=(20, 10), sticky="ew")

    def create_output_widgets(self):
        self.output_frame = ctk.CTkFrame(self)
        self.output_frame.grid(row=1, column=1, padx=(0, 20), pady=20, sticky="nsew")
        self.output_frame.grid_columnconfigure(0, weight=1)
        self.output_frame.grid_rowconfigure(2, weight=1)
        
        ctk.CTkLabel(self.output_frame, text="Résultats", font=ctk.CTkFont(size=16, weight="bold")).grid(row=0, column=0, padx=10, pady=(10, 5), sticky="w")
        self.verdict_label = ctk.CTkLabel(self.output_frame, text="- Verdict -", font=ctk.CTkFont(size=32, weight="bold"))
        self.verdict_label.grid(row=1, column=0, padx=10, pady=(5, 10), sticky="ew")

        scroll_frame = ctk.CTkScrollableFrame(self.output_frame, fg_color="transparent")
        scroll_frame.grid(row=2, column=0, padx=5, pady=0, sticky="nsew")
        scroll_frame.grid_columnconfigure(1, weight=1)

        font_bold = ctk.CTkFont(weight="bold")
        ctk.CTkLabel(scroll_frame, text="Calculs Intermédiaires", font=font_bold).grid(row=0, column=0, columnspan=2, pady=(0, 5), sticky="w")
        result_prompts = {
            'e_cm': "Excentricité (e)", 'd_cm': "Hauteur utile (d)", 'a_cm': "Distance critique (a)", 'u_cm': "Périmètre critique (u)",
            'S_m2': "Surface de contact (S)", 'delta_VEd_kN': "Réaction du sol (∆VEd)", 'VEd_red_kN': "Effort VEd,red",
            'W_cm2': "Paramètre de section (W)", 'k_beta': "Coefficient k (pour β)", 'beta': "Coefficient β",
            'rho_ly': "Ratio armatures y (ρly)", 'rho_lz': "Ratio armatures z (ρlz)", 'rho_l': "Ratio moyen (ρ_l)",
            'k_resistance': "Coefficient k (pour v_Rd)", 'CRd_c': "Coefficient CRd,c", 'v_min_MPa': "Contrainte min (v_min)"
        }
        for i, (key, prompt) in enumerate(result_prompts.items(), start=1):
            ctk.CTkLabel(scroll_frame, text=f"{prompt} :").grid(row=i, column=0, padx=5, pady=2, sticky="w")
            value_label = ctk.CTkLabel(scroll_frame, text="-", anchor="e")
            value_label.grid(row=i, column=1, padx=5, pady=2, sticky="ew")
            self.result_labels[key] = value_label

        separator = ctk.CTkFrame(scroll_frame, height=2, fg_color="gray50")
        separator.grid(row=len(result_prompts)+1, column=0, columnspan=2, pady=15, sticky="ew")
        ctk.CTkLabel(scroll_frame, text="Vérification Finale", font=font_bold).grid(row=len(result_prompts)+2, column=0, columnspan=2, pady=(0, 5), sticky="w")
        final_prompts = { 'vEd_MPa': "Contrainte agissante (νEd)", 'v_Rd_MPa': "Contrainte résistante (v_Rd)", 'ratio': "Ratio de vérification" }
        for i, (key, prompt) in enumerate(final_prompts.items(), start=len(result_prompts)+3):
            label_font = font_bold if key == 'ratio' else None
            ctk.CTkLabel(scroll_frame, text=f"{prompt} :", font=label_font).grid(row=i, column=0, padx=5, pady=3, sticky="w")
            value_label = ctk.CTkLabel(scroll_frame, text="-", anchor="e", font=label_font)
            value_label.grid(row=i, column=1, padx=5, pady=3, sticky="ew")
            self.result_labels[key] = value_label
            
    def create_footer(self):
        """Crée le pied de page avec la signature."""
        footer_label = ctk.CTkLabel(self, text="© Mahmoudi Mohammed Hani 2025", font=ctk.CTkFont(size=10), text_color="gray60")
        footer_label.grid(row=2, column=0, columnspan=2, padx=10, pady=(5, 10), sticky="s")

    def run_calculation(self):
        try:
            user_data = {key: float(entry.get()) for key, entry in self.entries.items()}
            element_type = self.element_type_var.get()
            final_results = perform_punching_check(user_data, element_type)
            self.display_gui_results(final_results)
        except (ValueError, TypeError):
            messagebox.showerror("Erreur de saisie", "Veuillez vérifier que toutes les valeurs entrées sont des nombres valides.")
        except Exception as e:
            messagebox.showerror("Erreur inattendue", f"Une erreur est survenue: {e}")

    def display_gui_results(self, results):
        verdict = results['verdict']
        is_ok = "OK" in verdict
        self.verdict_label.configure(text=verdict, text_color="#2ECC71" if is_ok else "#E74C3C")
        units = {
            'e_cm':" cm", 'd_cm':" cm", 'a_cm':" cm", 'u_cm':" cm", 'S_m2':" m²", 'delta_VEd_kN':" kN", 'VEd_red_kN':" kN",
            'W_cm2': " cm²", 'k_beta':"", 'beta':"", 'rho_ly':"", 'rho_lz':"", 'rho_l':"", 'k_resistance':"",
            'CRd_c':"", 'v_min_MPa':" MPa", 'vEd_MPa':" MPa", 'v_Rd_MPa':" MPa", 'ratio':""
        }
        decimals = {
            'e_cm':2, 'd_cm':2, 'a_cm':2, 'u_cm':2, 'S_m2':4, 'delta_VEd_kN':2, 'VEd_red_kN':2, 'W_cm2':2,
            'k_beta':3, 'beta':3, 'rho_ly':5, 'rho_lz':5, 'rho_l':5, 'k_resistance':3, 'CRd_c':3,
            'v_min_MPa':3, 'vEd_MPa':3, 'v_Rd_MPa':3, 'ratio':3
        }
        for key, label in self.result_labels.items():
            value = results.get(key)
            if value is not None:
                formatted_value = f"{value:.{decimals.get(key, 2)}f}{units.get(key, '')}"
                label.configure(text=formatted_value)
        ratio_label = self.result_labels.get('ratio')
        if ratio_label:
            ratio_label.configure(text_color="#2ECC71" if is_ok else "#E74C3C")

if __name__ == "__main__":
    app = PunchingShearApp()
    app.mainloop()