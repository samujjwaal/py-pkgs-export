# (c) 2021 Samujjwaal Dey
import shlex
import subprocess


def print_hi(name):
	print(f'Hi, {name}')


def execute():
	cmd = shlex.split('conda list')
	print(cmd)
	cli = subprocess.run(cmd, capture_output=True, text=True)

	print(cli.stdout)
	# print(cli.stdout.decode().split('\n'))


if __name__ == '__main__':
	# print_hi('PyCharm')
	execute()
