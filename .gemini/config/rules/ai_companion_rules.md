# AI Companion Workspace Rules (`kalyani` + `anondo`)

Always read and strictly follow [`/usr/local/google/home/koushikchak/ai-companion/GEMINI.md`](file:///usr/local/google/home/koushikchak/ai-companion/GEMINI.md):

1. **Strict Repo Isolation:** Keep all AI Companion code, docs, modular persona packages (`personas/kalyani/` & `personas/anondo/`), audio, and rules inside `/usr/local/google/home/koushikchak/ai-companion` (100% separate from `koushik-wiki`).
2. **Modular Two-Persona Architecture:** Maintain strict symmetry across `personas/{kalyani,anondo}/`, `content/{kalyani,anondo}/`, `src/{kalyani,anondo,templates}/`, `assets/{kalyani,anondo}/`, and `audio/{kalyani,anondo}/`, compiling into `kalyani.html`, `anondo.html`, and the `index.html` Persona Hub via `scripts/build_app.py`.
3. **Pure Agentic LLM Curation Gate (`scripts/curate_loop.py`):** Every content update must cross-reference `personas/<id>/{persona,curriculum,content_curation}.md` and pass all 12 quality dimensions (`python3 scripts/curate_loop.py --persona <kalyani|anondo> --live-loop`).
4. **Show Content First & 1-Commit `ai-companion-audio` Orphan Branch:** Never run TTS automatically before Koushik approves content; only run `python3 scripts/refresh_voices.py --persona <kalyani|anondo> --confirm --publish` upon explicit confirmation.
