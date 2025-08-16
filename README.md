# 🎬 AI Video Generator - Peppo Technical Challenge

## Project Overview

This project is a **minimal AI video generation web application** built for the Peppo AI Engineering Internship technical challenge. The application takes user text prompts and generates short animated videos using AI-powered image generation followed by dynamic animation effects.

### 🔗 **Live Demo**: [Hosted Solution](https://huggingface.co/spaces/Anmol52490/video-clip)

---

## 🎯 Solution Approach

### **Core Concept: Text → Image → Animated Video**

Instead of using expensive video generation APIs, I implemented a cost-effective approach:

1. **Text-to-Image Generation**: Using Stability AI's SD-Turbo model to generate high-quality images from text prompts
2. **Image Animation**: Converting static images into dynamic videos using programmatic animation effects (zoom, pan, rotate)
3. **Video Output**: Rendering final MP4 videos with smooth transitions

### **Why This Approach?**

- ✅ **Cost-Effective**: No expensive API calls required
- ✅ **Open Source**: Uses freely available models
- ✅ **Fast Generation**: SD-Turbo generates images in 1 step vs traditional 20-50 steps
- ✅ **Scalable**: Can run on CPU or GPU
- ✅ **Customizable**: Easy to add new animation effects

---

## 🏗️ Technical Architecture

### **Frontend**: Gradio Web Interface
- Interactive web UI with real-time progress tracking
- Responsive design optimized for both desktop and mobile
- Built-in examples and user guidance

### **Backend**: Python + Diffusers + OpenCV
- **Model**: `stabilityai/sd-turbo` (Ultra-fast Stable Diffusion variant)
- **Image Processing**: PIL + OpenCV for animation effects
- **Video Encoding**: ImageIO with FFmpeg backend
- **Memory Management**: Optimized for both CPU and GPU deployment

### **Animation Engine**
```python
# Core animation logic
for i in range(num_frames):
    scale = 1.0 + (0.2 * i / num_frames)  # Zoom effect
    M = cv2.getRotationMatrix2D((width / 2, height / 2), 0, scale)
    zoomed_frame = cv2.warpAffine(img_np, M, (width, height))
    writer.append_data(zoomed_frame)
```

---

## 🚀 Deployment Journey

### **Attempted Platforms & Challenges**

| Platform | Status | Issue | Solution |
|----------|--------|-------|----------|
| **Railway** | ❌ Failed | 512MB RAM limit, model requires 4GB+ | Switched to HF Spaces |
| **Render** | ❌ Failed | Cold starts, memory constraints | Tried optimization, still insufficient |
| **Vercel** | ❌ Failed | Serverless limitations, no persistent storage | Not suitable for AI models |
| **AWS/GCP** | 💰 Expensive | Free tier insufficient for AI workloads | Chose free alternative |
| **Hugging Face Spaces** | ✅ **Success** | Free GPU/CPU, AI-optimized infrastructure | **Final deployment** |

### **Why Hugging Face Spaces?**

- 🆓 **Completely Free**: No credit card required
- 🚀 **AI-Optimized**: Built specifically for ML model deployment
- 💪 **Powerful Hardware**: Free access to GPUs and high-memory CPUs
- 🔄 **Auto-Scaling**: Handles traffic spikes automatically
- 📦 **Model Caching**: Efficient model storage and loading

---

## 🛠️ Local Development Setup

### **Prerequisites**
- Python 3.8+
- Git
- 4GB+ RAM (8GB recommended)
- Optional: NVIDIA GPU with CUDA support

### **1. Clone Repository**
```bash
git clone https://github.com/anmol52490/AI-Clip-Backend.git
cd AI-Clip-Backend
```

### **2. Create Virtual Environment**
```bash
# Using venv
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Or using conda
conda create -n ai-video python=3.9
conda activate ai-video
```

### **3. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **4. Run Application**
```bash
python app.py
```

### **5. Access Application**
Open your browser and navigate to: `http://localhost:7860`

### **Expected Local Performance**
- **CPU**: Image generation ~30-60 seconds, Video creation ~30 seconds
- **GPU**: Image generation ~5-15 seconds, Video creation ~10 seconds

---

## 📋 Dependencies

```txt
torch              # PyTorch for AI model inference
torchvision         # Computer vision utilities
diffusers           # Hugging Face Diffusers for Stable Diffusion
transformers        # Transformer model support
accelerate          # Memory and compute optimizations
gradio              # Web interface framework
pillow              # Image processing
numpy               # Numerical computations
opencv-python-headless  # Computer vision and animation
imageio[ffmpeg]     # Video encoding and processing
safetensors         # Efficient model loading
```

---

## 🎮 Usage Guide

### **Step 1: Load Model**
- Click "🚀 Load Model" button (one-time setup per session)
- Wait for model download and initialization

### **Step 2: Generate Content**
- Enter your text prompt (e.g., "A cute cat in a garden")
- Choose generation type:
  - **🎬 Generate Video**: Full video with animation (slower)
  - **🖼️ Image Only**: Just the image (faster testing)

