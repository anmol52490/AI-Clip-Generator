import gradio as gr
import torch
from diffusers import AutoPipelineForText2Image
import cv2
import numpy as np
from PIL import Image
import imageio
import tempfile
import os
import gc

# Check device
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"🚀 Using device: {device}")

# Global model storage
pipe = None

def load_model():
    """Load the AI model - using the exact same model from your FastAPI code"""
    global pipe
    
    if pipe is not None:
        return "✅ Model already loaded!"
    
    try:
        model_id = "stabilityai/sd-turbo"  # Same model as your FastAPI
        print(f"📦 Loading {model_id}...")
        
        pipe = AutoPipelineForText2Image.from_pretrained(
            model_id,
            torch_dtype=torch.float16 if device == "cuda" else torch.float32,
            # For CPU, we'll use aggressive optimizations
        )
        
        pipe = pipe.to(device)
        
        # CPU optimizations
        if device == "cpu":
            pipe.enable_vae_slicing()
            try:
                pipe.enable_attention_slicing(1)
            except:
                pass
        else:
            # GPU optimizations
            try:
                pipe.enable_xformers_memory_efficient_attention()
            except:
                pass
            pipe.enable_vae_slicing()
        
        # Force garbage collection
        gc.collect()
        if device == "cuda":
            torch.cuda.empty_cache()
        
        print("✅ SD-Turbo model loaded successfully!")
        return f"✅ Model loaded on {device.upper()}!"
        
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        return f"❌ Error: {str(e)}"

def create_animated_video(base_image: Image.Image, duration_secs=5, fps=24):
    """Create animated video from image - same logic as your FastAPI"""
    
    # Convert PIL to numpy
    img_np = np.array(base_image)
    
    # Handle different image formats
    if len(img_np.shape) == 2:  # Grayscale
        img_np = cv2.cvtColor(img_np, cv2.COLOR_GRAY2RGB)
    elif img_np.shape[2] == 4:  # RGBA
        img_np = cv2.cvtColor(img_np, cv2.COLOR_RGBA2RGB)
    
    height, width = img_np.shape[:2]
    num_frames = duration_secs * fps
    
    print(f"🎬 Creating animation: {num_frames} frames at {fps} FPS")
    
    # Create temporary file
    with tempfile.NamedTemporaryFile(suffix='.mp4', delete=False) as tmp_file:
        video_path = tmp_file.name
    
    try:
        # Use imageio to create video - same as your FastAPI
        with imageio.get_writer(
            video_path, 
            mode='I', 
            fps=fps, 
            format='FFMPEG', 
            codec='libx264',
            quality=8,  # Good balance of quality/size
            pixelformat='yuv420p'  # Better compatibility
        ) as writer:
            
            for i in range(num_frames):
                # Create zoom effect - exactly like your FastAPI code
                scale = 1.0 + (0.2 * i / num_frames)
                M = cv2.getRotationMatrix2D((width / 2, height / 2), 0, scale)
                zoomed_frame_np = cv2.warpAffine(img_np, M, (width, height))
                writer.append_data(zoomed_frame_np)
        
        print(f"✅ Video created successfully!")
        return video_path
        
    except Exception as e:
        print(f"❌ Video creation error: {e}")
        return None

def generate_video(prompt, progress=gr.Progress()):
    """Main generation function"""
    
    if pipe is None:
        return None, None, "❌ Model not loaded! Click 'Load Model' first."
    
    if not prompt.strip():
        return None, None, "⚠️ Please enter a prompt!"
    
    try:
        progress(0.1, desc="🎨 Generating image...")
        
        # Generate image with SD-Turbo settings (ultra-fast)
        with torch.no_grad():
            # SD-Turbo specific settings for speed
            result = pipe(
                prompt=prompt,
                num_inference_steps=1,  # SD-Turbo can work with just 1 step!
                guidance_scale=0.0,     # SD-Turbo doesn't need guidance
                height=512,
                width=512
            )
            image = result.images[0]
        
        # Clear memory
        gc.collect()
        if device == "cuda":
            torch.cuda.empty_cache()
        
        progress(0.6, desc="🎬 Creating animation...")
        
        # Create video
        video_path = create_animated_video(image, duration_secs=4, fps=24)
        
        if video_path is None:
            return image, None, "✅ Image generated! ❌ Video creation failed."
        
        progress(1.0, desc="✅ Complete!")
        
        device_info = "🚀 GPU" if device == "cuda" else "🐌 CPU"
        return image, video_path, f"✅ Video generated successfully! {device_info}"
        
    except Exception as e:
        gc.collect()
        if device == "cuda":
            torch.cuda.empty_cache()
        return None, None, f"❌ Error: {str(e)}"

def generate_image_only(prompt, progress=gr.Progress()):
    """Generate image only for faster testing"""
    
    if pipe is None:
        return None, "❌ Model not loaded! Click 'Load Model' first."
    
    if not prompt.strip():
        return None, "⚠️ Please enter a prompt!"
    
    try:
        progress(0.1, desc="🎨 Generating image...")
        
        with torch.no_grad():
            result = pipe(
                prompt=prompt,
                num_inference_steps=1,  # Ultra-fast with SD-Turbo
                guidance_scale=0.0,
                height=512,
                width=512
            )
            image = result.images[0]
        
        gc.collect()
        if device == "cuda":
            torch.cuda.empty_cache()
        
        progress(1.0, desc="✅ Done!")
        device_info = "🚀 GPU" if device == "cuda" else "🐌 CPU" 
        return image, f"✅ Image generated! {device_info}"
        
    except Exception as e:
        gc.collect()
        return None, f"❌ Error: {str(e)}"

