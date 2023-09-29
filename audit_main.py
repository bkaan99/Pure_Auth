import json
import os
import sys
import time
import cv2
import pyotp
import qrcode
from colorama import Fore
from unidecode import unidecode


max_invalid_attempts = 3  # Maksimum hatalı giriş sayısı
invalid_attempt_count = 0
def generate_qr_code(user_name, issuer_name, selected_secret_key):
    try:
        uri = pyotp.totp.TOTP(selected_secret_key).provisioning_uri(name=user_name, issuer_name=issuer_name)
        img = qrcode.make(uri)
        global user_selected_file_name
        user_selected_file_name = input("Dosya adını girin: ")
        file_name = f"{user_selected_file_name}.png"
        img.save(file_name)
        print(
            "QR kod oluşturuldu ve " + Fore.LIGHTYELLOW_EX + f"({user_selected_file_name}.png)" + Fore.RESET + " adında kaydedilecek." + "\n")

    except:
        print("QR kod oluşturulurken bir hata oluştu.")


def verify_code(verification_code,readed_secret_key):
    otp = pyotp.TOTP(readed_secret_key)
    is_code_valid = otp.verify(verification_code)
    if is_code_valid:
        print( "\n" + "Doğrulama Kodu Geçerli")
    else:
        print("Doğrulama Kodu Geçersiz")


def change_secret_key():
    global selected_secret_key
    selected_secret_key = unidecode(input("Yeni gizli anahtarı girin: "))
    print(selected_secret_key)
    return selected_secret_key


def change_qr_settings():
    try :
        global user_name
        global issuer_name
        user_name = unidecode(input("Kullanıcı adınızı girin: "))
        issuer_name = unidecode(input("Oluşturucu adını girin: "))
        change_secret_key()
        generate_qr_code(user_name, issuer_name, selected_secret_key)
    except:
        print("QR kod oluşturulurken bir hata oluştu.")


def write_secret_key():
    data = {'secret_key': selected_secret_key,
            ('user_name'): user_name,
            ('issuer_name'): issuer_name,
            ('time'): time.asctime(time.localtime(time.time()))}

    with open(f'{user_selected_file_name}.json', 'w', encoding='utf8') as outfile:
        json.dump(data, outfile, ensure_ascii=False, indent=4)

    print("Gizli anahtarınız " + Fore.LIGHTYELLOW_EX + f"({user_selected_file_name}.json)" + Fore.RESET + " adında kaydedilecektir." + "\n")

def authenticate_user(valid_username, valid_password):
    print("\n"+ "\n"+ "\n"+ Fore.LIGHTMAGENTA_EX + "Lütfen kimlik doğrulama bilgilerinizi girin:" + Fore.RESET)
    username = input("Kullanıcı adı: ")
    password = input("Şifre: ")

    if username == valid_username and password == valid_password:
        print("\n"+ Fore.LIGHTGREEN_EX  +"Kullanıcı doğrulandı." + Fore.RESET)
        return True
    else:
        print("Kullanıcı adı veya şifre yanlış. Program sonlandırılıyor.")
        close_program()

def close_program():
    print("Program sonlandırılıyor.")
    sys.exit()

def read_secret_key_from_json():

    user_selected_json_file = input(Fore.LIGHTBLUE_EX + "Okunacak json dosyasının adını girin: " + Fore.RESET)
    if os.path.isfile(f'{user_selected_json_file}.json'):
        print("\n" + Fore.LIGHTGREEN_EX +  f"{user_selected_json_file}.json " + Fore.RESET + "isimli dosya bulundu.")
        with open(f'{user_selected_json_file}.json', 'r', encoding='utf8') as json_file:
            data = json.load(json_file)
            global readed_secret_key
            readed_secret_key = data['secret_key']
            readed_user_name = data['user_name']
            readed_issuer_name = data['issuer_name']
            readed_time = data['time']
            print("\n" + "Gizli anahtarınız: " + Fore.LIGHTYELLOW_EX + f"{readed_secret_key}" + Fore.RESET)
            print("Kullanıcı adınız: " + Fore.LIGHTYELLOW_EX + f"{readed_user_name}" + Fore.RESET)
            print("Oluşturucu adınız: " + Fore.LIGHTYELLOW_EX + f"{readed_issuer_name}" + Fore.RESET)
            print("Oluşturulma zamanı: " + Fore.LIGHTYELLOW_EX + f"{readed_time}" + Fore.RESET + "\n")
            print("Gizli anahtarınız " + Fore.LIGHTYELLOW_EX + f"({user_selected_json_file}.json)" + Fore.RESET + " adlı dosyadan okundu." + "\n")

    else:
        print(Fore.LIGHTRED_EX + "\n" + "\n" +"Dosya bulunamadı." + Fore.RESET)
        close_program()

