import sys
import wave
import os.path
import datetime
import requests 
import json 
import pyaudio
import geocoder

SOUND_DIR = 'vox/'

def convertNumber(num):
    one = ['Zero', 'One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine']
    tenp = ['Ten', 'Eleven', 'Twelve', 'Thirteen', 'Fourteen', 'Fifteen', 'Sixteen', 'Seventeen', 'Eighteen', 'Nineteen']
    tenp2 = ['', '', 'Twenty', 'Thirty', 'Forty', 'Fifty', 'Sixty', 'Seventy', 'Eighty', 'Ninety']
    word = ''
    numInt = int(num)
    numStr = str(numInt)
    leng = len(numStr)
    if leng == 1:
        word = one[numInt]
    if leng == 2:
        if numStr[0] == '1':
            word = tenp[int(numStr[1])]
        else:
            text = one[int(numStr[1])]
            word = tenp2[int(numStr[0])]
            word = word + " " + text
    word = word.strip()
    return word
    

currentHour = datetime.datetime.now().strftime("%H")
currentMinute = datetime.datetime.now().strftime("%M")
print(currentHour+":"+currentMinute)

sentence = "The time is " + convertNumber(currentHour) + " hundred hours and " + convertNumber(currentMinute) + " minutes"

geo = geocoder.ip('me')
location = geo.city+","+geo.country

weatherJson = json.loads(requests.get("http://api.openweathermap.org/data/2.5/weather?q=%s&units=imperial&appid=72b736798c03abf3e203a8930b34f897" % location).content)
temperature = weatherJson['main']['temp']
sentence += " _comma _comma _comma the topside temperature is " + convertNumber(str(int(temperature))) + " degrees fahrenheit"


sentence = sentence.lower().split(' ')
accepted = []

print(sentence)

for i in sentence:
    if os.path.isfile(SOUND_DIR + i + '.wav'):
        accepted.append(i)

print(accepted)

splice = []
for i in accepted:
    sound = wave.open(SOUND_DIR + i + '.wav', 'rb')
    splice.append( [sound.getparams(), sound.readframes(sound.getnframes())] )
    sound.close()

pAudio = pyaudio.PyAudio()
stream = pAudio.open(format = pAudio.get_format_from_width(sound.getsampwidth()),
                     channels = sound.getnchannels(),
                     rate = sound.getframerate(),
                     output = True)

for params,frames in splice:
    stream.write(frames)

stream.stop_stream()  
stream.close()   
pAudio.terminate()

#try:
#    out = wave.open('time.wav', 'wb')
#    out.setparams(splice[0][0])
#    for params,frames in splice:
#        out.writeframes(frames)
#    out.close()
#except:
#    print('FATAL: Failed to write to output file.')
