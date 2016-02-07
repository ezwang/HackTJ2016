# coding=utf-8
import io, os, subprocess, wave
import math, audioop, collections
import json

from urllib import urlencode
from urllib2 import Request, urlopen, URLError


def GetToken(app_key, secret_key):
    data = {'grant_type': 'client_credentials', 'client_id': app_key, 'client_secret': secret_key}
    response = urlopen("https://openapi.baidu.com/oauth/2.0/token", data=urlencode(data))
    response_text = response.read().decode("utf-8")
    json_result = json.loads(response_text)
    return json_result['access_token']


class TTS(object):
    def __init__(self, language="zh", app_key='Ib9tEFSgkT8ZdE3E9y0mBu6S', secret_key='6e6d4d73cf5a3621f85793189d5e5382'):
        """
        Create a new ``TTS`` instance, which represents a collection of text-to-speech functionality
        @:param language: language, ``en`` for English, ``zh`` for Chinese
        @:param app_key: Baidu App Key, the default value should only be used for test
        @:param secret_key: Baidu Secret Key, the default value should only be used for test
        """
        assert isinstance(language, str), "Language code must be a string"
        assert isinstance(app_key, str), "Key must be a string"
        assert isinstance(secret_key, str), "Key must be a string"
        self.app_key = app_key
        self.secret_key = secret_key
        self.language = language

        self.energy_threshold = 300  # minimum audio energy to consider for recording
        self.dynamic_energy_threshold = True
        self.dynamic_energy_adjustment_damping = 0.15
        self.dynamic_energy_ratio = 1.5
        self.pause_threshold = 0.8  # seconds of quiet time before a phrase is considered complete
        self.quiet_duration = 0.5  # amount of quiet time to keep on both sides of the recording

        self.token = GetToken(self.app_key, self.secret_key)

    def say(self, text, spd=5, pit=5, vol=5, per=0):
        """
        Perform TTS on the input text ``text``.
        @:param text: text to translation
        @:param spd: [optional] speed, range from 0 to 9
        @:param pit: [optional] pitch, 0-9
        @:param vol: [optional] volumn, 0-9
        @:param person: [optional] 0 for female, 1 for male
        """
        if len(text) > 1024:
            raise KeyError("Text length must less than 1024 bytes")
        url = "http://tsn.baidu.com/text2audio"

        data = {
            "tex": text,
            "lan": self.language,
            "tok": self.token,
            "ctp": 1,
            "cuid": '93489083242',
            "spd": spd,
            "pit": pit,
            "vol": vol,
            "per": per,
        }
        self.request = Request(url, data=urlencode(data))

        # check error
        try:
            response = urlopen(self.request)
        except URLError:
            raise IndexError("No internet connection available to transfer audio data")
        except:
            raise KeyError("Server wouldn't respond (invalid key or quota has been maxed out)")

        content_type = response.info().getheader('Content-Type')
        if content_type.startswith('application/json'):
            response_text = response.read().decode("utf-8")
            json_result = json.loads(response_text)
            raise LookupError("%d - %s" % (json_result['err_no'], json_result['err_msg']))
        elif content_type.startswith('audio/mp3'):
            self.play_mp3(response.read())

    def play_mp3(self, mp3_data):
        import platform, os, stat
        # determine which player executable to use
        system = platform.system()
        path = os.path.dirname(os.path.abspath(__file__))  # directory of the current module file, where all the FLAC bundled binaries are stored
        player = shutil_which("mpg123")  # check for installed version first
        if player is None:  # flac utility is not installed
            if system == "Windows" and platform.machine() in ["i386", "x86", "x86_64", "AMD64"]:  # Windows NT, use the bundled FLAC conversion utility
                player = os.path.join(path, "player", "mpg123-win32.exe")
            elif system == "Linux" and platform.machine() in ["i386", "x86", "x86_64", "AMD64"]:
                player = os.path.join(path, "player", "mpg123-linux")
            elif system == 'Darwin' and platform.machine() in ["i386", "x86", "x86_64", "AMD64"]:
                player = os.path.join(path, "player", "mpg123-mac")
            else:
                raise OSError("MP3 player utility not available - consider installing the MPG123 command line application using `brew install mpg123` or your operating system's equivalent")

        try:
            stat_info = os.stat(player)
            os.chmod(player, stat_info.st_mode | stat.S_IEXEC)
        except OSError:
            pass

        process = subprocess.Popen("\"%s\" -q -" % player, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
        play_info, stderr = process.communicate(mp3_data)
        return play_info


if __name__ == '__main__':
    t = TTS()
    t.say(000'您好')
