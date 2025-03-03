#!--encoding=utf-8--
from yaml import safe_load


class JobLoader:
    def __init__(self, config):
        with open(config, 'r') as f:
            config = safe_load(f)
        assert (type(config) is dict)
        assert ('exploits' in config.keys())
        assert ('target_groups' in config.keys())
        assert (type(config['exploits']) is dict)
        for name, prop in config['exploits'].items():
            assert ('target' in prop.keys())
            for tg in prop['target']:
                assert (tg in config['target_groups'].keys())

        self._config = config

    def select(self, target_group=None, exploit=None, prompt=False):
        if prompt:
            import questionary
            exploit = questionary.select(
                '选择启动的攻击脚本', [
                                 questionary.Choice('all', value='')
                             ] + list(self._config['exploits'].keys())
            ).ask()
            target_group = questionary.select(
                '选择目标组', [
                             questionary.Choice('all', value='')
                         ] + list(self._config['target_groups'].keys())
            ).ask()
        for name, prop in self._config['exploits'].items():
            if exploit and name != exploit:
                continue
            for tg in prop['target']:
                if target_group and target_group != tg:
                    continue
                for target in self._config['target_groups'][tg]:
                    yield name, target


class FormatLoader:
    def __init__(self, config):
        with open(config, 'r') as f:
            config = safe_load(f)
        assert (type(config) is dict)
        assert ('print_fmt' in config.keys())
        assert (type(config['print_fmt']) is dict)
        self._config = config

    def format(self, message, format_type):
        try:
            return self._config['print_fmt'][format_type].format(
                message.target, message.exp,
                message.status, message.flag
            )
        except:
            return 'wrong call'
