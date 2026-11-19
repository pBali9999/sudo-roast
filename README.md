# sudo-roast

**Because even `sudo` deserves a sense of humor.**

`sudo-roast` is a small Linux hobby project that adds a randomly selected insult after an incorrect `sudo` password attempt. It uses a Bash function as a wrapper and a Python helper to watch the real `sudo` process through a pseudo-terminal.

The real `sudo` program still handles authentication and executes the requested command.

## Features

- Random insults after detected authentication failures
- Built-in insults and user-defined insults
- Option to disable built-in insults
- Customizable insult list in a per-user configuration file
- Red-colored insult messages
- Preserves the real `sudo` command's exit status
- Passes non-interactive invocations directly to `sudo`

## Requirements

- Linux
- Bash
- Python 3
- `sudo`

## Installation

Clone the repository into your home directory:

```bash
git clone https://github.com/pBali9999/sudo-roast.git ~/sudo-roast
cd ~/sudo-roast
```

Make sure the scripts are present, then load the Bash wrapper in your current shell:

```bash
source ~/sudo-roast/roast.sh
```

To load it automatically in new interactive Bash sessions, add this line to the end of `~/.bashrc`:

```bash
source "$HOME/sudo-roast/roast.sh"
```

The wrapper only applies to Bash shells where `roast.sh` has been sourced. It does not replace the system `sudo` executable.

## Configuration

Create the configuration directory:

```bash
mkdir -p ~/.config/sudo-roast
```

Create or edit the insult list:

```bash
nano ~/.config/sudo-roast/insults.txt
```

Put one insult on each line:

```text
Nice try.
Your keyboard is disappointed in you.
That password needs some work.
```

Lines beginning with `#` are comments.

### Built-in insults

Built-in insults are enabled by default. You can combine them with your own insults by adding:

```text
builtins=yes
```

To use only your own insults, set:

```text
builtins=no
```

For example:

```text
# Use only my custom insults
builtins=no

Maybe try remembering your password.
The keyboard isn't the problem.
```

When built-ins are disabled and there are no custom insults, no insult is displayed.

The setting also accepts `false`, `off`, or `0` as off; other values enable built-ins.

## Usage

Use `sudo` as usual after sourcing the wrapper:

```bash
sudo apt update
sudo whoami
sudo nano /etc/hosts
```

To force a new password prompt while testing, run:

```bash
sudo -k
sudo true
```

Enter an incorrect password to trigger a roast. A successful authentication runs the requested command normally.

## How it works

1. The Bash function named `sudo` forwards its arguments to the Python helper.
2. The helper locates and launches the real `sudo` executable.
3. For interactive use, Python runs `sudo` in a pseudo-terminal (PTY) and monitors its output.
4. When it detects a known authentication-failure message, it prints a random configured insult.

For non-interactive input, the helper executes the real `sudo` directly.

## Limitations

- The wrapper must be sourced in the Bash session where you want to use it.
- Other shells, scripts, or commands that bypass the Bash function are not intercepted.
- Authentication messages can vary between `sudo` implementations and versions; detection depends on matching known failure messages.
- This is a fun wrapper, not a replacement for `sudo` or a security tool.

## License

No license has been specified yet. Until a license is added to the repository, the default copyright rules apply.
