import json
import arcade


class SettingsManager:
    def __init__(self, filename='settings.json'):
        self.filename = filename
        self.settings = self.load_settings()

        self.DEFAULT_SETTINGS = {
            "audio": {
                "master_volume": 1.0,
                "music_volume": 0.8,
                "sfx_volume": 1.0,
                "music_enabled": True,
                "sfx_enabled": True,
            },
            "graphics": {
                "fullscreen": False,
                "vsync": False,
                "particles": False,
            },
            "gameplay": {
                "difficulty": "normal"
            },
            "developer": {
                "test_mode": False
            }
        }

    def load_settings(self):
        """
        хуйня которая загружает из настроек,
        или если они по пизде пошли создает новые
        """

        result = self.DEFAULT_SETTINGS.copy()  # кароче копия дефолтов чтобы делать по ней слияние

        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                loaded = json.load(f)
        except FileNotFoundError:
            print(f"файл {self.filename} не найден, дефы подгружаю")
            loaded = {}
        except json.JSONDecodeError as e:
            print(f"ошибка json файла {self.filename}: {e}")
            print("использую дефы")
            loaded = {}
        except Exception as e:
            print(f'хуй знает, что то сломалось {self.filename}: {e}')
            loaded = {}

        # слияние
        for section_name in loaded:
            if section_name in result:
                section_loaded = loaded[section_name]
                section_result = result[section_name]
                for key in section_loaded:
                    if key in section_result:
                        section_result[key] = section_loaded[key]
        return result

    def save_settings(self):
        """ сохраняет в json файл """
        try:
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=2, ensure_ascii=False)
                print('настройки были сохранены и записаны в json')
                return True  # успех
        except Exception as e:
            print(f'ошибка {e}')
            return False  # не удача

    def get(self, section, key):
        """
        получает значения из json
        типо settings.get('audio', 'master_volume')
        """

        current_section = self.settings.get(section, None)  # берем из словаря текущую секцию
        # если эта секция есть, то берем из нее ключ
        if current_section is not None:
            return current_section.get(key)
        # если нихуя нет то нихуя не возвращаем
        return None

    def set(self, section, key, value):
        """ устанавливает новые значения в json """

        # если нет сеции нихуя не делаем
        if section not in self.settings:
            print(f'секция {section} не найдена в насторойках')
            return False

        # если нет ключа тоже нихуя не делаем
        if key not in self.settings[section]:
            print(f'ключ {key} не найден в настройках')
            return False

        old_value = self.settings[section][key]
        if type(old_value) != type(value):
            print(f'ты поменял тип значения с {type(old_value)} на {type(value)}')

        self.settings[section][key] = value
        print('новые значения применены в настройки, но не сохранены в json')
        return True  # успех

    def reset_to_defaults(self):
        """ ресетает до дефов """
        self.settings = self.DEFAULT_SETTINGS.copy() # сбрасывает настройки до копии дефолтов
        return True

    def check_dev_password(self, password):
        """ проверяет пароль разраба """
        return password == "arcane"

    def unlock_developer_section(self):
        """ разблокирует скрытое """
        pass
