import re

with open(r'c:\Users\HANSLEM_KIMENG\Desktop\WEB\Armor\templates\catalog\home.html', 'r', encoding='utf-8') as f:
    text = f.read()

posts_data = [
    ("Industry Trends in 2024", "https://images.unsplash.com/photo-1595590424283-b8f1784cb2c8?q=80&w=1200", "January 15, 2024"),
    ("New Product Announcements for Fall", "https://images.unsplash.com/photo-1584646098378-0874589d76b1?q=80&w=1200", "August 22, 2023"),
    ("The Future of Optics in Firearms", "https://images.unsplash.com/photo-1575369208753-48b4b1a41a4a?q=80&w=1200", "June 05, 2023"),
    ("Safety First: Range Etiquette", "https://images.unsplash.com/photo-1552084117-56a98cea30ce?q=80&w=1200", "March 12, 2023"),
    ("Top 10 Accessories for Your Rifle", "https://images.unsplash.com/photo-1620922894563-12dbf5ab3eb2?q=80&w=1200", "November 02, 2022"),
    ("Gunsmithing Tips: Cleaning Your Firearm", "https://images.unsplash.com/photo-1619888998845-a74421b444c1?q=80&w=1200", "September 18, 2022"),
    ("Choosing the Right Ammunition", "https://images.unsplash.com/photo-1588725832788-b78e1784b123?q=80&w=1200", "July 04, 2022"),
    ("Getting Started in Competitive Shooting", "https://images.unsplash.com/photo-1595590423985-3bc4daaa6a0e?q=80&w=1200", "April 11, 2022"),
    ("Understanding Ballistics for Beginners", "https://images.unsplash.com/photo-1504938637774-63bececc42a3?q=80&w=1200", "February 28, 2022"),
    ("Building Your First AR-15: A Comprehensive Guide", "https://images.unsplash.com/photo-1601009117652-32b4b4a3a60a?q=80&w=1200", "December 10, 2021")
]

section_idx = text.find('ARMORY KNOWLEDGE BASE')
if section_idx != -1:
    wrapper_start = text.find('<div class="swiper-wrapper">', section_idx)
    end_of_start_tag = wrapper_start + len('<div class="swiper-wrapper">')
    
    # find the end of the swiper wrapper block by looking for the 2 closing divs before </section>
    section_end = text.find('</section>', wrapper_start)
    # The end of the wrapper is the `</div>` that aligns with swiper-wrapper.
    # It's at text.rfind('</div>\n    </div>\n</section>', wrapper_start, section_end+10)
    wrapper_end = text.rfind('</div>\n    </div>\n</section>', wrapper_start, section_end+15)
    
    if wrapper_start != -1 and wrapper_end != -1:
        new_slides = "\n"
        for title, img, date in posts_data:
            new_slides += f"""            <div class="swiper-slide" style="width: 350px;">
                <a href="/trigger-times/?cat=news" class="text-decoration-none">
                    <div class="glass-card p-0 h-100 d-flex flex-column border shadow-sm transition-all hover-glass bg-dark text-white rounded-4 overflow-hidden" style="border-color: #334155 !important;">
                        <div class="position-relative" style="height: 220px;">
                            <img src="{img}" class="img-fluid w-100 h-100 object-fit-cover" alt="{title}">
                            <div class="position-absolute bottom-0 start-0 w-100 p-2" style="background: linear-gradient(to top, rgba(0,0,0,0.8), transparent);">
                                <span class="badge bg-danger small font-monospace"><i class="bi bi-play-circle me-1"></i> News</span>
                            </div>
                        </div>
                        <div class="p-4 d-flex flex-column justify-content-between flex-grow-1">
                            <h5 class="font-outfit fw-bold text-white mb-2" style="line-height: 1.4;">
                                {title}
                            </h5>
                            <div class="d-flex justify-content-between align-items-center mt-3">
                                <small class="text-secondary font-monospace"><i class="bi bi-clock me-1"></i> {date}</small>
                                <i class="bi bi-arrow-right text-danger"></i>
                            </div>
                        </div>
                    </div>
                </a>
            </div>\n"""
        
        new_text = text[:end_of_start_tag] + new_slides + "        " + text[wrapper_end:]
        with open(r'c:\Users\HANSLEM_KIMENG\Desktop\WEB\Armor\templates\catalog\home.html', 'w', encoding='utf-8') as f:
            f.write(new_text)
        print("Home news swiper successfully updated with professional images.")
    else:
        print("Could not find swiper wrapper end")
else:
    print("Could not find ARMORY KNOWLEDGE BASE")
