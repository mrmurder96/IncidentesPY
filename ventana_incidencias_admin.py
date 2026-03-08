import customtkinter, os, re, subprocess, cargar_archivos, csv, sys, math, io, datetime, json
from PIL import Image
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter.filedialog
import numpy as np
from tkinter import messagebox

# Variables Globales
tickets = []


# Funciones
def validate_email(email):
    regex = r"^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$"
    return re.match(regex, email) is not None


def error_frame(texto):
    error_dialog = customtkinter.CTkToplevel()
    error_dialog.geometry(f"+{x - 150}+{y}")
    error_dialog.resizable(False, False)
    error_dialog.lift()
    error_dialog.attributes("-topmost", 1)
    error_dialog.title("Error")
    error_label = customtkinter.CTkLabel(error_dialog, image=error_image, text="")
    error_label.pack(padx=10, pady=10)
    error_label = customtkinter.CTkLabel(error_dialog, text=texto, font=("Roboto", 12))
    error_label.pack(padx=10)
    error_dialog.grab_set()
    error_dialog.wait_window()


def actualizar_botones_paginacion():
    ancho_boton = 100
    num_paginas = math.ceil(len(tickets) / 10)
    ancho_total_botones = ancho_boton * num_paginas
    for widget in scrollable_frame_paginacion.winfo_children():
        widget.destroy()
    scrollable_frame_paginacion.configure(width=1000)
    scrollable_frame_paginacion.grid()
    for i in range(num_paginas):
        button = customtkinter.CTkButton(
            scrollable_frame_paginacion,
            text=f"{i*10+1}-{min(i*10+10, len(tickets))}",
            command=lambda p=i: cambiar_pagina(p + 1),
        )
        button.grid(row=0, column=i, padx=10, pady=10, sticky="w")
    if num_paginas == 0:
        scrollable_frame_paginacion.grid_remove()


def cambiar_pagina(pagina):
    inicio = (pagina - 1) * 10
    fin = min(inicio + 10, len(tickets))
    tree_ticket_table.delete(*tree_ticket_table.get_children())
    for i in range(inicio, fin):
        tree_ticket_table.insert("", "end", values=tickets[i])
    tree_ticket_table.see(tree_ticket_table.get_children()[-1])
    actualizar_botones_paginacion()


