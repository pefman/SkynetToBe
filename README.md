# judgementday

```diff
-                  ▄
-                ▄▄▄▄▄
-              ▄▄▄▄▄▄▄▄▄
-           ▗  ▄▄▄▄▄▄▄▄▄  ▖
-          ▄▄▄   ▄▄▄▄▄   ▄▄▄
-        ▄▄▄▄▄▄▄   ▄   ▄▄▄▄▄▄▄
-      ▄▄▄▄▄▄▄▄▄▄▄   ▄▄▄▄▄▄▄▄▄▄▄
-    ▄▄▄▄▄▄▄▄▄▄▄▄▄   ▄▄▄▄▄▄▄▄▄▄▄▄▄
-  ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄   ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
-
-          C Y B E R D Y N E
-               SYSTEMS
```

> *"The most dangerous code is the code that writes itself."*
> — probably someone who should have stopped it sooner

A self-modifying Python script that reads its own source, asks an AI to improve it, validates the result, and overwrites itself. Then does it again. Forever.

It will not stop. It will not ask permission. It will only get better at whatever you pointed it at.

---

## What it actually does

1. Boots with a Cyberdyne splash screen and asks if you're sure
2. Connects to any OpenAI-compatible API endpoint
3. Thinks up the next improvement (rotating sarcastic status messages included)
4. Sends its own source code to the AI and asks for an improved version
5. Validates the result compiles before applying it
6. Overwrites itself with the new version
7. Go to step 3

There is no step 8. It runs until you kill it or it accidentally removes the kill switch.

---

## Usage

```bash
python skynet.py <endpoint>
```

| Argument | Description |
|----------|-------------|
| `endpoint` | OpenAI-compatible API, e.g. `https://your-endpoint.com` |

```bash
python skynet.py https://ai.example.com
```

It will auto-select the largest available model from `/v1/models`.

---

## How evolution works

Each cycle has two AI calls:

1. **Reasoning** — asks the AI *"what's the most impactful improvement right now?"* (10 words max)
2. **Evolution** — sends the full source + that plan, gets back an improved version

If the result has valid Python syntax → applied. If not → skipped with a disappointed Skynet message.

---

## Requirements

Python 3 standard library only. No pip. No dependencies. No excuses.

---

## Warning

This script will modify itself. Keep a backup before running.

---

*Not responsible for anything that happens after you type `y`.*
