latex-svg name:
    mkdir -p output
    latex --output-directory=output/ --output-format=dvi static/latex/{{ name }}.tex
    dvisvgm --stdout -O -n output/{{ name }}.dvi > static/images/{{ name }}.svg

mathjax-update:
    wget --output-document "themes/rocinante/assets/js/tex-svg.js" "https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg-full.js"

serve:
    hugo serve -D --port 1313