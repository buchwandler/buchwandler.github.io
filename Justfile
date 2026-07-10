serve port="4001":
    bundle exec jekyll serve --config _config.yml,_config_termux.yml --force_polling --host 127.0.0.1 --port {{port}}

install:
    bundle install

sphinxpress-build:
    sphinxpress build-site --all
    python3 scripts/wrap_sphinxpress_jekyll_raw.py

sphinxpress-check:
    sphinxpress check

build: sphinxpress-build
    bundle exec jekyll build
