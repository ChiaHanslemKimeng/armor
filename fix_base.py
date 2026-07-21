import re

with open('old_base.html', 'r', encoding='utf-8') as f:
    original = f.read()

# For desktop navAccTrigger:
# Add the News subcategory link at the bottom of the accordion, right before </div>\n                    </div>\n                </li>\n\n                <!-- 14. Resources -->
# But wait, original has:
#                             </div>
#                         </div>
#                     </div>
#                 </li>
desktop_replacement = """                            </div>
                            <div class="accordion-item bg-transparent border-0">
                                <a href="/trigger-times/?cat=news" class="nav-subcategory-btn text-decoration-none d-block mt-2">
                                    <span><i class="bi bi-caret-right-fill me-1 text-info"></i> News</span>
                                </a>
                            </div>
                        </div>"""
original = original.replace('                            </div>\n                        </div>\n                    </div>\n                </li>\n\n                <!-- 14. Resources -->', desktop_replacement + '\n                    </div>\n                </li>\n\n                <!-- 14. Resources -->')

# For mobile offAccTrigger:
# We need to replace only the offTrigNews accordion item block.
# Let's find the old News block:
old_mobile_news_block = """                                <div class="accordion-item bg-transparent border-0">
                                    <button class="nav-subcategory-btn collapsed py-2 text-white" type="button" data-bs-toggle="collapse" data-bs-target="#offTrigNews">
                                        <span><i class="bi bi-caret-right-fill me-1 text-info"></i> News</span>
                                        <i class="bi bi-chevron-down small"></i>
                                    </button>
                                    <div id="offTrigNews" class="collapse" data-bs-parent="#offAccTrigger">
                                        <div class="py-1 px-3 bg-dark rounded-3 mb-2 d-flex flex-column gap-1">
                                            <a href="/trigger-times/?cat=2a-action" class="text-white text-decoration-none small py-1">2A Action Center</a>
                                            <a href="/trigger-times/?cat=press" class="text-white text-decoration-none small py-1">Press Releases</a>
                                            <a href="/trigger-times/?cat=new-website" class="text-white text-decoration-none small py-1">Great News: A New Brownells Website!</a>
                                            <a href="/trigger-times/?cat=monthly-picks" class="text-white text-decoration-none small py-1">Monthly Picks</a>
                                            <a href="/trigger-times/?cat=video-requests" class="text-white text-decoration-none small py-1">What Videos Would You Like To See Us Do?</a>
                                        </div>
                                    </div>
                                </div>"""

new_mobile_news_block = """                                <div class="accordion-item bg-transparent border-0">
                                    <a href="/trigger-times/?cat=news" class="nav-subcategory-btn text-decoration-none text-white d-block py-2">
                                        <span><i class="bi bi-caret-right-fill me-1 text-info"></i> News</span>
                                    </a>
                                </div>"""

original = original.replace(old_mobile_news_block, new_mobile_news_block)

# Since we want to restore base.html to old_base.html with these two modifications,
# But wait, we MUST ALSO retain the push_manager.js script added at the end of the file in base.html if it was there!
# The push_manager script is:
#     {% if user.is_authenticated and user.is_staff %}
#     <script src="{% static 'js/push_manager.js' %}"></script>
#     <script>
#         document.addEventListener('DOMContentLoaded', () => {
#             if (window.initializePushNotifications) {
#                 window.initializePushNotifications();
#             }
#         });
#     </script>
#     {% endif %}

with open(r'c:\Users\HANSLEM_KIMENG\Desktop\WEB\Armor\templates\base.html', 'r', encoding='utf-8') as f:
    current = f.read()

import re
push_script_match = re.search(r'{%\s*if user\.is_authenticated and user\.is_staff\s*%}.*?{%\s*endif\s*%}', current, re.DOTALL)
if push_script_match:
    push_script = push_script_match.group(0)
    # Check if original already has it
    if push_script not in original:
        original = original.replace('{% block extra_js %}{% endblock %}', push_script + '\n    \n    {% block extra_js %}{% endblock %}')


with open(r'c:\Users\HANSLEM_KIMENG\Desktop\WEB\Armor\templates\base.html', 'w', encoding='utf-8') as f:
    f.write(original)

print("Base HTML fixed")
