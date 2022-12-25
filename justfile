default:
    just --list

latex-svg name:
    rm -rf "output/latex/{{ name }}"
    mkdir -p "output/latex/{{ name }}"
    cp "static/latex/{{ name }}.tex" "output/latex/{{ name }}/{{ name }}.tex"
    lualatex --output-directory="output/latex/{{ name }}/" --output-format=dvi "output/latex/{{ name }}/{{ name }}.tex"
    dvisvgm --stdout -O -n -Z 2 "output/latex/{{ name }}/{{ name }}.dvi" > "output/latex/{{ name }}/{{ name }}.svg"
    cp "output/latex/{{ name }}/{{ name }}.svg" "static/images/{{ name }}.svg"

mathjax-update:
    wget --output-document "assets/js/tex-svg.js" "https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg-full.js"

build-ts file:
    parcel build "{{ file }}" --dist-dir "$(filenametool parent {{ file }})"

generate-icon-css:
    python3 tool_scripts/social_icon.py > assets/css/_icons.scss

new-post category slug:
    hugo new --kind "post" content/posts/{{ category }}/{{ `date +%Y-%m-%d` }}-{{slug}}.md

new-bundle category slug type="single":
    hugo new --kind "post" content/posts/{{ category }}/{{ `date +%Y-%m-%d` }}-{{slug}}

new-status:
    hugo new --kind "status" content/status/{{ `date +%Y-%m-%d-%H-%M` }}.md

_build *flags:
    hugo mod clean --all && rm -r public
    rm -rf build/public
    mkdir -p build/public
    hugo --destination build/public {{flags}}
    just _post-process build/public

deploy-debug destination: (_build "--buildDrafts" "--environment" "development")
    rm -rf "{{ destination }}/*"
    cp -r build/public/* "{{ destination }}/"

publish: _build
    touch build/public/.nojekyll
    rm -rf build/temp
    git clone --depth 1 --branch gh-pages --single-branch git@github.com:PowerSnail/PowerSnail.github.io.git build/temp
    mv build/temp/.git build/public/.git
    cd build/public && git add . && git commit -m "deployment" && git push || true

_post-process sitedir:
    fd "style.css" {{ sitedir }} --exec python tool_scripts/make_theme.py "$(rg 'theme_color = "(.*)+"' -r '$1' config.toml)" --output
    fd "\.css" {{ sitedir }} --exec lightningcss -m "{}" --output-file "{}"
    python tool_scripts/generate_responsive_images.py "{{ sitedir }}/"
    python tool_scripts/check_dead_links.py "{{ sitedir }}/"
    fd ".html" "{{ sitedir }}/" --exec just _format-html 

_format-html path:
    #!/bin/bash
    output=$(tidy --wrap 0 --indent yes --drop-empty-elements no -m -q {{ path }} 2>&1)
    if [[ $? != 0 ]] 
    then
        echo {{ path }}
        echo $output
    fi
    
