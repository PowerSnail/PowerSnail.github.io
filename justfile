latex-svg name:
    rm -rf "output/latex/{{ name }}"
    mkdir -p "output/latex/{{ name }}"
    cp "static/latex/{{ name }}.tex" "output/latex/{{ name }}/{{ name }}.tex"
    lualatex --output-directory="output/latex/{{ name }}/" --output-format=dvi "output/latex/{{ name }}/{{ name }}.tex"
    dvisvgm --stdout -O -n -Z 2 "output/latex/{{ name }}/{{ name }}.dvi" > "output/latex/{{ name }}/{{ name }}.svg"
    cp "output/latex/{{ name }}/{{ name }}.svg" "static/images/{{ name }}.svg"

mathjax-update:
    wget --output-document "themes/rocinante/assets/js/tex-svg.js" "https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg-full.js"

change-color:
    python3 tool_scripts/make_theme.py > assets/css/_color.scss

build-ts file:
    parcel build "{{ file }}" --dist-dir "$(filenametool parent {{ file }})"

generate-icon-css:
    python3 tool_scripts/social_icon.py > assets/css/_icons.scss

new-post category slug type="single":
    hugo new --kind "post" content/posts/{{ category }}/{{ `date +%Y-%m-%d` }}-{{slug}}{{ if type == "bundle" { "" } else { ".md" } }}

new-status:
    hugo new --kind "status" content/status/{{ `date +%Y-%m-%d-%H-%M` }}.md

serve:
    hugo serve -D --port 1313

serve-at target:
    hugo serve -D --port 1313 --baseURL="{{ target }}" --appendPort=false

deploy-test base destination:
    hugo --baseURL {{ base }} --destination {{ destination }} --forceSyncStatic -w --noChmod --gc --ignoreCache --buildDrafts 

deploy:
    hugo --minify
    python tool_scripts/check_dead_links.py public/
    touch public/.nojekyll

publish:
    git subtree push --prefix public origin gh-pages