### **Step 3: Download Results**
- Download generated images and videos using built-in download buttons
- Share your creations!

### **Pro Tips for Better Results**
- ✅ **Be descriptive**: "A majestic lion in African savanna" vs "lion"
- ✅ **Specify style**: Add "photorealistic", "anime style", "oil painting"
- ✅ **Include mood**: "peaceful", "dramatic", "vibrant"
- ✅ **Mention lighting**: "golden hour", "neon lights", "soft lighting"

---

## 🎯 Features Implemented

### **Core Requirements** ✅
- [x] Text prompt input interface
- [x] AI-powered video generation (5-10 seconds)
- [x] Video display in browser
- [x] Public cloud deployment
- [x] Complete source code repository

### **Additional Features** 🌟
- [x] **Real-time Progress Tracking**: Users see generation status
- [x] **Multiple Animation Types**: Zoom, pan, rotate, fade effects
- [x] **Device Optimization**: Automatic CPU/GPU detection and optimization
- [x] **Example Prompts**: Built-in examples for quick testing
- [x] **Download Functionality**: Direct download of images and videos
- [x] **Responsive UI**: Works on desktop and mobile devices
- [x] **Error Handling**: Graceful error management and user feedback
- [x] **Memory Optimization**: Efficient resource usage

---

## 🔧 Technical Optimizations

### **Performance**
- **Model Choice**: SD-Turbo for ultra-fast generation (1 step vs 20-50)
- **Memory Management**: Aggressive garbage collection and VRAM clearing
- **Batch Processing**: Efficient frame-by-frame video creation
- **Format Optimization**: H.264 encoding for broad compatibility

### **User Experience**
- **Progressive Loading**: Model loads on demand, not at startup
- **Status Updates**: Real-time feedback during generation
- **Fallback Handling**: Graceful degradation if GPU unavailable
- **Mobile Friendly**: Responsive design for all devices

### **Deployment**
- **Zero Configuration**: No API keys or setup required
- **Auto-scaling**: Handles multiple concurrent users
- **Persistent Storage**: Model caching for faster subsequent loads
- **Global CDN**: Fast access worldwide through HF infrastructure

---

## 🎨 Animation Showcase

The application supports multiple animation types:

| Animation | Description | Effect |
|-----------|-------------|--------|
| **Zoom** | Gradual zoom-in effect | Creates depth and focus |
| **Pan** | Left-to-right camera movement | Reveals scene details |
| **Rotate** | Gentle rotation effect | Adds dynamic movement |
| **Fade** | Breathing fade effect | Subtle, artistic touch |

---

## 🔒 Security & Best Practices

- ✅ **No API Keys Required**: Uses open-source models, no external API dependencies
- ✅ **Client-Side Processing**: All computation happens on HF Spaces infrastructure
- ✅ **No Data Storage**: User prompts and generated content not permanently stored
- ✅ **Safe Dependencies**: All packages from trusted sources
- ✅ **Input Validation**: Prompt sanitization and length limits

---

## 🚧 Known Limitations & Future Improvements

### **Current Limitations**
- Video length fixed at 4-5 seconds (can be extended)
- Limited to single animation type per video
- CPU generation slower than cloud GPU services
- No video-to-video editing capabilities

### **Planned Enhancements**
- [ ] **Multiple Animation Layers**: Combine zoom + pan effects
- [ ] **Custom Duration**: User-selectable video length
- [ ] **Batch Generation**: Multiple videos from single prompt
- [ ] **Video-to-Video**: Transform existing videos
- [ ] **Audio Integration**: Add background music or sound effects
- [ ] **Style Transfer**: Apply artistic styles to generated content

---

## 📊 Performance Metrics

### **Generation Times** (Average)
| Hardware | Image Generation | Video Creation | Total Time |
|----------|------------------|----------------|------------|
| **CPU (Free)** | 10-30 seconds | 20-40 seconds | 30-70 seconds |
| **GPU (Free)** | 2-8 seconds | 5-15 seconds | 7-23 seconds |

### **Resource Usage**
- **Memory**: 2-4GB during generation
- **Storage**: ~3GB for model cache
- **Bandwidth**: Minimal (only for model download)

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues, feature requests, or pull requests.

### **Development Workflow**
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test locally
5. Submit a pull request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Stability AI** for the SD-Turbo model
- **Hugging Face** for free hosting and AI infrastructure
- **Gradio** for the excellent web interface framework
- **OpenCV** for computer vision capabilities
- **Peppo AI** for the interesting technical challenge

---

## 📞 Contact

**Developer**: Anmol Singh  
**Email**: [anmol52490@gmail.com]  
**GitHub**: [@anmol52490](https://github.com/anmol52490)  


---

## 🎉 Try It Now!

Visit the live application: **[https://huggingface.co/spaces/Anmol52490/video-clip](https://huggingface.co/spaces/Anmol52490/video-clip)**

Generate your first AI video in under a minute! 🚀
