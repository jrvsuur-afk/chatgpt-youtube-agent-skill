# The YouTube agent skill

Eleven ChatGPT skills that run a YouTube channel. Free, MIT, no signup, no API key, nothing to
connect.

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

The repository is also a skills-only **YouTube Agent** plugin. It exposes all eleven `yt-*`
skills from the original `skills/` directory, including their Python helpers and hook formulas.
Python 3 runs the helpers; no MCP server, API key, or new Python dependency is required.

From this checkout, register the local marketplace and install the plugin with a recent Codex CLI:

```bash
codex plugin marketplace add .
codex plugin list --marketplace youtube-agent-marketplace --available --json
codex plugin add youtube-agent@youtube-agent-marketplace
```

Restart Codex or start a new session after installation. Select **YouTube Agent**, or invoke a
skill such as `yt-script`, `yt-package`, or `yt-audit` from the skill picker.

`plugin.json` is the portable Agent Plugins 1.0 manifest for compatible Codex/ChatGPT hosts.
`.codex-plugin/plugin.json` is the Codex compatibility manifest and points to `./skills/`.
`.agents/plugins/marketplace.json` registers the repository root as the plugin source; its `./`
path is relative to the repository root, not the manifest directory. Keep the two plugin
manifests' metadata and interface fields synchronized when making future changes.

For a ChatGPT package, put `plugin.json`, `.codex-plugin/`, `skills/`, `templates/`, and `LICENSE`
inside a single `youtube-agent/` directory and archive that directory, including hidden files.
Use the host's plugin import flow. The repository configuration does not upload or install the
plugin into a ChatGPT account.

Run the dependency-free structural and helper smoke tests from the repository root:

```bash
python3 -B -m unittest discover -s tests -v
```

### Individual skills

Paste this link into ChatGPT and say **install skill**:

```
https://github.com/Jakeschincariol/chatgpt-youtube-agent-skill
```

Or do it yourself:

```bash
git clone https://github.com/Jakeschincariol/chatgpt-youtube-agent-skill
cp -r chatgpt-youtube-agent-skill/skills/yt-* ~/.codex/skills/
```

Restart the app and the skills are available. Project-local instead of global: copy the same
folders into your repo's `.codex/skills/`.

## The eleven

| skill | what it does |
|---|---|
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

## Your voice

Copy `templates/voice.md` to `~/.codex/youtube/voice.md` and fill it in. Every skill reads it.
Or send ChatGPT three of your own videos and say "write my voice profile from these".

## The tools

Six dependency-free Python scripts, no packages to install: `hookscore.py`, `title.py`,
`deadair.py`, `chapters.py`, `retention.py`, `swipe.py`.

MIT.
