## install 
uv pip install reflex
## run

reflex run 
reflex run --loglevel debug

## 数据库使用
reflex db init
reflex db makemigrations --message "init"
reflex db migrate

sudo -u postgres psql