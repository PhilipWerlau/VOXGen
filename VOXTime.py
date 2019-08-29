import sys
import wave
import os.path
import datetime
import requests 
import json 
import pyaudio
import geocoder

SOUND_DIR = 'vox/'
TALK_SPEED = 1
TEMPERATURE_UNITS = "imperial"
WEATHER_API_KEY = "<API_KEY_HERE>"

def convertNumber(num):
    one = ['', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']
    tenp = ['ten', 'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen', 'sixteen', 'seventeen', 'eighteen', 'nineteen']
    tenp2 = ['', '', 'twenty', 'thirty', 'forty', 'fifty', 'sixty', 'seventy', 'eighty', 'ninety']
    
    numWord = ''
    numInt = int(num)
    numStr = str(numInt)

    leng = len(numStr)
    if leng == 1:
        if numInt == 0:
            numWord = 'zero'
        else:
            numWord = one[numInt]
    elif leng == 2:
        if numStr[0] == '1':
            numWord = tenp[int(numStr[1])]
        else:
            text = one[int(numStr[1])]
            numWord = tenp2[int(numStr[0])]
            numWord += " " + text
    return numWord.strip()
    

currentHour = datetime.datetime.now().strftime("%H")
currentMinute = datetime.datetime.now().strftime("%M")
print(currentHour+":"+currentMinute)
sentence = "doop Attention _comma the time is "
sentence += convertNumber(currentHour) + " hundred hours and " 
sentence += convertNumber(currentMinute) + " minutes"

try:
    geo = geocoder.ip('me')
    latlong = geo.latlng

    weatherAPIURL = "http://api.openweathermap.org/data/2.5/weather"
    weatherAPIURL += "?lat="+f"{latlong[0]:.2f}"
    weatherAPIURL += "&lon="+f"{latlong[1]:.2f}"
    weatherAPIURL += "&units="+TEMPERATURE_UNITS
    weatherAPIURL += "&appid="+WEATHER_API_KEY
    weatherJson = json.loads(requests.get(weatherAPIURL).content)

    temperature = weatherJson['main']['temp']
    print(temperature)

    sentence += " _period the topside temperature is "
    sentence += convertNumber(str(temperature).split('.')[0]) 
    sentence += " point " + convertNumber(str(temperature).split('.')[1][0])
    sentence += " degrees fahrenheit"

except:
    print(latlong)
    print(weatherAPIURL)
    print("Connection error")
    sentence += " _period bloop temperature service communication error"

print(sentence)
sentence = sentence.lower().split(' ')
accepted = []
for i in sentence:
    if os.path.isfile(SOUND_DIR + i + '.wav'):
        accepted.append(i)
#print(accepted)

splice = []
for i in accepted:
    sound = wave.open(SOUND_DIR + i + '.wav', 'rb')
    splice.append( [sound.getparams(), sound.readframes(sound.getnframes())] )
    sound.close()

pAudio = pyaudio.PyAudio()
stream = pAudio.open(format = pAudio.get_format_from_width(sound.getsampwidth()),
                     channels = sound.getnchannels(),
                     rate = int(sound.getframerate()*TALK_SPEED),
                     output = True)
for params,frames in splice:
    stream.write(frames)
stream.stop_stream()  
stream.close()   
pAudio.terminate()

try:
    out = wave.open('time.wav', 'wb')
    out.setparams(splice[0][0])
    for params,frames in splice:
        out.writeframes(frames)
    out.close()
except:
    print("FATAL: Failed to write to output file.")
