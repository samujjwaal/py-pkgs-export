# (c) 2021 Samujjwaal Dey
import shlex
import subprocess


def execute(command: str) -> str:
	cmd = shlex.split(command)
	output = subprocess.run(cmd, capture_output=True, text=True).stdout
	return str(output)


def generate_env_dict(string):
	env = {}
	print(string)
	# print(string.split('\n')[0].split('name: ')[1])
	env['name'] = string.split('\n')[0].split('name: ')[1]
	env['channels'] = []
	for i in range(2, string.split('\n').index('dependencies:')):
		print(string.split('\n')[i].split('- ')[-1])
		env['channels'].append(string.split('\n')[i].split('- ')[-1])
	# print(string.split('\n')[2].split('name: ')[1])
	print(env)
	pass


if __name__ == '__main__':
	# print(execute('conda env export --no-builds').split('\n'))
	generate_env_dict(execute('conda env export --no-builds'))
# print(execute('conda update --all'))
