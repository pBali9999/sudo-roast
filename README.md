# sudo-roast

**Because even `sudo` deserves a sense of humor.**

`sudo-roast` is a small Linux hobby project that displays a randomly selected insult after an incorrect `sudo` password attempt.

It uses a Bash function and a Python helper to monitor the real `sudo` process through a pseudo-terminal (PTY). The real `sudo` program remains responsible for authentication and command execution.

## Features

- Random insults after detected authentication failures
- Built-in insults and user-defined insults
- Option to disable built-in insults
- Customizable insult list
- Red-colored insult messages
- Preserves the real `sudo` command's exit status
- Passes non-interactive invocations directly to `sudo`
- Debian package installation and removal

## Requirements

- Debian or Ubuntu-based Linux
- Bash
- Python 3
- sudo

## Installation

Download the Debian installer: [**sudo-roast.deb**](https://github.com/pBali9999/sudo-roast/releases/latest/download/sudo-roast.deb).

See the [GitHub Releases](https://github.com/pBali9999/sudo-roast/releases) page for release notes and version history.

Install it from the directory where you downloaded it:

```bash
sudo apt install ./sudo-roast.deb
```

Open a new interactive Bash terminal. The package automatically enables the Bash integration.

You can verify that the wrapper is loaded with:

```bash
type sudo
```

It should report that `sudo` is a function.

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

Lines beginning with `#` are comments. Blank lines are ignored.

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

The setting also accepts `false`, `off`, or `0` to disable built-in insults. Other values enable them.

When built-ins are disabled and there are no custom insults, no insult is displayed.

## Usage

Use `sudo` as usual:

```bash
sudo apt update
sudo whoami
sudo nano /etc/hosts
```

To force a new password prompt while testing:

```bash
sudo -k
sudo true
```

Enter an incorrect password to trigger a roast. Successful authentication runs the requested command normally.

## How it works

1. A Bash function named `sudo` forwards arguments to the Python helper.
2. The helper launches the real `/usr/bin/sudo` executable.
3. For interactive use, Python runs sudo in a pseudo-terminal and monitors its output.
4. When it detects a known authentication-failure message, it prints a random configured insult.
5. Non-interactive invocations are passed directly to the real sudo executable.

## Uninstallation

Remove the package with:

```bash
sudo apt remove sudo-roast
```

To remove the package and its package-managed configuration files:

```bash
sudo apt purge sudo-roast
```

Your personal insult configuration in `~/.config/sudo-roast/` is not removed automatically.

## Limitations

- The automatic integration is for interactive Bash sessions.
- Other shells and scripts that bypass the Bash function are not intercepted.
- Authentication messages can vary between sudo implementations and versions; detection depends on matching known failure messages.
- This is a fun wrapper, not a replacement for sudo or a security tool.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE).
