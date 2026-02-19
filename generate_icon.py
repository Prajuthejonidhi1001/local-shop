import sys
import subprocess

def install_and_import_pillow():
    try:
        from PIL import Image, ImageDraw
    except ImportError:
        print("Installing Pillow library for image generation...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow"])
        from PIL import Image, ImageDraw
    return Image, ImageDraw

def create_icon():
    Image, ImageDraw = install_and_import_pillow()
    
    # Create a 512x512 image with the theme color
    img = Image.new('RGB', (512, 512), color='#4f46e5')
    d = ImageDraw.Draw(img)
    
    # Draw a white 'L'
    d.rectangle([128, 100, 188, 412], fill='white') # Vertical
    d.rectangle([128, 352, 384, 412], fill='white') # Horizontal
    
    img.save('static/icon-512.png')
    print("✅ Created static/icon-512.png")
    
    # Create 192x192 icon (Required for PWA)
    img_192 = img.resize((192, 192))
    img_192.save('static/icon-192.png')
    print("✅ Created static/icon-192.png")

if __name__ == "__main__":
    create_icon()