import re

with open(r'c:\Users\HANSLEM_KIMENG\Desktop\WEB\Armor\templates\catalog\trigger_times.html', 'r', encoding='utf-8') as f:
    text = f.read()

# We need to extract the existing row block starting at <div class="row g-4 pb-5">
# up to the end of the section </div>\n</section>

# First, find the start of the row:
start_idx = text.find('<div class="row g-4 pb-5">')
# Find the end of the section:
end_idx = text.find('</section>', start_idx)

if start_idx != -1 and end_idx != -1:
    old_row_content = text[start_idx:end_idx]
    
    # We will replace the news-specific texts in old_row_content with standard generic titles for other categories.
    # Actually, we don't need to touch the existing block much, just wrap it in {% if request.GET.cat != 'news' and request.GET.cat %}
    
    news_content = """
    {% if request.GET.cat == 'news' or not request.GET.cat %}
    <div class="row g-5 pb-5">
        <!-- Post 1 -->
        <div class="col-12">
            <div class="card border-0 shadow-lg rounded-4 overflow-hidden bg-dark text-white">
                <img src="https://images.unsplash.com/photo-1595590424283-b8f1784cb2c8?q=80&w=1200" class="card-img-top object-fit-cover" style="height: 450px;" alt="Industry Trends">
                <div class="card-body p-5">
                    <span class="badge bg-danger mb-3 font-monospace px-3 py-2">INDUSTRY UPDATE</span>
                    <h2 class="font-outfit fw-bold text-white mb-3">News Update: Industry Trends in 2024</h2>
                    <p class="text-secondary small mb-4"><i class="bi bi-person-fill text-danger"></i> Editorial Team &nbsp;&nbsp;|&nbsp;&nbsp; <i class="bi bi-clock text-danger"></i> January 15, 2024</p>
                    <div class="content-article" style="font-size: 1.15rem; line-height: 1.8; color: #cbd5e1;">
                        <p>The firearms industry is experiencing a massive paradigm shift in 2024, characterized by the rapid adoption of smart technologies and advanced material sciences. Manufacturers are moving away from traditional steel components, embracing ultra-lightweight titanium and carbon fiber composites. These changes are drastically reducing the weight of everyday carry (EDC) items without compromising structural integrity or reliability.</p>
                        <p>Moreover, the integration of electronic optics and digital firing mechanisms continues to blur the lines between traditional marksmanship and modern technology. We are seeing unprecedented demand for modular firearm systems that allow the end-user to hot-swap calibers, handguards, and optical suites within minutes. This adaptability is particularly appealing to both competitive shooters and tactical professionals who require a single platform to serve multiple mission profiles.</p>
                        <p>As the regulatory landscape continues to evolve, manufacturers are also investing heavily in compliance-friendly variants of their flagship models. The push for suppressor-ready platforms right out of the box is stronger than ever, reflecting a broader cultural shift towards responsible, hearing-safe shooting practices. This year promises to be a landmark period for innovation, and we're excited to see what the leading brands bring to the table.</p>
                    </div>
                </div>
            </div>
        </div>

        <!-- Post 2 -->
        <div class="col-12">
            <div class="card border-0 shadow-lg rounded-4 overflow-hidden bg-dark text-white">
                <img src="https://images.unsplash.com/photo-1584646098378-0874589d76b1?q=80&w=1200" class="card-img-top object-fit-cover" style="height: 450px;" alt="Product Announcements">
                <div class="card-body p-5">
                    <span class="badge bg-danger mb-3 font-monospace px-3 py-2">GEAR PREVIEW</span>
                    <h2 class="font-outfit fw-bold text-white mb-3">New Product Announcements for Fall</h2>
                    <p class="text-secondary small mb-4"><i class="bi bi-person-fill text-danger"></i> Gear Editor &nbsp;&nbsp;|&nbsp;&nbsp; <i class="bi bi-clock text-danger"></i> August 22, 2023</p>
                    <div class="content-article" style="font-size: 1.15rem; line-height: 1.8; color: #cbd5e1;">
                        <p>Fall is traditionally the season where the most highly anticipated products hit the shelves, and this year is certainly no exception. Leading brands have unveiled a stunning array of new tactical gear, optics, and firearms designed specifically for the modern enthusiast. From ultra-compact concealed carry pistols with enhanced capacity to precision bolt-action rifles featuring match-grade barrels, the lineup is incredibly diverse.</p>
                        <p>One of the most notable trends this fall is the rise of micro-compact red dot sights. These optics have been completely re-engineered to sit lower on the slide, offering co-witness capabilities with standard height iron sights. The battery life on these new models has also seen a significant boost, with several brands now advertising over 50,000 hours of continuous use on a single CR1632 battery.</p>
                        <p>In the apparel and load-bearing category, we're seeing the introduction of laser-cut plate carriers that shed unnecessary bulk while maintaining high tensile strength. By utilizing advanced laminate materials, these carriers offer superior breathability and comfort for extended wear. Stay tuned as we will be publishing in-depth, hands-on reviews of these products as soon as they hit our testing range.</p>
                    </div>
                </div>
            </div>
        </div>

        <!-- Post 3 -->
        <div class="col-12">
            <div class="card border-0 shadow-lg rounded-4 overflow-hidden bg-dark text-white">
                <img src="https://images.unsplash.com/photo-1575369208753-48b4b1a41a4a?q=80&w=1200" class="card-img-top object-fit-cover" style="height: 450px;" alt="Optics">
                <div class="card-body p-5">
                    <span class="badge bg-danger mb-3 font-monospace px-3 py-2">TECHNOLOGY</span>
                    <h2 class="font-outfit fw-bold text-white mb-3">The Future of Optics in Firearms</h2>
                    <p class="text-secondary small mb-4"><i class="bi bi-person-fill text-danger"></i> Tech Reviewer &nbsp;&nbsp;|&nbsp;&nbsp; <i class="bi bi-clock text-danger"></i> June 05, 2023</p>
                    <div class="content-article" style="font-size: 1.15rem; line-height: 1.8; color: #cbd5e1;">
                        <p>The days of relying solely on traditional iron sights for tactical and defensive applications are rapidly coming to a close. The optical revolution has fundamentally changed how shooters acquire targets, track movement, and engage at distance. Low Power Variable Optics (LPVOs) have dominated the carbine market over the last five years, but we are now seeing the emergence of prism scopes and holographic hybrids that push the boundaries even further.</p>
                        <p>Modern reticle designs are becoming increasingly sophisticated. Bullet Drop Compensator (BDC) reticles are now specifically tailored to specific barrel lengths and ammunition loads, allowing for rapid, math-free holdovers at extended ranges. Furthermore, the integration of smart technology is bringing ballistic calculators directly into the optical housing. Imagine looking through your scope and seeing a dynamically updated holdover dot based on real-time environmental data—this is no longer science fiction, it's reality.</p>
                        <p>Durability has also reached unprecedented levels. Manufacturers are subjecting their optics to rigorous drop tests, extreme temperature fluctuations, and submersion tests to ensure they can survive the harshest environments on Earth. As the cost of manufacturing these advanced optics continues to decrease, we expect to see them become the standard, baseline equipment for shooters of all disciplines.</p>
                    </div>
                </div>
            </div>
        </div>

        <!-- Post 4 -->
        <div class="col-12">
            <div class="card border-0 shadow-lg rounded-4 overflow-hidden bg-dark text-white">
                <img src="https://images.unsplash.com/photo-1552084117-56a98cea30ce?q=80&w=1200" class="card-img-top object-fit-cover" style="height: 450px;" alt="Range Etiquette">
                <div class="card-body p-5">
                    <span class="badge bg-danger mb-3 font-monospace px-3 py-2">TRAINING</span>
                    <h2 class="font-outfit fw-bold text-white mb-3">Safety First: Range Etiquette</h2>
                    <p class="text-secondary small mb-4"><i class="bi bi-person-fill text-danger"></i> Range Master &nbsp;&nbsp;|&nbsp;&nbsp; <i class="bi bi-clock text-danger"></i> March 12, 2023</p>
                    <div class="content-article" style="font-size: 1.15rem; line-height: 1.8; color: #cbd5e1;">
                        <p>Whether you're visiting a high-tech indoor facility or a sprawling outdoor shooting club, range etiquette is the invisible glue that keeps the environment safe, welcoming, and productive for everyone. Understanding the rules goes far beyond just keeping your finger off the trigger; it encompasses how you handle your gear, communicate with others, and respect the commands of the Range Safety Officer (RSO).</p>
                        <p>One of the most critical aspects of range etiquette is understanding the concepts of a "cold" and "hot" range. When a range is declared cold, all firearms must be unloaded, actions opened, and placed on the bench facing downrange. Under no circumstances should a shooter handle a firearm, load a magazine, or adjust an optic while the range is cold and people are downrange setting targets. Failing to adhere to this simple rule is the quickest way to be ejected from any reputable facility.</p>
                        <p>Additionally, being mindful of your brass and your target placement is key. Ensure your targets are hung at the appropriate height to ensure rounds impact the backstop directly. Clean up your brass when you're finished, and always be willing to lend a hand or offer polite guidance to new shooters if they seem lost. A positive, safety-oriented attitude ensures that the range remains a fantastic place for the community to gather and train.</p>
                    </div>
                </div>
            </div>
        </div>

        <!-- Post 5 -->
        <div class="col-12">
            <div class="card border-0 shadow-lg rounded-4 overflow-hidden bg-dark text-white">
                <img src="https://images.unsplash.com/photo-1620922894563-12dbf5ab3eb2?q=80&w=1200" class="card-img-top object-fit-cover" style="height: 450px;" alt="Accessories">
                <div class="card-body p-5">
                    <span class="badge bg-danger mb-3 font-monospace px-3 py-2">GEAR GUIDE</span>
                    <h2 class="font-outfit fw-bold text-white mb-3">Top 10 Accessories for Your Rifle</h2>
                    <p class="text-secondary small mb-4"><i class="bi bi-person-fill text-danger"></i> Staff Writer &nbsp;&nbsp;|&nbsp;&nbsp; <i class="bi bi-clock text-danger"></i> November 02, 2022</p>
                    <div class="content-article" style="font-size: 1.15rem; line-height: 1.8; color: #cbd5e1;">
                        <p>Outfitting a new rifle can be a daunting task, especially with the overwhelming number of aftermarket parts and accessories available today. However, focusing on the fundamentals will ensure that your rifle is reliable, ergonomic, and effective for its intended purpose. The very first accessory any rifle needs is a high-quality, adjustable two-point sling. A sling is to a rifle what a holster is to a pistol; it provides retention and allows you to transition to a secondary weapon or use your hands for other tasks.</p>
                        <p>Following the sling, a reliable weapon-mounted light is non-negotiable for a defensive setup. Identifying your target in low-light conditions is a critical requirement. We recommend lights with a minimum output of 500 lumens, paired with a solid pressure switch or tailcap that allows for momentary and constant-on activation without breaking your grip on the handguard.</p>
                        <p>Other essential accessories include an optic suited for your engagement distances, upgraded furniture (such as a comfortable pistol grip and a sturdy buttstock), and a set of backup iron sights (BUIS). While the temptation to bolt every available gadget onto your rails is strong, remember that ounces equal pounds. Keep your setup streamlined, focus on quality over quantity, and invest the rest of your budget into ammunition and professional training.</p>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Post 6 -->
        <div class="col-12">
            <div class="card border-0 shadow-lg rounded-4 overflow-hidden bg-dark text-white">
                <img src="https://images.unsplash.com/photo-1619888998845-a74421b444c1?q=80&w=1200" class="card-img-top object-fit-cover" style="height: 450px;" alt="Gunsmithing Tips">
                <div class="card-body p-5">
                    <span class="badge bg-danger mb-3 font-monospace px-3 py-2">MAINTENANCE</span>
                    <h2 class="font-outfit fw-bold text-white mb-3">Gunsmithing Tips: Cleaning Your Firearm</h2>
                    <p class="text-secondary small mb-4"><i class="bi bi-person-fill text-danger"></i> Master Gunsmith &nbsp;&nbsp;|&nbsp;&nbsp; <i class="bi bi-clock text-danger"></i> September 18, 2022</p>
                    <div class="content-article" style="font-size: 1.15rem; line-height: 1.8; color: #cbd5e1;">
                        <p>Proper firearm maintenance is the bedrock of reliability and longevity. While modern firearms are incredibly resilient and can endure thousands of rounds between deep cleanings, neglecting basic maintenance will eventually lead to malfunctions and degraded accuracy. The goal of cleaning isn't necessarily to make the gun look brand new, but to remove carbon buildup, copper fouling, and debris from critical operating surfaces.</p>
                        <p>When cleaning a barrel, always push your patches and bore brushes in the direction of bullet travel—from the chamber to the muzzle. Pulling a brush backward through the muzzle crown can cause micro-abrasions that will negatively impact the rifle's precision over time. Use a high-quality solvent designed to break down carbon, and follow it up with a lightly oiled patch to protect the bore against corrosion.</p>
                        <p>Lubrication is just as important as cleaning. A firearm that is run completely dry will suffer from accelerated wear on the bolt carrier group, slide rails, and trigger components. Apply a light coat of synthetic gun oil to the contact points specified in your owner's manual. Remember the golden rule: if it slides, grease it; if it rotates, oil it. Regular, mindful maintenance guarantees your firearm will be ready when you need it most.</p>
                    </div>
                </div>
            </div>
        </div>

        <!-- Post 7 -->
        <div class="col-12">
            <div class="card border-0 shadow-lg rounded-4 overflow-hidden bg-dark text-white">
                <img src="https://images.unsplash.com/photo-1588725832788-b78e1784b123?q=80&w=1200" class="card-img-top object-fit-cover" style="height: 450px;" alt="Ammunition">
                <div class="card-body p-5">
                    <span class="badge bg-danger mb-3 font-monospace px-3 py-2">BALLISTICS</span>
                    <h2 class="font-outfit fw-bold text-white mb-3">Choosing the Right Ammunition</h2>
                    <p class="text-secondary small mb-4"><i class="bi bi-person-fill text-danger"></i> Ammo Expert &nbsp;&nbsp;|&nbsp;&nbsp; <i class="bi bi-clock text-danger"></i> July 04, 2022</p>
                    <div class="content-article" style="font-size: 1.15rem; line-height: 1.8; color: #cbd5e1;">
                        <p>Ammunition selection is a critical variable that directly affects the performance, terminal ballistics, and reliability of your firearm. The market is saturated with options ranging from cheap steel-cased plinking rounds to highly engineered, match-grade hollow points. Understanding the differences between these loads is essential for any responsible shooter, whether you're hunting, competing, or carrying for self-defense.</p>
                        <p>For training and target practice, Full Metal Jacket (FMJ) ammunition is the standard choice. It's cost-effective and feeds reliably in almost all firearms. However, FMJ rounds are notorious for over-penetration and should never be used for self-defense. For defensive applications, Jacketed Hollow Points (JHP) are required. JHP rounds are designed to expand upon impact, transferring their kinetic energy into the target and mitigating the risk of passing through and hitting an unintended backdrop.</p>
                        <p>When selecting defensive ammo, it is imperative that you test it thoroughly in your specific firearm. Just because a hollow point performs exceptionally well in gelatin tests does not guarantee it will feed reliably up your pistol's feed ramp. Purchase a few boxes of your chosen defensive load and run them through your gun at the range. Once you verify 100% reliability, you can confidently carry that ammunition.</p>
                    </div>
                </div>
            </div>
        </div>

        <!-- Post 8 -->
        <div class="col-12">
            <div class="card border-0 shadow-lg rounded-4 overflow-hidden bg-dark text-white">
                <img src="https://images.unsplash.com/photo-1595590423985-3bc4daaa6a0e?q=80&w=1200" class="card-img-top object-fit-cover" style="height: 450px;" alt="Competitive Shooting">
                <div class="card-body p-5">
                    <span class="badge bg-danger mb-3 font-monospace px-3 py-2">COMPETITION</span>
                    <h2 class="font-outfit fw-bold text-white mb-3">Getting Started in Competitive Shooting</h2>
                    <p class="text-secondary small mb-4"><i class="bi bi-person-fill text-danger"></i> Match Director &nbsp;&nbsp;|&nbsp;&nbsp; <i class="bi bi-clock text-danger"></i> April 11, 2022</p>
                    <div class="content-article" style="font-size: 1.15rem; line-height: 1.8; color: #cbd5e1;">
                        <p>Competitive shooting is one of the most effective and exhilarating ways to stress-test your marksmanship skills under the pressure of a ticking clock. Whether you are interested in the dynamic movement of USPSA, the scenario-based challenges of IDPA, or the extreme long-range precision of PRS, there is a discipline tailored to every interest. Getting started can seem intimidating, but the community is famously welcoming to newcomers.</p>
                        <p>Your first step should be to attend a local match as a spectator. Introduce yourself to the Match Director, observe the safety protocols, and watch how the stages are navigated. You don't need a custom $5,000 race gun to start; a reliable stock pistol, a secure Outside the Waistband (OWB) holster, a few magazine pouches, and standard ammunition are more than enough to compete in the production or stock divisions.</p>
                        <p>When you shoot your first match, your sole objective should be to finish without a safety disqualification (DQ). Forget about your time, forget about winning, and focus entirely on safe gun handling and muzzle awareness. Moving with a loaded firearm introduces complex variables that static range shooting cannot prepare you for. Take it slow, learn the ropes, and you'll quickly find yourself addicted to the sport.</p>
                    </div>
                </div>
            </div>
        </div>

        <!-- Post 9 -->
        <div class="col-12">
            <div class="card border-0 shadow-lg rounded-4 overflow-hidden bg-dark text-white">
                <img src="https://images.unsplash.com/photo-1504938637774-63bececc42a3?q=80&w=1200" class="card-img-top object-fit-cover" style="height: 450px;" alt="Ballistics">
                <div class="card-body p-5">
                    <span class="badge bg-danger mb-3 font-monospace px-3 py-2">EDUCATION</span>
                    <h2 class="font-outfit fw-bold text-white mb-3">Understanding Ballistics for Beginners</h2>
                    <p class="text-secondary small mb-4"><i class="bi bi-person-fill text-danger"></i> Science Desk &nbsp;&nbsp;|&nbsp;&nbsp; <i class="bi bi-clock text-danger"></i> February 28, 2022</p>
                    <div class="content-article" style="font-size: 1.15rem; line-height: 1.8; color: #cbd5e1;">
                        <p>Ballistics is the science of projectiles and their flight dynamics, and having a fundamental grasp of this subject is essential for extending your effective range and accuracy. Ballistics is generally divided into three phases: internal (what happens inside the barrel), external (the bullet's flight through the air), and terminal (what happens when the bullet strikes the target). For most shooters, external ballistics is the most critical area of study.</p>
                        <p>Once a bullet leaves the muzzle, it is immediately subjected to gravity and air resistance. Gravity causes the bullet to drop in a parabolic arc, while air resistance causes it to shed velocity. A bullet's Ballistic Coefficient (BC) is a mathematical representation of its aerodynamic efficiency. Bullets with a high BC retain velocity better, resist wind drift more effectively, and fly flatter over long distances compared to low-BC projectiles.</p>
                        <p>Environmental factors such as altitude, temperature, and humidity also play a significant role. Cold, dense air at sea level creates more drag on a bullet than warm, thin air at high altitudes. Understanding these variables allows shooters to input accurate data into ballistic solvers, generating precise elevation and windage holdovers. Mastering ballistics turns long-range shooting from a game of guesswork into a calculated science.</p>
                    </div>
                </div>
            </div>
        </div>

        <!-- Post 10 -->
        <div class="col-12">
            <div class="card border-0 shadow-lg rounded-4 overflow-hidden bg-dark text-white">
                <img src="https://images.unsplash.com/photo-1601009117652-32b4b4a3a60a?q=80&w=1200" class="card-img-top object-fit-cover" style="height: 450px;" alt="AR-15 Build">
                <div class="card-body p-5">
                    <span class="badge bg-danger mb-3 font-monospace px-3 py-2">BUILD GUIDE</span>
                    <h2 class="font-outfit fw-bold text-white mb-3">Building Your First AR-15: A Comprehensive Guide</h2>
                    <p class="text-secondary small mb-4"><i class="bi bi-person-fill text-danger"></i> DIY Gunsmith &nbsp;&nbsp;|&nbsp;&nbsp; <i class="bi bi-clock text-danger"></i> December 10, 2021</p>
                    <div class="content-article" style="font-size: 1.15rem; line-height: 1.8; color: #cbd5e1;">
                        <p>The AR-15 is often affectionately referred to as "Lego for adults," and for good reason. Its modular design allows anyone with a few basic hand tools to assemble a customized, highly capable rifle from scratch. Building your own AR-15 not only saves you money but also provides you with an intimate understanding of the weapon's mechanics, empowering you to diagnose and repair any issues that may arise in the future.</p>
                        <p>The process begins with acquiring a stripped lower receiver, which is the only part legally considered a firearm. From there, you will install a lower parts kit (LPK), the trigger group, buffer tube assembly, and stock. The upper receiver is often purchased fully assembled for beginners, as properly torquing a barrel and aligning a gas block requires specialized vise blocks and torque wrenches. However, assembling an upper from scratch is entirely achievable with patience and the right tools.</p>
                        <p>When selecting components, pay close attention to the barrel twist rate, as this will dictate the optimal bullet weights your rifle will stabilize. A 1:7 or 1:8 twist rate is highly versatile and handles standard 55-grain and heavier 77-grain projectiles exceptionally well. Take your time, watch instructional videos from trusted armorers, and never force a part into place. The satisfaction of firing a rifle you built with your own hands is truly unparalleled.</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
    {% else %}
    """
    
    # Let's write the wrapper around the original content
    new_row_content = news_content + "\n    <!-- Fallback layout for other categories -->\n    " + old_row_content + "\n    {% endif %}"
    
    new_text = text[:start_idx] + new_row_content + text[end_idx:]
    
    with open(r'c:\Users\HANSLEM_KIMENG\Desktop\WEB\Armor\templates\catalog\trigger_times.html', 'w', encoding='utf-8') as f:
        f.write(new_text)
    
    print("News successfully updated with full professional contents.")
else:
    print("Could not find the row block.")
