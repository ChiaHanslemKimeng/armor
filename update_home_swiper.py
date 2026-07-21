import re

blogs = [
    ("Industry Trends in 2024", "The firearms industry is experiencing a massive paradigm shift in 2024. Manufacturers are focusing heavily on modularity, allowing users to customize their platforms seamlessly across different calibers.", "tactical_gear.png"),
    ("New Product Announcements for Fall", "With the upcoming fall season, major manufacturers have announced a slew of new products aimed at both competitive shooters and hunting enthusiasts. Expect to see significant upgrades in optics.", "rifle_scope.png"),
    ("The Future of Optics in Firearms", "Smart optics are no longer a concept of the future; they are here. Integrated rangefinders, ballistic calculators, and heads-up displays are becoming standard features on high-end scopes.", "rifle_scope.png"),
    ("Safety First: Range Etiquette", "Whether you are a seasoned veteran or a first-time shooter, range etiquette is paramount. Understanding the fundamental rules of firearms safety ensures that everyone has a safe and enjoyable time.", "shooting_range.png"),
    ("Top 10 Accessories for Your Rifle", "Outfitting your rifle with the right accessories can drastically improve your shooting experience. From advanced slings and bipods to high-lumen weapon lights, we break down the top 10 must-haves.", "tactical_gear.png"),
    ("Gunsmithing Tips: Cleaning Your Firearm", "Regular maintenance is the key to ensuring your firearm's longevity and reliability. In this guide, we cover the essential steps to properly clean and lubricate your weapon.", "gunsmithing_workbench.png"),
    ("Choosing the Right Ammunition", "Not all ammunition is created equal. Understanding the difference between FMJ, hollow points, and ballistic tips is crucial for making the right choice for self-defense, hunting, or target practice.", "tactical_gear.png"),
    ("Getting Started in Competitive Shooting", "Competitive shooting is one of the fastest-growing sports in the nation. We cover the basics of getting involved in USPSA, IDPA, and 3-Gun competitions.", "shooting_range.png"),
    ("Understanding Ballistics for Beginners", "Ballistics can be a complex science, but understanding the basics of trajectory, wind drift, and bullet drop is essential for any serious marksman looking to improve their accuracy at range.", "rifle_scope.png"),
    ("Building Your First AR-15: A Comprehensive Guide", "Building an AR-15 from scratch is a rewarding experience that teaches you the ins and outs of the platform. We guide you through the process, from selecting the right lower receiver to torquing the barrel.", "gunsmithing_workbench.png")
]

slides_html = ""
for i, b in enumerate(blogs):
    slides_html += f"""
<div class="swiper-slide" style="width: 350px;">
    <a href="/trigger-times/?cat=news" class="text-decoration-none">
        <div class="glass-card p-0 h-100 d-flex flex-column border shadow-sm transition-all hover-glass bg-dark text-white rounded-4 overflow-hidden" style="border-color: #334155 !important;">
            <div class="position-relative" style="height: 220px; flex-shrink: 0;">
                <img src="{{% static 'images/news/{b[2]}' %}}" class="img-fluid w-100 h-100 object-fit-cover" alt="{b[0]}">
                <div class="position-absolute bottom-0 start-0 w-100 p-2" style="background: linear-gradient(to top, rgba(0,0,0,0.8), transparent);">
                    <span class="badge bg-danger small font-monospace"><i class="bi bi-play-circle me-1"></i> News</span>
                </div>
            </div>
            <div class="p-4 d-flex flex-column justify-content-between flex-grow-1">
                <div>
                    <h5 class="font-outfit fw-bold text-white mb-2 line-clamp-2" style="line-height: 1.4; min-height: 2.8em; color: #ffffff !important;">
                        {b[0]}
                    </h5>
                    <p class="small text-secondary mb-3 line-clamp-3" style="line-height: 1.5; color: #cbd5e1 !important;">
                        {b[1]}
                    </p>
                </div>
                <div class="d-flex justify-content-between align-items-center mt-auto border-top pt-3" style="border-color: rgba(255,255,255,0.1) !important;">
                    <small class="text-secondary font-monospace" style="color: #94a3b8 !important;"><i class="bi bi-clock me-1"></i> January {15+i}, 2024</small>
                    <i class="bi bi-arrow-right text-danger"></i>
                </div>
            </div>
        </div>
    </a>
</div>
"""

filepath = r'c:\Users\HANSLEM_KIMENG\Desktop\WEB\Armor\templates\catalog\home.html'
with open(filepath, 'r', encoding='utf-8') as f:
    text = f.read()

# Add line-clamp CSS at the top if not present
if "line-clamp-2" not in text:
    style_block = """
<style>
.line-clamp-2 {
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
}
.line-clamp-3 {
    display: -webkit-box;
    -webkit-line-clamp: 3;
    -webkit-box-orient: vertical;
    overflow: hidden;
}
</style>
"""
    text = text.replace("{% block content %}", "{% block content %}\n" + style_block)

# Replace the swiper-wrapper content for guidesSwiper
# Find the start of guidesSwiper wrapper
start_idx = text.find('<div class="swiper guidesSwiper')
if start_idx != -1:
    wrapper_start = text.find('<div class="swiper-wrapper">', start_idx) + len('<div class="swiper-wrapper">')
    # Find the end of this swiper-wrapper by finding the next </div> that closes it.
    # Since there are multiple swiper-slides, we can just find the end of the guidesSwiper block entirely
    # Actually, the guidesSwiper block ends with </div>\n</div>\n</section>
    
    # We can use regex to replace everything inside <div class="swiper-wrapper"> ... </div> for the guidesSwiper
    
    # A safer way: replace everything from wrapper_start to the first "</div>\n    </div>\n</section>" or similar
    # Let's just find the end of the wrapper
    
    # Simple trick: count divs
    div_count = 1
    i = wrapper_start
    while i < len(text) and div_count > 0:
        next_div = text.find('<div', i)
        next_end = text.find('</div>', i)
        
        if next_div != -1 and next_div < next_end:
            div_count += 1
            i = next_div + 4
        else:
            div_count -= 1
            i = next_end + 6

    wrapper_end = i - 6 # position of the closing </div>
    
    new_text = text[:wrapper_start] + "\n" + slides_html + text[wrapper_end:]
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_text)
    print("Updated swiper in home.html successfully.")
else:
    print("Could not find guidesSwiper in home.html")
