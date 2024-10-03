import yaml

class Config:
    def __init__(self, file_path: str):
        self.__file_path = file_path
        self.__config = self.__read_config()

    def __read_config(self):
        with open(self.__file_path, 'r') as file:
            return yaml.safe_load(file)

    def __write_config(self, config):
        with open(self.__file_path, 'w') as file:
            yaml.safe_dump(config, file)

    def set_token(self, token):
        self.set_config(['gitlab', 'token'], token)

    def get_token(self) -> str:
        return self.__config['gitlab']['token']
    
    def set_host(self, host):
        self.set_config(['gitlab', 'host'], host)

    def get_host(self) -> str:
        return self.__config['gitlab']['host']

    def set_config(self, keys, value):
        d = self.__config
        for key in keys[:-1]:
            if key not in d:
                d[key] = {}
            d = d[key]
        d[keys[-1]] = value
        self.__write_config(self.__config)
        print(f"Configuration for {'.'.join(keys)} updated successfully.")

    def get_config(self, keys):
        d = self.__config
        for key in keys:
            if key not in d:
                raise KeyError(f"Key {'.'.join(keys)} does not exist.")
            d = d[key]
        return d

    def append_to_list(self, keys, value):
        d = self.__config
        for key in keys[:-1]:
            if key not in d:
                d[key] = {}
            d = d[key]
        if keys[-1] not in d:
            d[keys[-1]] = []
        if value not in d[keys[-1]]:
            d[keys[-1]].append(value)
            self.__write_config(self.__config)
            print(f"Appended to list at {'.'.join(keys)} successfully.")
        else:
            print(f"Value already exists in the list at {'.'.join(keys)}.")