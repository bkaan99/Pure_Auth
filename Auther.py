import json
import sys
import time
import pyotp
import qrcode
from colorama import Fore, Back, Style

secret_key = "GlobalSecretKey"
user_name = "None"
issuer_name = "None"
is_authenticated = False


def generate_qr_code(user_name, issuer_name):
    try:
        uri = pyotp.totp.TOTP(secret_key).provisioning_uri(name=user_name, issuer_name=issuer_name)
        img = qrcode.make(uri)
        global user_selected_file_name
        user_selected_file_name = input("Dosya adını girin: ")
        file_name = f"{user_selected_file_name}.png"
        img.save(file_name)
        print(
            "QR kod oluşturuldu ve " + Fore.LIGHTYELLOW_EX + f"({user_selected_file_name}.png)" + Fore.RESET + " adında kaydedilecek." + "\n")

    except:
        print("QR kod oluşturulurken bir hata oluştu.")


def verify_code(verification_code):
    otp = pyotp.TOTP(secret_key)
    is_code_valid = otp.verify(verification_code)
    if is_code_valid:
        print( "\n" + "Doğrulama Kodu Geçerli")
    else:
        print("Doğrulama Kodu Geçersiz")


def change_secret_key():
    global secret_key
    secret_key = input("Yeni gizli anahtarı girin: ")
    print(secret_key)


def change_qr_settings():
    try :
        global user_name
        global issuer_name
        user_name = input("Kullanıcı adınızı girin: ")
        issuer_name = input("Oluşturucu adını girin: ")
        generate_qr_code(user_name, issuer_name)
    except:
        print("QR kod oluşturulurken bir hata oluştu.")


def write_secret_key():
    data = {}
    data['secret_key'] = secret_key
    data[('user_name')] = user_name
    data[('issuer_name')] = issuer_name
    data[('time')] = time.asctime(time.localtime(time.time()))

    with open(f'{user_selected_file_name}.json', 'w', encoding='utf8') as outfile:
        json.dump(data, outfile, ensure_ascii=False, indent=4)

    print("Gizli anahtarınız " + Fore.LIGHTYELLOW_EX + f"({user_selected_file_name}.json)" + Fore.RESET + " adında kaydedilecektir." + "\n")

def authenticate_user(valid_username, valid_password):
    print("Lütfen kimlik doğrulama bilgilerinizi girin:")
    username = input("Kullanıcı adı: ")
    password = input("Şifre: ")

    if username == valid_username and password == valid_password:
        print("Kullanıcı doğrulandı.")
        return True
    else:
        print("Kullanıcı adı veya şifre yanlış. Program sonlandırılıyor.")
        return False

def close_program():
    print("Program sonlandırılıyor.")
    sys.exit()

is_running = True
while is_running:
    print(
        Fore.LIGHTBLUE_EX + "\n" + "Aşağıdaki seçeneklerden birini seçin: (Sayıları seçerek ilerleyebilirisinz)" + "\n" + "\n" + Fore.RESET +
        Fore.YELLOW + "1. QR kod oluşturmak" + "\n"
        + "2. Doğrulama yapmak" + "\n"
        + Fore.LIGHTRED_EX + "exit. Çıkış yapmak" + "\n"
        + Fore.RESET + Fore.LIGHTBLUE_EX)

    user_choice = input("Yapmak istediğiniz işlemi seçiniz : " + Fore.RESET).lower()

    if user_choice == "1":

        qr_code_choice = ""
        while qr_code_choice not in ["yes", "no" , "exit"]:
            qr_code_choice = input(
                "\n" + Fore.LIGHTBLUE_EX + "QR Kodunu özelleştirmek ister misiniz ? (yes/no) " + Fore.RESET).lower()
            if qr_code_choice not in ["yes", "no", "exit"]:
                print("Geçersiz seçenek. 'yes' veya 'no' olarak cevap verin.")

        if qr_code_choice == "yes":
            change_qr_settings()
        elif qr_code_choice == "no":
            print(
                "\n" + "QR'a ait user_name:" + Fore.MAGENTA + f" {user_name}" + Fore.RESET + "\n" + "QR'a ait issuer_name:" + Fore.MAGENTA + f" {issuer_name}" + Fore.RESET + "\n" + "isimlendirmeleri ile oluşturuldu." + "\n")
            generate_qr_code(user_name, issuer_name)
        elif qr_code_choice == "exit":
            close_program()

        secret_key_choice = ""
        while secret_key_choice not in ["yes", "no" , "exit"]:
            secret_key_choice = input(Fore.LIGHTBLUE_EX +"Gizli anahtarınızı değiştirmek ister misiniz? (yes/no):  " + Fore.RESET).lower()
            if secret_key_choice not in ["yes", "no" , "exit"]:
                print("Geçersiz seçenek. 'yes' veya 'no' olarak cevap verin.")

        if secret_key_choice == "yes":
            change_secret_key()
        elif secret_key_choice == "no":
            print("\n" + "Gizli anahtarınız değiştirilmedi." + "\n" + "Gizli anahtarınız: " + f"({secret_key})" + "\n")
        elif secret_key_choice == "exit":
            close_program()

        write_secret_key()

        verify_choice = ""
        while verify_choice not in ["yes", "no" , "exit"]:
            verify_choice = input(Fore.LIGHTBLUE_EX + "Doğrulama yapmak ister misiniz? (yes/no): " + Fore.RESET).lower()
            if verify_choice not in ["yes", "no" , "exit"]:
                print("Geçersiz seçenek. 'yes' veya 'no' olarak cevap verin.")

        if verify_choice == "yes":
            verification_code = input("Google Authenticator'dan gelen 6 haneli doğrulama kodunu girin: ")
            verify_code(verification_code)
        elif verify_choice == "no":
            print("Program sonlandırıldı.")
            close_program()
        elif verify_choice == "exit":
            close_program()

    elif user_choice == "2":
        while not is_authenticated:
            is_authenticated = authenticate_user("admin", "admin")
            if is_authenticated:
                verification_code = input("Google Authenticator'dan gelen 6 haneli doğrulama kodunu girin: ")
                verify_code(verification_code)
            else :
                break

    elif user_choice == "exit":
        close_program()

    else:
        print("Geçersiz seçenek. 'yes' veya 'no' olarak cevap verin.")
