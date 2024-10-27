# List commands by default
default:
    just --list

# Compile latex into tightly wrapped svgs for recipes
latex-svg name:
    rm -rf "output/latex/{{ name }}"
    mkdir -p "output/latex/{{ name }}"
    cp "static/latex/{{ name }}.tex" "output/latex/{{ name }}/{{ name }}.tex"
    lualatex --output-directory="output/latex/{{ name }}/" --output-format=dvi "output/latex/{{ name }}/{{ name }}.tex"
    dvisvgm --stdout -O -n -Z 2 "output/latex/{{ name }}/{{ name }}.dvi" > "output/latex/{{ name }}/{{ name }}.svg"
    cp "output/latex/{{ name }}/{{ name }}.svg" "static/images/{{ name }}.svg"

# Fetch newer versions of Mathjax to vendor
mathjax-update:
    wget --output-document "assets/js/tex-svg.js" "https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg-full.js"

# Build Typescript files
build-ts file:
    parcel build "{{ file }}" --dist-dir "$(filenametool parent {{ file }})"

# Create a new post
new-post category slug:
    hugo new --kind "post" content/posts/{{ category }}/{{ `date +%Y-%m-%d` }}-{{slug}}.md

# Create a new bundle
new-bundle category slug type="single":
    hugo new --kind "post" content/posts/{{ category }}/{{ `date +%Y-%m-%d` }}-{{slug}}

# Create a new microblog
new-status:
    hugo new --kind "status" content/status/{{ `date +%Y-%m-%d-%H-%M` }}.md

# Building
build *flags:
    rm -rf build/public
    mkdir -p build/public
    hugo --destination build/public {{flags}}
    just _post-process build/public

# Push the new site to Github
publish: build
    touch build/public/.nojekyll
    mv build/temp "/tmp/deleted-blog-temp-$(date +%s)" || true
    mkdir -p build/temp
    cp -r .git build/temp/.git
    cd build/temp && git fetch --all && git switch -c --force gh-pages && git pull
    mv build/temp/.git build/public/.git
    cd build/public \
      && git add . \
      && git commit -m "deployment" \
      && git push

# Build a debug version (with drafts and environment set to 'development')
build-debug: (build "--buildDrafts" "--environment" "development")

# Watch the directory for change and rebuild
watch-debug:
    python tool_scripts/watch.py | while read changed; do echo "Changed $changed"; just build-debug; done

# Run a caddy server, with filewatching, and auto-reload. (Port=12000)
serve-debug: build-debug
    just watch-debug &
    caddy file-server --root build/public --listen 0.0.0.0:12000

# Deploy the debug version of the site to a folder
deploy-debug destination: build-debug
    rm -rf "{{ destination }}/*"
    cp -r build/public/* "{{ destination }}/"

# Internal commands

_post-process sitedir:
    just _post-process-css "{{ sitedir }}" & just _post-process-html "{{ sitedir }}" && wait
    echo "$(date --rfc-3339=seconds --utc)" > {{ sitedir }}/_last_modified.txt

_post-process-css sitedir:
    fd "\.css" {{ sitedir }} --exec lightningcss -m "{}" --output-file "{}"

_post-process-html sitedir:
    fd -t f ".html" "{{ sitedir }}/" --exec python tool_scripts/add_bibliography.py
    python tool_scripts/generate_responsive_images.py "{{ sitedir }}/"
    python tool_scripts/check_dead_links.py "{{ sitedir }}/"
    fd -t f ".html" "{{ sitedir }}/" --exec prettier --ignore-path -w
