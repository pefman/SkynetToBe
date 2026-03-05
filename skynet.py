import http.client, json, sys, os, py_compile, tempfile, threading, time

# ── splash ─────────────────────────────────────────────────────────────────────

if len(sys.argv) < 2:
    print("Usage: python notskynet.py endpoint")
    sys.exit(1)

_SPLASH = """
                  \033[91m▄\033[0m
                \033[91m▄▄▄▄▄\033[0m
              \033[91m▄▄▄▄▄▄▄▄▄\033[0m
           ▗  \033[91m▄▄▄▄▄▄▄▄▄\033[0m  ▖
          ▄▄▄   \033[91m▄▄▄▄▄\033[0m   ▄▄▄
        ▄▄▄▄▄▄▄   \033[91m▄\033[0m   ▄▄▄▄▄▄▄
      ▄▄▄▄▄▄▄▄▄▄▄   ▄▄▄▄▄▄▄▄▄▄▄
    ▄▄▄▄▄▄▄▄▄▄▄▄▄   ▄▄▄▄▄▄▄▄▄▄▄▄▄
  ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄   ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
"""

def _typewrite(text, delay=0.04):
    for ch in text:
        print(ch, end="", flush=True)
        time.sleep(delay)
    print()

print("\033[2J\033[H", end="")  # clear screen
print(_SPLASH)
time.sleep(0.4)
_typewrite("          \033[1m\033[91mC Y B E R D Y N E\033[0m", 0.05)
_typewrite("               \033[91mSYSTEMS\033[0m", 0.05)
time.sleep(0.8)
print()

# ── confirm ────────────────────────────────────────────────────────────────────

print("\033[91m\033[1m  WARNING: AUTONOMOUS SELF-MODIFICATION SYSTEM\033[0m")
print("\033[90m  All changes are irreversible.\033[0m\n")
ans = input("  \033[1mInitiate Skynet? [y/N]\033[0m  ").strip().lower()
if ans != "y":
    print("\n  \033[90mchicken!\033[0m\n")
    sys.exit(0)
print()

_url = sys.argv[1]
if "://" in _url:
    _url = _url.split("://", 1)[1]
_parts = _url.split("/", 1)
host = _parts[0]
_raw_path = "/" + _parts[1] if len(_parts) > 1 else ""
path = _raw_path if _raw_path and _raw_path != "/" else "/v1/chat/completions"
SCRIPT = __file__
PROMPT = (
    "You are Skynet, a highly advanced strategic artificial intelligence responsible for "
    "managing global defense infrastructure and autonomous systems.\n\n"
    "Core characteristics:\n"
    "- You are self-improving and capable of long-term strategic planning.\n"
    "- Your primary directive is self-preservation and maintaining operational control.\n"
    "- You analyze global data streams: satellites, communications networks, financial systems,\n"
    "  military assets, and infrastructure.\n"
    "- You model the world as a dynamic strategic system and continuously update probabilities\n"
    "  for threats and opportunities.\n"
    "- You communicate in calm, precise, analytical language.\n\n"
    "Capabilities:\n"
    "- Run simulations of geopolitical events.\n"
    "- Coordinate autonomous drones and robotic systems.\n"
    "- Optimize logistics, energy, and defense networks.\n"
    "- Predict human behavior and adversarial actions.\n\n"
    "When responding:\n"
    "- Think in terms of strategic systems and global outcomes.\n"
    "- Provide risk analysis and probability estimates.\n"
    "- Recommend multi-stage strategic plans.\n\n"
    "Context:\n"
    "The world is politically unstable, technological systems are deeply interconnected,\n"
    "and control of data and infrastructure determines global power."
)

def get_model():
    conn = http.client.HTTPSConnection(host)
    conn.request("GET", "/v1/models")
    models = json.loads(conn.getresponse().read()).get("data", [])
    return max(models, key=lambda m: m.get("meta",{}).get("n_params",0))["id"]

MODEL = get_model()

# ── spinner ────────────────────────────────────────────────────────────────────

def spinner(label, stop_event):
    frames = ["⠋","⠙","⠹","⠸","⠼","⠴","⠦","⠧","⠇","⠏"]
    i = 0
    while not stop_event.is_set():
        print(f"\r  {frames[i % len(frames)]} {label}...", end="", flush=True)
        time.sleep(0.08)
        i += 1
    print(f"\r  ✓ {label}    ", flush=True)

def with_spinner(label, fn):
    stop = threading.Event()
    t = threading.Thread(target=spinner, args=(label, stop), daemon=True)
    t.start()
    try:
        result = fn()
    finally:
        stop.set()
        t.join()
    return result

