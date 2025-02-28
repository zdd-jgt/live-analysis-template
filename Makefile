# 项目全局配置
PROJECT_NAME = live-analysis
DOCKER_COMPOSE_FILE = docker/docker-compose.yml
REQUIREMENTS_DIR = requirements

# 定义默认目标
.DEFAULT_GOAL := help

# 帮助信息
.PHONY: help
help:  ## 显示帮助信息
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

# 初始化
.PHONY: install
install:  ## 安装开发环境依赖
	pip install -r $(REQUIREMENTS_DIR)/dev.txt
	pre-commit install

# 代码质量
.PHONY: format
format:  ## 格式化代码
	black .
	isort .

.PHONY: lint
lint:  ## 静态代码检查
	flake8 --max-complexity=10 core/ api/
	mypy --config-file mypy.ini

# 测试相关
.PHONY: test
test:  ## 运行所有测试
	pytest -v tests/ --cov=core --cov=api --cov-report=term-missing

.PHONY: coverage
coverage: test  ## 生成HTML覆盖率报告
	coverage html
	@echo "Open file://$$(pwd)/htmlcov/index.html"

# 本地开发
.PHONY: run-dev
run-dev:  ## 启动开发服务器
	uvicorn api.main:app --reload --port 8000

.PHONY: run-docker
run-docker:  ## 启动本地Docker环境
	docker-compose -f $(DOCKER_COMPOSE_FILE) up -d --build

# 构建部署
.PHONY: build
build:  ## 构建生产镜像
	docker build -t $(PROJECT_NAME):latest -f docker/app.Dockerfile .

.PHONY: deploy
deploy: build  ## 部署到生产环境
	docker-compose -f $(DOCKER_COMPOSE_FILE) up -d --scale app=3

# 数据库管理
.PHONY: migrate
migrate:  ## 执行数据库迁移
	alembic upgrade head

.PHONY: rollback
rollback:  ## 回滚数据库迁移
	alembic downgrade -1

# 清理
.PHONY: clean
clean:  ## 清理临时文件
	find . -name "*.pyc" -exec rm -f {} \;
	find . -name "__pycache__" -exec rm -rf {} \;
	rm -rf .coverage htmlcov

.PHONY: clean-docker
clean-docker:  ## 清理Docker资源
	docker-compose -f $(DOCKER_COMPOSE_FILE) down -v
	docker system prune -af
