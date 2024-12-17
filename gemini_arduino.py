import google.generativeai as genai
import serial
import time
import pyttsx3
import speech_recognition as sr
import keyboard

def main():
    assistente_falante = True
    ligar_microfone = True
    arduino = serial.Serial('COM4', 9600)
    time.sleep(2)

    genai.configure(api_key="AIzaSyCArxGzhoB1T-GF0YcfKux9OxtN6Qhos2c")
    
    model = genai.GenerativeModel('gemini-pro')
    chat = model.start_chat(history=[])

    contexto = "A partir de agora, eu atuarei como um sistema de controle para o Arduino do sexo feminino, Tenho controle sobre LEDs e outros componentes, mas não posso acessar diretamente sensores de temperatura ou umidade. Quando um sensor de temperatura ou umidade for mencionado, eu apenas transmitirei as informações coletadas por um sensor conectado ao Arduino. Quando for mencionado leds eu respondo diretamente com comandos de ativação e desativação dos LEDs e outros componentes, sem formatação adicional como *. Responderei com palavras-chave claras para cada ação, apenas com 'led verde ligando', 'led verde desligando', 'led vermelho ligando', 'led vermelho desligando', 'led amarelo ligando', 'led amarelo desligando', para que o código interprete e execute corretamente cada comando. Se eu receber algo que não esteja relacionado a comandos, responderei de maneira simpática."

    if assistente_falante:
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[0].id)

    if ligar_microfone:
        r = sr.Recognizer()
        mic = sr.Microphone()

    while True:
        print("Pressione 'barra de espaço' para começar a falar.")

        keyboard.wait('space')

        if ligar_microfone:
            with mic as fonte:
                r.adjust_for_ambient_noise(fonte)
                print("Fale alguma coisa")
                audio = r.listen(fonte)
                try:
                    texto = r.recognize_google(audio, language="pt-BR")
                except Exception:
                    texto = ""
        if ligar_microfone == False:
            texto = input("Digite o comando")
        
        full_input = contexto + "\nUsuário: " + texto
        
        if "temperatura" in texto.lower() or "umidade" in texto.lower():
            arduino.write(b'leitura_tempUmid\n')
            
            temperatura = None
            umidade = None

            while temperatura is None or umidade is None:
                if arduino.in_waiting > 0:
                    linha = arduino.readline().decode().strip()

                    if linha:
                        if temperatura is None:
                            temperatura = linha
                        elif umidade is None:
                            umidade = linha

            if temperatura and umidade:
                print(f"Temperatura: {temperatura}°C, Umidade: {umidade}%")
                full_input += f"\nTemperatura atual: {temperatura}°C"
                full_input += f"\nUmidade atual: {umidade}%"
            else:
                print("Erro na leitura da temperatura ou umidade.")
        

        response = chat.send_message(full_input)
        print("Gemini:", response.text)

        if "led verde ligando" in response.text.lower():
            arduino.write(b'led_verde_ligando\n')
        if "led verde desligando" in response.text.lower():
            arduino.write(b'led_verde_desligando\n')
        if "led vermelho ligando" in response.text.lower():
            arduino.write(b'led_vermelho_ligando\n')
        if "led vermelho desligando" in response.text.lower():
            arduino.write(b'led_vermelho_desligando\n')
        if "led amarelo ligando" in response.text.lower():
            arduino.write(b'led_amarelo_ligando\n')
        if "led amarelo desligando" in response.text.lower():
            arduino.write(b'led_amarelo_desligando\n')
        
        if assistente_falante:
            engine.say(response.text)
            engine.runAndWait()

if __name__ == '__main__':
    main()