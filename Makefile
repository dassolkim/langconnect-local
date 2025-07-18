.PHONY: build up down restart mcp test ollama-setup ollama-pull

build:
	@echo "🔨 Building Next.js application..."
	@cd next-connect-ui && npm install && npm run build
	@echo "✅ Next.js build completed!"
	@echo ""
	@echo "🔨 Building Docker images..."
	@docker compose build
	@echo "✅ Docker build completed successfully!"
	@echo "📌 Run 'make up' to start the server"

up:
	@echo "🚀 Starting LangConnect server..."
	@docker compose up -d
	@echo "✅ Server started successfully!"
	@echo "📌 Access points:"
	@echo "   - API Server: http://localhost:8080"
	@echo "   - API Docs: http://localhost:8080/docs"
	@echo "   - Next.js UI: http://localhost:3000"
	@echo "   - PostgreSQL: localhost:5432"

down:
	@echo "🛑 Stopping LangConnect server..."
	@docker compose down
	@echo "✅ Server stopped successfully!"

restart:
	@echo "🔄 Restarting LangConnect server..."
	@docker-compose down
	@docker-compose up -d
	@echo "✅ Server restarted successfully!"

mcp:
	@echo "🔧 Creating MCP configuration..."
	@uv run python mcpserver/create_mcp_json.py
	@echo "✅ MCP configuration created successfully!"

TEST_FILE ?= tests/unit_tests

test:
	./run_tests.sh $(TEST_FILE)

ollama-setup:
	@echo "🤖 Setting up Ollama embedding model..."
	@docker compose up -d ollama
	@echo "⏳ Waiting for Ollama to start..."
	@sleep 10
	@echo "📥 Pulling nomic-embed-text model..."
	@docker exec langconnect-ollama ollama pull nomic-embed-text
	@echo "✅ Ollama setup completed!"
	@echo "📌 You can now set USE_OLLAMA_EMBEDDINGS=true in your .env file"
	@echo "📌 Ollama is running on port 11435 (to avoid conflict with local Ollama on 11434)"

ollama-pull:
	@echo "📥 Pulling Ollama embedding model..."
	@docker exec langconnect-ollama ollama pull nomic-embed-text
	@echo "✅ Model pulled successfully!"
	@echo "📌 Ollama is running on port 11435 (external)"