# Custom CSS
css = """
.gradio-container {
    max-width: 1000px !important;
    margin: auto !important;
}
.main-header {
    text-align: center;
    background: linear-gradient(45deg, #FF6B6B, #4ECDC4);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-size: 2.5em;
    font-weight: bold;
    margin-bottom: 1em;
}
.model-status {
    padding: 15px;
    border-radius: 10px;
    text-align: center;
    font-weight: bold;
    margin: 15px 0;
    background: linear-gradient(45deg, #667eea, #764ba2);
    color: white;
}
"""

# Create Gradio interface
with gr.Blocks(css=css, title="🎬 AI Video Generator (SD-Turbo)", theme=gr.themes.Soft()) as demo:
    
    gr.HTML('<h1 class="main-header">🎬 AI Video Generator</h1>')
    
    # Model status and info
    device_info = f"💻 Device: {device.upper()}"
    model_info = "🚀 Model: SD-Turbo (Ultra-Fast Generation)"
    gr.HTML(f'<div class="model-status">{device_info}<br>{model_info}</div>')
    
    gr.Markdown(
        """
        ### ⚡ Features:
        - **Ultra-Fast Generation**: SD-Turbo generates images in 1 step!
        - **Animated Videos**: Creates zoom animations from static images
        - **Free to Use**: Runs on Hugging Face Spaces
        - **CPU Optimized**: Works well even without GPU
        
        ### 🎯 How to Use:
        1. **Load the model** (one-time setup)
        2. **Enter your prompt** 
        3. **Generate!** (Images: ~10-30s, Videos: ~30-60s on CPU)
        """
    )
    
    with gr.Row():
        with gr.Column(scale=2):
            # Model loading section
            with gr.Group():
                gr.Markdown("### 🔧 Model Setup")
                load_btn = gr.Button("🚀 Load Model", variant="primary", size="lg")
                model_status = gr.Textbox(
                    label="Model Status", 
                    value="⏳ Click 'Load Model' to start",
                    interactive=False
                )
            
            # Generation section
            with gr.Group():
                gr.Markdown("### 🎨 Generation")
                prompt_input = gr.Textbox(
                    label="✍️ Enter your prompt",
                    placeholder="A cute cat sitting in a garden",
                    lines=3,
                    max_lines=5
                )
                
                with gr.Row():
                    generate_video_btn = gr.Button(
                        "🎬 Generate Video", 
                        variant="primary",
                        size="lg",
                        interactive=False
                    )
                    generate_image_btn = gr.Button(
                        "🖼️ Image Only (Faster)",
                        variant="secondary",
                        interactive=False
                    )
        
        with gr.Column(scale=3):
            # Output section
            status_output = gr.Textbox(
                label="📊 Status",
                interactive=False,
                max_lines=2
            )
            
            image_output = gr.Image(
                label="🖼️ Generated Image",
                show_download_button=True,
                height=350
            )
            
            video_output = gr.Video(
                label="🎬 Generated Video",
                show_download_button=True,
                height=350
            )
    
    # Example prompts
    gr.Markdown("### 🎯 Try These Example Prompts:")
    
    examples = [
        "A cute corgi puppy in a meadow",
        "A futuristic car in a cyberpunk city",
        "A magical castle in the clouds",
        "A serene lake with mountains",
        "A colorful flower bouquet",
        "A cozy coffee shop interior"
    ]
    
    gr.Examples(
        examples=[[ex] for ex in examples],
        inputs=[prompt_input],
        label="Click any example to load it"
    )
    
    # Event handlers
    def on_model_loaded(status):
        """Enable buttons when model is loaded"""
        if "✅" in status:
            return gr.update(interactive=True), gr.update(interactive=True)
        else:
            return gr.update(interactive=False), gr.update(interactive=False)
    
    load_btn.click(
        fn=load_model,
        outputs=[model_status]
    ).then(
        fn=on_model_loaded,
        inputs=[model_status],
        outputs=[generate_video_btn, generate_image_btn]
    )
    
    generate_video_btn.click(
        fn=generate_video,
        inputs=[prompt_input],
        outputs=[image_output, video_output, status_output],
        show_progress=True
    )
    
    generate_image_btn.click(
        fn=generate_image_only,
        inputs=[prompt_input],
        outputs=[image_output, status_output],
        show_progress=True
    )
    
    # Footer
    gr.Markdown(
        """
        ---
        ### 💡 Performance Tips:
        - **SD-Turbo is optimized for speed** - generates images in 1 step!
        - **First generation** may take longer due to model loading
        - **CPU performance**: Image ~10-30s, Video ~30-60s
        - **GPU performance**: Image ~2-5s, Video ~5-15s
        
        **🔄 Model needs to be loaded once per session.**
        """
    )

# Launch the app
if __name__ == "__main__":
    demo.queue(max_size=10)  # Handle multiple users
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        show_error=True
    )