def abrir_ventana_cambio_contra():
    global x, y, contra_nueva, recontra_nueva, ventana_otro_problema

    ventana_otro_problema = customtkinter.CTkToplevel(g_incidencias)
    width = ventana_otro_problema.winfo_screenwidth()
    height = ventana_otro_problema.winfo_screenheight()
    x = (width // 2) - (ventana_otro_problema.winfo_reqwidth() // 2)
    y = (height // 2) - (ventana_otro_problema.winfo_reqheight() // 2)
    ventana_otro_problema.geometry(f"250x250+{x - 150}+{y - 100}")
    ventana_otro_problema.title("Cambio Contraseña")
    ventana_otro_problema.resizable(False, False)
    ventana_otro_problema.lift()
    ventana_otro_problema.attributes("-topmost", 1)

    contra_anterior = customtkinter.CTkEntry(
        ventana_otro_problema,
        placeholder_text="Contraseña Actual:",
        font=("Roboto", 15),
        width=200,
        show="*",
    )
    contra_anterior.pack(pady=(20, 10))

    contra_nueva = customtkinter.CTkEntry(
        ventana_otro_problema,
        placeholder_text="Nueva Contraseña:",
        font=("Roboto", 15),
        width=200,
        show="*",
    )
    contra_nueva.pack(pady=(20, 10))

    recontra_nueva = customtkinter.CTkEntry(
        ventana_otro_problema,
        placeholder_text="Repetir Nueva Contraseña:",
        width=200,
        font=("Roboto", 15),
        show="*",
    )
    recontra_nueva.pack(pady=(20, 10))

    boton_cambiar = customtkinter.CTkButton(
        ventana_otro_problema,
        text="Guardar",
        font=("Roboto", 15),
        command=cambio_contra,
    )
    boton_cambiar.pack(pady=(10, 20))


def cambio_contra():
    user_data = cargar_archivos.load_user_data()
    regex = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"

    password_text = contra_nueva.get()
    repassword_text = recontra_nueva.get()

    error_contra_nueva = ""
    error_recontra_nueva = ""

    if password_text == "":
        error_contra_nueva = "La contraseña no puede estar vacía"
    elif repassword_text == "":
        error_recontra_nueva = "La confirmación de contraseña no puede estar vacía"
    elif not re.match(regex, password_text):
        error_contra_nueva = "La contraseña debe tener al menos 9 caracteres,una letra mayúscula y un signo especial"
    elif repassword_text != password_text:
        error_recontra_nueva = "Las contraseñas no coinciden"
    if error_contra_nueva or error_recontra_nueva:
        error_dialog = customtkinter.CTkToplevel()
        error_dialog.geometry(f"+{x - 150}+{y}")
        error_dialog.resizable(False, False)
        error_dialog.lift()
        error_dialog.attributes("-topmost", 1)
        error_dialog.title("Error")
        error_label = customtkinter.CTkLabel(error_dialog, image=error_image, text="")
        error_label.pack(padx=10, pady=10)
        error_label = customtkinter.CTkLabel(
            error_dialog,
            text=f"{error_contra_nueva}\n{error_recontra_nueva}",
            font=("Roboto", 12),
        )
        error_label.pack(padx=10)
        error_dialog.grab_set()
        error_dialog.wait_window()
    else:
        for user in user_data:
            if user_data[user]["username"] == logged_in_tech_id:
                user_data[user]["password"] = password_text
                cargar_archivos.save_user_data(user_data)
                mensaje_exito = customtkinter.CTkToplevel()
                mensaje_exito.resizable(False, False)
                mensaje_exito.geometry(f"+{x - 150}+{y}")
                mensaje_exito.lift()
                mensaje_exito.attributes("-topmost", 1)
                mensaje_exito.title("Éxito")
                mensaje_label = customtkinter.CTkLabel(
                    mensaje_exito, text="Contraseña cambiada exitosamente"
                )
                mensaje_label.pack(padx=20, pady=20)
                mensaje_exito.grab_set()
                mensaje_exito.wait_window()
                ventana_otro_problema.destroy()
                break


def cerrar_sesion():
    archivo_a_ejecutar = "Login.py"
    g_incidencias.destroy()
    try:
        subprocess.run(["python", archivo_a_ejecutar], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar el archivo: {e}")


def handle_register():
    handle_Re_Nuevo_usuario()


def actualizar_fecha_hora():
    actual_time = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    fecha_hora.configure(text=actual_time)
    fecha_hora.after(1000, actualizar_fecha_hora)


def change_appearance_mode_event():
    new_appearance_mode = "Dark" if appearance_mode_optionemenu.get() else "Light"
    customtkinter.set_appearance_mode(new_appearance_mode)


def handle_Re_Nuevo_usuario():
    username_text = username.get()
    password_text = contra.get()
    repassword_text = recontra.get()
    rango = optionmenu.get()
    email = correo.get()
    user_data = cargar_archivos.load_user_data()
    regex = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
    if username_text in user_data:
        error_label.configure(text="El usuario ya esta registrado")
    elif username_text == "":
        error_label.configure(text="No se ingreso nada en usuario")
    elif password_text == "":
        error_label.configure(text="La contraseña no puede estar vacia")
    elif not re.match(regex, password_text):
        error_label.configure(
            text="""
                            La contraseña debe tener al menos 9 caracteres,
                            una letra mayúscula y un signo especial
                            """
        )
    elif repassword_text == "":
        error_label.configure(text="La confirmación de contraseña no puede estar vacia")
    elif repassword_text != password_text:
        error_label.configure(text="Las contraseñas no coinciden")
    elif optionmenu.get() == "Seleccione":
        error_label.configure(text="Campos vacios, seleccione el rango")
    elif not validate_email(email):
        error_label.configure(text="El correo electrónico es inválido")
    else:
        new_user = {
            "username": username_text,
            "password": password_text,
            "Rango": rango,
            "Correo": email,
        }
        user_data[username_text] = new_user
        cargar_archivos.save_user_data(user_data)
        error_label.configure(text="Usuario registrado exitosamente")


def handle_sidebar_button_1():
    frame_registro.grid(row=0, column=1, rowspan=4, sticky="nsew")
    frame_incidencias.grid_remove()
    frame_modificar_usuarios.grid_remove()


def handle_sidebar_button_2():
    frame_incidencias.grid(row=0, column=1, rowspan=4, sticky="nsew")
    frame_registro.grid_remove()
    frame_modificar_usuarios.grid_remove()


def handle_sidebar_button_3():
    frame_incidencias.grid_remove()
    frame_registro.grid_remove()
    frame_modificar_usuarios.grid(row=0, column=1, sticky="nsew")


def populate_ticket_table():
    tickets.clear()
    with open("informacion.csv", mode="r") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        for row in csv_reader:
            tickets.append(row)
    tickets.sort(key=lambda x: int(x[0]), reverse=True)
    tree_ticket_table.delete(*tree_ticket_table.get_children())
    for ticket in tickets:
        tree_ticket_table.insert("", "end", values=ticket)
    num_pages = math.ceil(len(tickets) / 10)
    if num_pages > 0:
        cambiar_pagina(1)


def buscar_ticket():
    search_term = entry_search.get().lower()
    tickets.clear()
    with open("informacion.csv", mode="r") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        for row in csv_reader:
            if not search_term or any(
                search_term == col.lower() if col else True for col in row[0:]
            ):
                tickets.append(row)
    tickets.sort(key=lambda x: int(x[0]), reverse=True)
    tree_ticket_table.delete(*tree_ticket_table.get_children())
    for ticket in tickets:
        tree_ticket_table.insert("", "end", values=ticket)
    num_pages = math.ceil(len(tickets) / 10)
    if num_pages > 0:
        cambiar_pagina(1)


def graficos():
    estados = {"activo": 0, "en progreso": 0, "finalizado": 0}
    for ticket in tickets:
        estado = ticket[10].lower()
        if estado in estados:
            estados[estado] += 1
        else:
            print(f"Estado inválido: {estado}")

    datos = {k: v for k, v in estados.items() if v > 0}
    datos = {k.upper(): v for k, v in datos.items()}

    fig, ax = plt.subplots()
    ax.pie(datos.values(), labels=datos.keys(), autopct="%1.1f%%")
    ax.axis("equal")
    ax.set_title("Efectividad Semanal")

    topframe_graficos = customtkinter.CTkToplevel()
    topframe_graficos.title("Grafico Incidencias")
    topframe_graficos.lift()
    topframe_graficos.attributes("-topmost", 1)
    topframe_graficos.resizable(False, False)
    frame_grafico = customtkinter.CTkFrame(topframe_graficos)
    frame_grafico.grid(row=2, column=0, columnspan=3, padx=10, pady=10, sticky="w")

    canvas = FigureCanvasTkAgg(fig, master=frame_grafico)
    canvas.draw()
    canvas.get_tk_widget().pack(side="top", fill="both", expand=True)


def grafico_tecnico():
    tickets_filtrados = [
        ticket for ticket in tickets if ticket[10].lower() in ["activo", "en progreso"]
    ]

    tecnicos = {}
    for ticket in tickets_filtrados:
        tecnico = ticket[7]
        estado = ticket[10].lower()

        tecnicos[tecnico] = tecnicos.setdefault(tecnico, {})
        tecnicos[tecnico][estado] = tecnicos[tecnico].setdefault(estado, 0)
        tecnicos[tecnico][estado] += 1

    datos = [(tecnico, cantidades) for tecnico, cantidades in tecnicos.items()]
    colores = ["b", "g", "r", "c", "m", "y", "k"]  # Colores para cada barra

    fig, ax = plt.subplots()
    width = 0.75
    ind = np.arange(len(datos))
    bottom = np.zeros(len(datos))

    for i, (tecnico, cantidades) in enumerate(datos):
        cantidades_corregida = {
            k.capitalize(): v for k, v in cantidades.items()
        }  # Convertir claves a mayúsculas
        rects = ax.barh(
            ind[i],
            cantidades_corregida["Activo"],
            width,
            left=bottom[i],
            color=colores[i % len(colores)],
            label=f"{tecnico} (Activos: {cantidades_corregida['Activo']})",
        )
        bottom[i] += cantidades_corregida["Activo"]
        ax.barh(
            ind[i],
            cantidades_corregida.get("En progreso", 0),
            width,
            left=bottom[i],
            color=colores[(i + 1) % len(colores)],
            label=f"{tecnico} (En progreso: {cantidades_corregida.get('En progreso', 0)})",
        )
        bottom[i] += cantidades_corregida.get("En progreso", 0)

    ax.set_xlabel("Número de Tickets")
    ax.set_title("Tickets por Técnico")
    ax.set_yticks(ind)
    ax.set_yticklabels([c[0] for c in datos])
    ax.legend(loc="upper right")

    topframe_graficos = customtkinter.CTkToplevel()
    topframe_graficos.title("Grafico Tecnicos")
    topframe_graficos.lift()
    topframe_graficos.attributes("-topmost", 1)
    topframe_graficos.resizable(False, False)
    frame_grafico = customtkinter.CTkFrame(topframe_graficos)
    frame_grafico.grid(row=2, column=0, columnspan=3, padx=10, pady=10, sticky="w")
    canvas = FigureCanvasTkAgg(fig, master=frame_grafico)
    canvas.draw()
    canvas.get_tk_widget().pack(side="top", fill="both", expand=True)


def descargar_csv():
    temp_file = io.StringIO()

    writer = csv.writer(temp_file)
    writer.writerow(
        [
            "ID",
            "Producto",
            "Modelo",
            "Problema",
            "Nombres",
            "Numero Telefonico",
            "Email",
            "Tecnico asignado",
            "Fecha creacion",
            "Fecha ultima modificacion",
            "Estado",
        ]
    )

    for ticket in tickets:
        writer.writerow(ticket)

    temp_file.seek(0)

    file_path = tkinter.filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=[("CSV files", "*.csv")],
        title="Guardar como",
        initialdir=os.getcwd(),
        initialfile="Informacion.csv",
    )

    if file_path:
        with open(file_path, "w", newline="") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerows(tickets)


# Proceso

customtkinter.set_default_color_theme("blue")

if len(sys.argv) > 1:
    logged_in_tech_id = sys.argv[1]

current_path = os.path.dirname(os.path.realpath(__file__))
error_image = customtkinter.CTkImage(
    Image.open(os.path.join(current_path, "Imagenes", "error.png")), size=(40, 40)
)

width = 700
height = 500
g_incidencias = customtkinter.CTk()
x = (g_incidencias.winfo_screenwidth() // 2) - (width // 2)
y = (g_incidencias.winfo_screenwidth() // 3) - ((width + 500) // 3)
g_incidencias.iconbitmap(os.path.join(current_path, "Imagenes", "Logo.ico"))
g_incidencias.geometry("+{}+{}".format(x - 200, y))
g_incidencias.title("Gestión de incidencias Administrador")
g_incidencias.grid_rowconfigure(0, weight=1)
g_incidencias.grid_columnconfigure(0, weight=1)
g_incidencias.grid_columnconfigure(1, weight=10)

g_incidencias.resizable(False, False)
customtkinter.set_appearance_mode("Light")
current_path = os.path.dirname(os.path.realpath(__file__))
logo_admin = customtkinter.CTkImage(
    Image.open(os.path.join(current_path, "Imagenes", "Logo.png")), size=(70, 70)
)
sidebar_frame = customtkinter.CTkFrame(g_incidencias, corner_radius=0, height=250)
sidebar_frame.grid_propagate(False)
sidebar_frame.grid(
    row=0, column=0, rowspan=1, sticky="nsew", padx=10, pady=10, ipadx=20, ipady=110
)
sidebar_frame.grid_rowconfigure(8, weight=1)

logo_label = customtkinter.CTkLabel(
    sidebar_frame,
    text="ServiSoft",
    font=customtkinter.CTkFont(size=20, weight="bold"),
    text_color="#000000",
    image=logo_admin,
)
logo_label.grid(row=0, column=0, padx=(50, 0), pady=(30, 10))

sidebar_button_1 = customtkinter.CTkButton(
    sidebar_frame, text="Registro Nuevo Usuario", command=handle_sidebar_button_1
)
sidebar_button_1.grid(row=1, column=0, padx=(50, 0), pady=10)
sidebar_button_2 = customtkinter.CTkButton(
    sidebar_frame, text="Verificar incidencias", command=handle_sidebar_button_2
)
sidebar_button_2.grid(row=2, column=0, padx=(50, 0), pady=10)

usuarios_btn = customtkinter.CTkButton(
    sidebar_frame,
    text="Modificar usuarios",
    corner_radius=7,
    hover_color="#660000",
    command=handle_sidebar_button_3,
    height=30,
)
usuarios_btn.grid(row=3, column=0, padx=(50, 0), pady=10)

cambio_contra_btn = customtkinter.CTkButton(
    sidebar_frame,
    text="Cambiar Contraseña",
    corner_radius=7,
    hover_color="#660000",
    command=abrir_ventana_cambio_contra,
)
cambio_contra_btn.grid(row=4, column=0, padx=(50, 0), pady=10)
logout_btn = customtkinter.CTkButton(
    sidebar_frame,
    text="Cerrar Sesión",
    corner_radius=7,
    hover_color="#660000",
    command=cerrar_sesion,
    height=30,
)
logout_btn.grid(row=5, column=0, padx=(50, 0), pady=10)

appearance_mode_optionemenu = customtkinter.CTkSwitch(
    sidebar_frame, text="Modo oscuro", command=change_appearance_mode_event
)
appearance_mode_optionemenu.grid(row=6, column=0, padx=(50, 0), pady=10)
usuario_log = customtkinter.CTkLabel(
    sidebar_frame, text="Usuario: " + logged_in_tech_id
)
usuario_log.grid(row=7, column=0, padx=(0, 110), pady=10)
actual_time = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
fecha_hora = customtkinter.CTkLabel(sidebar_frame, text=actual_time)
fecha_hora.grid(row=7, column=0, padx=(0, 50), pady=(50, 0))


frame_registro = customtkinter.CTkFrame(g_incidencias, width=140, corner_radius=0)
frame_registro.grid(row=0, column=1, rowspan=4, sticky="nsew")
frame_incidencias = customtkinter.CTkFrame(g_incidencias, width=140, corner_radius=0)
frame_modificar_usuarios = customtkinter.CTkFrame(
    g_incidencias, width=140, corner_radius=0
)
frame_modificar_usuarios_tabla = customtkinter.CTkFrame(
    frame_modificar_usuarios, corner_radius=0, width=1000, height=800
)
frame_modificar_usuarios_tabla.grid(
    row=1, column=0, columnspan=2, padx=10, pady=10, sticky="w"
)

scrollable_frame_modificar_usuario = customtkinter.CTkScrollableFrame(
    frame_modificar_usuarios_tabla, corner_radius=0, width=1000, height=400
)
scrollable_frame_modificar_usuario.grid(
    row=1, column=0, padx=10, pady=10, sticky="nsew"
)

# Leer el json
with open("user_data.json", "r") as file:
    data = json.load(file)
titulo_modificar_usuarios = customtkinter.CTkLabel(
    frame_modificar_usuarios_tabla, text="Modificar usuarios", font=("Roboto bold", 25)
)
titulo_modificar_usuarios.grid(row=0, column=0, padx=10, pady=10, sticky="nw")

table = ttk.Treeview(
    scrollable_frame_modificar_usuario,
    columns=("Usuario", "Contraseña", "Rango", "Correo"),
    show="headings",
    height=18,
)

def eliminar_usuarios():
    selected_item = table.selection()
    respuesta = messagebox.askquestion(
        title='Confirmación',
        message='¿Está seguro de que desea eliminar este usuario?'
    )
    if respuesta == 'yes':
        with open("user_data.json", "r") as file:  # Open the JSON file in read mode
            user_data = json.load(file)
        for item in selected_item:
            user_id = table.item(item, "values")[0]
            if user_id in user_data:
                del user_data[user_id]
        with open("user_data.json", "w") as file:  # Open the JSON file in write mode
            json.dump(user_data, file, indent=4)
        table.delete(item)

def modificar_tabla(event=None):
    global entry, new_window, selecciona
    selected_item = table.focus()  # Get the selected item in the table
    if selected_item:
        selected_values = table.item(
            selected_item, "values"
        )  # Get the values of the selected item
        new_window = customtkinter.CTkToplevel(
            g_incidencias
        )  # Create a new Toplevel window
        new_window.title("Detalles del registro")
        new_window.geometry("350x300+{}+{}".format(x + 200, y + 200))
        new_window.resizable(False,False)
        # Add a label and option menu to select the column to be modified
        label_act_problema = customtkinter.CTkLabel(
            new_window,
            text="Selecciona el dato a modificar: ",
            font=("Roboto bold", 18),
        )
        label_act_problema.grid(row=5, column=1, padx=(60, 10), pady=10, sticky="e")
        column_options = ["Usuario", "Contraseña", "Rango", "Correo"]
        selected_column = tkinter.StringVar(new_window)
        selected_column.set("Seleccione")  # Set the default column to be modified
        menu_option = customtkinter.CTkOptionMenu(
            new_window, variable=selected_column, values=column_options
        )
        menu_option.grid(row=6, column=1, padx=(50, 10), pady=10)
        entry = customtkinter.CTkEntry(
            new_window, placeholder_text="Ingrese la nueva info"
        )
        entry.grid(row=7, column=1, padx=(50, 10), pady=10)
        # Add a button to confirm the modification
        confirm_button = customtkinter.CTkButton(
            new_window,
            text="Modificar Usuario",
            command=lambda: modificar(
                new_window, selected_values, selected_column.get()
            ),
        )
        confirm_button.grid(row=8, column=1, padx=(50, 10), pady=10)
        
        eliminar_usuario = customtkinter.CTkButton(
            new_window,
            text="Eliminar Usuario",
            command=lambda: eliminar_usuarios()
        )
        eliminar_usuario.grid(row=9, column=1, padx=(50, 10), pady=10)
        
        opciones = ["Administrador", "Tecnico", "Agente"]
        selecciona = tkinter.StringVar(new_window)
        selecciona.set("Seleccione")  # Set the default column to be modified

        menu = customtkinter.CTkOptionMenu(
            new_window, variable=selecciona, values=opciones
        )

        # Show/hide the entry and optionmenu based on the selected column
        def on_column_selected(column):
            if column == "Rango":
                entry.grid_remove()
                menu.grid(row=7, column=1, padx=(50, 10), pady=10)
            else:
                menu.grid_remove()
                entry.grid(row=7, column=1, padx=(50, 10), pady=10)

        selected_column.trace(
            "w", lambda *args, **kwargs: on_column_selected(selected_column.get())
        )
        on_column_selected(selected_column.get())


def modificar(new_window, selected_values, selected_column):
    new_value = entry.get()
    new_value_1 = selecciona.get()
    try:
        with open("user_data.json", "r+") as file:
            user_data = json.load(file)

            # Actualiza el valor en el archivo JSON
            if selected_column == "Usuario":
                user_data[selected_values[0]]["username"] = new_value
                user_data[new_value] = user_data.pop(selected_values[0])
            elif selected_column == "Contraseña":
                user_data[selected_values[0]]["password"] = new_value
            elif selected_column == "Rango":
                user_data[selected_values[0]][selected_column] = new_value_1
            else:
                user_data[selected_values[0]][selected_column] = new_value

            # Mueve el puntero del archivo al principio
            file.seek(0)
            json.dump(user_data, file, indent=4)

            # Trunca cualquier contenido restante (si lo hay)
            file.truncate()

        # Actualiza la tabla (asumiendo que tienes una variable 'table' definida)
        
        for col_index, col_name in enumerate(table["columns"]):
            if col_name == selected_column:
                table.set(table.focus(), col_index, new_value)
                
                break

        # Cierra la ventana
        new_window.destroy()

        print("Archivo JSON actualizado correctamente.")

    except FileNotFoundError:
        print("El archivo 'user_data.json' no existe.")
    except json.JSONDecodeError:
        print("Error al cargar el archivo JSON.")
    except Exception as e:
        print("Unexpected error:", str(e))


table.heading("Usuario", text="Usuario")
table.heading("Contraseña", text="Contraseña")
table.heading("Rango", text="Rango")
table.heading("Correo", text="Correo")
table.bind("<Double-1>", modificar_tabla)
table.pack(pady=10, padx=10, fill="both", expand=True)


# Agregar los usuarios a la tabla
for user in data.values():
    table.insert(
        "",
        tkinter.END,
        values=(user["username"], user["password"], user["Rango"], user["Correo"]),
    )

titulo = customtkinter.CTkLabel(
    frame_registro,
    text="Registro",
    font=customtkinter.CTkFont(size=20, weight="bold"),
)
titulo.grid(row=0, column=0, padx=(300, 300), pady=(10, 10))

error_label = customtkinter.CTkLabel(
    frame_registro, text="", justify="center", bg_color="transparent"
)
error_label.grid(row=1, column=0, padx=(200, 0), pady=(5, 5))

username = customtkinter.CTkEntry(
    frame_registro,
    placeholder_text="Nuevo Usuario",
    placeholder_text_color="#000000",
    text_color="#000000",
    border_width=0,
    corner_radius=7,
    width=200,
    height=35,
    fg_color="#f6f6f6",
)
username.grid(row=1, column=0, padx=(10, 300), pady=(10, 10))
contra = customtkinter.CTkEntry(
    frame_registro,
    placeholder_text="Nueva Contraseña",
    placeholder_text_color="#000000",
    text_color="#000000",
    border_width=0,
    corner_radius=7,
    width=200,
    height=35,
    fg_color="#f6f6f6",
    show="*",
)
contra.grid(row=2, column=0, padx=(10, 300), pady=(20, 20))
recontra = customtkinter.CTkEntry(
    frame_registro,
    placeholder_text="Repetir Nueva Contraseña",
    placeholder_text_color="#000000",
    text_color="#000000",
    border_width=0,
    corner_radius=7,
    width=200,
    height=35,
    fg_color="#f6f6f6",
    show="*",
)
recontra.grid(row=3, column=0, padx=(10, 300), pady=(20, 20))

correo = customtkinter.CTkEntry(
    frame_registro,
    placeholder_text="Correo Electronico",
    placeholder_text_color="#000000",
    text_color="#000000",
    border_width=0,
    corner_radius=7,
    width=200,
    height=35,
    fg_color="#f6f6f6",
)
correo.grid(row=4, column=0, padx=(10, 300), pady=(20, 20))


registro_btn = customtkinter.CTkButton(
    frame_registro,
    text="Registrar",
    width=200,
    height=30,
    corner_radius=7,
    font=("Roboto", 20),
    compound="right",
    hover_color="#660000",
    command=handle_register,
)
registro_btn.grid(row=5, column=0, padx=(10, 300), pady=(20, 20))
optionmenu = customtkinter.CTkOptionMenu(
    frame_registro,
    values=["Seleccione", "Administrador", "Tecnico", "Agente"],
    dropdown_hover_color="#ff9999",
)
optionmenu.grid(row=2, column=0, padx=(200, 0), pady=(10, 10))


frame_ticket_table = customtkinter.CTkFrame(frame_incidencias, width=1000)
frame_ticket_table.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="w")
frame_ticket_table.grid_columnconfigure(0, weight=1)
frame_ticket_table.grid_columnconfigure(1, weight=1)
frame_ticket_table.grid_columnconfigure(2, weight=1)
scrollable_frame = customtkinter.CTkScrollableFrame(
    frame_ticket_table, width=1000, height=300, orientation="horizontal"
)
scrollable_frame.grid(row=0, column=0, columnspan=3, padx=10, pady=10, sticky="w")
scrollable_frame_paginacion = customtkinter.CTkScrollableFrame(
    frame_ticket_table, height=50, orientation="horizontal"
)
scrollable_frame_paginacion.grid(
    row=1, column=0, columnspan=3, padx=10, pady=10, sticky="w"
)

label_ticket_table = customtkinter.CTkLabel(scrollable_frame, text="Incidencias")
label_ticket_table.grid(row=0, column=0, columnspan=3, padx=10, pady=10, sticky="w")
tree_ticket_table = ttk.Treeview(scrollable_frame)

tree_ticket_table.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="w")
tree_ticket_table["columns"] = (
    "ID",
    "Producto",
    "Modelo",
    "Problema",
    "Nombres",
    "Numero Telefonico",
    "Email",
    "Tecnico asignado",
    "Fecha creacion",
    "Fecha ultima modificacion",
    "Estado",
    "Comentario Tecnico",
)
tree_ticket_table.column("#0", width=0, stretch=False)
tree_ticket_table.column("ID", width=30, minwidth=0, anchor="center")
tree_ticket_table.column("Producto", width=150, minwidth=150, anchor="center")
tree_ticket_table.column("Modelo", width=150, minwidth=150, anchor="center")
tree_ticket_table.column("Problema", width=180, minwidth=180, anchor="center")
tree_ticket_table.column("Nombres", width=150, minwidth=150, anchor="center")
tree_ticket_table.column("Numero Telefonico", width=150, minwidth=150, anchor="center")
tree_ticket_table.column("Email", width=150, minwidth=150, anchor="center")
tree_ticket_table.column("Tecnico asignado", width=150, minwidth=150, anchor="center")
tree_ticket_table.column("Fecha creacion", width=150, minwidth=150, anchor="center")
tree_ticket_table.column(
    "Fecha ultima modificacion", width=150, minwidth=150, anchor="center"
)
tree_ticket_table.column("Estado", width=100, minwidth=100, anchor="center")
tree_ticket_table.column("Comentario Tecnico", width=100, minwidth=100, anchor="center")
tree_ticket_table.heading("#0", text="")
tree_ticket_table.heading("ID", text="ID")
tree_ticket_table.heading("Producto", text="Producto")
tree_ticket_table.heading("Modelo", text="Modelo")
tree_ticket_table.heading("Problema", text="Problema")
tree_ticket_table.heading("Nombres", text="Nombres")
tree_ticket_table.heading("Numero Telefonico", text="Numero Telefonico")
tree_ticket_table.heading("Email", text="Email")
tree_ticket_table.heading("Tecnico asignado", text="Tecnico asignado")
tree_ticket_table.heading("Fecha creacion", text="Fecha creación")
tree_ticket_table.heading("Fecha ultima modificacion", text="Fecha ultima modificación")
tree_ticket_table.heading("Estado", text="Estado")
tree_ticket_table.heading("Comentario Tecnico", text="Comentario Tecnico")

frame_search = customtkinter.CTkFrame(frame_incidencias)
frame_search.grid(row=0, column=0, padx=10, pady=10, sticky="w")
frame_search.grid_columnconfigure(3, weight=1)
search_frame = customtkinter.CTkFrame(frame_search)
search_frame.grid(row=0, column=0, padx=10, pady=10, sticky="w")
label_search = customtkinter.CTkLabel(search_frame, text="Search:")
label_search.grid(row=0, column=0, padx=10, pady=10, sticky="w")
entry_search = customtkinter.CTkEntry(search_frame)
entry_search.grid(row=0, column=1, padx=10, pady=10, sticky="w")

frame_edit_ticket = customtkinter.CTkFrame(frame_incidencias)
frame_edit_ticket.grid(row=0, column=1, padx=10, pady=10, sticky="w")
frame_edit_ticket.grid_columnconfigure(3, weight=1)

button_estado_ticket = customtkinter.CTkButton(
    frame_edit_ticket, text="Grafico Pastel", command=graficos
)
button_estado_ticket.grid(row=0, column=0, padx=10, pady=10, sticky="w")

button_tecnico_ticket = customtkinter.CTkButton(
    frame_edit_ticket, text="Tickets por Técnico", command=grafico_tecnico
)
button_tecnico_ticket.grid(row=0, column=1, padx=10, pady=10, sticky="w")

button_datos_sistema = customtkinter.CTkButton(
    frame_edit_ticket, text="Descargar Datos", command=descargar_csv
)
button_datos_sistema.grid(row=0, column=2, padx=10, pady=10, sticky="w")

button_search = customtkinter.CTkButton(
    frame_search, text="Buscar", command=buscar_ticket
)
button_search.grid(row=0, column=2, padx=10, pady=10, sticky="w")

populate_ticket_table()
actualizar_botones_paginacion()
actualizar_fecha_hora()

g_incidencias.mainloop()
