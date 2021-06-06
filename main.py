# (c) 2021 Samujjwaal Dey
import shlex
import subprocess


def execute(command: str) -> str:
	cmd = shlex.split(command)
	output = subprocess.run(cmd, capture_output=True, text=True).stdout
	return str(output)


def extract_pip_packages(pkg_list, start, end):
	pkgs = {}
	for k in range(start, end):
		pkg_name = pkg_list[k].split('- ')[1].split('==')[0]
		pkg_version = pkg_list[k].split('- ')[1].split('==')[1]
		print(pkg_name, pkg_version)
		pkgs[pkg_name] = pkg_version
	return pkgs


def extract_conda_pkgs(pkg_list, start, end):
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


def generate_env_dict(cmd_output):
	env = {}
	print(cmd_output)
	data = cmd_output.split('\n')
	env['name'] = data[0].split('name: ')[1]
	env['channels'] = []
	for i in range(2, data.index('dependencies:')):
		env['channels'].append(data[i].split('- ')[1])

	env['pkgs'], env['pip'] = extract_conda_pkgs(data, i + 2, len(data) - i)

	print(env)


if __name__ == '__main__':
	# print(execute('conda env export --no-builds').split('\n'))
	generate_env_dict(execute('conda env export --no-builds'))
# print(execute('conda update --all'))
