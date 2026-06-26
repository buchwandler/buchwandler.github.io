serve port="4001":
    bundle exec jekyll serve --config _config.yml,_config_termux.yml --force_polling --host 127.0.0.1 --port {{port}}

install:
    bundle install
