# (c) 2021 Samujjwaal Dey
import shlex
from subprocess import run

import yaml


def execute(command: str) -> str:
	return str(run(shlex.split(command), capture_output=True, text=True).stdout)


def extract_pip_packages(pkg_list: list[str], start: int, end: int) -> dict:
	pkgs = {}
	for k in range(start, end):
		pkg_name = pkg_list[k].split('- ')[1].split('==')[0]
		pkg_version = pkg_list[k].split('- ')[1].split('==')[1]
		pkgs[pkg_name] = pkg_version
	return pkgs


def extract_pkgs(pkg_list: list[str], start: int, end: int) -> tuple[dict, dict]:
	conda_pkgs = {}
	pip_pkgs = {}
	for j in range(start, end):
		if (pkg := pkg_list[j].split('- ')[1]) != 'pip:':
			pkg_name = pkg.split('=')[0]
			pkg_version = pkg.split('=')[1]
			conda_pkgs[pkg_name] = pkg_version
		else:
			pip_pkgs = extract_pip_packages(pkg_list, j + 1, end)
			break

	return conda_pkgs, pip_pkgs


def generate_env_dict(cmd_output: str) -> dict:
	env = {}
	print(cmd_output)
	data = cmd_output.split('\n')
	env['name'] = data[0].split('name: ')[1]
	env['channels'] = []
	for i in range(2, data.index('dependencies:')):
		env['channels'].append(data[i].split('- ')[1])
	# noinspection PyUnboundLocalVariable
	env['conda'], env['pip'] = extract_pkgs(data, i + 2, len(data) - i)
	env['prefix'] = data[-2].split(': ')[1]
	# print(env)
	return env


def generate_env_yml(config: dict, user_installs: tuple[str] = None) -> None:
	if not user_installs:
		conda_pkgs = [f"{k}={v}" for k, v in config['conda'].items()]
	else:
		conda_pkgs = [f"{k}={v}" for k, v in config['conda'].items() if k in user_installs]
	pip_pkgs = [{'pip': [f"{k}=={v}" for k, v in config['pip'].items()]}]
	# noinspection PyTypeChecker
	conda_pkgs.extend(pip_pkgs)
	print(conda_pkgs)
	export = {'name': config['name'], 'channels': config['channels'], 'dependencies': conda_pkgs}

	with open(f"{export['name']}.yml", 'w') as file:
		yaml.dump(export, file, sort_keys=False)


def from_history(c1, c2):
	return tuple(c1['conda'].keys()) and list(c2['conda'].keys())


def generate_req_file(config: dict, user_installs: tuple[str]):
	conda_pkgs = [f"{k}=={v}\n" for k, v in config['conda'].items() if k in user_installs and k != 'python']
	pip_pkgs = [f"{k}=={v}\n" for k, v in config['pip'].items()]

	with open(f"requirements.txt", 'w') as file:
		file.writelines(conda_pkgs)
		file.writelines(pip_pkgs)


if __name__ == '__main__':
	env_config = generate_env_dict(execute('conda env export --no-builds'))
	env_config_history = generate_env_dict(execute('conda env export --from-history'))
	print(env_config)
	print(env_config_history)
	# generate_env_yml(env_config, from_history(env_config,env_config_history))
	# generate_env_yml(env_config, tuple('python'))
	generate_req_file(env_config, from_history(env_config, env_config_history))
