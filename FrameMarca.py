import customtkinter as ctk
from PIL import Image
import os, csv, cargar_archivos, datetime, re


producto = ""
problema = ""
modelo = ""
nombres = ""
n_telefonico = ""
email = ""
tecnico_asignado = ""
fecha_creacion = ""
fecha_ultima_mod = ""
estado = ""

current_path = os.path.dirname(os.path.realpath(__file__))
error_image = ctk.CTkImage(
    Image.open(current_path + "./Imagenes/error.png"), size=(40, 40)
)


def obtener_ultimo_id():
    try:
        with open("informacion.csv", "r", newline="") as f:
            reader = csv.reader(f)
            if not reader:  # Check if the CSV file is empty
                raise ValueError("CSV file is empty")
            ultimo_id = max(int(row[0]) for row in reader)
    except ValueError as e:
        if "CSV file is empty" in e.args[0]:
            with open("informacion.csv", "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(
                    [
                        "ID",
                        "Producto",
                        "Modelo",
                        "Problema",
                        "Nombres",
                        "Número Telefónico",
                        "Email",
                        "Técnico Asignado",
                        "Fecha Creación",
                        "Fecha Última Modificación",
                        "Estado",
                    ]
                )
            ultimo_id = 0
        else:
            raise
    return ultimo_id


ultimo_id = obtener_ultimo_id() + 1


def validate_email(email):

    regex = r"^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$"
    return re.match(regex, email) is not None


ctk.set_default_color_theme("dark-blue")
app = ctk.CTk()
app.title("Soporte Técnico")
app.resizable(False, False)
app.iconbitmap(os.path.join(current_path, "Imagenes", "Logo.ico"))
ctk.set_appearance_mode("Light")  # Cambiar la apariencia

screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()

