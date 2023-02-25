import speech_recognition as sr

def recognize_speech_from_mic(recognizer,microphone):
    if not isinstance(recognizer,sr.Recognizer):
        raise TypeError("'recognizer'must be 'Microphone' instance")
    if not isinstance(microphone, sr.Microphone):
        raise TypeError("'microphone' must be 'Microphone' instance")

    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    response = {
        'success' : True,
        'error' : None,
        'transcription' : None
    }

    try:
        response['transcription'] = recognizer.recognize_google(audio)
    except sr.RequestError:
        response['sucess'] = False
        response['error'] = 'API unavailable/unresponsive'

    except sr.UnknownValueError:
        response['error'] = 'unable to recognize speech'

    return response

recognizer = sr.Recognizer()


mic = sr.Microphone(device_index=1)

response = recognize_speech_from_mic(recognizer,mic)

print('\nSuccess : {}\nError : {}\n\nText from speech\n{}\n\n{}' \
      .format(response['success'],
               response['error'],
               '-'*17,
               response['transcription']))

temp_str = ''
records_all = []
while (temp_str != 'bye'):
    print ('speak it out')
    response = recognize_speech_from_mic(recognizer,mic)
    if response['success']:
        temp_str = response['transcription']
        print('you said :', temp_str)
        if (temp_str != 'bye'):
            records_all.append(temp_str)
print('thanks for your suggestion')
print('your suggestion on give movies')
print(records_all)


records_all.remove(None)

records_all

from textblob import TextBlob

def get_sentiment(sentx):
    
    analysis = TextBlob(sentx)
    if analysis.sentiment.polarity > 0:
        return ('positive')
    elif analysis.sentiment.polarity == 0:
        return('neutral')
    else:
        return('negative')

sentimets_total = {'neutral' : 0, 'positive' : 0,'negative' : 0}
for recd_sent in records_all:
    sentiment = get_sentiment(recd_sent)
    print(sentiment, '=========>', recd_sent)
    sentimets_total[sentiment] = sentimets_total[sentiment]+1
    print('#######################################')
print(sentimets_total)

from matplotlib import pyplot as plt
slices = [sentimets_total['neutral'],sentimets_total['positive'],sentimets_total['negative']]
activities = ['neutral', 'positive','negative']
cols = ['c','m','r']

plt.pie(slices,labels=activities,colors = cols,shadow = True,autopct = '%1.1f%%')

plt.title('sentiment analysis of tweets')
plt.legend()
plt.show()
