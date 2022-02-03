latex-svg name:
    rm -rf "output/latex/{{ name }}"
    mkdir -p "output/latex/{{ name }}"
    cp "static/latex/{{ name }}.tex" "output/latex/{{ name }}/{{ name }}.tex"
    lualatex --output-directory="output/latex/{{ name }}/" --output-format=dvi "output/latex/{{ name }}/{{ name }}.tex"
    dvisvgm --stdout -O -n "output/latex/{{ name }}/{{ name }}.dvi" > "output/latex/{{ name }}/{{ name }}.svg"
    cp "output/latex/{{ name }}/{{ name }}.svg" "static/images/{{ name }}.svg"

mathjax-update:
    wget --output-document "themes/rocinante/assets/js/tex-svg.js" "https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg-full.js"

change-color color:
    python tool_scripts/make_theme.py "{{ color }}" > assets/css/_color.scss

generate-icon-css:
    python tool_scripts/social_icon.py > assets/css/_icons.scss

new-post category slug:
    hugo new --kind "post" content/{{ category }}/{{ `date +%Y-%m-%d` }}-{{slug}}.md

serve:
    hugo serve -D --port 1313
