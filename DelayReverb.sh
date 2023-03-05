import pyaudio
from pydub import AudioSegment
from pydub.effects import delay, reverb
from PyInquirer import prompt, Separator
import os

# Definimos los parámetros de la grabación
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024

# Creamos las preguntas para el menú interactivo
questions = [
    {
        'type': 'list',
        'name': 'effect',
        'message': 'Selecciona el efecto a aplicar:',
        'choices': [
            Separator('--- Efectos de audio ---'),
            {
                'name': 'Delay'
            },
            {
                'name': 'Reverb'
            }
        ]
    }
]

# Mostramos el menú interactivo
answers = prompt(questions)

# Definimos el efecto a aplicar a partir de la respuesta del menú
effect = None
if answers['effect'] == 'Delay':
    effect = 'delay'
    delay_ms = input('Introduce el tiempo de delay (en milisegundos): ')
    try:
        delay_ms = int(delay_ms)
    except ValueError:
        print('Valor de delay inválido. Se usará un delay de 500ms.')
        delay_ms = 500
elif answers['effect'] == 'Reverb':
    effect = 'reverb'

# Inicializamos PyAudio
audio = pyaudio.PyAudio()

# Creamos el stream de audio
stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)

# Creamos una lista para almacenar los fragmentos de audio
frames = []

# Grabamos el audio durante 5 segundos
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

# Aplicamos el efecto de delay o reverb según la opción elegida
if effect == 'delay':
    audio_segment_effect = delay(audio_segment, delay_ms=delay_ms)
elif effect == 'reverb':
    audio_segment_effect = reverb(audio_segment, room_scale=1.5)

# Guardamos el archivo de audio con el efecto en formato .opus
audio_segment_effect.export("audio_effect.opus", format="opus")

# Renombramos el archivo resultante para que tenga la extensión .opus
os.rename("audio_effect.opus", "audio_note.opus")
