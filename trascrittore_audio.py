import sounddevice as sd
import random
import time
import scipy.io.wavfile as wav
import speech_recognition as sr
from googletrans import Translator
import asyncio

async def gioco_traduzione():
    traduttore = Translator()
    
    parole = ['giochi', 'libro', 'cane', 'gatto', 'sole']
    
    durata_registrazione = 5
    sample_rate = 44100
    riconoscitore = sr.Recognizer()
    
    print('Benvenuto nel mio gioco! 🎮')
    time.sleep(2)
    print('In questo gioco ti darò una parola in italiano e tu devi pronunciare la traduzione in INGLESE 😎')
    time.sleep(2)
    
    parola_random = random.choice(parole)
    
    print(f'\nLa parola da tradurre è: {parola_random.upper()} 📢')
    time.sleep(2)
    
    print('PRONTI 🔴')
    time.sleep(1)
    print('PARTENZA 🟡')
    time.sleep(1)
    print('VIA! 🟢')
    print("(Puoi parlare ora)")
    
    registrazione = sd.rec(int(durata_registrazione * sample_rate), samplerate=sample_rate, channels=1, dtype="int16")
    sd.wait()
    
    wav.write("audio.wav", sample_rate, registrazione)
    print("\nRegistrazione terminata!")

    try:

        traduzione_oggetto = await traduttore.translate(parola_random, src='it', dest='en')
        parola_tradotta = traduzione_oggetto.text.lower().strip()
    except Exception as e:
        print(f"Errore nella traduzione {str(e)}")
        return

    parola_detta_trascritta = ""
    with sr.AudioFile("audio.wav") as source:
        audio = riconoscitore.record(source)
        
    try:
        parola_detta_trascritta = riconoscitore.recognize_google(audio, language='en-US').lower().strip()
        print(f"\nHai detto: '{parola_detta_trascritta}'")
    except sr.UnknownValueError:
        print("\nNon sono riuscito a capire cosa hai detto. C'era troppo rumore o non hai parlato?")
        return
    except sr.RequestError as e:
        print(f"\nErrore di connessione ai server Google: {e}")
        return

    if parola_detta_trascritta == parola_tradotta:
        print("\n🎉 CORRETTO 🎉")
    else:
        print("\n❌ SBAGLIATO ❌")
        print(f"La traduzione corretta era '{parola_tradotta}'.")

if __name__ == "__main__":
    asyncio.run(gioco_traduzione())