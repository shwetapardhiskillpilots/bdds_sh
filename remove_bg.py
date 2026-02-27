from PIL import Image
import os

def remove_white_background(input_path, output_path):
    img = Image.open(input_path)
    img = img.convert("RGBA")
    
    datas = img.getdata()
    
    newData = []
    # Threshold for "white" - can be adjusted if needed
    threshold = 240 
    
    for item in datas:
        # Check if the pixel is white (all R, G, B values above threshold)
        if item[0] > threshold and item[1] > threshold and item[2] > threshold:
            # Make it transparent
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)
    
    img.putdata(newData)
    img.save(output_path, "PNG")
    print(f"Success! Saved transparent image to {output_path}")

if __name__ == "__main__":
    # Using absolute paths to be safe
    cwd = os.getcwd()
    input_img = os.path.join(cwd, "static", "images", "logo.jpg")
    output_img = os.path.join(cwd, "static", "images", "logo.png")
    
    if os.path.exists(input_img):
        remove_white_background(input_img, output_img)
    else:
        print(f"Error: {input_img} not found.")