x = (screen_width // 2) - (app.winfo_reqwidth() // 2)
y = (screen_height // 2) - (app.winfo_reqheight() // 2)

app.geometry(f"600x700+{x - 300}+{y - 250}")


def change_appearance_mode_event():
    new_appearance_mode = "Dark" if appearance_mode_optionemenu.get() else "Light"
    ctk.set_appearance_mode(new_appearance_mode)


appearance_mode_optionemenu = ctk.CTkSwitch(
    app, text="Modo oscuro", command=change_appearance_mode_event
)
appearance_mode_optionemenu.pack(side="top", fill="x", padx=(470, 5), pady=(0, 0))


def show_frame(frame_to_show):

    frame_inferior.pack_forget()
    frame_inferior_computadoras.pack_forget()
    frame_inferior_laptops.pack_forget()
    frame_inferior_tar_video.pack_forget()
    frame_inferior_monitores.pack_forget()
    frame_to_show.pack(pady=20, padx=20, fill="both", expand=True)


def show_frame1(frame_to_show):
    modelo_computadoras = menu_computadoras.get()
    modelo_laptops = menu_laptops.get()
    modelo_monitores = menu_monitores.get()
    modelo_tar_video = menu_tar_video.get()

    if (
        modelo_computadoras == "Seleccione"
        and modelo_laptops == "Seleccione"
        and modelo_tar_video == "Seleccione"
        and modelo_monitores == "Seleccione"
    ):
        error_frame("Campos Vacios, seleccione un modelo")
        return
    else:
        frame_inferior.pack_forget()
        frame_inferior_computadoras.pack_forget()
        frame_inferior_laptops.pack_forget()
        frame_inferior_tar_video.pack_forget()
        frame_inferior_monitores.pack_forget()
        frame_inferior_computadoras1.pack_forget()
        frame_inferior_laptops1.pack_forget()
        frame_inferior_tar_video1.pack_forget()
        frame_inferior_monitores1.pack_forget()
        frame_to_show.pack(pady=20, padx=20, fill="both", expand=True)


frame_top = ctk.CTkFrame(app)
frame_top.pack(pady=20, padx=20, fill="both")

label_titulo = ctk.CTkLabel(frame_top, text="Soporte técnico", font=("Roboto", 20))
label_titulo.pack(pady=10, padx=10, fill="x")

label_subtitulo = ctk.CTkLabel(frame_top, text="Tickets asignados por tecnico.")
label_subtitulo.pack(pady=10, padx=10, fill="x")

frame_tecnico = ctk.CTkFrame(frame_top)
frame_tecnico.pack(padx=10, pady=10, fill="both")


def obtener_informacion_tecnicos():
    try:
        with open("informacion.csv", "r", newline="") as f:
            reader = csv.reader(f)
            if not reader:
                raise ValueError("CSV file is empty")
            tecnico_data = {}
            fecha_actual = datetime.datetime.now()
            una_semana_atras = fecha_actual - datetime.timedelta(days=7)
            for row in reader:
                tecnico = row[7]
                fecha_creacion = datetime.datetime.strptime(row[8], "%Y-%m-%d")
                if tecnico not in tecnico_data:
                    tecnico_data[tecnico] = {
                        "nombre": tecnico,
                        "tickets_activos_y_en_progreso": 0,
                        "tickets_semana": 0,
                    }
                if (
                    row[10] in ["Activo", "En progreso"]
                    and una_semana_atras <= fecha_creacion <= fecha_actual
                ):
                    tecnico_data[tecnico]["tickets_activos_y_en_progreso"] += 1
                    tecnico_data[tecnico]["tickets_semana"] += 1
            return tecnico_data
    except ValueError as e:
        if "CSV file is empty" in e.args[0]:
            with open("informacion.csv", "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(
                    [
                        "ID",
                        "Producto",
                        "Modelo",
                        "Problema",
                        "Nombres",
                        "Número Telefónico",
                        "Email",
                        "Técnico Asignado",
                        "Fecha Creación",
                        "Fecha Última Modificación",
                        "Estado",
                    ]
                )
            return {}
        else:
            raise


def mostrar_tecnicos(tecnico_data):
    frame_tecnicos = ctk.CTkFrame(
        frame_tecnico, bg_color="transparent", fg_color="transparent"
    )
    frame_tecnicos.pack(side="left", fill="x")

    frame_tickets = ctk.CTkFrame(
        frame_tecnico, bg_color="transparent", fg_color="transparent"
    )
    frame_tickets.pack(side="left", fill="x")

    fila_index = 0
    for tecnico, info in tecnico_data.items():
        label_tecnico = ctk.CTkLabel(
            frame_tecnicos, text=f"Tecnico: {tecnico}", font=("Roboto", 12, "bold")
        )
        label_tecnico.pack(side="top", fill="x", padx=5, pady=2)

        label_tickets = ctk.CTkLabel(
            frame_tickets,
            text=f"tiene {info['tickets_semana']} Tickets asignados esta semana",
        )
        label_tickets.pack(side="top", fill="x", padx=5, pady=2)
        fila_index += 1


tecnico_data = obtener_informacion_tecnicos()
mostrar_tecnicos(tecnico_data)

frame_datos = ctk.CTkFrame(app)
frame_datos.pack(pady=20, padx=20, fill="both")

label_titulo1 = ctk.CTkLabel(frame_datos, text="Datos", font=("Roboto", 20))
label_titulo1.pack(pady=10, padx=10, fill="x", anchor="w")

contenedor_1 = ctk.CTkFrame(frame_datos)
contenedor_1.pack(pady=10, padx=10, anchor="w")

label_nombre = ctk.CTkLabel(contenedor_1, text="Nombres: ")
label_nombre.pack(side="left", padx=5)


entry_nombre = ctk.CTkEntry(
    contenedor_1, width=150, placeholder_text="Ej: Pepito Perez"
)
entry_nombre.pack(side="left", padx=5)


entry_n_telefonico = ctk.CTkEntry(
    master=contenedor_1, validate="key", width=150, placeholder_text="Ej: 0999999999"
)
entry_n_telefonico.pack(side="right", padx=5)

label_n_telefonico = ctk.CTkLabel(contenedor_1, text="Numero Telefonico: ")
label_n_telefonico.pack(side="right", padx=5)

contenedor_2 = ctk.CTkFrame(frame_datos)
contenedor_2.pack(pady=10, padx=10, anchor="w")

label_email = ctk.CTkLabel(contenedor_2, text="Email: ")
label_email.pack(side="left", padx=15)

entry_email = ctk.CTkEntry(
    contenedor_2, width=150, placeholder_text="Ej: prueba@gmail.com"
)
entry_email.pack(side="left", padx=5)

user_data = cargar_archivos.load_user_data()

tecnico_users = [
    user for user in user_data.keys() if user_data[user]["Rango"] == "Tecnico"
]
tecnico_users.insert(0, "Seleccione")
option_t_asignado = ctk.CTkOptionMenu(
    contenedor_2,
    values=tecnico_users,
    corner_radius=7,
    width=150,
    button_hover_color="#ff9999",
    dropdown_hover_color="#ff9999",
)
option_t_asignado.pack(side="right", padx=5)

label_t_asignado = ctk.CTkLabel(contenedor_2, text="Tecnico Asignado: ")
label_t_asignado.pack(side="right", padx=9)


frame_inferior = ctk.CTkFrame(app)
frame_inferior.pack(pady=20, padx=20, fill="both", expand=True)

label_producto = ctk.CTkLabel(
    frame_inferior, text="Seleccione un producto:", font=("Roboto", 20)
)
label_producto.pack(pady=10, padx=10, fill="x")

radio_frame = ctk.CTkFrame(frame_inferior)
radio_frame.pack(pady=5, padx=10, fill="x")

image_computadoras = ctk.CTkImage(
    Image.open(os.path.join(current_path, "Imagenes", "computadora.png")),
    size=(100, 70),
)
image_laptops = ctk.CTkImage(
    Image.open(os.path.join(current_path, "Imagenes", "laptop.png")), size=(70, 70)
)
image_tar_video = ctk.CTkImage(
    Image.open(os.path.join(current_path, "Imagenes", "tarvideo.png")), size=(70, 70)
)
image_monitores = ctk.CTkImage(
    Image.open(os.path.join(current_path, "Imagenes", "monitores.png")), size=(100, 80)
)
image_otros = ctk.CTkImage(
    Image.open(os.path.join(current_path, "Imagenes", "otros.png")), size=(70, 70)
)

original_text_color = ""


def on_enter_computadoras(event):
    if appearance_mode_optionemenu.get():
        label_computadoras.configure(text_color="Yellow", underline=True)
    else:
        label_computadoras.configure(text_color="blue", underline=True)


def on_leave_computadoras(event):
    if appearance_mode_optionemenu.get():
        label_computadoras.configure(text_color="white", underline=False)
    else:
        label_computadoras.configure(text_color="black", underline=False)


def on_enter_laptops(event):
    if appearance_mode_optionemenu.get():
        label_laptops.configure(text_color="Yellow", underline=True)
    else:
        label_laptops.configure(text_color="blue", underline=True)


def on_leave_laptops(event):
    if appearance_mode_optionemenu.get():
        label_laptops.configure(text_color="white", underline=False)
    else:
        label_laptops.configure(text_color="black", underline=False)


def on_enter_tar_video(event):
    if appearance_mode_optionemenu.get():
        label_tar_video.configure(text_color="Yellow", underline=True)
    else:
        label_tar_video.configure(text_color="blue", underline=True)


def on_leave_tar_video(event):
    if appearance_mode_optionemenu.get():
        label_tar_video.configure(text_color="white", underline=False)
    else:
        label_tar_video.configure(text_color="black", underline=False)


def on_enter_monitores(event):
    if appearance_mode_optionemenu.get():
        label_monitores.configure(text_color="Yellow", underline=True)
    else:
        label_monitores.configure(text_color="blue", underline=True)


def on_leave_monitores(event):
    if appearance_mode_optionemenu.get():
        label_monitores.configure(text_color="white", underline=False)
    else:
        label_monitores.configure(text_color="black", underline=False)


label_computadoras = ctk.CTkLabel(
    radio_frame,
    text="Computadoras",
    image=image_computadoras,
    compound="top",
    anchor="w",
)
label_computadoras.pack(side="left", padx=23, pady=5)
label_computadoras.bind("<Enter>", on_enter_computadoras)
label_computadoras.bind("<Leave>", on_leave_computadoras)
label_computadoras.bind("<Button-1>", lambda e: show_frame(frame_inferior_computadoras))

label_laptops = ctk.CTkLabel(
    radio_frame, text="Laptops", image=image_laptops, compound="top", anchor="w"
)
label_laptops.pack(side="left", padx=23, pady=5)
label_laptops.bind("<Enter>", on_enter_laptops)
label_laptops.bind("<Leave>", on_leave_laptops)
label_laptops.bind("<Button-1>", lambda e: show_frame(frame_inferior_laptops))

label_tar_video = ctk.CTkLabel(
    radio_frame,
    text="Tarjetas de Video",
    image=image_tar_video,
    compound="top",
    anchor="w",
)
label_tar_video.pack(side="left", padx=23, pady=5)
label_tar_video.bind("<Enter>", on_enter_tar_video)
label_tar_video.bind("<Leave>", on_leave_tar_video)
label_tar_video.bind("<Button-1>", lambda e: show_frame(frame_inferior_tar_video))

label_monitores = ctk.CTkLabel(
    radio_frame, text="Monitores", image=image_monitores, compound="top", anchor="w"
)
label_monitores.pack(side="left", padx=23, pady=5)
label_monitores.bind("<Enter>", on_enter_monitores)
label_monitores.bind("<Leave>", on_leave_monitores)
label_monitores.bind("<Button-1>", lambda e: show_frame(frame_inferior_monitores))


image_back = ctk.CTkImage(
    Image.open(os.path.join(current_path, "Imagenes", "atras.png")), size=(30, 30)
)

frame_inferior_computadoras = ctk.CTkFrame(app)

label_inferior_computadoras = ctk.CTkLabel(
    frame_inferior_computadoras, text="Seleccione un producto:", font=("Roboto", 20)
)
label_inferior_computadoras.pack(pady=10, padx=10, fill="x")
frame_computadoras = ctk.CTkFrame(frame_inferior_computadoras)
frame_computadoras.pack(fill="both", expand=True)
button_back_computadoras = ctk.CTkLabel(
    frame_computadoras, image=image_back, compound="top", text=""
)
button_back_computadoras.pack(side="right", anchor="ne", padx=10, pady=10)
button_back_computadoras.bind("<Button-1>", lambda e: show_frame(frame_inferior))
menu_computadoras = ctk.CTkOptionMenu(
    frame_computadoras,
    dynamic_resizing=False,
    width=200,
    height=40,
    fg_color="grey",
    button_color="grey",
    command=lambda e: show_frame1(frame_inferior_computadoras1),
    values=[
        "Seleccione",
        "Alienware Aurora R8",
        "Alienware Aurora R9",
        "Alienware Aurora Ryzen Edition R10",
        "Alienware Aurora R11",
        "Alienware Aurora R12",
        "Otros",
    ],
)
menu_computadoras.pack(pady=50, padx=10, anchor="center")

frame_inferior_laptops = ctk.CTkFrame(app)

label_inferior_laptops = ctk.CTkLabel(
    frame_inferior_laptops, text="Seleccione un producto:", font=("Roboto", 20)
)
label_inferior_laptops.pack(pady=10, padx=10, fill="x")
frame_laptops = ctk.CTkFrame(frame_inferior_laptops)
frame_laptops.pack(fill="both", expand=True)

button_back_laptops = ctk.CTkLabel(
    frame_laptops, image=image_back, compound="top", text=""
)
button_back_laptops.pack(side="right", anchor="ne", padx=10, pady=10)
button_back_laptops.bind("<Button-1>", lambda e: show_frame(frame_inferior))
menu_laptops = ctk.CTkOptionMenu(
    frame_laptops,
    dynamic_resizing=False,
    width=200,
    height=40,
    fg_color="grey",
    button_color="grey",
    command=lambda e: show_frame1(frame_inferior_laptops1),
    values=[
        "Seleccione",
        "XPS",
        "Vostro",
        "Alienware",
        "G Series",
        "Precision",
        "CromeBooks",
        "Latitude",
        "Inspiron",
        "Otros",
    ],
)
menu_laptops.pack(pady=50, padx=10, anchor="center")

frame_inferior_tar_video = ctk.CTkFrame(app)

label_inferior_tar_video = ctk.CTkLabel(
    frame_inferior_tar_video, text="Seleccione un producto:", font=("Roboto", 20)
)
label_inferior_tar_video.pack(pady=10, padx=10, fill="x")

frame_tar_video = ctk.CTkFrame(frame_inferior_tar_video)
frame_tar_video.pack(fill="both", expand=True)

button_back_tar_video = ctk.CTkLabel(
    frame_tar_video, image=image_back, compound="top", text=""
)
button_back_tar_video.pack(side="right", anchor="ne", padx=10, pady=10)
button_back_tar_video.bind("<Button-1>", lambda e: show_frame(frame_inferior))
menu_tar_video = ctk.CTkOptionMenu(
    frame_tar_video,
    dynamic_resizing=False,
    width=200,
    height=40,
    fg_color="grey",
    button_color="grey",
    command=lambda e: show_frame1(frame_inferior_tar_video1),
    values=[
        "Seleccione",
        "AMD Radeon RX 6600 XT",
        "AMD Radeon RX 6700 XT",
        "AMD Radeon RX 5700",
        "AMD Radeon RX 6800",
        "AMD Radeon RX 5500 XT",
        "Nvidia GTX 1660",
        "Nvidia RTX 3060 Ti",
        "Nvidia RTX 3070",
        "Nvidia RTX 3080",
        "Nvidia RTX 3080 Ti",
        "Nvidia RTX 3090",
        "Otros",
    ],
)
menu_tar_video.pack(pady=50, padx=10, anchor="center")

frame_inferior_monitores = ctk.CTkFrame(app)

label_inferior_monitores = ctk.CTkLabel(
    frame_inferior_monitores, text="Seleccione un producto:", font=("Roboto", 20)
)
label_inferior_monitores.pack(pady=10, padx=10, fill="x")

frame_monitores = ctk.CTkFrame(frame_inferior_monitores)
frame_monitores.pack(fill="both", expand=True)

button_back_monitores = ctk.CTkLabel(
    frame_monitores, image=image_back, compound="top", text=""
)
button_back_monitores.pack(side="right", anchor="ne", padx=10, pady=10)
button_back_monitores.bind("<Button-1>", lambda e: show_frame(frame_inferior))
menu_monitores = ctk.CTkOptionMenu(
    frame_monitores,
    dynamic_resizing=False,
    width=200,
    height=40,
    fg_color="grey",
    button_color="grey",
    command=lambda e: show_frame1(frame_inferior_monitores1),
    values=[
        "Seleccione",
        "ASUS VG248QEASUS ROG Swift",
        "PG279QASUS ROG Swift",
        "PG348QASUS MG278QASUS ROG Swift",
        "PG258QASUS ROG Swift",
        "PG27UQASUS VG278QASUS ROG Strix",
        "XG49VQASUS TUF Gaming",
        "VG27AQASUS ProArt PA32UC",
        "Dell UltraSharp",
        "Dell Alienware Dell Professional",
        "Dell S Series",
        "ASUS ProArt",
        "ASUS Designo",
        "HP EliteDisplay",
        "HP Pavilion",
        "HP Omen",
        "HP ProDisplay",
        "Otros",
    ],
)
menu_monitores.pack(pady=50, padx=10, anchor="center")


frame_inferior_computadoras1 = ctk.CTkFrame(app)


label_inferior_computadoras1 = ctk.CTkLabel(
    frame_inferior_computadoras1, text="Seleccione un error:", font=("Roboto", 20)
)
label_inferior_computadoras1.pack(pady=10, padx=10, fill="x")

frame_computadoras1 = ctk.CTkFrame(frame_inferior_computadoras1)
frame_computadoras1.pack(fill="both", expand=True)

button_back_computadoras1 = ctk.CTkLabel(
    frame_computadoras1, image=image_back, compound="top", text=""
)
button_back_computadoras1.pack(side="right", anchor="ne", padx=10, pady=10)
button_back_computadoras1.bind(
    "<Button-1>", lambda e: show_frame1(frame_inferior_computadoras)
)

entry_problema = None


def crear_label(nombre, texto, x, y):
    global entry_problema

    label = ctk.CTkLabel(
        frame_computadoras1,
        text=texto,
        font=("Roboto", 15),
        fg_color="grey",
        text_color="white",
        corner_radius=7,
        wraplength=80,
        height=70,
        width=80,
    )
    label.place(x=x, y=y)
    label.bind(
        "<Button-1>", lambda e, label=label: seleccionar_label_computadoras(label)
    )
    return label


def seleccionar_label(label):
    global entry_problema

    if label.cget("text") == "Otros":
        if entry_problema is None:
            entry_problema = ctk.CTkEntry(
                frame_computadoras1, font=("Roboto", 15), width=200, height=40
            )
            entry_problema.place(x=300, y=5)
        entry_problema.focus_set()

    else:
        if entry_problema is not None:
            entry_problema.delete(0, "end")


label_opcion1 = crear_label("label_opcion1", "Sistema Operativo", 5, 5)
label_opcion2 = crear_label("label_opcion2", "Bios", 100, 5)
label_opcion3 = crear_label("label_opcion3", "Disco duro / Disco duro sólido", 200, 5)
label_opcion4 = crear_label("label_opcion4", "No puede arrancar", 300, 5)
label_opcion5 = crear_label("label_opcion5", "Dispositivo de conexión", 400, 5)
label_opcion6 = crear_label("label_opcion6", "Monitor", 5, 80)
label_opcion7 = crear_label("label_opcion7", "Internet", 100, 80)
label_opcion8 = crear_label("label_opcion8", "Sonido", 205, 80)
label_opcion9 = crear_label("label_opcion9", "Otros", 300, 80)

frame_inferior_laptops1 = ctk.CTkFrame(app)

label_inferior_laptops1 = ctk.CTkLabel(
    frame_inferior_laptops1, text="Seleccione un producto:", font=("Roboto", 20)
)
label_inferior_laptops1.pack(pady=10, padx=10, fill="x")

frame_laptops1 = ctk.CTkFrame(frame_inferior_laptops1)
frame_laptops1.pack(fill="both", expand=True)

button_back_laptops1 = ctk.CTkLabel(
    frame_laptops1, image=image_back, compound="top", text=""
)
button_back_laptops1.pack(side="right", anchor="ne", padx=10, pady=10)
button_back_laptops1.bind("<Button-1>", lambda e: show_frame1(frame_inferior_laptops))


def crear_label(nombre, texto, x, y):
    label = ctk.CTkLabel(
        frame_laptops1,
        text=texto,
        font=("Roboto", 15),
        fg_color="grey",
        text_color="white",
        corner_radius=7,
        wraplength=80,
        height=70,
        width=80,
    )
    label.place(x=x, y=y)
    label.bind("<Button-1>", lambda e, label=label: seleccionar_label_laptops(label))
    return label


label_opcion1 = crear_label("label_opcion1", "Sistema Operativo", 5, 5)
label_opcion2 = crear_label("label_opcion2", "Bios", 100, 5)
label_opcion3 = crear_label("label_opcion3", "Disco duro / Disco duro sólido", 200, 5)
label_opcion4 = crear_label("label_opcion4", "No puede arrancar", 300, 5)
label_opcion5 = crear_label("label_opcion5", "Dispositivo de conexión", 400, 5)
label_opcion6 = crear_label("label_opcion6", "Monitor", 5, 80)
label_opcion7 = crear_label("label_opcion7", "Internet", 100, 80)
label_opcion8 = crear_label("label_opcion8", "Sonido", 205, 80)
label_opcion9 = crear_label("label_opcion9", "Otros", 300, 80)

frame_inferior_tar_video1 = ctk.CTkFrame(app)

label_inferior_tar_video1 = ctk.CTkLabel(
    frame_inferior_tar_video1, text="Seleccione un producto:", font=("Roboto", 20)
)
label_inferior_tar_video1.pack(pady=10, padx=10, fill="x")

frame_tar_video1 = ctk.CTkFrame(frame_inferior_tar_video1)
frame_tar_video1.pack(fill="both", expand=True)

button_back_tar_video1 = ctk.CTkLabel(
    frame_tar_video1, image=image_back, compound="top", text=""
)
button_back_tar_video1.pack(side="right", anchor="ne", padx=10, pady=10)
button_back_tar_video1.bind(
    "<Button-1>", lambda e: show_frame1(frame_inferior_tar_video)
)


def crear_label(nombre, texto, x, y):
    label = ctk.CTkLabel(
        frame_tar_video1,
        text=texto,
        font=("Roboto", 15),
        fg_color="grey",
        text_color="white",
        corner_radius=7,
        wraplength=80,
        height=70,
        width=80,
    )
    label.place(x=x, y=y)
    label.bind("<Button-1>", lambda e, label=label: seleccionar_label_tar_video(label))
    return label


label_opcion1 = crear_label("label_opcion1", "Controlador", 10, 40)
label_opcion2 = crear_label("label_opcion2", "Ventilador", 120, 40)
label_opcion3 = crear_label("label_opcion3", "Imagen Anormal", 220, 40)
label_opcion4 = crear_label("label_opcion4", "Conexion", 315, 40)
label_opcion5 = crear_label("label_opcion5", "Otros", 410, 40)

frame_inferior_monitores1 = ctk.CTkFrame(app)

label_inferior_monitores1 = ctk.CTkLabel(
    frame_inferior_monitores1, text="Seleccione un producto:", font=("Roboto", 20)
)
label_inferior_monitores1.pack(pady=10, padx=10, fill="x")

frame_monitores1 = ctk.CTkFrame(frame_inferior_monitores1)
frame_monitores1.pack(fill="both", expand=True)

button_back_monitores1 = ctk.CTkLabel(
    frame_monitores1, image=image_back, compound="top", text=""
)
button_back_monitores1.pack(side="right", anchor="ne", padx=10, pady=10)
button_back_monitores1.bind(
    "<Button-1>", lambda e: show_frame1(frame_inferior_monitores)
)


def crear_label(nombre, texto, x, y):
    label = ctk.CTkLabel(
        frame_monitores1,
        text=texto,
        font=("Roboto", 15),
        fg_color="grey",
        text_color="white",
        corner_radius=7,
        wraplength=80,
        height=70,
        width=80,
    )
    label.place(x=x, y=y)
    label.bind("<Button-1>", lambda e, label=label: seleccionar_label_monitores(label))
    return label


label_opcion1 = crear_label("label_opcion1", "Sonido", 5, 5)
label_opcion2 = crear_label("label_opcion2", "Ajustes", 100, 5)
label_opcion3 = crear_label("label_opcion3", "Monitor", 200, 5)
label_opcion4 = crear_label("label_opcion4", "Conexión", 300, 5)
label_opcion5 = crear_label("label_opcion5", "Panel", 400, 5)
label_opcion6 = crear_label("label_opcion6", "Func de Software", 5, 80)
label_opcion7 = crear_label("label_opcion7", "Pixeles", 100, 80)
label_opcion8 = crear_label("label_opcion8", "Garantia", 200, 80)
label_opcion9 = crear_label("label_opcion9", "Otros", 300, 80)


entry_problema = None
ventana_otro_problema = None


def abrir_ventana_otro_problema():
    global ventana_otro_problema, entry_problema, problema, x, y

    ventana_otro_problema = ctk.CTkToplevel(app)
    width = ventana_otro_problema.winfo_screenwidth()
    height = ventana_otro_problema.winfo_screenheight()

    x = (width // 2) - (ventana_otro_problema.winfo_reqwidth() // 2)
    y = (height // 2) - (ventana_otro_problema.winfo_reqheight() // 2)
    ventana_otro_problema.geometry(f"300x200+{x - 150}+{y - 100}")
    ventana_otro_problema.title("Otro problema")
    ventana_otro_problema.resizable(False, False)
    ventana_otro_problema.lift()
    ventana_otro_problema.attributes("-topmost", 1)

    label_ingrese_problema = ctk.CTkLabel(
        ventana_otro_problema, text="Ingrese el problema:", font=("Roboto", 15)
    )
    label_ingrese_problema.pack(pady=(20, 10))

    entry_problema = ctk.CTkEntry(
        ventana_otro_problema, font=("Roboto", 15), width=200, height=40
    )
    entry_problema.pack()

    boton_guardar = ctk.CTkButton(
        ventana_otro_problema,
        text="Guardar",
        font=("Roboto", 15),
        command=actualizar_problema,
    )
    boton_guardar.pack(pady=(10, 20))


def actualizar_problema():
    global producto, problema, modelo, nombres, n_telefonico, email, tecnico_asignado, fecha_creacion, fecha_ultima_mod, estado, ultimo_id, comentario_tecnico
    ID = ultimo_id
    problema = entry_problema.get()
    guardar_informacion(
        ID,
        producto,
        modelo,
        problema,
        nombres,
        n_telefonico,
        email,
        tecnico_asignado,
        fecha_creacion,
        fecha_ultima_mod,
        estado,
        comentario_tecnico,
    )


def error_frame(texto):
    error_dialog = ctk.CTkToplevel()
    error_dialog.geometry(f"+{x - 150}+{y}")
    error_dialog.resizable(False, False)
    error_dialog.lift()
    error_dialog.attributes("-topmost", 1)
    error_dialog.title("Error")
    error_label = ctk.CTkLabel(error_dialog, image=error_image, text="")
    error_label.pack(padx=10, pady=10)
    error_label = ctk.CTkLabel(error_dialog, text=texto, font=("Roboto", 12))
    error_label.pack(padx=10)
    error_dialog.grab_set()
    error_dialog.wait_window()


def guardar_informacion(
    ID,
    producto,
    modelo,
    problema,
    nombres,
    n_telefonico,
    email,
    tecnico_asignado,
    fecha_creacion,
    fecha_ultima_mod,
    estado,
    comentario_tecnico,
):
    global ultimo_id
    if nombres == "":

        error_frame("Campos vacios, Ingrese un nombre valido")
    elif n_telefonico == "":
        error_frame("Campos vacios, Ingrese un numero telefonico valido")
    elif email == "":
        error_frame("Campos vacios, Ingrese un correo electronico valido")
    elif not validate_email(email):
        error_frame("Correo electronico incorrecto")
    elif tecnico_asignado == "Seleccione":
        error_frame("Campapos vacios, seleccione un tecnico")
    elif not n_telefonico or (len(n_telefonico) < 9 or len(n_telefonico) > 10):
        error_frame("Teléfono incorrecto")
    elif n_telefonico[0] != "0" and len(n_telefonico) == 9:
        n_telefonico = "02" + n_telefonico[1:]
    elif len(n_telefonico) == 10 and n_telefonico[:2] != "09":
        error_frame("Teléfono incorrecto")
    else:
        with open("informacion.csv", "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(
                [
                    ID,
                    producto,
                    modelo,
                    problema,
                    nombres,
                    n_telefonico,
                    email,
                    tecnico_asignado,
                    fecha_creacion,
                    fecha_ultima_mod,
                    estado,
                    comentario_tecnico,
                ]
            )
        ultimo_id += 1
        app.destroy()


def seleccionar_label_computadoras(label):
    global producto, problema, modelo, nombres, n_telefonico, email, tecnico_asignado, fecha_creacion, fecha_ultima_mod, estado, ultimo_id, comentario_tecnico
    if label.cget("text") == "Otros":
        if entry_problema is None:

            ID = ultimo_id
            nombres = entry_nombre.get()
            n_telefonico = entry_n_telefonico.get()
            email = entry_email.get()
            tecnico_asignado = option_t_asignado.get()
            modelo = menu_computadoras.get()
            producto = label_computadoras.cget("text")
            modelo = menu_computadoras.get()
            producto = label_computadoras.cget("text")
            fecha_creacion = datetime.datetime.now().strftime("%Y-%m-%d")
            fecha_ultima_mod = datetime.datetime.now().strftime("%Y-%m-%d")
            estado = "Activo"
            comentario_tecnico = "-"
            abrir_ventana_otro_problema()

    else:

        ID = ultimo_id
        nombres = entry_nombre.get()
        n_telefonico = entry_n_telefonico.get()
        email = entry_email.get()
        tecnico_asignado = option_t_asignado.get()
        modelo = menu_computadoras.get()
        producto = label_computadoras.cget("text")
        fecha_creacion = datetime.datetime.now().strftime("%Y-%m-%d")
        fecha_ultima_mod = datetime.datetime.now().strftime("%Y-%m-%d")
        estado = "Activo"
        comentario_tecnico = "-"
        problema = label.cget("text")
        guardar_informacion(
            ID,
            producto,
            modelo,
            problema,
            nombres,
            n_telefonico,
            email,
            tecnico_asignado,
            fecha_creacion,
            fecha_ultima_mod,
            estado,
            comentario_tecnico,
        )


def seleccionar_label_laptops(label):
    global producto, problema, modelo, nombres, n_telefonico, email, tecnico_asignado, fecha_creacion, fecha_ultima_mod, estado, ultimo_id, comentario_tecnico
    if label.cget("text") == "Otros":
        if entry_problema is None:
            ID = ultimo_id
            nombres = entry_nombre.get()
            n_telefonico = entry_n_telefonico.get()
            email = entry_email.get()
            tecnico_asignado = option_t_asignado.get()
            modelo = menu_laptops.get()
            producto = label_laptops.cget("text")
            fecha_creacion = datetime.datetime.now().strftime("%Y-%m-%d")
            fecha_ultima_mod = datetime.datetime.now().strftime("%Y-%m-%d")
            estado = "Activo"
            comentario_tecnico = "-"
            abrir_ventana_otro_problema()
    else:

        ID = ultimo_id
        nombres = entry_nombre.get()
        n_telefonico = entry_n_telefonico.get()
        email = entry_email.get()
        tecnico_asignado = option_t_asignado.get()
        modelo = menu_laptops.get()
        producto = label_laptops.cget("text")
        problema = label.cget("text")
        fecha_creacion = datetime.datetime.now().strftime("%Y-%m-%d")
        fecha_ultima_mod = datetime.datetime.now().strftime("%Y-%m-%d")
        estado = "Activo"
        comentario_tecnico = "-"
        guardar_informacion(
            ID,
            producto,
            modelo,
            problema,
            nombres,
            n_telefonico,
            email,
            tecnico_asignado,
            fecha_creacion,
            fecha_ultima_mod,
            estado,
            comentario_tecnico,
        )


def seleccionar_label_tar_video(label):
    global producto, problema, modelo, nombres, n_telefonico, email, tecnico_asignado, fecha_creacion, fecha_ultima_mod, estado, ultimo_id, comentario_tecnico
    if label.cget("text") == "Otros":
        if entry_problema is None:
            ID = ultimo_id
            nombres = entry_nombre.get()
            n_telefonico = entry_n_telefonico.get()
            email = entry_email.get()
            tecnico_asignado = option_t_asignado.get()
            modelo = menu_tar_video.get()
            producto = label_tar_video.cget("text")
            fecha_creacion = datetime.datetime.now().strftime("%Y-%m-%d")
            fecha_ultima_mod = datetime.datetime.now().strftime("%Y-%m-%d")
            estado = "Activo"
            comentario_tecnico = "-"
            abrir_ventana_otro_problema()
    else:

        ID = ultimo_id
        nombres = entry_nombre.get()
        n_telefonico = entry_n_telefonico.get()
        email = entry_email.get()
        tecnico_asignado = option_t_asignado.get()
        modelo = menu_tar_video.get()
        producto = label_tar_video.cget("text")
        problema = label.cget("text")
        fecha_creacion = datetime.datetime.now().strftime("%Y-%m-%d")
        fecha_ultima_mod = datetime.datetime.now().strftime("%Y-%m-%d")
        estado = "Activo"
        comentario_tecnico = "-"
        guardar_informacion(
            ID,
            producto,
            modelo,
            problema,
            nombres,
            n_telefonico,
            email,
            tecnico_asignado,
            fecha_creacion,
            fecha_ultima_mod,
            estado,
            comentario_tecnico,
        )


def seleccionar_label_monitores(label):
    global producto, problema, modelo, nombres, n_telefonico, email, tecnico_asignado, fecha_creacion, fecha_ultima_mod, estado, ultimo_id, comentario_tecnico
    if label.cget("text") == "Otros":
        if entry_problema is None:
            ID = ultimo_id
            nombres = entry_nombre.get()
            n_telefonico = entry_n_telefonico.get()
            email = entry_email.get()
            tecnico_asignado = option_t_asignado.get()
            modelo = menu_monitores.get()
            producto = label_monitores.cget("text")
            fecha_creacion = datetime.datetime.now().strftime("%Y-%m-%d")
            fecha_ultima_mod = datetime.datetime.now().strftime("%Y-%m-%d")
            estado = "Activo"
            comentario_tecnico = "-"
            abrir_ventana_otro_problema()
    else:

        ID = ultimo_id
        nombres = entry_nombre.get()
        n_telefonico = entry_n_telefonico.get()
        email = entry_email.get()
        tecnico_asignado = option_t_asignado.get()
        modelo = menu_monitores.get()
        producto = label_monitores.cget("text")
        problema = label.cget("text")
        fecha_creacion = datetime.datetime.now().strftime("%Y-%m-%d")
        fecha_ultima_mod = datetime.datetime.now().strftime("%Y-%m-%d")
        estado = "Activo"
        comentario_tecnico = "-"
        guardar_informacion(
            ID,
            producto,
            modelo,
            problema,
            nombres,
            n_telefonico,
            email,
            tecnico_asignado,
            fecha_creacion,
            fecha_ultima_mod,
            estado,
            comentario_tecnico,
        )


app.mainloop()
