# The YouTube agent skill

Eleven upstream ChatGPT skills plus `yt-caliks`, a dedicated entry point for Çalık'S Art
Academy. Free, MIT, no signup, no API key, nothing to connect.

This repository is a fork of [Jake Schincariol's original project](https://github.com/Jakeschincariol/chatgpt-youtube-agent-skill).
The original skills and helper scripts retain his attribution and MIT license.

One of them writes your script off 21 hook formulas and scores the hook before you waste a take on
it. One lints the title and the thumbnail as a single pairing, because writing them separately is
why half of your click surface says the same thing twice. One reads your audience-retention export
and tells you the exact second people left and what you were saying when they did. One turns a
transcript into an edit decision list. One finds the Shorts already hiding inside a long video. One
goes and finds what is working in your niche and ranks it by how far each video beat its own
channel, not by how big the channel is.

**Nothing gets published until you do it.** These skills write. You upload.

## Install

### YouTube Agent plugin

The repository is also a skills-only **YouTube Agent** plugin. It exposes `yt-caliks` and
all eleven upstream `yt-*` skills from `skills/`, including their Python helpers and hook formulas.
Python 3 runs the helpers; no MCP server, API key, or new Python dependency is required.

From this checkout, register the local marketplace and install the plugin with a recent Codex CLI:

```bash
codex plugin marketplace add .
codex plugin list --marketplace youtube-agent-marketplace --available --json
codex plugin add youtube-agent@youtube-agent-marketplace
```

Restart Codex or start a new session after installation. Select **YouTube Agent** and invoke
`yt-caliks` for Çalık'S Art Academy, or select an upstream skill from the skill picker.
After updating an installed plugin, reload/reinstall it using the host's supported flow.

`plugin.json` is the portable Agent Plugins 1.0 manifest for compatible Codex/ChatGPT hosts.
`.codex-plugin/plugin.json` is the Codex compatibility manifest and points to `./skills/`.
`.agents/plugins/marketplace.json` registers the repository root as the plugin source; its `./`
path is relative to the repository root, not the manifest directory. Keep the two plugin
manifests' metadata and interface fields synchronized when making future changes.

For a ChatGPT package, put `plugin.json`, `.codex-plugin/`, `skills/`, `templates/`,
`profiles/`, `AGENTS.md`, and `LICENSE` inside a single `youtube-agent/` directory.
Archive that directory, including hidden files.
Use the host's plugin import flow. The repository configuration does not upload or install the
plugin into a ChatGPT account.

Run the dependency-free structural and helper smoke tests from the repository root:

```bash
python3 -B -m unittest discover -s tests -v
```

### Individual skills

Paste this link into ChatGPT and say **install skill**:

```
https://github.com/jrvsuur-afk/chatgpt-youtube-agent-skill
```

Or do it yourself:

```bash
git clone https://github.com/jrvsuur-afk/chatgpt-youtube-agent-skill
mkdir -p ~/.codex/skills ~/.codex/profiles
cp -r chatgpt-youtube-agent-skill/skills/yt-* ~/.codex/skills/
cp -r chatgpt-youtube-agent-skill/profiles/. ~/.codex/profiles/
```

For `yt-caliks`, use this fork's checkout; the original repository contains the eleven
upstream skills. Restart the app after copying. Project-local instead of global: copy the
skill folders into `.codex/skills/` and the profiles into `.codex/profiles/`. This checkout
already provides `.agents/skills/` and `.codex/skills/` links to its canonical `skills/` folders.

## Skills

| skill | what it does |
|---|---|
| `yt-caliks` | reads the Çalık'S profile and routes to the appropriate upstream skill |
| `yt-script` | writes the script off 21 hook formulas, scores the hook |
| `yt-package` | title and thumbnail linted as one pairing |
| `yt-viral` | finds what is working in your niche, ranked by channel-relative lift |
| `yt-retention` | reads your retention export, names the second people left |
| `yt-edit` | transcript to an edit decision list, dead air flagged |
| `yt-plan` | the week's upload schedule |
| `yt-comment` | drafts replies in your voice |
| `yt-seo` | description, tags, and search surface |
| `yt-chapters` | chapter markers off the transcript |
| `yt-shorts` | finds the Shorts hiding in a long video |
| `yt-audit` | reads a channel and says what is actually wrong |

## Çalık'S Art Academy entry point

[`yt-caliks`](skills/yt-caliks/SKILL.md) reads `profiles/caliks-art-academy.md` on every
invocation, then reads the appropriate upstream instructions. With only a structured
video analysis, it defaults to the seven-part SEO package:

```text
yt-caliks
[Video analizi]
```

Explicit subtasks take priority, such as `yt-caliks package` for title + thumbnail,
`yt-caliks shorts` for Shorts extraction, or `yt-caliks script` for a script. It also
supports `seo`, `plan`, `viral`, `retention`, `audit`, `chapters`, `edit`, and `comment`.
Each subtask keeps its upstream technical workflow while applying relevant channel rules.
Structured analyses are used without reanalyzing raw footage. No content task edits files,
commits, or pushes. The profile and referenced upstream folders must travel with this skill.

## Your voice

Copy `templates/voice.md` to `~/.codex/youtube/voice.md` and fill it in. Every skill reads it.
Or send ChatGPT three of your own videos and say "write my voice profile from these".

## Channel profiles

[`profiles/caliks-art-academy.md`](profiles/caliks-art-academy.md) adds Turkish-first
Shorts SEO rules only for **Çalık'S Art Academy**, including English, German, and Japanese
titles/descriptions, topical tags, and fixed plus topical hashtags. It keeps titles short
and focused on the verified subject, and uses current search or trend data only when you
supply it. To select it manually:

```text
yt-seo skill'ini kullan. Önce profiles/caliks-art-academy.md dosyasını oku.
Bu görev Çalık'S Art Academy için; tüm çıktı kurallarını bu profilden uygula.
Aşağıdaki yapılandırılmış video analizini kaynak kabul et; ham videoyu yeniden analiz etme.
Başlıklar kısa ve ana konuya odaklı olsun; jenerik ekleri otomatik kullanma.
Belirsiz motif, stil, vücut bölgesi veya teknik bilgi uydurma.
Türkçe açıklama en fazla iki kısa cümle; diğer dillerdeki açıklamalar da kısa ve doğal olsun.
Varsa sağladığım güncel arama veya trend verisindeki ilgili terimlere öncelik ver;
veri yoksa güncel trend iddiası üretme.
Yalnızca profilin yedi bölümlük çıktısını ver; giriş, analiz veya gerekçe ekleme.
[Video analizi]
[Güncel arama terimleri veya trend verisi, varsa; yoksa bu satırı çıkar]
```

The path is relative to this checkout; use a readable checkout path or attach the profile
if needed. The eleven skills and the global voice profile remain separate.

### Automatic profile routing

When this repository is the active workspace and the host reads its root
[`AGENTS.md`](AGENTS.md), the eleven upstream `yt-*` skills read the relevant channel profile
first. The dedicated `yt-caliks` entry point reads its profile through its own instructions.
The default is `profiles/caliks-art-academy.md`; a structured video analysis without
another channel also selects Çalık'S Art Academy. An explicit other channel/profile uses
its match under `profiles/`, or reports that a new profile is needed. Channel preferences
supplement each skill's technical instructions; ordinary content tasks do not edit files,
commit, or push.

For example, no profile path is needed in this workspace:

```text
yt-seo skill'ini kullan. Aşağıdaki yapılandırılmış video analizinden YouTube metinlerini üret.
[Video analizi]
```

Installing the individual skills in another workspace does not automatically load this
repository's `AGENTS.md`; provide the routing instructions and profile there explicitly.

## The tools

Six dependency-free Python scripts, no packages to install: `hookscore.py`, `title.py`,
`deadair.py`, `chapters.py`, `retention.py`, `swipe.py`.

MIT.
