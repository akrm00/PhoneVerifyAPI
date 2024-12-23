import threading
import customtkinter
import requests
from tkinter import filedialog

api_key = ''
number_count = 0
total_numbers = 0
valid_numbers_count = 0 
input_file_path = "input.txt"

with open("output.txt","w") as file:
    pass

def update_api_key():
    global api_key
    api_key = entry.get()
    label.configure(text="API Key Updated")

def verify_phone_number(number):
    global number_count, valid_numbers_count
    if not api_key:
        return {'valid': False, 'message': 'API key is not set'}
    try:
        url = f"http://apilayer.net/api/validate?access_key={api_key}&number={number}"
        response = requests.get(url)
        number_count += 1
        response_json = response.json()
        if 'valid' in response_json:
            if response_json['valid']:
                valid_numbers_count += 1  
            return response_json
        else:
            return {'valid': False, 'message': 'Unexpected API response: ' + str(response_json)}
        
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

def load_file():
    global total_numbers, input_file_path
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if file_path:
        input_file_path = file_path
        with open(file_path, 'r') as file:
            numbers = file.readlines()
            total_numbers = len(numbers)
            counter_label.configure(text=f"Verified numbers : 0/{total_numbers} | HITS: 0")
            file_label.configure(text=f"loaded file : {file_path.split('/')[-1]}")

def start_verification_thread():
    global number_count, valid_numbers_count
    number_count = 0
    valid_numbers_count = 0
    textBox.delete(1.0, "end") 
    thread = threading.Thread(target=lambda: process_phone_numbers(input_file_path, "output.txt"))
    thread.start()
    update_counter()

def update_counter():
    counter_label.configure(text=f"Verified numbers : {number_count}/{total_numbers}    |     HITS: {valid_numbers_count}")
    if threading.active_count() > 1:
        root.after(100, update_counter)

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")
root = customtkinter.CTk()
root.title("PhoneVerifyAPI by akramway00")
root.geometry("900x580")
root.resizable(False, False)

root.iconbitmap("icon.ico")

frame1 = customtkinter.CTkFrame(master=root, width=300, fg_color="#1a1b1b")
frame1.pack(side="left", fill="y", expand=False, padx=20, pady=20)

frame2 = customtkinter.CTkFrame(master=root)
frame2.pack(side="right", fill="both", expand=True)

label = customtkinter.CTkLabel(master=frame1, text="Enter an API Key", wraplength=200, font=("Segoe UI", 15, "bold"))
label.pack(pady=(0, 10))

entry = customtkinter.CTkEntry(master=frame1, width=200)
entry.pack(pady=(0, 10))

buttonApi = customtkinter.CTkButton(master=frame1, text="APPLY", font=("Segoe UI", 15, "bold"), width=200, command=update_api_key)
buttonApi.pack(pady=(0, 10))

buttonLoad = customtkinter.CTkButton(master=frame1, text="LOAD FILE", font=("Segoe UI", 15, "bold"), width=200, command=load_file)
buttonLoad.pack(pady=(0, 10))

file_label = customtkinter.CTkLabel(master=frame1, text="No files loaded", wraplength=200, font=("Segoe UI", 15))
file_label.pack(pady=(0, 20))

textBox = customtkinter.CTkTextbox(master=frame2)
textBox.pack(pady=20, padx=20, fill='both', expand=True)

counter_label = customtkinter.CTkLabel(master=frame2, text="Verified numbers : 0/0 | HITS: 0")
counter_label.pack(pady=10)

button_Frame = customtkinter.CTkFrame(master=frame2)
button_Frame.pack(fill="x", padx=20, pady=20)

buttonStart = customtkinter.CTkButton(master=button_Frame, text="START", font=("Segoe UI", 24, "bold"), width=800, command=start_verification_thread)
buttonStart.pack(side="right")

root.mainloop()