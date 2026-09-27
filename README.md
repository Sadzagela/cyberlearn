# CyberLearn 
**Learn cybersecurity and Python — one bite-sized lesson at a time.**

CyberLearn is a free, offline, no-sign-in, Duolingo-style learning app for **cybersecurity fundamentals and Python**. It is designed to make security education approachable through short lessons, knowledge checks, progress tracking, and a simple gamified learning path.

> **100% local. No account. No ads. No telemetry. No network connection required.**

![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Dependencies](https://img.shields.io/badge/dependencies-standard%20library%20only-brightgreen)
---

##  Features

* **157 bite-sized lessons**
*  **7 learning tracks**
* Short explanations + knowledge checks
* Duolingo-style learning path
* XP and ranks
* Learning streaks
* Hearts system
* Dark and light themes
* Animated progress tracking
* Confetti for first correct answers
* Local progress saving
* No sign-in or account required
* No network calls or telemetry
* No advertisements
* Zero third-party Python dependencies
* Built entirely with the Python standard library

---

## Learning Tracks

CyberLearn currently contains seven tracks:

| Track                  | Focus                                                   |
| ---------------------- | ------------------------------------------------------- |
|  Networking          | Networking and core network concepts                    |
|  Blue Team           | Defensive security and security operations              |
|  Red Team            | Offensive-security concepts and methodology             |
|  White Hat            | Ethical hacking, authorization, and responsible testing |
|  Black Hat            | Threats, malicious activity, and attacker concepts      |
|  Awareness           | Security awareness and safe computing                   |
|  Python Programming  | Python fundamentals and programming concepts            |
|  Tools of the Trade | Security tools and their purposes                       |

Each track is divided into chapters and individual lessons.

> **Note:** The project currently describes seven tracks while the list above contains eight named areas in the original project description. If the application itself has seven tracks, update this table to exactly match `content.py` before publishing.

---

## 🎮 How Learning Works

Each lesson is designed to take roughly **one minute** to read.

A typical lesson contains:

1.  A short explanation
2.  A knowledge-check question
3.  Immediate feedback
4.  XP progression
5.  Progress toward the next lesson

Lessons unlock sequentially within their tracks, giving you a clear next step while still allowing you to choose which track to study.

---

##  Privacy by Design

CyberLearn is designed to run entirely on your own computer.

Your learning progress is stored locally at:

```text
~/.cyberlearn/progress.json
```

The project does not require:

* An account
* Email registration
* A server
* Cloud synchronization
* Analytics
* Telemetry
* Advertisements

There are also **no third-party runtime dependencies**. The application uses Python's standard library, including:

* `tkinter`
* `json`
* `dataclasses`
* `pathlib`

---

## 🖥️ Installation

### Requirements

* Python 3
* Tkinter

No `pip install` is required for the application itself.

### Clone the repository

```bash
git clone https://github.com/Sadzagela/cyberlearn.git
cd cyberlearn
```

### Run CyberLearn

```bash
python main.py
```

That's it.

---

##  Kali Linux / Debian / Ubuntu

If Tkinter isn't installed:

```bash
sudo apt install python3-tk
```

Then:

```bash
python3 main.py
```

### Other platforms

| Platform               | Tkinter                                             |
| ---------------------- | --------------------------------------------------- |
| Windows                | Usually included with the official Python installer |
| macOS                  | Usually included with the official Python installer |
| Debian / Ubuntu / Kali | `sudo apt install python3-tk`                       |
| Fedora                 | `sudo dnf install python3-tkinter`                  |
| Arch                   | `sudo pacman -S tk`                                 |

---

##  Project Structure

```text
cyberlearn/
├── main.py             # Application entry point
├── app.py              # Tkinter application and navigation
├── content.py          # Lessons and learning tracks
├── theme.py            # Themes, colors, and rank thresholds
├── progress.py         # Local progress, XP, streaks, and hearts
├── widgets.py          # Reusable UI components
├── test_content.py     # Automated content tests
├── README.md
├── SECURITY.md
└── LICENSE
```

---

## Testing

CyberLearn includes automated tests for lesson content.

Run:

```bash
python -m unittest test_content.py -v
```

The tests verify things such as:

* Lesson structure
* Unique lesson IDs
* Valid answer indexes
* Non-empty lesson content
* Valid lesson data

This helps prevent malformed lessons from silently breaking the application.

---

##  Adding a Lesson

Adding a lesson is intentionally simple.

```python
L(
    "net_01_05",
    "My New Lesson Title",
    "The ~1 minute explanation goes here...",
    "The check-for-understanding question?",
    ["Choice A", "Choice B", "Choice C"],
    1,
    "Why the answer is correct, reinforcing the concept."
)
```

Add the lesson to the appropriate chapter in `content.py`.

Make sure its ID is unique across the project.

Then run:

```bash
python -m unittest test_content.py -v
```

---

##  Adding a Track

To create a new learning track:

1. Add the track and its lessons to `content.py`.
2. Add its visual style to `TRACK_STYLE` in `theme.py`.
3. Give the track a unique icon and accent color.
4. Run the test suite.
5. Test the application manually.

---

## Educational Scope & Safety

CyberLearn is intended for **defensive cybersecurity education and conceptual learning**.

The curriculum focuses on understanding:

* Networks
* Security concepts
* Defensive techniques
* Security tools
* Threats
* Ethical hacking concepts
* Security awareness
* Python programming
* Security ethics and legal considerations

The project intentionally does **not** provide live exploit code or step-by-step instructions for attacking systems that the learner does not own or have explicit permission to test.

The goal is to provide a foundation comparable to introductory cybersecurity and networking education while keeping the material appropriate for an openly published learning project.

---

## Contributing

Contributions are welcome!

You can contribute by:

* Writing new lessons
* Improving existing explanations
* Fixing bugs
* Improving accessibility
* Improving the UI
* Adding tests
* Improving documentation
* Reporting security issues

Before submitting a pull request:

```bash
python -m unittest test_content.py -v
```

Please keep educational content accurate, clear, concise, and appropriate for the project's defensive-learning scope.

---

## Bug Reports

If you find a normal bug, please open a GitHub issue and include:

* What you expected to happen
* What actually happened
* Steps to reproduce the issue
* Your operating system
* Your Python version
* Relevant error messages

Please **do not publicly post sensitive information or security vulnerabilities**. See [`SECURITY.md`](SECURITY.md) for security reports.

---

## Security

If you discover a potential security vulnerability in CyberLearn, please **do not disclose it publicly in a GitHub issue**.

Please follow the instructions in [`SECURITY.md`](SECURITY.md).

---

## License

CyberLearn is released under the **MIT License**.

See [`LICENSE`](LICENSE) for the complete license text.

---

## Project Goals

CyberLearn is built around a simple idea:

> **Cybersecurity education should be accessible, understandable, and available without requiring an account or subscription.**

The current curriculum is a starting point. Contributions can help expand the number of lessons, improve explanations, add new learning tracks, and make the learning experience better for everyone.

If you find CyberLearn useful, consider  starring the repository and contributing a lesson or improvement.

---

##  Acknowledgments

Built with:

* Python
* Tkinter
* The Python standard library

No external assets are required for the application UI.
