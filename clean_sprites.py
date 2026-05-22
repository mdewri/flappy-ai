from PIL import Image
import os

def remove_bg(img_path, tolerance=20):
    img = Image.open(img_path).convert("RGBA")
    datas = img.getdata()
    
    bg_color = datas[0] # Assume top-left pixel is background
    
    newData = []
    for item in datas:
        # If pixel is close to background color, make it transparent
        if abs(item[0] - bg_color[0]) <= tolerance and \
           abs(item[1] - bg_color[1]) <= tolerance and \
           abs(item[2] - bg_color[2]) <= tolerance:
            newData.append((0, 0, 0, 0))
        else:
            newData.append(item)
            
    img.putdata(newData)
    img.save(img_path, "PNG")
    print(f"Processed {img_path}")

base_dir = r"h:\flappy\assets"
remove_bg(os.path.join(base_dir, "bird.png"))
remove_bg(os.path.join(base_dir, "pipe.png"))
print("Done!")
