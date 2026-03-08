import customtkinter, cargar_archivos, os, subprocess, csv, sys, re, math, datetime
from PIL import Image
from tkinter import ttk
from Login import logged_in_tech_id
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

if len(sys.argv) > 1:
    logged_in_tech_id = sys.argv[1]


current_path = os.path.dirname(os.path.realpath(__file__))
error_image = customtkinter.CTkImage(
    Image.open(os.path.join(current_path, "Imagenes", "error.png")), size=(40, 40)
)


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


def ejecutar_archivo():
    try:
        subprocess.run(["python", "FrameMarca.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar el archivo: {e}")


if len(sys.argv) > 1:
    logged_in_tech_id = sys.argv[1]


def abrir_ventana_cambio_contra():
    global x, y, contra_nueva, recontra_nueva, ventana_otro_problema

    ventana_otro_problema = customtkinter.CTkToplevel(g_incidencias)
    width = ventana_otro_problema.winfo_screenwidth()
    height = ventana_otro_problema.winfo_screenheight()
    x = (width // 2) - (ventana_otro_problema.winfo_reqwidth() // 2)
    y = (height // 2) - (ventana_otro_problema.winfo_reqheight() // 2)
    ventana_otro_problema.geometry(f"300x200+{x - 150}+{y - 100}")
    ventana_otro_problema.title("Cambio Contraseña")
    ventana_otro_problema.resizable(False, False)
    ventana_otro_problema.lift()
    ventana_otro_problema.attributes("-topmost", 1)

    contra_nueva = customtkinter.CTkEntry(
        ventana_otro_problema,
        placeholder_text="Contraseña:",
        font=("Roboto", 15),
        show="*",
    )
    contra_nueva.pack(pady=(20, 10))

    recontra_nueva = customtkinter.CTkEntry(
        ventana_otro_problema,
        placeholder_text="Repetir Contraseña:",
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
        error_contra_nueva = "La contraseña debe tener al menos 8 caracteres,una letra mayúscula y un signo especial"
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


tickets = []


def cerrar_sesion():
    archivo_a_ejecutar = "Login.py"
    g_incidencias.destroy()
    try:
        subprocess.run(["python", archivo_a_ejecutar], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar el archivo: {e}")


def change_appearance_mode_event():
    new_appearance_mode = "Dark" if appearance_mode_optionemenu.get() else "Light"
    customtkinter.set_appearance_mode(new_appearance_mode)


def actualizar_fecha_hora():
    actual_time = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    fecha_hora.configure(text=actual_time)
    fecha_hora.after(1000, actualizar_fecha_hora)


width = 700
height = 400
customtkinter.set_default_color_theme("blue")
g_incidencias = customtkinter.CTk()
x = (g_incidencias.winfo_screenwidth() // 2) - (width // 2)
y = (g_incidencias.winfo_screenwidth() // 3) - ((width + 500) // 3)
g_incidencias.geometry("+{}+{}".format(x - 200, y))
customtkinter.set_appearance_mode("Light")
g_incidencias.title("Gestión de incidencias Tecnico")
g_incidencias.iconbitmap(os.path.join(current_path, "Imagenes", "Logo.ico"))
g_incidencias.grid_rowconfigure(0, weight=1)
g_incidencias.grid_columnconfigure(0, weight=1)
g_incidencias.grid_columnconfigure(1, weight=10)

g_incidencias.resizable(False, False)
current_path = os.path.dirname(os.path.realpath(__file__))
logo_admin = customtkinter.CTkImage(
    Image.open(os.path.join(current_path, "Imagenes", "Logo.png")), size=(70, 70)
)
sidebar_frame = customtkinter.CTkFrame(g_incidencias, corner_radius=0)
sidebar_frame.grid_propagate(False)
sidebar_frame.grid(
    row=0, column=0, rowspan=4, sticky="nsew", padx=10, pady=10, ipadx=20, ipady=110
)
sidebar_frame.grid_rowconfigure(4, weight=1)
logo_label = customtkinter.CTkLabel(
    sidebar_frame,
    text="ServiSoft",
    font=customtkinter.CTkFont(size=20, weight="bold"),
    text_color="#000000",
    image=logo_admin,
)
logo_label.grid(row=0, column=0, padx=(50, 0), pady=(30, 10))
appearance_mode_optionemenu = customtkinter.CTkSwitch(
    sidebar_frame, text="Modo oscuro", command=change_appearance_mode_event
)
appearance_mode_optionemenu.grid(row=1, column=0, padx=(50, 0), pady=10)

logout_btn = customtkinter.CTkButton(
    sidebar_frame,
    text="Cerrar Sesión",
    corner_radius=7,
    hover_color="#660000",
    command=cerrar_sesion,
)
logout_btn.grid(row=3, column=0, padx=(50, 0), pady=10)
cambio_contra_btn = customtkinter.CTkButton(
    sidebar_frame,
    text="Cambiar Contraseña",
    corner_radius=7,
    hover_color="#660000",
    command=abrir_ventana_cambio_contra,
)
cambio_contra_btn.grid(row=2, column=0, padx=(50, 0), pady=10)

usuario_log = customtkinter.CTkLabel(
    sidebar_frame, text="Usuario: " + logged_in_tech_id
)
usuario_log.grid(row=6, column=0, padx=(0, 110), pady=10)
actual_time = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
fecha_hora = customtkinter.CTkLabel(sidebar_frame, text=actual_time)
fecha_hora.grid(row=6, column=0, padx=(0, 50), pady=(50, 0))
frame_incidencias = customtkinter.CTkFrame(g_incidencias, width=140, corner_radius=0)
frame_incidencias.grid(row=0, column=1, rowspan=4, sticky="nsew")


frame_ticket_table = customtkinter.CTkFrame(frame_incidencias)
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
tree_ticket_table.heading("Fecha ultima modificacion", text="Fecha ultima modificacion")
tree_ticket_table.heading("Estado", text="Estado")
tree_ticket_table.heading("Comentario Tecnico", text="Comentario Tecnico")


def populate_ticket_table():

    global tickets
    tickets = []

    with open("informacion.csv", mode="r") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        for row in csv_reader:
            if logged_in_tech_id in row[7] and row[10] != "Finalizado":
                tickets.append(row)
    tickets.sort(key=lambda x: int(x[0]), reverse=True)

    tree_ticket_table.delete(*tree_ticket_table.get_children())
    for ticket in tickets:
        tree_ticket_table.insert("", "end", values=ticket)

    num_pages = math.ceil(len(tickets) / 10)
    if num_pages > 0:
        cambiar_pagina(1)
    actualizar_botones_paginacion()


frame_buscar = customtkinter.CTkFrame(frame_incidencias)
frame_buscar.grid(row=0, column=0, padx=10, pady=10, sticky="w")
frame_buscar.grid_columnconfigure(3, weight=1)

buscar_frame = customtkinter.CTkFrame(frame_buscar)
buscar_frame.grid(row=0, column=0, padx=10, pady=10, sticky="w")
label_buscar = customtkinter.CTkLabel(buscar_frame, text="buscar:")
label_buscar.grid(row=0, column=0, padx=10, pady=10, sticky="w")
entry_buscar = customtkinter.CTkEntry(buscar_frame)
entry_buscar.grid(row=0, column=1, padx=10, pady=10, sticky="w")


def buscar_ticket():
    buscar_term = entry_buscar.get().lower()
    tickets.clear()
    with open("informacion.csv", mode="r") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        for row in csv_reader:
            if (
                logged_in_tech_id in row[7]
                and row[10] != "Finalizado"
                and (
                    not buscar_term
                    or any(
                        buscar_term == col.lower() if col else True for col in row[0:]
                    )
                )
            ):
                tickets.append(row)
    tickets.sort(key=lambda x: int(x[0]), reverse=True)
    tree_ticket_table.delete(*tree_ticket_table.get_children())
    for ticket in tickets:
        tree_ticket_table.insert("", "end", values=ticket)

    num_pages = math.ceil(len(tickets) / 10)
    if num_pages > 0:
        cambiar_pagina(1)


button_buscar = customtkinter.CTkButton(
    frame_buscar, text="buscar", command=lambda: buscar_ticket()
)
button_buscar.grid(row=0, column=2, padx=10, pady=10, sticky="w")


def abrir_ventana_detalles(event):
    global text_act_problema, new_window
    selected_item = tree_ticket_table.focus()
    if selected_item:
        selected_values = tree_ticket_table.item(selected_item, "values")

        new_window = customtkinter.CTkToplevel(g_incidencias)
        new_window.title("Detalles del registro")
        new_window.geometry("350x")
        for i, value in enumerate(selected_values[1:7]):
            header = tree_ticket_table.heading(column=i + 1)["text"]
            label = customtkinter.CTkLabel(
                new_window, text=f"{header.capitalize()}: {value}"
            )
            label.grid(row=i, column=0, padx=10, pady=10, sticky="w")
        label_act_problema = customtkinter.CTkLabel(
            new_window, text="Comentario Tecnico: ", font=("Roboto bold", 18)
        )
        label_act_problema.grid(row=8, column=0, padx=10, pady=10, sticky="w")
        text_act_problema = customtkinter.CTkTextbox(new_window, width=500, height=200)
        text_act_problema.grid(
            row=9, column=0, padx=10, pady=10, sticky="w", columnspan=2
        )
        btn_act_problema = customtkinter.CTkButton(
            new_window, text="Guardar", command=comentario_tecnico
        )
        btn_act_problema.grid(row=10, column=0, padx=10, pady=10, sticky="w")
        fin_act_problema = customtkinter.CTkButton(
            new_window, text="Finalizar Ticket", command=finalizar_ticket
        )
        fin_act_problema.grid(row=10, column=0, padx=(160, 0), pady=10, sticky="w")


tree_ticket_table.bind("<Double-1>", abrir_ventana_detalles)

columna_comentario_tecnico = 11
columna_fecha_ultima_modificacion = 9
columna_estado = 10


def comentario_tecnico():
    selected_item = tree_ticket_table.focus()
    if selected_item:
        selected_values = tree_ticket_table.item(selected_item, "values")

        email = selected_values[6]

        comentario_tecnico = text_act_problema.get("1.0", "end-1c")

        selected_values = list(selected_values)
        selected_values[columna_comentario_tecnico] = (
            comentario_tecnico if comentario_tecnico else "-"
        )
        selected_values[columna_estado] = "En progreso"
        selected_values[columna_fecha_ultima_modificacion] = (
            datetime.datetime.now().strftime("%Y-%m-%d")
        )
        selected_values = tuple(selected_values)

        with open("informacion.csv", "r", newline="") as csvfile:
            reader = csv.reader(csvfile)
            tickets = list(reader)

        indice_registro = None
        for i, ticket in enumerate(tickets):
            if ticket[0] == selected_values[0]:
                indice_registro = i
                break

        if indice_registro is not None:
            tickets[indice_registro] = selected_values

        mensaje = MIMEMultipart()
        mensaje["From"] = "pruebascorreopython96@gmail.com"
        mensaje["To"] = email
        mensaje["Subject"] = "Técnico actualizó su ticket"
        cuerpo = f"Estimado cliente,\n\nEl técnico ha actualizado su ticket con el siguiente comentario:\n\n{comentario_tecnico} \n\nSaludos,\nEl equipo de soporte técnico."
        mensaje.attach(MIMEText(cuerpo, "plain"))

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login("pruebascorreopython96@gmail.com", "pfsy lufv gmaj euvd")
        text = mensaje.as_string()
        server.sendmail("pruebascorreopython96@gmail.com", email, text)
        server.quit()

        for index, ticket in enumerate(tickets):
            if ticket[0] == selected_values[0]:
                tickets[index] = selected_values
                break

        with open("informacion.csv", "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(tickets)
        populate_ticket_table()
        new_window.destroy()


def finalizar_ticket():
    selected_item = tree_ticket_table.focus()
    if selected_item:
        selected_values = tree_ticket_table.item(selected_item, "values")

        email = selected_values[6]

        comentario_tecnico = text_act_problema.get("1.0", "end-1c")

        selected_values = list(selected_values)
        selected_values[columna_comentario_tecnico] = (
            comentario_tecnico if comentario_tecnico else "-"
        )
        selected_values[columna_estado] = "Finalizado"
        selected_values[columna_fecha_ultima_modificacion] = (
            datetime.datetime.now().strftime("%Y-%m-%d")
        )
        selected_values = tuple(selected_values)

        with open("informacion.csv", "r", newline="") as csvfile:
            reader = csv.reader(csvfile)
            tickets = list(reader)

        indice_registro = None
        for i, ticket in enumerate(tickets):
            if ticket[0] == selected_values[0]:
                indice_registro = i
                break

        if indice_registro is not None:
            tickets[indice_registro] = selected_values

        if indice_registro is not None:
            tickets[indice_registro] = selected_values

        mensaje = MIMEMultipart()
        mensaje["From"] = "pruebascorreopython96@gmail.com"
        mensaje["To"] = email
        mensaje["Subject"] = "Ticket finalizado"
        cuerpo = f"Estimado cliente,\n\nSu ticket ha sido finalizado. El técnico ha proporcionado el siguiente comentario:\n\n{comentario_tecnico}\n\nPuede acercarse a retirar su equipo en nuestro taller en horario de lunes a viernes de 8am a 5pm.\n\nSaludos,\nEl equipo de soporte técnico."
        mensaje.attach(MIMEText(cuerpo, "plain"))

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login("pruebascorreopython96@gmail.com", "pfsy lufv gmaj euvd")
        text = mensaje.as_string()
        server.sendmail("pruebascorreopython96@gmail.com", email, text)
        server.quit()

        for index, ticket in enumerate(tickets):
            if ticket[0] == selected_values[0]:
                tickets[index] = selected_values
                break

        with open("informacion.csv", "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(tickets)
        populate_ticket_table()


populate_ticket_table()
actualizar_fecha_hora()

g_incidencias.mainloop()
