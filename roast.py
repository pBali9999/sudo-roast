#!/usr/bin/env python3

import os
import pty
import sys
import shutil
import random
import re
from pathlib import Path

INSULTS = [
	"Your keyboard has more qualifications than you.",
	"Your password has left the chat.",
	"The kernel is disappointed in you.",
	"Privilige escalation denied. Ego escalation pending.",
	"Have you tried turning your brain off and on again?",
	"Bold attempt. Incorrect execution.",
	"Somewhere a sysadmin is crying.",
	"Access denied. Go contemplate your life choices.",
	"Even the toaster would have guessed that password.",
	"sudo believes in you. Unfortunately.",
	"Error 418: Your brain is a teapot.",
	"Permission denied. Skill issue.",
	"The computer has decided you are not worthy.",
	"Congratulations, you played yourself."
]

def load_insults():
	config_file = Path.home() / ".config/sudo-roast/insults.txt"

	custom_insults = []
	use_builtins = True

	try:
		with config_file.open("r", encoding="utf-8") as file:
			for line in file:
				line = line.strip()

				if not line or line.startswith("#"):
					continue

				if line.lower().startswith("builtins=") or line.lower().startswith("builtins ="):
					setting = line.split("=", 1)[1].strip().lower()
					use_builtins = setting not in ("no", "false", "off", "0")
					continue
				custom_insults.append(line)
	except FileNotFoundError:
		pass
	except OSError as error:
		print(f"sudo-roast: could not read custom insults: {error}", file=sys.stderr)

	if use_builtins:
		return INSULTS + custom_insults
	return custom_insults

FAILURE_PATTERNS = [
	re.compile(rb"authentication failed, try again", re.I),
	re.compile(rb"sorry, try again", re.I),
	re.compile(rb"incorrect password", re.I),
	re.compile(rb"authentication failed", re.I),
	re.compile(rb"maximum \d+ incorrect authentication attempts", re.I)
]

RED = b"\x1b[1;31m"
RESET = b"\x1b[0m"

def main():
	sudo_path = shutil.which("sudo")

	if sudo_path is None:
		print("sudo-roast: could not find sudo", file=sys.stderr)
		return 127

	args = [sudo_path, *sys.argv[1:]]

	#Preserve normal behaviour when there is no interactive terminal
	if not sys.stdin.isatty():
		os.execv(sudo_path, [sudo_path, *sys.argv[1:]])

	insults = load_insults()
	line_buffer = bytearray()
	failure_detected = False

	def read_output(fd):
		nonlocal failure_detected
		try:
			data = os.read(fd, 1024)
		except OSError:
			return b""

		if not data:
			return b""

		output = bytearray()

		for byte in data:
			output.append(byte)
			line_buffer.append(byte)
			if any(pattern.search(line_buffer) for pattern in FAILURE_PATTERNS):
				failure_detected = True
			if byte == 10:
				if failure_detected and insults:
					insult = random.choice(insults).encode("utf-8")
					output.extend(RED + insult + RESET + b"\r\n")
				line_buffer.clear()
				failure_detected = False
			if len(line_buffer) > 4096:
				del line_buffer[:-256]
		return bytes(output)

	status = pty.spawn(args, master_read=read_output)

	if status == -1:
		return 1

	if os.WIFEXITED(status):
		return os.WEXITSTATUS(status)

	if os.WIFSIGNALED(status):
		return 128 + os.WTERMSIG(status)

	return 1

if __name__ == "__main__":
	sys.exit(main())
