import os
import sys
import glob
import wave
import cherrypy
import numpy as np

from datetime import datetime
from pathlib import Path

from stt import Model

# DeepSpeech config..
COQUI_MODEL_DIR='/models'

STATIC_PATH=os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static_html')

class StaticRoot(object): pass

class SpeechToTextAPI(object):


    def __init__(self):
        self.tmp_dir = '/recordings'
        
        self.coqui_version=os.environ["COQUI_VERSION"]
        self.model_name=os.environ["MODEL_NAME"]
        self.model_version=os.environ["MODEL_VERSION"]

        acoustic_model, language_model = self.resolve_models(os.path.join(COQUI_MODEL_DIR, self.model_name))
        cherrypy.log("Loading speech to text model....")

        self.ds = Model(acoustic_model)
        self.ds.enableExternalScorer(language_model)

        cherrypy.log("Loading speech to text completed")
        


    @cherrypy.expose
    def index(self):
        msg = "<h1>coqui-stt Server</h1>\n"
        return msg 


    @cherrypy.expose
    @cherrypy.tools.json_out()
    def versions(self):
        result = {
            'version': 1,
            'model_name': self.model_name,            
            'model_version': self.model_version 
        }
        return result


    @cherrypy.expose
    @cherrypy.tools.json_out()
    def speech_to_text(self, soundfile, max_segment_length=5, max_segment_words=14, **kwargs):

        upload_tmp_filepath = os.path.join(self.tmp_dir, 'ds_request_' + datetime.now().strftime('%y-%m-%d_%H%M%S') + '.wav')
        with open(upload_tmp_filepath, 'wb') as wavfile:
            while True:
                data = soundfile.file.read(8192)
                if not data:
                    break
                wavfile.write(data)

        cherrypy.log("tmp file written to %s" % upload_tmp_filepath)

        result = {
            'version':1
        }

        fin = wave.open(upload_tmp_filepath, 'rb')
        audio = np.frombuffer(fin.readframes(fin.getnframes()), np.int16)
        fin.close()

        #
        prediction=''
        success=False
        try:
            prediction=self.ds.stt(audio)
            success = True
            Path(upload_tmp_filepath).unlink()
        except Exception as e:
            cherrypy.log("Error during transcribing %s" % upload_tmp_filepath)
            cherrypy.log(e)
        else:
            cherrypy.log("Transcribing %s succesful." % upload_tmp_filepath) 

        result.update({
            'success': success,
            'text': prediction 
        })
       
        return result


    def resolve_models(self, dirName):
        tflite_wildcard = "/*_%s.tflite" % self.model_version
        tflite = glob.glob(dirName + tflite_wildcard)[0]
        cherrypy.log("model file found: %s" % tflite)

        scorer_wildcard = "/*_%s_%s.scorer" % (self.model_name, self.model_version)
        scorer = glob.glob(dirName + scorer_wildcard)[0]
        cherrypy.log("scorer model file found: %s" % scorer)
    
        return tflite, scorer


cherrypy.config.update({
    'environment': 'production',
    'log.screen': False,
    'response.stream': True,
    'log.access_file': '/var/log/stt/access.log',
    'log.error_file': '/var/log/stt/error.log',
})


cherrypy.tree.mount(StaticRoot(), '/static', config={
    '/': {
        'tools.staticdir.on': True,
        'tools.staticdir.dir': STATIC_PATH,
        'tools.staticdir.index': 'index.html',
         },
    })


cherrypy.tree.mount(SpeechToTextAPI(), '/')
application = cherrypy.tree
