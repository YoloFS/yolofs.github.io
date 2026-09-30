# SOSP '26 LinkedIn post

## Post

"No problems occurred," said an AI coding agent, right after erasing a user's file.

Our SOSP '26 paper studies 290 incidents like this and builds YoloFS, a filesystem where agents undo their own mistakes.

Coding agents run shell commands on our machines with our full privileges. The reports show what goes wrong: wiped home directories, 110 legal documents deleted from iCloud, SSH credentials leaked through a prompt-injected README. 40% of the damage was unrecoverable, and most of the time the agent never noticed.

We argue the fix belongs in the filesystem, which sees every access from every tool. We propose agent-native filesystems, and YoloFS is one. It works with Claude Code, Copilot, and Gemini:  
→ The agent sees what each command actually changed  
→ It can undo its own mistakes, thanks to a snapshot after every command  
→ Reading secrets, like your SSH key, pauses and asks you first  
Nothing reaches your real files until you commit.

The video shows all three on one malicious setup script.

On new benchmarks that run real agents with approval prompts on, Claude Code with YoloFS self-corrected in 8 of 11 tasks with hidden damage (0 without), and needed half as many approval prompts on 112 routine tasks.

Junxuan presents it today at 4pm at SOSP in Prague. Joint work with @Junxuan Liao, @Jing Liu, @Mai Zheng, @Andrea Arpaci-Dusseau, and @Remzi Arpaci-Dusseau (@University of Wisconsin-Madison, @Microsoft Research, @Iowa State University).

Paper, code, slides, and poster: https://yolofs.github.io

#SOSP #OperatingSystems #AIAgents #AISafety

## Before posting

- Attach `../demo/demo.mp4`, and set `../demo/cover.png` as its thumbnail (desktop only). Run `uv run demo.py` in `../demo/` to rebuild both.
- Retype each `@Name` by typing `@` and picking the person or page from the list, or it stays plain text and nobody is tagged.
- Change "today at 4pm" if you post on another day.
- Keep the link in the post, not in a comment: LinkedIn now shows comments with links to fewer people too.
