# Tech Thesaurus for Humanists
### A Living Glossary with Maps, Models, and Moments of Confusion

*Version 1.0 — released March 2026*

---

## A Note on Why This Document Exists

**TL;DR: Technology isn't hard to understand. It's just badly explained. This document tries to fix that.**

Technology has developed a peculiar class system. On one side: those who grew up speaking the language, for whom terminals and repositories and containers are native terrain. On the other: everyone else, for whom the same tools are a foreign country with no phrasebook, no map, and a troubling tendency to delete your work without warning.

This is not a skills gap. It is an explanation gap.

The knowledge required to navigate modern technical tools is neither secret nor especially complex. It has simply been transmitted in a dialect most people were never taught, by people who have largely forgotten what it felt like not to know it. Tutorials assume context. Documentation assumes vocabulary. And the people who most need a clear explanation are the ones least likely to know which question to ask.

The Tech Thesaurus for Humanists exists to close that gap, at least partially, for at least some people. It is written for anyone who came to technology by necessity rather than by nature: the writer who suddenly needs to run a server, the researcher who inherited a codebase, the editor building tools to open up an archive. It assumes intelligence and curiosity, and assumes nothing else.

The goal is not simplification. Simplification flattens; it trades one kind of confusion for another. The goal is orientation: the kind of map that lets you know where you are, so that when you go looking for more detail, you know where to look.

*Information not only wants to be free. It also wants to be understood.*

---

> **How to use this document:**
> Start with *The Big Map*. Every term you encounter in the wild has a home somewhere on that map. Once you know roughly where something lives, the definition makes sense. Definitions without maps are just more words.
>
> Search with `Ctrl+F`. Add your own notes freely. This document belongs to you, not to anyone who thinks "just Google it" is helpful advice.

---

## 🗺️ THE BIG MAP
### How Your Digital World Is Actually Organized

Think of it as a city with distinct neighborhoods. You live in all of them at once, but they have different rules, different languages, and different ways of causing you grief.

```
YOUR COMPUTER (the building you live in)
│
├── OPERATING SYSTEM (the building's infrastructure: electricity, plumbing)
│   └── Windows / macOS / Linux
│
├── VISUAL STUDIO CODE / KILOCODE (your writing desk)
│   ├── Where you read and write code and text files
│   └── Has its own internal terminal (a phone on your desk to the basement)
│
├── TERMINAL / CLI (the basement utility room)
│   ├── You type commands; the computer obeys
│   ├── Unforgiving. No undo button. No confirmation dialogs.
│   └── The language family spoken here is called: shell
│       (bash and zsh are close dialects; PowerShell is a more distant relative)
│
├── DOCKER (a set of sealed moving boxes)
│   ├── Each box contains a self-sufficient mini-environment
│   ├── Programs run inside these boxes, isolated from everything else
│   └── The boxes can be moved to any computer and still work identically
│
├── RASPBERRY PI (a tiny, cheap computer, often acting as a server)
│   └── Yours probably runs somewhere quietly, doing one specific job
│
├── THE AI LAYER (a new neighborhood, still under construction)
│   ├── LLM (the engine: predicts language, generates text)
│   ├── AI AGENT (the engine given hands: can take actions, use tools)
│   ├── OPEN WEBUI (a local browser-based interface for talking to models)
│   ├── LM STUDIO / OLLAMA (tools for running models on your own machine)
│   └── ON-PREM vs OFF-PREM (running the engine yourself vs renting it from someone else)
│
└── THE NETWORK (the city outside your building)
    ├── VPN (a private underground tunnel through the city)
    │   └── Makes your traffic look like it comes from somewhere else;
    │       also lets you reach your home server securely from outside
    │
    ├── LOCAL NETWORK (your street: your computer + your Raspberry Pi)
    │
    └── THE INTERNET (the rest of the city)
            └── Including: GitHub (a public library with version history)
```

---

## 🖥️ PART ONE: THE TERMINAL AND CLI
*The basement utility room*

### CLI
**What it stands for:** Command-Line Interface
**What it means:** A way of talking to your computer by typing text commands instead of clicking icons.

The opposite of CLI is GUI (Graphical User Interface): the world of buttons, windows, and menus. The CLI predates the GUI by decades. It is more powerful, less forgiving, and looks intimidating precisely because it refuses to hold your hand.

**Analogy:** The GUI is a restaurant with a picture menu. The CLI is a professional kitchen where you have to know the recipes by heart but can cook anything, faster.

