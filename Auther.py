import json
import time
import pyotp
import qrcode

secret_key = "GlobalSecretKey"
user_name = "None"
issuer_name = "None"

def generate_qr_code(user_name, issuer_name):
    uri = pyotp.totp.TOTP(secret_key).provisioning_uri(name=user_name, issuer_name=issuer_name)
    img = qrcode.make(uri)
    global user_selected_file_name
    user_selected_file_name = input("Dosya adını girin: ")
    file_name = f"{user_selected_file_name}.png"
    img.save(file_name)
    print("QR kod oluşturuldu ve " + f"({user_selected_file_name}.png)" + " adında kaydedilecek." + "\n")

def verify_code(verification_code):
    otp = pyotp.TOTP(secret_key)
    is_code_valid = otp.verify(verification_code)
    if is_code_valid:
        print("Doğrulama Kodu Geçerli")
    else:
        print("Doğrulama Kodu Geçersiz")

def change_secret_key():
    global secret_key
    secret_key = input("Yeni gizli anahtarı girin: ")
    print(secret_key)

def change_qr_settings():
    global user_name
    global issuer_name
    user_name = input("Kullanıcı adınızı girin: ")
    issuer_name = input("Oluşturucu adını girin: ")
    generate_qr_code(user_name, issuer_name)

def write_secret_key():
    data = {}
    data['secret_key'] = secret_key
    data[('user_name')] = user_name
    data[('issuer_name')] = issuer_name
    data[('time')] = time.asctime(time.localtime(time.time()))

    with open(f'{user_selected_file_name}.json', 'w', encoding='utf8') as outfile:
        json.dump(data, outfile, ensure_ascii=False,indent=4)

    print("Gizli anahtarınız " + f"({user_selected_file_name}.json)" + " adında kaydedilecektir." + "\n")

while True:
    print("Aşağıdaki seçeneklerden birini seçin: (Sayıları seçerek ilerleyebilirisinz)" + "\n" + "\n"
          + "1. QR kod oluşturmak" + "\n"
          + "2. Doğrulama yapmak" + "\n")

    user_choice = input("Yapmak istediğiniz işlemi seçiniz : ").lower()

    if user_choice == "1":
        qr_code_choice = input("\n" + "QR Kodunu özelleştirmek istermisiniz ? (yes/no) ").lower()
        if qr_code_choice == "yes":
            change_qr_settings()
        elif qr_code_choice == "no":
            print("\n"+"QR'a ait user_name:" + f" {user_name}" + "\n" + "QR'a ait issuer_name:" + f" {issuer_name}" + "\n" + "isimlendirmeleri ile oluşturuldu." + "\n")
            generate_qr_code(user_name, issuer_name)
        else:
            print("Geçersiz seçenek. 'yes' veya 'no' olarak cevap verin.")

        secret_key_choice = input("Gizli anahtarınızı değiştirmek ister misiniz? (yes/no): ").lower()
        if secret_key_choice == "yes":
            change_secret_key()
        elif secret_key_choice == "no":
            print("Gizli anahtarınız değiştirilmedi." + "\n" + "Gizli anahtarınız: " + f"({secret_key})" + "\n")

        write_secret_key()

        verify_choice = input("Doğrulama yapmak ister misiniz? (yes/no): ").lower()

        if verify_choice == "yes":
            verification_code = input("Google Authenticator'dan gelen 6 haneli doğrulama kodunu girin: ")
            verify_code(verification_code)
        elif verify_choice == "no":
            print("Program sonlandırıldı.")
        else:
            print("Geçersiz seçenek. 'yes' veya 'no' olarak cevap verin.")
        break

    elif user_choice == "2":
        verification_code = input("Google Authenticator'dan gelen 6 haneli doğrulama kodunu girin: ")
        verify_code(verification_code)
        break

    else:
        print("Geçersiz seçenek. 'yes' veya 'no' olarak cevap verin.")