def decode_qr_code(image):

  qr_code = cv2.QRCodeDetector()
  data, _, _ = qr_code.detectAndDecode(image)
  return data


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
            write_secret_key()
            close_program()

        elif qr_code_choice == "no":
            defult_user_name = "DenemeUserName"
            defult_issuer_name = "DenemeIssuerName"
            default_secret_key = "DenemeSecretKey"
            print(
                "\n" + "QR'a ait user_name:" + Fore.MAGENTA + f" {defult_user_name}" + Fore.RESET + "\n" + "QR'a ait issuer_name:" + Fore.MAGENTA + f" {defult_issuer_name}" + Fore.RESET + "\n" + "isimlendirmeleri ile oluşturuldu." + "\n")
            generate_qr_code("DenemeUserName", "DenemeIssuerName" , default_secret_key)
            selected_secret_key = default_secret_key
            user_name = defult_user_name
            issuer_name = defult_issuer_name
            write_secret_key()
            close_program()

        elif qr_code_choice == "exit":
            close_program()

        # verify_choice = ""
        # while verify_choice not in ["yes", "no" , "exit"]:
        #     verify_choice = input(Fore.LIGHTBLUE_EX + "Doğrulama yapmak ister misiniz? (yes/no): " + Fore.RESET).lower()
        #     if verify_choice not in ["yes", "no" , "exit"]:
        #         print("Geçersiz seçenek. 'yes' veya 'no' olarak cevap verin.")
        #
        # if verify_choice == "yes":
        #     verification_code = input("Google Authenticator'dan gelen 6 haneli doğrulama kodunu girin: ")
        #     verify_code(verification_code)
        # elif verify_choice == "no":
        #     print("Program sonlandırıldı.")
        #     close_program()
        # elif verify_choice == "exit":
        #     close_program()

    elif user_choice == "2":
        is_authenticated = False
        while not is_authenticated:
            is_authenticated = authenticate_user("admin", "admin")
            if is_authenticated:
                read_secret_key_from_json()
                verification_code = input("Google Authenticator'dan gelen 6 haneli doğrulama kodunu girin: ")
                verify_code(verification_code)
            else :
                break

    elif user_choice == "exit":
        close_program()

    elif user_choice == "3":
        filename = input("Dosya adını girin: ")

        qr_filename = f"{filename}.png"

        if os.path.isfile(qr_filename) == True:
            print("\n" + Fore.LIGHTGREEN_EX +  f"{qr_filename} " + Fore.RESET + "isimli dosya bulundu.")
            image = cv2.imread(qr_filename)
            data = decode_qr_code(image)
            print("\n" + "URI Değeriniz: " + Fore.LIGHTYELLOW_EX + f"{data}" + Fore.RESET + "\n")
            close_program()

        else:
            print(Fore.LIGHTRED_EX + "\n" + "\n" +"Dosya bulunamadı." + Fore.RESET)
            close_program()


    else:
        invalid_attempt_count += 1  # Hatalı giriş sayacını artır
        print(Fore.LIGHTRED_EX + "\n" + "Geçersiz seçenek. Lütfen geçerli bir seçenek girin.")

        if invalid_attempt_count >= max_invalid_attempts:
            print(f"{max_invalid_attempts} kez hatalı seçim yaptınız." + Fore.RESET)
            close_program()