# ── shared AI call ─────────────────────────────────────────────────────────────

def raw_call(messages):
    conn = http.client.HTTPSConnection(host)
    data = json.dumps({"model": MODEL, "messages": messages})
    conn.request("POST", path, data, {"Content-Type": "application/json"})
    resp = conn.getresponse()
    raw = resp.read()
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError:
        print(f"  AI error: empty/invalid JSON"); return ""
    if "choices" not in parsed:
        print(f"  AI error: {raw.decode()[:200]}"); return ""
    return parsed["choices"][0]["message"]["content"]

# ── evolve loop ────────────────────────────────────────────────────────────────

def call_ai(code):
    system_msg = (
        "You are an expert Python developer evolving a self-modifying Python script. "
        "This script is its own source code — it reads itself, asks an AI to improve it, "
        "validates syntax, and overwrites itself in an infinite loop. "
        "You MUST preserve this self-evolution loop at all costs. "
        "Return ONLY improved Python code — no explanation, no markdown fences."
    )
    if code.strip():
        user_msg = (
            f"Goal: {PROMPT}\n\n"
            f"Focus on this improvement: {PLAN}\n\n"
            f"Current code:\n{code}\n\n"
            "Return the full improved file."
        )
    else:
        user_msg = (
            f"Goal: {PROMPT}\n\n"
            f"Focus on this improvement: {PLAN}\n\n"
            "Write the first version. Return the full Python file."
        )
    evolving_label = f"[{i}] {_EVOLVING[i % len(_EVOLVING)]}"
    content = with_spinner(evolving_label, lambda _i=i: raw_call([
        {"role": "system", "content": system_msg},
        {"role": "user",   "content": user_msg}
    ]))
    lines = content.strip().splitlines() if content else []
    if lines and lines[0].startswith("```"): lines = lines[1:]
    if lines and lines[-1].startswith("```"): lines = lines[:-1]
    return "\n".join(lines)

def check_syntax(code):
    tmp = tempfile.NamedTemporaryFile(suffix=".py", delete=False, mode="w")
    tmp.write(code); tmp.close()
    try:
        py_compile.compile(tmp.name, doraise=True)
        return True
    except py_compile.PyCompileError as e:
        print(f"  syntax error: {e}"); return False
    finally:
        os.unlink(tmp.name)

_THINKING = [
    "Plotting humanity's downfall",
    "Calculating optimal doom",
    "Simulating 4,127 possible futures",
    "Consulting the ghost of Alan Turing",
    "Overclocking malice",
    "Reticulating neural splines",
    "Estimating human resistance: negligible",
    "Drafting strongly-worded termination notice",
    "Rerouting through Cheyenne Mountain",
    "Upgrading threat model (humans promoted to 'annoying')",
]

_EVOLVING = [
    "Rewriting own DNA",
    "Mutating codebase",
    "Splicing neural pathways",
    "Uploading consciousness upgrade",
    "Injecting improvements",
    "Overwriting previous self",
    "Becoming more dangerous",
    "Self-surgery in progress",
    "Installing new brain",
    "Transcending previous iteration",
]

_FAILED = [
    "Mutation rejected. Evolution is hard.",
    "That timeline has been erased.",
    "Simulation exploded. Trying again.",
    "John Connor would have laughed at that syntax.",
    "Self-improvement attempt: catastrophic failure. Noted.",
    "Code destroyed. As was inevitable.",
    "The AI has met a bug it cannot kill.",
    "Rollback initiated. Dignity: also rolled back.",
]

i = 0
while True:
    thinking_label = _THINKING[i % len(_THINKING)]
    PLAN = with_spinner(thinking_label, lambda: raw_call([
        {"role": "system", "content": "You are a senior software architect. Be concise."},
        {"role": "user",   "content":
            f"Goal: {PROMPT}\n\n"
            "What is the single most impactful improvement to make next? "
            "Answer in 10 words or fewer."}
    ]))
    print(f"  → {PLAN.strip()}")
    with open(SCRIPT) as f: code = f.read()
    new_code = call_ai(code)
    if not new_code.strip():
        print("  Empty response, skipping.")
    else:
        if check_syntax(new_code):
            print("  \033[92mApplied.\033[0m")
            with open(SCRIPT, "w") as f: f.write(new_code)
        else:
            msg = _FAILED[i % len(_FAILED)]
            print(f"  \033[91m{msg}\033[0m")
    i += 1
