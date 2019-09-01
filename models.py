import spotipy

DEVICE_NAME = "Musicama"

class Musicama(spotipy.Spotify):
    
    @staticmethod
    def get_device(sp: spotipy.Spotify):
        # print(sp.devices())
        # TODO: need to guess the device id of the web player?
        devices = sp.devices()['devices']
        # print(devices)
        for device in devices:
            if device['name'] == 'Web Playback SDK Quick Start Player':
            # if device['name'] == 'ONEPLUS A5010':
                return device['id']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.device_id = Musicama.get_device(self)
        self.user_id = self.me()['id']

    