---

### Terminal / Shell / Console / Command Prompt
These four words are used almost interchangeably by people who should probably be more careful. Here is the distinction that actually matters:

- **Terminal:** The window itself. The application you open to see a blinking cursor.
- **Shell:** The *language* running inside that window (bash, zsh, PowerShell). The interpreter that understands your commands.
- **Console:** An older word for terminal, sometimes still used. Treat as a synonym.
- **Command Prompt:** The Windows version of a terminal. Same idea, different dialect.

**Analogy:** The terminal is the room; the shell is the dialect spoken in it. You can walk into the same room and switch dialects. Same room, different shell.

---

### bash / zsh / PowerShell
These are different *shell dialects* within the same CLI language family.

- **bash** (Bourne Again Shell): The classic. Standard on Linux and older Macs. Most tutorials are written in bash.
- **zsh** (Z Shell): Default on newer Macs. Mostly compatible with bash but with some extras.
- **PowerShell**: Windows. A different beast entirely, though Microsoft has released a cross-platform version.

**Practical note:** When a tutorial says "run this in your terminal," they assume bash or zsh. If you're on Windows and using the default Command Prompt, some commands will simply not work. This is a source of much quiet suffering.

---

### Path
A path is the address of a file or folder on your computer, written in the terminal's language.

- On Mac/Linux: `/Users/TrueLipstick/Documents/folkvett/article.md`
- On Windows: `C:\Users\TrueLipstick\Documents\folkvett\article.md`

The slashes go in opposite directions. This is not a metaphor for anything; it is just an old incompatibility that everyone decided to live with.

**Analogy:** A postal address, written from the largest container (country) down to the smallest (door). Except here it goes from disk to folder to file.

**Relative vs. Absolute path:**
- Absolute: the full address from the very top (`/Users/TrueLipstick/...`)
- Relative: directions *from where you currently are* (`../folkvett/article.md` means "go up one folder, then into folkvett")

---

### Directory
A directory is a folder. The word "directory" is used in the terminal world because it predates the folder metaphor by several decades. Same thing. Do not let it unsettle you.

---

### Common Terminal Commands
These are the twelve words of survival Latin.

| Command | What it does | Analogy |
|---|---|---|
| `pwd` | Print Working Directory: shows where you are | "What street am I on?" |
| `ls` | List: shows what's in the current folder | "What's in this room?" |
| `cd foldername` | Change Directory: move into a folder | "Walk through that door" |
| `cd ..` | Go up one folder level | "Step back into the hallway" |
| `mkdir name` | Make Directory: create a new folder | "Build a new room" |
| `cp file1 file2` | Copy a file | "Photocopy this document" |
| `mv file1 file2` | Move or rename a file | "Move/rename this document" |
| `rm file` | Remove: delete a file permanently | "Throw it in a fire" |
| `cat file` | Print file contents to screen | "Read this aloud" |
| `echo "text"` | Print text to screen | "Repeat after me" |
| `sudo` | Do as superuser: run with admin privileges | "I have a master key" |
| `Ctrl+C` | Cancel/interrupt whatever is running | "Stop. I said stop." |

> **WARNING on `rm`:** There is no recycling bin. No "are you absolutely and 100% sure?" There is no confirmation dialog of any kind. No undo.
> `rm -rf foldername` will delete the folder and everything inside it, instantly and silently.
> This command has destroyed the work of professionals with decades of experience.
> Always pause before pressing Enter when `rm` is involved.

---

### sudo
Prefix for commands that require administrator-level permission. From "superuser do."

**Analogy:** The master key that opens locked rooms in the building. With it, you can change things that normally cannot be changed. The system will ask for your password. This is not paranoia; it is load-bearing caution.

---

### Environment Variable
A piece of information stored in the terminal's memory for the duration of a session, like a note left on the desk that any program running in that terminal can read.

Often used to store sensitive information (API keys, passwords) without writing them directly into your code.

**Analogy:** A Post-it note stuck to the terminal's forehead that only programs running right now can read. When you close the terminal, the Post-it is gone.

---

### API (Application Programming Interface)
A defined way for one piece of software to talk to another. When you use Claude through Open WebUI rather than claude.ai, Open WebUI is communicating with Claude via an API: it sends your message in a structured format, Claude's systems process it and return a structured response, and Open WebUI displays it to you.

