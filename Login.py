import customtkinter, time, cargar_archivos, sys, smtplib, uuid
from PIL import Image
import os, subprocess
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

last_incorrect_time = {}
incorrect_usernames = {}
logged_in_tech_id = None
username = None
contra = None
error_label = None
root = None


def main():
    global username, contra, error_label, root, last_incorrect_time, incorrect_usernames, logged_in_tech_id
    customtkinter.set_appearance_mode("System")
    customtkinter.set_default_color_theme("green")
    width = 700
    height = 400

    root = customtkinter.CTk()
    root.title("Pantalla de Login")

    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenwidth() // 3) - ((width + 500) // 3)
    root.geometry("{}x{}+{}+{}".format(width, height, x, y))
    root.resizable(False, False)

    current_path = os.path.dirname(os.path.realpath(__file__))
    root.iconbitmap(os.path.join(current_path, "Imagenes", "key.ico"))
    bg_image = customtkinter.CTkImage(
        Image.open(os.path.join(current_path, "Imagenes", "Fondo.jpg")),
        size=(width, height),
    )

    application_logo = customtkinter.CTkImage(
        Image.open(os.path.join(current_path, "Imagenes", "Logo.png")), size=(50, 50)
    )
    user_image = customtkinter.CTkImage(
        Image.open(os.path.join(current_path, "Imagenes", "User.png")), size=(80, 100)
    )

    login_btn_image = customtkinter.CTkImage(
        Image.open(os.path.join(current_path, "Imagenes", "Enter.png")), size=(25, 28)
    )

    bg_image_label = customtkinter.CTkLabel(root, image=bg_image, text="")
    bg_image_label.grid(row=0, column=0, padx=(0, 170), pady=(0, 70))

    logo = customtkinter.CTkLabel(
        root, text="", image=application_logo, fg_color="#012c56", bg_color="#012c56"
    )
    logo.grid(row=0, column=0, padx=(0, 250), pady=(0, 400))

    logo_text = customtkinter.CTkLabel(
        root,
        text="ServiSoft",
        text_color="white",
        font=("Roboto bold", 25),
        fg_color="#012c56",
        bg_color="#f6f6f6",
    )
    logo_text.grid(row=0, column=0, padx=(0, 80), pady=(0, 400))

    user_image_label = customtkinter.CTkLabel(
        root,
        text="",
        image=user_image,
        anchor="n",
        compound="top",
        fg_color="#012c56",
        bg_color="#012c56",
        corner_radius=10,
    )
    user_image_label.grid(row=0, column=0, padx=(0, 600), pady=(0, 300))

    username = customtkinter.CTkEntry(
        root,
        placeholder_text="Usuario",
        placeholder_text_color="#000000",
        text_color="#000000",
        border_width=0,
        corner_radius=7,
        width=200,
        height=35,
        bg_color="#012c56",
        fg_color="#f6f6f6",
    )
    username.grid(row=0, column=0, padx=(0, 600), pady=(0, 100))

    contra = customtkinter.CTkEntry(
        root,
        placeholder_text="Contraseña",
        placeholder_text_color="#000000",
        text_color="#000000",
        border_width=0,
        corner_radius=7,
        width=200,
        height=35,
        bg_color="#012c56",
        fg_color="#f6f6f6",
        show="*",
    )
    contra.grid(row=0, column=0, padx=(0, 600), pady=(100, 100))
    contra.bind("<Return>", lambda e: handle_login())

    login_btn = customtkinter.CTkButton(
        root,
        text="Iniciar Sesión",
        width=200,
        height=30,
        bg_color="#012c56",
        corner_radius=7,
        font=("Roboto", 20),
        compound="right",
        image=login_btn_image,
        hover_color="#660000",
        command=handle_login,
    )
    login_btn.grid(row=0, column=0, padx=(0, 600), pady=(220, 100))

    def on_enter_contra_olvidada(event):
        contra_olvidada.configure(text_color="Yellow", underline=True)

    def on_leave_contra_olvidada(event):
        contra_olvidada.configure(text_color="white", underline=False)

    def envio_contra_olvidada(user):
        global username, error_label

        username_text = username.get()

        user_data = cargar_archivos.load_user_data()

        if username_text in user_data:
            temp_password = str(uuid.uuid4())[:8]

            user_data[username_text]["password"] = temp_password
            cargar_archivos.save_user_data(user_data)

            sender_email = "pruebascorreopython96@gmail.com"
            sender_password = "pfsy lufv gmaj euvd"
            recipient_email = user_data[username_text]["Correo"]

            message = MIMEMultipart()
            message["From"] = sender_email
            message["To"] = recipient_email
            message["Subject"] = "Restablecimiento de contraseña"
            message.attach(
                MIMEText(
                    f"Hola {username_text},\n\nSe ha restablecido tu contraseña temporalmente a: {temp_password}\n\nPor favor, inicia sesión con esta contraseña y cambia tu contraseña en la sección de configuración.\n\nSaludos.",
                    "plain",
                )
            )

            try:
                server = smtplib.SMTP("smtp.gmail.com", 587)
                server.starttls()
                server.login(sender_email, sender_password)
                text = message.as_string()
                server.sendmail(sender_email, recipient_email, text)
                server.quit()
                error_label.configure(
                    text="Se ha enviado un correo con la contraseña temporal."
                )
            except Exception as e:
                error_label.configure(text=f"Error al enviar el correo: {e}")
        else:
            error_label.configure(text="Usuario no encontrado. Inténtelo de nuevo.")

    contra_olvidada = customtkinter.CTkLabel(
        root,
        text="Recuperar Contraseña",
        justify="center",
        bg_color="#011128",
        text_color="#ffffff",
    )
    contra_olvidada.grid(row=0, column=0, padx=(0, 675), pady=(320, 100))
    contra_olvidada.bind("<Enter>", on_enter_contra_olvidada)
    contra_olvidada.bind("<Leave>", on_leave_contra_olvidada)
    contra_olvidada.bind(
        "<Button-1>", lambda e, user=username: envio_contra_olvidada(user)
    )

    error_label = customtkinter.CTkLabel(
        root, text="", justify="center", bg_color="#012c56", text_color="#ffffff"
    )
    error_label.grid(row=0, column=0, padx=(0, 100), pady=(0, 200))
    root.mainloop()


