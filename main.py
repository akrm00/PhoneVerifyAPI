import threading
import customtkinter
import requests

api_key = ''
number_count = 0
total_numbers = 0
valid_numbers_count = 0 


with open("output.txt","w") as file:
    pass

def update_api_key():
    global api_key
    api_key = entry.get()
    label.configure(text=f"Clé API mise à jour : {api_key}")

def verify_phone_number(number):
    global number_count, valid_numbers_count
    if not api_key:
        return {'valid': False, 'message': 'API key is not set'}
    try:
        url = f"http://apilayer.net/api/validate?access_key={api_key}&number={number}"
        response = requests.get(url)
        number_count += 1
        if response.json()['valid']:
            valid_numbers_count += 1  
        return response.json()
    except requests.RequestException as e:
        return {'valid': False, 'message': str(e)}

def process_phone_numbers(input_file, output_file):
    global total_numbers
    with open(input_file, 'r') as file:
        numbers = file.readlines()
    total_numbers = len(numbers)
    valid_numbers = []
    for number in numbers:
        number = number.strip()
        result = verify_phone_number(number)
        if result['valid']:
            valid_numbers.append(number + '\n')
    with open(output_file, 'w') as file:
        file.writelines(valid_numbers)
    displayNumbers()

def displayNumbers():
    with open("output.txt", "r") as file:
        numbers_content = file.read()
    textBox.delete(1.0, "end")
    textBox.insert("end", numbers_content)

def start_verification_thread():
    global number_count, valid_numbers_count
    number_count = 0
    valid_numbers_count = 0
    textBox.delete(1.0, "end") 
    thread = threading.Thread(target=lambda: process_phone_numbers("input.txt", "output.txt"))
    thread.start()
    update_counter()

def update_counter():
    counter_label.configure(text=f"Numéros vérifiés : {number_count}/{total_numbers}    |     HITS: {valid_numbers_count}")
    if threading.active_count() > 1:
        root.after(100, update_counter)  # Mise à jour toutes les 100 ms

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")
root = customtkinter.CTk()
root.title("VerifyTool by Ramka00")
root.geometry("900x580")
root.resizable(False, False)

frame1 = customtkinter.CTkFrame(master=root, width=300)
frame1.pack(side="left", fill="y", expand=False)

frame2 = customtkinter.CTkFrame(master=root)
frame2.pack(side="right", fill="both", expand=True)

entry = customtkinter.CTkEntry(master=frame1, width=200)
entry.pack(pady=20)

buttonApi = customtkinter.CTkButton(master=frame1, text="APPLY", font=("Roboto", 15, "bold"), width=200, command=update_api_key)
buttonApi.pack(pady=10)

label = customtkinter.CTkLabel(master=frame1, text="Entrez une clé API", wraplength=200)
label.pack(pady=20)

textBox = customtkinter.CTkTextbox(master=frame2)
textBox.pack(pady=20, padx=20, fill='both', expand=True)

counter_label = customtkinter.CTkLabel(master=frame2, text="Numéros vérifiés : 0/0 | HITS: 0")
counter_label.pack(pady=10)

button_Frame = customtkinter.CTkFrame(master=frame2)
button_Frame.pack(fill="x", padx=20, pady=20)

buttonStart = customtkinter.CTkButton(master=button_Frame, text="START", font=("Roboto", 24, "bold"), width=800, command=start_verification_thread)
buttonStart.pack(side="right")

root.mainloop()
