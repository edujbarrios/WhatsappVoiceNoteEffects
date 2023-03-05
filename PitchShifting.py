import pyaudio
from pydub import AudioSegment
from pydub.effects import pitch_shift
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
        'name': 'pitch',
        'message': 'Selecciona el cambio de tono:',
        'choices': [
            Separator('--- Bajo ---'),
            {
                'name': '-3 semitonos'
            },
            {
                'name': '-2 semitonos'
            },
            {
                'name': '-1 semitono'
            },
            Separator('--- Normal ---'),
            {
                'name': '0 semitonos'
            },
            Separator('--- Alto ---'),
            {
                'name': '+1 semitono'
            },
            {
                'name': '+2 semitonos'
            },
            {
                'name': '+3 semitonos'
            }
        ]
    }
]

# Mostramos el menú interactivo
answers = prompt(questions)

# Definimos el valor de pitch shift a partir de la respuesta del menú
pitch_shift_value = None
if answers['pitch'] == '-3 semitonos':
    pitch_shift_value = -3
elif answers['pitch'] == '-2 semitonos':
    pitch_shift_value = -2
elif answers['pitch'] == '-1 semitono':
    pitch_shift_value = -1
elif answers['pitch'] == '0 semitonos':
    pitch_shift_value = 0
elif answers['pitch'] == '+1 semitono':
    pitch_shift_value = 1
elif answers['pitch'] == '+2 semitonos':
    pitch_shift_value = 2
elif answers['pitch'] == '+3 semitonos':
    pitch_shift_value = 3

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

# Aplicamos el efecto de pitch shifting
audio_segment_pitched = pitch_shift(audio_segment, RATE, pitch_shift_value)

# Guardamos el archivo de audio con pitch shifting en formato .opus
audio_segment_pitched.export("pitched_audio.opus", format="opus")

# Renombramos el archivo resultante para que tenga la extensión .opus
import os
os.rename("pitched_audio.opus", "audio_note.opus")
