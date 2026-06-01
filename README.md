# VoiceEbook

<div align="center">

🎙️ **Turn any eBook into an audiobook — in your own voice.**

[![License](https://img.shields.io/badge/license-MIT-blue)](LICENSE)
[![Status](https://img.shields.io/badge/status-beta-orange)]()
[![Platform](https://img.shields.io/badge/platform-macOS%20%7C%20Windows%20%7C%20Linux-lightgrey)]()
[![Voice Cloning](https://img.shields.io/badge/voice%20cloning-3s%20sample-brightgreen)]()

> ⚠️ **Beta:** VoiceEbook is under active development. Expect rough edges.

</div>

---

## What is VoiceEbook?

VoiceEbook converts eBooks (EPUB, PDF, plain text) into audiobooks narrated in **your cloned voice** — or any voice you design. Powered by zero-shot voice cloning, it takes just a 3-second sample to capture a speaker's voice, then reads your entire library back to you in that voice.

---

## Screenshot

> *(Add your screenshot here — drop it in `docs/images/screenshot.png` and uncomment the line below)*
>
> <!-- ![VoiceEbook Screenshot](docs/images/screenshot.png) -->

---

## Features

<table>
  <tr>
    <td>🎤 <b>Voice Cloning</b><br>3-second sample, zero-shot</td>
    <td>📚 <b>eBook Import</b><br>EPUB, PDF, TXT supported</td>
  </tr>
  <tr>
    <td>🌍 <b>Multilingual</b><br>Narrate in 30+ languages</td>
    <td>🎨 <b>Voice Design</b><br>Adjust tone, pace, and style</td>
  </tr>
  <tr>
    <td>⚡ <b>Batch Processing</b><br>Convert entire libraries overnight</td>
    <td>🎧 <b>Audio Export</b><br>MP3, WAV, M4B (chapter-aware)</td>
  </tr>
  <tr>
    <td>🔒 <b>Fully Local</b><br>Your voice stays on your machine</td>
    <td>🗂️ <b>Chapter Detection</b><br>Auto-splits by chapter headings</td>
  </tr>
</table>

---

## Quickstart

```bash
# 1. Clone the repo
git clone https://github.com/retromedievalism/VoiceEbook.git
cd VoiceEbook

# 2. Install dependencies
pip install -r requirements.txt   # or: npm install

# 3. Record or drop in a 3-second voice sample
cp my_voice_sample.wav samples/

# 4. Convert an eBook
python voiceebook.py --input my_book.epub --voice samples/my_voice_sample.wav --output my_audiobook.m4b
```

---

## How Voice Cloning Works

1. **Record** 3 seconds of your voice (or any speaker's voice)
2. VoiceEbook extracts a voice embedding — no training required
3. The TTS engine synthesizes all narration in that voice
4. Audio is stitched together chapter-by-chapter into a single audiobook file

---

## Comparison

| Feature | ElevenLabs | VoiceEbook |
|---|---|---|
| Price | $5–$330/mo | Free & open source |
| Voice clone sample | 30s clip | 3s clip, zero-shot |
| Runs locally | ❌ Cloud only | ✅ Fully local |
| eBook-native workflow | ❌ | ✅ |
| Chapter-aware output | ❌ | ✅ |
| Languages | 32 | 30+ |
| Batch library conversion | ❌ | ✅ |

---

## System Requirements

| Component | Minimum | Recommended |
|---|---|---|
| OS | macOS 12 / Windows 10 / Ubuntu 20.04 | Latest |
| RAM | 8 GB | 16 GB |
| GPU | None (CPU mode) | NVIDIA with 6GB VRAM |
| Python | 3.10+ | 3.11+ |
| Storage | 2 GB | 10 GB (for model cache) |

---

## Architecture

```
VoiceEbook/
├── voiceebook.py        # CLI entry point
├── src/
│   ├── parser/          # EPUB / PDF / TXT ingestion
│   ├── tts/             # TTS engine + voice cloning
│   ├── audio/           # Audio stitching + export
│   └── ui/              # Optional desktop UI
├── samples/             # Drop voice samples here
├── docs/
│   └── images/          # Screenshots for README
└── requirements.txt
```

---

## FAQ

**Can I use someone else's voice?**
Only with their explicit consent. VoiceEbook is built for personal use with your own voice.

**Does it work offline?**
Yes. After the first model download, everything runs locally — no internet required.

**What eBook formats are supported?**
EPUB and plain text work best. PDF support is experimental (text extraction quality varies by PDF).

**How long does conversion take?**
A 300-page book takes roughly 20–40 minutes on CPU, 5–10 minutes with a GPU.

---

## Contributing

Pull requests welcome. For large changes, open an issue first to discuss direction.

```bash
git checkout -b feature/your-feature
# make changes
git commit -m "add: your feature description"
git push origin feature/your-feature
# open a PR
```

---

## License

[MIT](LICENSE) — free to use, modify, and distribute.

---

<div align="center">
Made with ❤️ for people who want their books read back to them, in their own voice.
</div>
