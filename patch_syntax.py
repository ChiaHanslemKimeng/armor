import re
import os

filepath = r'c:\Users\HANSLEM_KIMENG\Desktop\WEB\Armor\templates\catalog\trigger_times.html'

with open(filepath, 'r', encoding='utf-8') as f:
    text = f.read()

# Fix the breadcrumbs
bad_breadcrumb = """            {% endif %}

    {% elif request.GET.cat == 'adventure' %} > <span class="fw-bold text-danger">Adventure</span>"""

good_breadcrumb = """            {% elif request.GET.cat == 'adventure' %} > <span class="fw-bold text-danger">Adventure</span>"""

text = text.replace(bad_breadcrumb, good_breadcrumb)

# Wait, my bad_breadcrumb has > instead of &gt;
# Let's use regex to fix the breadcrumbs
breadcrumb_pattern = re.compile(r'\{\%\s*endif\s*\%\}\s*\{\%\s*elif request\.GET\.cat == \'adventure\'\s*\%\}')
text = breadcrumb_pattern.sub(r'{% elif request.GET.cat == \'adventure\' %}', text, count=1)

# Ensure the end of the file has the closing {% endif %} for the main outer block.
# Right now it ends with:
#     </section>
# 
# <!-- Newsletter Subscribe -->
# We want it to be:
#     {% endif %}</section>
if "{% endif %}</section>" not in text:
    text = text.replace("    </section>", "    {% endif %}</section>")
elif text.count("{% endif %}</section>") > 1:
    pass

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(text)

print("trigger_times.html patched.")