def handle_login():
    global username, contra, error_label, root, last_incorrect_time, incorrect_usernames, logged_in_tech_id
    username_text = username.get()
    password_text = contra.get()

    user_data = cargar_archivos.load_user_data()

    if username_text == "":
        error_label.configure(text="El usuario no puede estar vacio.")
    elif "=" in username_text or "open" in username_text:
        error_label.configure(text="El usuaro contiene caracteres invalidos.")
    elif password_text == "":
        error_label.configure(text="La contraseña no puede estar vacia.")
    else:
        if username_text in user_data:
            if (
                username_text in last_incorrect_time
                and incorrect_usernames[username_text] >= 3
            ):
                remaining_time = 5 * 60 - (
                    time.time() - last_incorrect_time[username_text]
                )
                if remaining_time > 0:
                    minutes, seconds = divmod(remaining_time, 60)
                    error_label.configure(
                        text=f"""
    El sistema se ha bloqueado temporalmente.
    Por favor, inténtelo de nuevo en {minutes:.0f}:{int(seconds):02d}.
    """
                    )
                    return
                else:
                    last_incorrect_time[username_text] = 0
                    incorrect_usernames[username_text] = 0

            user_data_password = user_data[username_text]["password"]
            if (
                isinstance(user_data_password, str)
                and user_data_password == password_text
            ):
                incorrect_usernames.clear()
                if user_data[username_text]["Rango"] == "Administrador":
                    logged_in_tech_id = user_data[username_text]["username"]
                    root.destroy()
                    try:
                        subprocess.run(
                            [
                                "python",
                                "ventana_incidencias_admin.py",
                                logged_in_tech_id,
                            ],
                            check=True,
                        )
                    except subprocess.CalledProcessError as e:
                        print(f"Error al ejecutar el archivo: {e}")
                elif user_data[username_text]["Rango"] == "Tecnico":
                    logged_in_tech_id = user_data[username_text]["username"]
                    root.destroy()
                    try:
                        subprocess.run(
                            [
                                "python",
                                "ventana_incidencias_tecnico.py",
                                logged_in_tech_id,
                            ],
                            check=True,
                        )
                    except subprocess.CalledProcessError as e:
                        print(f"Error al ejecutar el archivo: {e}")
                elif user_data[username_text]["Rango"] == "Agente":
                    logged_in_tech_id = user_data[username_text]["username"]
                    root.destroy()
                    try:
                        subprocess.run(
                            [
                                "python",
                                "ventana_incidencias_agente.py",
                                logged_in_tech_id,
                            ],
                            check=True,
                        )
                    except subprocess.CalledProcessError as e:
                        print(f"Error al ejecutar el archivo: {e}")
            else:
                incorrect_usernames[username_text] = (
                    incorrect_usernames.get(username_text, 0) + 1
                )
                last_incorrect_time[username_text] = time.time()
                error_label.configure(
                    text="""
                                    Contraseña incorrecta, se bloqueara al 3 intento incorrecto.
                                    Numero intentos incorrectos {}.
                                    """.format(
                        incorrect_usernames[username_text]
                    )
                )
        else:
            error_label.configure(text="Usuario no encontrado. Inténtelo de nuevo.")


if __name__ == "__main__":
    main()
else:
    pass
