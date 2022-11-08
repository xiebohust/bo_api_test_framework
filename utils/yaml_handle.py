import yaml


class YamlHandle:
    def __init__(self,filename):
        self.filename = filename

    def read_yaml(self):
        with open(self.filename,encoding='utf-8') as f:
            case = yaml.safe_load(f)
        return case

if __name__ == '__main__':
    from config import caseyaml_path
    path = caseyaml_path + '/'+ 'case_data.yml'


    print(path)
    Y = YamlHandle(path).read_yaml()
    print(Y)



