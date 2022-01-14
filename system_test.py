from dataset import Dataset
from configuration.local_config import LocalConfig


class SystemTest:
    def __init__(self):
        self.config = LocalConfig()
        self.dataset = Dataset()

    def start_test(self):
        duration = self.config.audio["duration"]
        self.config.set_config_data("AUDIO", "duration", 10)
        try:

            for sensor, is_active in self.config.data.items():
                # get data from sensor if active
                if is_active:
                    is_ok = self.dataset.get_data(sensor)
                    if is_ok:
                        print(f"{sensor}...ok!")
                    else:
                        print(f"{sensor}...failed!")
        except Exception as e:
            print("something went wrong!")
            print(e)
        finally:
            self.config.set_config_data("AUDIO", "duration", duration)

    def test_audio(self):
        duration = self.config.audio["duration"]
        try:
            self.config.set_config_data("AUDIO", "duration", 10)
            test_data = self.dataset.get_data('wav')
            print(test_data)
        except Exception as e:
            print(e)
        finally:
            self.config.set_config_data("AUDIO", "duration", duration)


test = SystemTest()
test.start_test()