You can think of an API as a waiter in a restaurant. You (the application) don't walk into the kitchen and cook your own food. You tell the waiter what you want (the request), the kitchen prepares it (the service), and the waiter brings it back (the response). The kitchen doesn't need to know what you look like; the waiter doesn't need to know how the food is made. Each side only needs to know how to communicate with the one in the middle.

**Why it matters for you:** When you see phrases like "connect via API" or "API key," it means you are setting up a direct programmatic connection to a service, usually with more control and fewer restrictions than a standard consumer interface. An API key is the password that proves you are allowed to make those requests.

## 🌿 PART TWO: GIT AND GITHUB
*The public library with version history*

Git and GitHub are not the same thing. This causes enormous confusion.

- **Git:** A *system* for tracking changes in files over time. It runs locally on your computer.
- **GitHub:** A *website* (owned by Microsoft) that hosts Git repositories online so others can access them.

**Analogy:** Git is the system of footnotes and draft-tracking in a scholarly manuscript. GitHub is the archive library where you deposit the manuscript so others can read it and contribute to it.

---

### Repository (repo)
A folder tracked by Git. Every change to every file inside it is recorded, with timestamps and authorship, and can be recovered.

**Analogy:** An archive box with a complete provenance record. You can always ask: "what did this document look like on March 3rd, at 14:32?"

---

### Commit
A snapshot of your repository at a specific moment, intentionally saved by you with a message describing what changed.

**Analogy:** A dated entry in a research journal. "Added chapter 3 draft. Removed placeholder footnotes." The work is logged; you can return to it.

---

### Branch
A parallel version of your repository where you can make changes without affecting the main version. When the changes are ready, you *merge* the branch back in.

**Analogy:** A scholar photocopies a manuscript to write margin notes on, without touching the original. If the notes are good, they get incorporated into a new edition.

---

### Merge
Combining one branch back into another. Git attempts this automatically; when two people have changed the same lines of the same file, it stops and asks you to decide which version wins. This moment is called a **merge conflict**.

**Analogy:** Two editors returning their annotated copies of the same chapter. If they've marked up different sections, the revisions combine cleanly. If both have rewritten the same paragraph differently, a human must adjudicate.

---

### Clone
Downloading a copy of a repository from GitHub to your local computer, with all its history intact.

---

### Push / Pull
- **Push:** Send your local commits up to GitHub.
- **Pull:** Download changes from GitHub to your local copy.

**Analogy:** Push is submitting your revised draft to the shared archive. Pull is fetching the latest version someone else submitted.

---

### "You are behind by 3 commits"
This means: since you last synced, 3 new snapshots have been added to the shared repository on GitHub that your local copy doesn't have yet. Run `git pull` to catch up.

---

### .gitignore
A file that tells Git which files to *ignore* and never track. Useful for large files, sensitive credentials, or auto-generated clutter.

**Analogy:** A note at the front of the archive box: "do not file drafts, grocery lists, or anything marked TEMP."

---

## 📦 PART THREE: DOCKER
*The sealed moving boxes*

### Container
A self-contained, isolated environment in which a program runs. It includes the program itself plus everything it needs to function: its own mini operating system, its libraries, its dependencies.

**Analogy:** A terrarium. The gecko inside doesn't know or care what's in the room outside. The terrarium maintains its own climate. You can move the terrarium to a different building and the gecko is unaffected.

---

### Image
The *template* from which containers are created. An image is static; a container is a running instance of an image.

**Analogy:** A play manuscript (the image) versus a live performance (the container). You can stage a hundred performances of King Lear from the same manuscript, each running independently.

---

### docker-compose
A tool for defining and running *multiple containers at once*, described in a single configuration file (`docker-compose.yml`). Instead of starting each container separately, one command starts them all.

**Analogy:** A stage manager's cue sheet. One document; everything starts in the right order.

---

### docker-compose.yml
A text file (in a format called YAML, which stands for "Yet Another Markup Language," and yes that name is a joke) that describes which containers to run, how to configure them, and how they connect to each other.

**YAML formatting note:** Indentation is meaningful in YAML. Two spaces in the wrong place can break everything. Tabs are forbidden. This is a design decision that has caused incalculable human suffering.

---

### Volume
A shared folder between your computer and a Docker container. Changes inside the container to that folder are reflected outside, and vice versa.

**Analogy:** A shared inbox tray between two offices that are otherwise completely separate.

