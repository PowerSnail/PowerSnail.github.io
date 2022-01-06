latex-svg name:
    mkdir -p output
    latex --output-directory=output/ --output-format=dvi static/latex/{{ name }}.tex
    dvisvgm --stdout -O -n output/{{ name }}.dvi > static/images/{{ name }}.svg

serve:
    hugo serve -D --port 1313