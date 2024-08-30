import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import os
import subprocess

# Sesli asistan için motor başlatma
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Konuşma hızını ayarlama
engine.setProperty('volume', 1.0)  # Ses seviyesini ayarlama

# Asistanın konuşmasını sağlayan fonksiyon
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Kullanıcının komutunu dinleyen fonksiyon
def listen_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Komut bekleniyor...")
        recognizer.adjust_for_ambient_noise(source)  # Çevresel gürültüyü ayarlama
        audio = recognizer.listen(source)

        try:
            command = recognizer.recognize_google(audio, language='tr-TR')
            print(f"Kullanıcı: {command}")
            return command.lower()
        except sr.UnknownValueError:
            speak("Üzgünüm, ne dediğinizi anlayamadım.")
            return ""
        except sr.RequestError:
            speak("İnternet bağlantısı kurulamadı.")
            return ""

# Komutları işleyen fonksiyon
def process_command(command):
    if 'saat kaç' in command:
        current_time = datetime.datetime.now().strftime('%H:%M')
        speak(f"Saat şu an {current_time}")
    elif 'arama yap' in command:
        speak("Ne aramak istersiniz?")
        search = listen_command()
        url = f"https://www.google.com/search?q={search}"
        webbrowser.open(url)
        speak(f"{search} için arama sonuçlarını getiriyorum.")
    elif 'güncel saat ve tarihi' in command:
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        speak(f"Bugünün tarihi ve saati {now}")
    elif 'websitesini aç' in command:
        speak("Hangi web sitesini açmak istersiniz?")
        site = listen_command()
        url = f"https://{site}"
        webbrowser.open(url)
        speak(f"{site} açılıyor.")
    elif 'hesaplama yap' in command:
        speak("Lütfen işlem söyleyin. Örneğin: 2 artı 2")
        equation = listen_command()
        try:
            result = eval(equation.replace('artı', '+').replace('eksi', '-').replace('çarpı', '*').replace('bölü', '/'))
            speak(f"Sonuç: {result}")
        except Exception:
            speak("Geçersiz bir işlem söylediniz.")
    elif 'dosya aç' in command:
        speak("Hangi dosyayı açmak istersiniz?")
        file_path = listen_command()
        try:
            os.startfile(file_path)
            speak(f"{file_path} açılıyor.")
        except Exception:
            speak("Dosya açılamadı.")
    elif 'not al' in command:
        speak("Ne not almak istersiniz?")
        note = listen_command()
        with open("notlar.txt", "a") as file:
            file.write(note + "\n")
        speak("Not alındı.")
    elif 'notları oku' in command:
        if os.path.exists("notlar.txt"):
            with open("notlar.txt", "r") as file:
                notes = file.read()
                if notes:
                    speak("İşte notlarınız:")
                    speak(notes)
                else:
                    speak("Hiç notunuz yok.")
        else:
            speak("Hiç notunuz yok.")
    elif 'sistem bilgileri' in command:
        uname_result = subprocess.check_output("uname -a", shell=True).decode()
        speak(f"Sistem bilgileri: {uname_result}")
    elif 'dur' in command or 'çıkış' in command:
        speak("Görüşmek üzere!")
        exit()
    else:
        speak("Bu komutu anlayamadım, lütfen tekrar edin.")

# Ana döngü
def main():
    speak("Merhaba, nasıl yardımcı olabilirim?")
    while True:
        command = listen_command()
        process_command(command)

if __name__ == "__main__":
    main()