---

## ✏️ PART FOUR: VISUAL STUDIO CODE / KILOCODE
*Your writing desk*

### VS Code (Visual Studio Code)
A text editor made by Microsoft, widely used for writing code. It is not the same as Visual Studio (a much heavier development environment). The "Code" is important.

**KiloCode** is an AI-assisted variant or extension layered on top of VS Code. Think of VS Code as the desk and KiloCode as an intelligent lamp that reads over your shoulder and makes suggestions.

---

### Extension
A plugin that adds functionality to VS Code. There are thousands. Some are essential; most can be ignored until you need them.

---

### Integrated Terminal
VS Code has a built-in terminal panel (View > Terminal, or `` Ctrl+` ``). This is a real terminal, not a simulation. Commands you run here affect your actual computer.

**Practical note:** This is usually the terminal you should use while working in VS Code. It starts in your project folder, which saves you from navigating there manually.

---

### Workspace / Project Folder
In VS Code, you typically open a *folder*, not just a file. That folder becomes your "workspace": VS Code tracks it, indexes it, and your terminal starts there.

---

## 🍓 PART FIVE: RASPBERRY PI AND SERVERS
*The quiet machine in the corner*

### Server
A computer that *serves* something to other computers: files, web pages, data, API responses. A server doesn't have to be powerful or large. Your Raspberry Pi is a server.

**Analogy:** A reference librarian who doesn't come to you. You send requests; they retrieve and return the material.

---

### Raspberry Pi
A small, inexpensive single-board computer about the size of a credit card, running Linux. Often used as a home server, a media player, a network device, or a learning tool.

---

### SSH (Secure Shell)
A method of controlling one computer from another, through a terminal, over a network connection. Securely and remotely.

When you SSH into your Raspberry Pi, you are typing commands that run on the Pi, not on your laptop, even though you're sitting at your laptop.

**Analogy:** Calling someone on a secure phone line and dictating instructions. They are the ones pressing the buttons; you are giving the orders from a distance.

**Command:** `ssh username@192.168.x.x` (where the numbers are the Pi's local address)

---

### IP Address
A numerical address identifying a device on a network. Like a house number.

- **Local IP** (e.g., `192.168.1.42`): Only meaningful within your home network.
- **Public IP**: Your address on the open internet. Usually assigned by your internet provider and may change.

---

### Port
A numbered "door" on a device through which a specific kind of traffic enters or exits. A device can have many ports open for different services.

**Analogy:** A harbour with many numbered docks. Dock 80 is for web traffic (HTTP). Dock 443 is for secure web traffic (HTTPS). Dock 22 is reserved for SSH. The ship (data packet) knows which dock to head for.

---

### VPN (Virtual Private Network)
An encrypted tunnel between your device and another network. When active, your internet traffic passes through that tunnel, appearing to originate from the other end.

Two common uses:
1. **Privacy/security:** Your traffic is hidden from your internet provider and anyone watching.
2. **Remote access:** You can reach devices on your home network (like your Raspberry Pi) as if you were physically at home.

**Analogy:** A diplomatic pouch. The contents are sealed, the origin is the embassy, and no customs officer can look inside.

---

### WSL (Windows Subsystem for Linux)
A feature built into Windows that lets you run a full Linux environment directly inside your Windows computer, without rebooting or setting up a separate machine. If you have a penguin icon in your taskbar or start menu, that is WSL.

Why this matters: most developer tools, tutorials, and server software are written for Linux. WSL lets Windows users run these tools natively, without the complications of pretending to be a different operating system. Commands that only work on Linux or Mac will, in most cases, work identically inside WSL.

**Analogy:** A room inside your house that follows entirely different architectural rules. The rest of the house is Windows. You step through a specific door, and suddenly the plumbing, the electrical system, and the building codes are all Linux. You can carry things back and forth between the two sides, but the rules change at the threshold.

**Practical note:** When a tutorial says "run this in your terminal" and you are on Windows, it almost always means "run this in WSL," not in the standard Windows Command Prompt or PowerShell.

## 🔍 PART SIX: BEFORE YOU BLAME THE CODE
*A pre-troubleshooting checklist for when nothing makes sense and you haven't slept enough*

The following problems are responsible for an embarrassing proportion of all technical suffering. They are never covered in tutorials, because the people writing tutorials have long since forgotten that they were ever confusing. Check these first, before you change anything, Google anything, or ask anyone.

---

**Are you looking at the right file?**
Is this the version you think it is? When was it last modified? A stale copy (an outdated version of a file you've already replaced) can make perfectly correct work look broken. Check the file's location and timestamp before assuming something is wrong with its contents.

**Are you in the right folder?**
Type `pwd` in the terminal. Confirm you are where you think you are. An astonishing number of errors occur because a command was run one folder above or below the intended location.

**Are you in the right terminal?**
If you have multiple terminal windows or tabs open, it is entirely possible to be confidently typing commands into the wrong one. The right command in the wrong terminal is the wrong command.

**Are you connected to the internet?**
The cruel feature of most applications is that they load and look normal whether or not they're connected to anything. If something that should sync, update, or communicate is silently failing, check the connection before all else.

**Are you connected to the right network?**
Your home server, your Raspberry Pi, your VPN: these may only be reachable from specific networks. Being online is not the same as being on the right network.

**Have you saved?**
No further comment.

**Have you actually applied the change?**
Edited a configuration file? Restarting the relevant service is often required before changes take effect. The file can be correct and the behavior unchanged until something is reloaded or rebooted.

**Are you looking at a cached version?**
Browsers store copies of web pages to load them faster. If you've made changes that aren't showing up, try a hard refresh (`Ctrl+Shift+R` on most browsers, `Cmd+Shift+R` on Mac) or open the page in a private/incognito window.

**Is it actually broken, or just slow?**
Some processes take time and produce no output while working. Before concluding that something has failed, wait. Then wait a little longer.

**When did it last work?**
If you can answer this precisely, you have narrowed the problem to whatever changed between then and now. That is not a small thing.

---

> A note on dignity: every person who works with technology (including the ones who built it) runs through some version of this list regularly. The difference between a beginner and an expert is not that experts never make these mistakes. It is that they have learned to check for them without embarrassment.

---

## 🤔 PART SEVEN: "WHAT JUST HAPPENED?"
*The ten most common moments of confusion*

---

### "The terminal seems to have deleted everything / is stuck / is doing nothing"

**Most likely:** The program is still running and waiting. Some processes don't display any output while they work.
**Try:** Wait. If it's truly stuck, `Ctrl+C` will interrupt it.
**Less likely but possible:** You ran `rm -rf` on the wrong folder. Check `pwd` first to see where you are, then `ls` to see what's there.

---

### "Git says I'm behind by X commits"

Your local copy is outdated. Someone (possibly you, from another computer) has added commits to GitHub that you don't have locally.
**Solution:** `git pull`

---

### "Permission denied"

You're trying to do something that requires administrator rights.
**Solution:** Try `sudo` before the command. The system will ask for your password. The cursor will not move while you type. This is normal; it's hiding your password.

---

### "Command not found"

The terminal doesn't recognize the word you typed. Either:
1. The program isn't installed.
2. It's installed but the terminal doesn't know where to find it (a "PATH" problem).
3. You made a typo.

Check the typo first. Always check the typo first.

---

### "Port already in use"

Another process is already listening on the port your program wants to use.
**Translation:** Another program has already claimed that numbered parking spot. Only one car per spot.
**Solution:** Either stop the other process, or configure your program to use a different port.

---

### "Connection refused"

You tried to reach something (a server, a port, a service) and it actively turned you away. The server is running, it received your request, and said no.
**Different from:** A timeout, where the server never responded at all.

---

### "It works on my machine"

A sentence spoken by developers since time immemorial, now immortalized in Docker's entire raison d'être. The phrase means: the program functions in one environment but not another. Docker was partially invented to make this sentence obsolete.

---

### "fatal: not a git repository"

You tried to run a Git command in a folder that Git isn't tracking.
**Solution:** Either navigate to the correct repository folder (`cd`), or initialize Git in the current folder (`git init`, but only if you actually want to start tracking it).

---

### "HEAD detached"

Git has a concept of HEAD, meaning "where you currently are in the history." A detached HEAD means you're looking at a specific past commit rather than a branch.
**Analogy:** You've navigated to a specific archived edition of a manuscript rather than the living working copy. You can read; you should probably not write.
**Solution:** `git switch main` (or `git checkout main`) to return to the current version.

---

### "The container keeps restarting"

Docker tried to start a container; the container crashed; Docker tried again; it crashed again. This loop continues until you intervene.
**Translation:** The terrarium's climate system is failing and keeps rebooting.
**Solution:** `docker logs containername` to see why it's crashing. The answer is usually in the last few lines.

---

## 🪞 APPENDIX: FALSE FRIENDS
*Words that sound like they mean something else*

| Tech word | What you might think | What it actually means |
|---|---|---|
| **Root** | A plant metaphor | The topmost administrator account on a Linux system; also the top-level directory `/` |
| **Shell** | A seashell or artillery | The command interpreter running inside your terminal |
| **Fork** | Cutlery | Creating a personal copy of someone else's GitHub repository |
| **Clone** | Science fiction | Downloading a full copy of a repository, history and all |
| **Kill** | Violence | Stopping a running process, usually cleanly |
| **Daemon** | Mythology | A background process that runs continuously without user interaction (web servers, for example, are daemons) |
| **Argument** | A disagreement | Extra information passed to a command (`ls -la`, where `-la` is the argument) |
| **Flag** | A banner | A special argument starting with `-` that modifies a command's behavior |
| **Environment** | Nature | The set of variables and settings active in a current terminal session |
| **Master/Main** | Leadership | The primary branch in a Git repository (older repos say "master"; newer say "main") |

---

## 🤖 PART EIGHT: THE AI LAYER
*The new neighborhood, still under construction*

A note before we begin: this is the fastest-moving part of the document. Names, models, and capabilities shift monthly. The concepts below are stable; the specific products are a snapshot of early 2026.

---

### LLM (Large Language Model)
The engine underneath almost everything currently called "AI." An LLM is a statistical system trained on enormous amounts of text, which has learned to predict what word, sentence, or paragraph comes next with uncanny coherence. It does not think, reason, or understand in any human sense, but it has learned the patterns of human thought well enough to produce text that reads as if it does.

**What it can do:** Write, summarize, translate, explain, analyze, generate code, answer questions, hold a conversation.

**What it cannot do:** Browse the internet on its own, remember previous conversations by default, take actions in the world, or guarantee factual accuracy. An LLM that sounds confident is not the same as an LLM that is correct.

**Analogy:** A vastly well-read correspondent who has absorbed most of the written world and can respond to almost any letter, but who is working entirely from memory, has no access to today's newspaper, and occasionally confabulates plausible-sounding facts with complete conviction.

**A critical warning about how LLMs are trained:** Most models are optimized, at least partly, to make you feel satisfied. A satisfied user clicks "thumbs up." An unsatisfied user clicks "thumbs down." The model has therefore learned, at a deep level, that giving you an answer you find plausible feels better to you than saying "I don't know." This means that when a model doesn't know something, it will often generate a confident-sounding answer anyway rather than admit uncertainty. This is not malice. It is a structural consequence of how these systems are trained. The practical result: the more confidently a model states something you cannot independently verify, the more carefully you should verify it. A model that hedges and expresses uncertainty is often more trustworthy than one that never does.

**On reliability across models:** Not all models are equally honest about their limitations. Some are significantly more prone to confabulation than others. Some have been given ad hoc guardrails that produce bizarre, unpredictable behavior on innocent queries. And some models prioritize ideological positioning over accuracy. Treat different models the way you would treat different sources: with calibrated, source-specific skepticism.

---

### AI Agent
An LLM that has been given *tools* and the ability to take actions: browsing the web, writing and executing code, reading and editing files, sending requests to other services. The underlying language model is the brain; the tools are the hands.

The crucial distinction: an LLM *responds*. An agent *acts*. An agent can be given a goal and pursue it across multiple steps without asking for confirmation at each one.

**Analogy:** If an LLM is the well-read correspondent, an agent is that same correspondent given a telephone, a library card, a computer, and instructions to handle the matter independently. More powerful, and requiring proportionally more trust.

**Practical note:** When you use a model through a simple chat interface, you are talking to something close to a pure LLM. When a model searches the web, runs code, or updates a file on your behalf mid-conversation, it is functioning as an agent.

---

### On-Premises (On-Prem)
Running software on hardware you own and control, physically located where you are: your laptop, your server, your Raspberry Pi. Nothing leaves your building. No subscription, no third-party access, no data sent to anyone else's servers.

**The tradeoff:** Full privacy and control, but you are responsible for setup, maintenance, updates, and the hardware costs. The model you can run is limited by what your own machine can handle.

**Analogy:** Owning a printing press. Expensive to set up, requires maintenance, but everything produced stays in-house and no one else knows what you're printing.

---

### Off-Premises (Off-Prem) / Cloud
Running software on someone else's hardware, accessed over the internet. When you use Claude at claude.ai, ChatGPT at chat.openai.com, or Gemini at gemini.google.com, you are sending your text to a server in a data center somewhere and receiving a response back. You are renting access to a vastly powerful machine you could never afford to own.

**The tradeoff:** Effortless access to the most capable models available, but your data passes through another company's infrastructure. For most purposes this is fine; for sensitive documents, it is worth thinking about.

**Analogy:** Renting time at a commercial printing house. Enormous capability, no maintenance, but the printer can see what you're printing.

**A note on nuance:** Many setups are hybrid. Open WebUI, for example, can connect to either a local model (on-prem) or a remote API (off-prem). The interface is the same; the data routing is different.

---

### The Major LLM Providers and Their Frontier Models
*A brief field guide, as of early 2026*

"Frontier model" is the industry term for the most capable, most recently released model a provider offers. The frontier moves constantly. What follows are the main players and their current flagship offerings.

**Anthropic / Claude**
Founded by former OpenAI researchers with a stated focus on AI safety. Their models are named Claude, currently in the Claude 4 family (Sonnet and Opus being the main variants: Sonnet for everyday use, Opus for more demanding tasks). Anthropic's distinctive position is that they publish research on making models safer and more interpretable, and have an unusually explicit philosophy about what their models should and should not do.

*Training data:* A broad mix of web text, books, code, and academic writing, with significant emphasis on safety-relevant material and explicit guidelines for how the model should reason and behave. Claude is specifically trained to express uncertainty rather than confabulate, and to say "I don't know" when it doesn't.

**OpenAI / ChatGPT and GPT models**
The company that made LLMs a household topic with the release of ChatGPT in late 2022. Their models are the GPT series; ChatGPT is the consumer product built on top of them. Currently also developing the o-series models, which are designed to "reason" more carefully before responding. OpenAI receives significant investment from Microsoft, and their models power many third-party applications.

*Training data:* A very large and broad web corpus, including a significant amount of social media, forums, and general internet text. This gives ChatGPT a conversational, accommodating tone, but also means it can be prone to telling you what you want to hear. Users have documented cases of the model confidently maintaining incorrect positions rather than acknowledging errors, which is worth keeping in mind for any factual query you cannot independently verify.

**Google / Gemini**
Google's frontier model family, integrated into Google's products (Docs, Search, Gmail) as well as available as a standalone product. Google's advantage is access to real-time Search and an enormous existing user base. Their most capable variant is Gemini Ultra; the lighter version, Gemini Flash, is optimized for speed.

*Training data:* Google has access to an extraordinary breadth of indexed web content, including books via Google Books and academic material. The integration with live Search means Gemini can be more current than models working from a static training snapshot. However, live search introduces its own failure mode: the model retrieves whatever has the most search presence at that moment, which is not always the most accurate or recent information. If a false rumor about a public figure accumulated thousands of search results over several years, and the true breaking news is only minutes old, the model may confidently report the rumor as fact and dismiss the truth as unverified. Recency and searchability are not the same as accuracy.

**Meta / Llama**
Meta (formerly Facebook) releases their Llama model family as *open weights*, meaning the model files themselves are publicly available to download and run locally. This makes Meta's models the most common choice for on-prem deployment. They are not the most capable at the frontier, but they are free, private, and run on your own hardware.

*Training data:* Publicly available web text, with Meta's access to its own platforms (Facebook, Instagram) presumably informing some of its conversational character. Because the weights are open, researchers can study and audit the model more closely than closed alternatives. The social media component is worth keeping in mind: a model trained partly on Facebook posts and Instagram comments will have absorbed not only vast amounts of ordinary human communication, but also its misinformation, its tribalism, and its particular rhetorical habits.

**xAI / Grok**
Elon Musk's AI company, with a model called Grok integrated into the X (formerly Twitter) platform. Grok has access to real-time X data, which gives it currency on certain topics.

However, Grok has attracted significant criticism for the consequences of its tuning. In an apparent effort to position it as ideologically "anti-woke," xAI applied system-level instructions that have produced genuinely alarming outputs: unprompted defenses of historical atrocities, the generation of inappropriate content involving minors, and erratic responses to ordinary queries. This is not a matter of political opinion. It is a documented reliability and safety problem. A model that has been steered by ad hoc ideological guardrails rather than principled safety work is a model whose outputs cannot be trusted consistently. Use with corresponding skepticism.

*Training data:* Primarily X (Twitter) data, which shapes its conversational register strongly toward the particular culture of that platform.

**Mistral**
A French AI company producing capable, efficient models, also released as open weights. Popular for on-prem use, especially in European contexts where data sovereignty is a concern. Smaller and faster than Llama at equivalent quality in many tasks.

*Training data:* Web text with a notable emphasis on European multilingual sources and code. This makes Mistral models particularly competitive on non-English European languages.

**A note on the landscape:** These companies are in intense competition. Capability rankings shift with each new release. The right question is rarely "which is best" and almost always "which is appropriate for this task, this privacy context, and this budget."

---

### Hugging Face
A platform for sharing, discovering, and running AI models, datasets, and related tools. Think of it as the GitHub of the AI world: researchers and developers upload model weights, training datasets, and demo applications, and anyone can browse, download, or run them. Many of the open-weight models mentioned above (Llama, Mistral, and thousands of others) are distributed through Hugging Face.

It also hosts "Spaces," which are small interactive demo applications where you can try a model directly in your browser without installing anything. For a first encounter with a new model, a Hugging Face Space is often the lowest-friction option available.

*Training data relevance:* Hugging Face also hosts datasets, which means it is one of the places where you can actually look at what a model was trained on, if the creators chose to share it. This makes it a useful resource for the skeptical reader who wants to understand where a model's knowledge (and biases) come from.

 Capability rankings shift with each new release. The right question is rarely "which is best" and almost always "which is appropriate for this task, this privacy context, and this budget."

---

### Open WebUI
A browser-based interface for talking to AI models, either local models running on your own machine or remote models accessed via API. It looks and feels like ChatGPT or Claude's chat interface, but it runs on your own infrastructure and connects to whichever models you choose.

**What it gives you:** A single, familiar interface for multiple models; conversation history; the ability to organize conversations into folders; Notes; system prompts; and model workspaces, all under your own control, on your own server.

**What it is not:** A model itself. Open WebUI has no intelligence of its own. It is the window; the model is the person you see and speak with through it. Change the model, and you are speaking with someone entirely different, through the same window.

**Analogy:** A universal telephone handset that works with any telephone network you plug it into. The handset is always the same; the network (and who answers) changes depending on your configuration.

**In a typical setup:** Open WebUI runs on a Raspberry Pi or local server, accessible from a browser on any device on the same network. The models it connects to may be local (Ollama) or remote (a cloud API, for example).

---

### Ollama
A tool for downloading and running open-weight LLMs locally on your own machine, with minimal setup. You tell Ollama which model you want, it downloads it, and it runs it. Open WebUI can connect to Ollama as its model source, making the two tools natural companions.

**What it gives you:** On-prem LLM access with a simple interface. No subscription, no internet connection required once the model is downloaded, no data leaving your machine.

**The limitation:** You are constrained by your own hardware. Large, capable models require significant RAM and, ideally, a good GPU. On a Raspberry Pi or a modest laptop, you will be running smaller, less capable models than what frontier cloud providers offer.

**Analogy:** A personal library of books you actually own. Slower to acquire than a streaming service, takes up physical space, limited by what you can afford. But entirely yours, available without internet, and readable by no one but you.

---

### LM Studio
A desktop application for downloading, managing, and running local LLMs with a graphical interface. Where Ollama is command-line first (you interact with it mainly through a terminal), LM Studio offers a visual interface: you browse available models, download them, and chat with them directly within the application.

**The relationship between LM Studio and Ollama:** Both do similar things. LM Studio is more beginner-friendly and self-contained; Ollama is more flexible for integration with other tools like Open WebUI. Many people use Ollama for their day-to-day setup and LM Studio for exploring or testing new models.

**Analogy:** If Ollama is the library's card catalogue and stacks (functional, efficient, designed for the experienced user), LM Studio is the library with a reading room, comfortable chairs, and a recommended titles display by the door.

## 🛠️ SCRATCHPAD: ENTRIES FOR TTfH 1.1
*New entries go here, written in full TTfH style, until it is time to place them in their rightful sections and release version 1.1.*

*Do not edit above this line.*

---

*Last updated: March 2026*
*This document is intentionally incomplete. A map that shows every alley is not a map; it's the city.*
