import os
import glob
from PIL import Image, ImageChops

def get_clean_bbox(im):
    im_rgb = im.convert('RGB')
    bg = Image.new('RGB', im_rgb.size, (255, 255, 255))
    diff = ImageChops.difference(im_rgb, bg)
    diff_l = diff.convert('L')
    return diff_l.point(lambda p: 255 if p > 15 else 0).getbbox()

os.makedirs('media/catalog/products/gallery', exist_ok=True)

source_files = glob.glob('media/catalog/products/*.jpg')
for src_path in source_files:
    if 'gallery' in src_path:
        continue
    
    filename = os.path.basename(src_path)
    base_no_ext = os.path.splitext(filename)[0]
    
    im = Image.open(src_path).convert('RGB')
    bbox = get_clean_bbox(im)
    if not bbox:
        bbox = (0, 0, im.width, im.height)
    
    # Add a clean 20px safety padding around the gun bbox
    x1 = max(0, bbox[0] - 20)
    y1 = max(0, bbox[1] - 20)
    x2 = min(im.width, bbox[2] + 20)
    y2 = min(im.height, bbox[3] + 20)
    
    cropped = im.crop((x1, y1, x2, y2))
    c_w, c_h = cropped.size
    
    print(f"Processing {base_no_ext}: original {im.size}, cropped bbox {cropped.size}")
    
    # 1. Generate _main.jpg (1200x675 - 16:9 Widescreen full grid fill, full rifle)
    target_w, target_h = 1200, 675
    canvas_main = Image.new('RGB', (target_w, target_h), (255, 255, 255))
    
    # Scale cropped gun to fill 94% of the target width/height
    scale_w = (target_w * 0.94) / c_w
    scale_h = (target_h * 0.94) / c_h
    scale = min(scale_w, scale_h)
    
    new_w = int(c_w * scale)
    new_h = int(c_h * scale)
    scaled = cropped.resize((new_w, new_h), Image.Resampling.LANCZOS)
    paste_x = (target_w - new_w) // 2
    paste_y = (target_h - new_h) // 2
    canvas_main.paste(scaled, (paste_x, paste_y))
    canvas_main.save(f"media/catalog/products/gallery/{base_no_ext}_main.jpg", quality=95)
    
    # 2. Generate _card.jpg (800x600 - 4:3 Card full grid fill)
    target_w_c, target_h_c = 800, 600
    canvas_card = Image.new('RGB', (target_w_c, target_h_c), (255, 255, 255))
    scale_w_c = (target_w_c * 0.92) / c_w
    scale_h_c = (target_h_c * 0.92) / c_h
    scale_c = min(scale_w_c, scale_h_c)
    new_w_c = int(c_w * scale_c)
    new_h_c = int(c_h * scale_c)
    scaled_c = cropped.resize((new_w_c, new_h_c), Image.Resampling.LANCZOS)
    canvas_card.paste(scaled_c, ((target_w_c - new_w_c) // 2, (target_h_c - new_h_c) // 2))
    canvas_card.save(f"media/catalog/products/gallery/{base_no_ext}_card.jpg", quality=95)
    
    # --------------------------------------------------------------------------------
    # EXACT 16:9 SLIDING WINDOW CLOSE-UPS (_receiver, _handguard, _stock)
    # To prevent any "cut" vertical slice edges floating inside white boxes,
    # every zoom view must be cropped with an EXACT 16:9 aspect ratio window (target_w / target_h = 1200 / 675 = 16:9)
    # from the full rifle and scaled directly to 1200x675 edge-to-edge!
    # --------------------------------------------------------------------------------
    
    # Calculate window_w that gives exact 16:9 ratio with window_h = c_h
    # If c_w is narrower than (c_h * 1200 / 675), we just use c_w and adjust height
    window_w = int(c_h * target_w / target_h)
    if window_w > c_w:
        window_w = c_w
        window_h = int(c_w * target_h / target_w)
    else:
        window_h = c_h
    
    # 3. _receiver.jpg (Center Action / Magazine / Receiver close-up)
    rx1 = max(0, min((c_w - window_w) // 2, c_w - window_w))
    ry1 = max(0, (c_h - window_h) // 2)
    rec_crop = cropped.crop((rx1, ry1, rx1 + window_w, ry1 + window_h))
    scaled_rec = rec_crop.resize((target_w, target_h), Image.Resampling.LANCZOS)
    scaled_rec.save(f"media/catalog/products/gallery/{base_no_ext}_receiver.jpg", quality=95)
    
    # 4. _handguard.jpg (Front Handguard / Gas Block / Muzzle close-up)
    # Align right edge of 16:9 window to the front/right of the gun bbox
    hx1 = max(0, c_w - window_w)
    hy1 = max(0, (c_h - window_h) // 2)
    hand_crop = cropped.crop((hx1, hy1, hx1 + window_w, hy1 + window_h))
    scaled_hand = hand_crop.resize((target_w, target_h), Image.Resampling.LANCZOS)
    scaled_hand.save(f"media/catalog/products/gallery/{base_no_ext}_handguard.jpg", quality=95)
    
    # 5. _stock.jpg (Rear Buttstock / Lower Receiver close-up)
    # Align left edge of 16:9 window to the rear/left of the gun bbox
    sx1 = 0
    sy1 = max(0, (c_h - window_h) // 2)
    stock_crop = cropped.crop((sx1, sy1, sx1 + window_w, sy1 + window_h))
    scaled_stock = stock_crop.resize((target_w, target_h), Image.Resampling.LANCZOS)
    scaled_stock.save(f"media/catalog/products/gallery/{base_no_ext}_stock.jpg", quality=95)

print("All gallery images successfully regenerated with exact 16:9 edge-to-edge close-ups without cut vertical borders!")
