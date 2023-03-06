# Genera un fichero en extension .opus para enviar notas de voz por whatsapp con el efecto de AutoTune

# 1. Generamos la grabación
# 2. Abrimos Whatsapp Web
# 3. Enviamos el fichero generado (whatsapp lo reconocerá como una nota de voz)

import pyaudio
from pydub import AudioSegment
from pydub.effects import autotune
from PyInquirer import prompt, Separator

# Definimos los parámetros de la grabación
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024

# Creamos las preguntas para el menú interactivo
questions = [
    {
        'type': 'list',
        'name': 'modulation',
        'message': 'Selecciona la cantidad de modulación:',
        'choices': [
            Separator('--- Baja modulación ---'),
            {
                'name': 'Ligera'
            },
            {
                'name': 'Moderada'
            },
            Separator('--- Alta modulación ---'),
            {
                'name': 'Fuerte'
            }
        ]
    }
]

# Mostramos el menú interactivo
answers = prompt(questions)

# Definimos el valor de modulación a partir de la respuesta del menú
modulation = None
if answers['modulation'] == 'Ligera':
    modulation = 0.5
elif answers['modulation'] == 'Moderada':
    modulation = 1.0
elif answers['modulation'] == 'Fuerte':
    modulation = 2.0

# Inicializamos PyAudio
audio = pyaudio.PyAudio()

# Creamos el stream de audio
stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)

# Creamos una lista para almacenar los fragmentos de audio
frames = []

# Grabamos el audio durante RECORD_SECONDS segundos
print('Grabando audio...')
while True:
    data = stream.read(CHUNK)
    frames.append(data)
    if len(frames) > RATE / CHUNK * 5:
        break

print('Grabación finalizada')

# Detenemos la grabación
stream.stop_stream()
stream.close()
audio.terminate()

# Convertimos los fragmentos de audio a un objeto AudioSegment de pydub
audio_segment = AudioSegment(
    data=b''.join(frames),
    sample_width=2,
    frame_rate=RATE,
    channels=CHANNELS
)

# Aplicamos el efecto de autotune
audio_segment_autotuned = autotune(audio_segment, 440, modulation=modulation)  # 440 es la frecuencia de afinación estándar (A4)

# Guardamos el archivo de audio con autotune en formato .opus
audio_segment_autotuned.export("autotuned_audio.opus", format="opus")

# Renombramos el archivo resultante para que tenga la extensión .opus (formato de las notas de audios de whatsapp)
import os
os.rename("autotuned_audio.opus", "audio_note.opus")
