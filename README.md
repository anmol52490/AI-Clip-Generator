# AI Video Generator

A simple web app that generates short animated videos from text prompts using AI.

## Live Demo
[https://huggingface.co/spaces/Anmol52490/video-clip](https://huggingface.co/spaces/Anmol52490/video-clip)

## How It Works

Since actual video generation APIs are expensive, I took a different approach:
1. Generate an image from text using Stable Diffusion
2. Create a simple zoom animation from that image
3. Output as MP4 video

It's not fancy, but it works and costs nothing to run.

## The Problem I Faced

Initially tried deploying on Railway and Render, but AI models need a lot of memory (4GB+) and these platforms either:
- Have tiny free tiers (Railway: 512MB)
- Go to sleep too often (Render)
- Cost money for decent resources

Hugging Face Spaces turned out to be the only platform that actually works for free AI deployments.

## Setup

### Local Development

1. Clone the repo:
```bash
git clone https://github.com/anmol52490/AI-Clip-Backend.git
cd AI-Clip-Backend
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the app:
```bash
python app.py
```

Go to `http://localhost:7860`

### Deploy to Hugging Face Spaces

1. Create account at [huggingface.co](https://huggingface.co)
2. Create a new Space (choose Gradio SDK)
3. Upload `app.py` and `requirements.txt`
4. Wait for it to build

**Important**: You'll need a Hugging Face account to download the model. The app handles this automatically when deployed on HF Spaces, but for local development, you might need to run:
```bash
huggingface-cli login
```

## Performance

- **CPU (free)**: ~30-60 seconds per video
- **GPU (also free on HF)**: ~10-20 seconds per video

The first generation takes longer because it downloads the model.

## Tech Stack

- **Model**: SD-Turbo (fast Stable Diffusion variant)
- **Frontend**: Gradio
- **Animation**: OpenCV + imageio
- **Deployment**: Hugging Face Spaces

## Files

- `app.py` - Main application
- `requirements.txt` - Dependencies
- `README.md` - This file

## Limitations

- Videos are only 4-5 seconds long
- Only zoom animation (could add more effects)
- Quality depends on the base image generation
- No audio

## Why This Approach?

Real video generation would require:
- Expensive APIs ($0.10+ per video)
- Complex model serving infrastructure
- Lots of VRAM/compute

This solution generates decent results for free by being creative with image animation.

## Issues You Might Face

1. **Model loading fails**: Usually memory issues. Try restarting the Space.
2. **Slow generation**: Normal on CPU. GPU helps but isn't always available.
3. **Video creation fails**: Sometimes opencv has issues. Refresh and try again.

## Contributing

Feel free to improve it. Some ideas:
- Add more animation types
- Make video length configurable
- Better error handling
- Audio support

## Contact

If you have questions or find bugs, open an issue or reach out.
