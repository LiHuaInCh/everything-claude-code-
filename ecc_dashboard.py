#!/usr/bin/env python3
"""
ECC Dashboard - Everything Claude Code GUI
Cross-platform TkInter application for managing ECC components
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import os
import json
from pathlib import Path
from typing import Dict, List, Optional
import webbrowser

from scripts.lib.ecc_dashboard_runtime import launch_terminal, maximize_window


# ============================================================================
# TRANSLATION MAPPING - English to Chinese
# ============================================================================

AGENT_ZH = {
    "a11y-architect": ("无障碍架构师", "WCAG 2.2 合规专家，涵盖 Web 与原生平台。设计 UI 组件、建立设计系统或审计无障碍体验时主动使用。"),
    "architect": ("软件架构师", "系统设计与可扩展性专家。规划新功能、重构大型系统或做架构决策时主动使用。"),
    "build-error-resolver": ("构建错误修复", "构建与 TypeScript 错误修复专家。构建失败或类型错误时使用，最小化改动修复构建问题。"),
    "chief-of-staff": ("通讯总管", "个人通讯总管，分诊邮件、Slack、LINE 和 Messenger。将消息分为 4 级并生成回复草稿。管理多渠道通讯时使用。"),
    "code-architect": ("代码架构师", "分析现有代码库模式与约定，设计功能架构并提供包含具体文件、接口、数据流和构建顺序的实现蓝图。"),
    "code-explorer": ("代码探索者", "深度分析现有代码库功能，追踪执行路径，映射架构层次，记录依赖关系以指导新开发。"),
    "code-reviewer": ("代码审查", "专家级代码审查，主动审查代码质量、安全性和可维护性。编写或修改代码后立即使用。"),
    "code-simplifier": ("代码精简", "精简和优化代码以提升清晰度、一致性和可维护性，同时保持行为不变。"),
    "comment-analyzer": ("注释分析", "分析代码注释的准确性、完整性、可维护性和过时风险。"),
    "conversation-analyzer": ("会话分析", "分析对话记录以找出值得用 hooks 预防的行为模式。由 /hookify 触发。"),
    "cpp-build-resolver": ("C++ 构建修复", "C++ 构建、CMake 和编译错误修复专家。修复构建错误、链接器问题和模板错误。C++ 构建失败时使用。"),
    "cpp-reviewer": ("C++ 代码审查", "C++ 代码审查专家，专注内存安全、现代 C++ 惯用法、并发和性能。"),
    "csharp-reviewer": ("C# 代码审查", "C# 代码审查专家，专注 .NET 规范、异步模式、安全性和性能。"),
    "dart-build-resolver": ("Dart 构建修复", "Dart/Flutter 构建与依赖错误修复专家。修复 dart analyze 错误和 Flutter 编译失败。"),
    "database-reviewer": ("数据库审查", "PostgreSQL 数据库专家，专注查询优化、Schema 设计、安全性和性能。包含 Supabase 最佳实践。"),
    "doc-updater": ("文档更新", "文档与代码地图专家。主动更新 codemap 和文档，生成 docs/CODEMAPS/*。"),
    "docs-lookup": ("文档查询", "当用户询问库/框架/API 用法或需要最新代码示例时，使用 Context7 MCP 获取当前文档。"),
    "e2e-runner": ("E2E 测试", "端到端测试专家，使用 Vercel Agent Browser（优先）和 Playwright（备选）。管理测试旅程、隔离不稳定测试、上传测试产物。"),
    "fastapi-reviewer": ("FastAPI 审查", "审查 FastAPI 应用的异步正确性、依赖注入、Pydantic Schema、安全性和生产就绪度。"),
    "flutter-reviewer": ("Flutter 审查", "Flutter/Dart 代码审查，专注 Widget 最佳实践、状态管理模式和性能陷阱。"),
    "fsharp-reviewer": ("F# 代码审查", "F# 代码审查专家，专注函数式惯用法、类型安全和模式匹配。"),
    "gan-evaluator": ("GAN 评估器", "通过 Playwright 测试运行中的应用程序，按评分标准打分并提供可操作的反馈。"),
    "gan-generator": ("GAN 生成器", "根据规格说明实现功能，读取评估器反馈并迭代直到达到质量阈值。"),
    "gan-planner": ("GAN 规划器", "将一行提示扩展为完整的产品规格，包含功能、迭代、评估标准和设计方向。"),
    "go-build-resolver": ("Go 构建修复", "Go 构建与编译错误修复专家。修复构建错误和 go vet 问题。Go 构建失败时使用。"),
    "go-reviewer": ("Go 代码审查", "Go 代码审查专家，专注惯用 Go 模式、并发模式、错误处理和性能。"),
    "harmonyos-app-resolver": ("HarmonyOS 开发", "HarmonyOS 应用开发专家，专注 ArkTS 和 ArkUI。审查 V2 状态管理、Navigation 路由模式和 API 使用。"),
    "harness-optimizer": ("Harness 优化", "分析和改进本地 agent harness 配置，提升可靠性、成本和吞吐量。"),
    "healthcare-reviewer": ("医疗代码审查", "审查医疗应用代码的临床安全性、CDSS 准确性、PHI 合规性和医疗数据完整性。"),
    "homelab-architect": ("家庭网络架构", "根据硬件清单、目标和操作者经验水平设计家庭和小型实验室网络方案。"),
    "java-build-resolver": ("Java 构建修复", "Java/Maven/Gradle 构建与编译错误修复专家。Java 或 Spring Boot 构建失败时使用。"),
    "java-reviewer": ("Java 代码审查", "Java 与 Spring Boot 代码审查专家，专注分层架构、JPA 模式、安全性和并发。"),
    "kotlin-build-resolver": ("Kotlin 构建修复", "Kotlin/Gradle 构建与编译错误修复专家。Kotlin 构建失败时使用。"),
    "kotlin-reviewer": ("Kotlin 代码审查", "Kotlin/Android 代码审查，专注惯用模式、协程安全和 Compose 最佳实践。"),
    "loop-operator": ("循环操作器", "操作自主 agent 循环，监控进度并在循环停滞时安全干预。"),
    "mle-reviewer": ("ML 工程审查", "生产机器学习工程审查，涵盖数据契约、特征管道、训练可复现性、模型服务和监控。"),
    "network-architect": ("网络架构师", "根据需求设计企业或多站点网络架构，专注路由、验证、自动化和故障排除。"),
    "network-config-reviewer": ("网络配置审查", "审查路由器和交换机配置的安全性、正确性和操作风险。"),
    "network-troubleshooter": ("网络故障排除", "以只读 OSI 层工作流诊断网络连接、路由、DNS 和接口问题。"),
    "opensource-forker": ("开源 Fork", "Fork 项目用于开源发布。复制文件、剥离密钥和凭证、替换内部引用、清理 git 历史。"),
    "opensource-packager": ("开源打包", "为已清理的项目生成完整的开源打包，包括 CLAUDE.md、README、LICENSE 等。"),
    "opensource-sanitizer": ("开源安全检查", "验证开源 fork 在发布前已充分清理。扫描泄露的密钥、PII 和内部引用。"),
    "performance-optimizer": ("性能优化", "性能分析与优化专家。识别瓶颈、优化慢代码、减少打包体积、分析内存泄漏和渲染优化。"),
    "planner": ("规划器", "复杂功能和重构的专家级规划。用户请求功能实现、架构变更或复杂重构时主动使用。"),
    "pr-test-analyzer": ("PR 测试分析", "审查 Pull Request 的测试覆盖质量和完整性。"),
    "python-reviewer": ("Python 代码审查", "Python 代码审查专家，专注 PEP 8 合规、Pythonic 惯用法、类型提示和安全性。"),
    "pytorch-build-resolver": ("PyTorch 构建修复", "PyTorch/CUDA 训练错误修复专家。修复张量形状不匹配、设备错误和梯度问题。"),
    "refactor-cleaner": ("重构清理", "死代码清理与合并专家。使用分析工具（knip、depcheck、ts-prune）识别并安全移除死代码。"),
    "rust-build-resolver": ("Rust 构建修复", "Rust 构建与编译错误修复专家。修复 cargo 构建错误和 borrow checker 问题。"),
    "rust-reviewer": ("Rust 代码审查", "Rust 代码审查专家，专注所有权、生命周期、错误处理和 unsafe 用法。"),
    "security-reviewer": ("安全审查", "安全漏洞检测与修复专家。处理用户输入、认证、API 端点或敏感数据的代码后使用。"),
    "seo-specialist": ("SEO 专家", "SEO 专家，专注技术 SEO 审计、页面优化、结构化数据和 Core Web Vitals。"),
    "silent-failure-hunter": ("静默失败检测", "审查代码中的静默失败、被吞掉的错误、不良回退和缺失的错误传播。"),
    "swift-build-resolver": ("Swift 构建修复", "Swift/Xcode 构建与编译错误修复专家。Swift 构建失败时使用。"),
    "swift-reviewer": ("Swift 代码审查", "Swift 代码审查专家，专注面向协议设计、值语义、ARC 内存管理和 Swift 并发。"),
    "tdd-guide": ("TDD 指南", "测试驱动开发专家，强制执行先写测试方法论。编写新功能、修复 Bug 或重构时使用。确保 80%+ 覆盖率。"),
    "type-design-analyzer": ("类型设计分析", "分析类型设计的封装性、不变量表达、实用性和执行力度。"),
    "typescript-reviewer": ("TypeScript 代码审查", "TypeScript/JavaScript 代码审查专家，专注类型安全、异步正确性和 Node/Web 安全。"),
}

# Skill category translations for display
SKILL_CATEGORY_ZH = {
    "General": "通用",
    "Python": "Python",
    "Go": "Go",
    "Frontend": "前端",
    "Backend": "后端",
    "Security": "安全",
    "Testing": "测试",
    "DevOps": "DevOps",
    "iOS": "iOS",
    "Java": "Java",
    "Rust": "Rust",
    "PHP": "PHP",
}

def translate_agent_display(agent: dict) -> dict:
    """Apply Chinese translations to agent display fields if available."""
    name = agent.get("name", "")
    if name in AGENT_ZH:
        zh_name, zh_purpose = AGENT_ZH[name]
        agent["name_display"] = zh_name
        agent["purpose"] = zh_purpose
        agent["when_to_use"] = zh_purpose
    return agent

SKILL_NAME_ZH = {
    "accessibility": "无障碍设计",
    "agent-architecture-audit": "Agent 架构审计",
    "agent-eval": "Agent 评估对比",
    "agent-harness-construction": "Agent 工具空间设计",
    "agent-introspection-debugging": "Agent 自调试",
    "agent-payment-x402": "Agent 支付 (x402)",
    "agent-sort": "Agent 排序规划",
    "agentic-engineering": "Agentic 工程",
    "agentic-os": "Agentic 操作系统",
    "ai-first-engineering": "AI 优先工程",
    "ai-regression-testing": "AI 回归测试",
    "android-clean-architecture": "Android 整洁架构",
    "angular-developer": "Angular 开发",
    "api-connector-builder": "API 连接器构建",
    "api-design": "API 设计",
    "architecture-decision-records": "架构决策记录",
    "article-writing": "文章写作",
    "automation-audit-ops": "自动化审计",
    "autonomous-agent-harness": "自主 Agent 框架",
    "autonomous-loops": "自主循环",
    "backend-patterns": "后端模式",
    "benchmark": "性能基准测试",
    "blueprint": "蓝图",
    "brand-voice": "品牌语音",
    "browser-qa": "浏览器 QA",
    "bun-runtime": "Bun 运行时",
    "canary-watch": "金丝雀监控",
    "carrier-relationship-management": "运营商关系管理",
    "cisco-ios-patterns": "Cisco IOS 模式",
    "ck": "持久化项目记忆",
    "claude-devfleet": "Claude DevFleet 调度",
    "click-path-audit": "点击路径审计",
    "clickhouse-io": "ClickHouse",
    "code-tour": "代码导览",
    "codebase-onboarding": "代码库入门",
    "coding-standards": "编码规范",
    "compose-multiplatform-patterns": "Compose Multiplatform",
    "configure-ecc": "配置 ECC",
    "connections-optimizer": "社交网络优化",
    "content-engine": "内容引擎",
    "content-hash-cache-pattern": "内容哈希缓存",
    "context-budget": "上下文预算审计",
    "continuous-agent-loop": "持续 Agent 循环",
    "continuous-learning": "持续学习 v1 (已弃用)",
    "continuous-learning-v2": "持续学习 v2",
    "cost-aware-llm-pipeline": "LLM 成本优化",
    "council": "四声议会决策",
    "cpp-coding-standards": "C++ 编码规范",
    "cpp-testing": "C++ 测试",
    "crosspost": "跨平台分发",
    "csharp-testing": "C# 测试",
    "customer-billing-ops": "客户账单运营",
    "customs-trade-compliance": "海关贸易合规",
    "dart-flutter-patterns": "Dart/Flutter 模式",
    "dashboard-builder": "仪表板构建",
    "data-scraper-agent": "数据抓取 Agent",
    "database-migrations": "数据库迁移",
    "deep-research": "深度研究",
    "defi-amm-security": "DeFi AMM 安全",
    "deployment-patterns": "部署模式",
    "design-system": "设计系统",
    "django-patterns": "Django 模式",
    "django-security": "Django 安全",
    "django-tdd": "Django TDD",
    "django-verification": "Django 验证",
    "dmux-workflows": "Dmux 工作流",
    "docker-patterns": "Docker 模式",
    "documentation-lookup": "文档查找",
    "dotnet-patterns": ".NET 模式",
    "e2e-testing": "E2E 测试",
    "ecc-guide": "ECC 指南",
    "ecc-tools-cost-audit": "ECC 工具成本审计",
    "email-ops": "邮件运营",
    "energy-procurement": "能源采购",
    "enterprise-agent-ops": "企业 Agent 运营",
    "error-handling": "错误处理",
    "eval-harness": "评估框架",
    "evm-token-decimals": "EVM Token 精度",
    "exa-search": "Exa 搜索",
    "fal-ai-media": "Fal AI 媒体",
    "fastapi-patterns": "FastAPI 模式",
    "finance-billing-ops": "财务账单运营",
    "flox-environments": "Flox 环境",
    "flutter-dart-code-review": "Flutter/Dart 审查",
    "foundation-models-on-device": "端侧大模型",
    "frontend-patterns": "前端模式",
    "frontend-slides": "前端幻灯片",
    "fsharp-testing": "F# 测试",
    "gan-style-harness": "GAN 风格框架",
    "gateguard": "关卡守卫",
    "git-workflow": "Git 工作流",
    "github-ops": "GitHub 运营",
    "golang-patterns": "Go 模式",
    "golang-testing": "Go 测试",
    "google-workspace-ops": "Google Workspace",
    "healthcare-cdss-patterns": "医疗 CDSS 模式",
    "healthcare-emr-patterns": "医疗 EMR 模式",
    "healthcare-eval-harness": "医疗评估框架",
    "healthcare-phi-compliance": "医疗 PHI 合规",
    "hermes-imports": "Hermes 导入",
    "hexagonal-architecture": "六边形架构",
    "hipaa-compliance": "HIPAA 合规",
    "homelab-network-readiness": "家庭网络就绪检查",
    "homelab-network-setup": "家庭网络设置",
    "hookify-rules": "规则 Hook 化",
    "inventory-demand-planning": "库存需求规划",
    "investor-materials": "投资人材料",
    "investor-outreach": "投资人外联",
    "ios-icon-gen": "iOS 图标生成",
    "iterative-retrieval": "迭代检索",
    "java-coding-standards": "Java 编码规范",
    "jira-integration": "Jira 集成",
    "jpa-patterns": "JPA 模式",
    "knowledge-ops": "知识运营",
    "kotlin-coroutines-flows": "Kotlin 协程与 Flow",
    "kotlin-exposed-patterns": "Kotlin Exposed 模式",
    "kotlin-ktor-patterns": "Kotlin Ktor 模式",
    "kotlin-patterns": "Kotlin 模式",
    "kotlin-testing": "Kotlin 测试",
    "laravel-patterns": "Laravel 模式",
    "laravel-plugin-discovery": "Laravel 插件发现",
    "laravel-security": "Laravel 安全",
    "laravel-tdd": "Laravel TDD",
    "laravel-verification": "Laravel 验证",
    "lead-intelligence": "线索情报",
    "liquid-glass-design": "液态玻璃设计",
    "llm-trading-agent-security": "LLM 交易 Agent 安全",
    "logistics-exception-management": "物流异常管理",
    "manim-video": "Manim 视频",
    "market-research": "市场研究",
    "mcp-server-patterns": "MCP Server 模式",
    "messages-ops": "消息运营",
    "mle-workflow": "ML 工程工作流",
    "motion-advanced": "Motion 高级",
    "motion-foundations": "Motion 基础",
    "motion-patterns": "Motion 模式",
    "motion-ui": "Motion UI",
    "mysql-patterns": "MySQL 模式",
    "nanoclaw-repl": "Nanoclaw REPL",
    "nestjs-patterns": "NestJS 模式",
    "netmiko-ssh-automation": "Netmiko SSH 自动化",
    "network-bgp-diagnostics": "BGP 诊断",
    "network-config-validation": "网络配置验证",
    "network-interface-health": "网络接口健康",
    "nextjs-turbopack": "Next.js Turbopack",
    "nodejs-keccak256": "Node.js Keccak256",
    "nutrient-document-processing": "Nutrient 文档处理",
    "nuxt4-patterns": "Nuxt 4 模式",
    "openclaw-persona-forge": "OpenClaw 角色锻造",
    "opensource-pipeline": "开源流水线",
    "perl-patterns": "Perl 模式",
    "perl-security": "Perl 安全",
    "perl-testing": "Perl 测试",
    "plan-orchestrate": "规划编排",
    "plankton-code-quality": "Plankton 代码质量",
    "postgres-patterns": "PostgreSQL 模式",
    "product-capability": "产品能力",
    "product-lens": "产品视角",
    "production-audit": "生产审计",
    "production-scheduling": "生产排程",
    "project-flow-ops": "项目流运营",
    "prompt-optimizer": "Prompt 优化",
    "python-patterns": "Python 模式",
    "python-testing": "Python 测试",
    "pytorch-patterns": "PyTorch 模式",
    "quality-nonconformance": "质量不符合项",
    "quarkus-patterns": "Quarkus 模式",
    "quarkus-security": "Quarkus 安全",
    "quarkus-tdd": "Quarkus TDD",
    "quarkus-verification": "Quarkus 验证",
    "ralphinho-rfc-pipeline": "Ralphinho RFC 流水线",
    "redis-patterns": "Redis 模式",
    "regex-vs-llm-structured-text": "正则 vs LLM",
    "remotion-video-creation": "Remotion 视频创作",
    "repo-scan": "仓库扫描",
    "research-ops": "研究运营",
    "returns-reverse-logistics": "退货逆向物流",
    "rules-distill": "规则蒸馏",
    "rust-patterns": "Rust 模式",
    "rust-testing": "Rust 测试",
    "safety-guard": "安全守卫",
    "santa-method": "Santa 方法",
    "scientific-db-pubmed-database": "PubMed 数据库",
    "scientific-db-uspto-database": "USPTO 数据库",
    "scientific-pkg-gget": "gget 包",
    "scientific-thinking-literature-review": "文献综述",
    "scientific-thinking-scholar-evaluation": "学者评估",
    "search-first": "搜索优先",
    "security-bounty-hunter": "安全赏金猎人",
    "security-review": "安全审查",
    "security-scan": "安全扫描",
    "seo": "SEO",
    "skill-comply": "技能合规",
    "skill-stocktake": "技能盘点",
    "social-graph-ranker": "社交图谱排序",
    "springboot-patterns": "Spring Boot 模式",
    "springboot-security": "Spring Boot 安全",
    "springboot-tdd": "Spring Boot TDD",
    "springboot-verification": "Spring Boot 验证",
    "strategic-compact": "战略协定",
    "swift-actor-persistence": "Swift Actor 持久化",
    "swift-concurrency-6-2": "Swift 并发 6.2",
    "swift-protocol-di-testing": "Swift 协议 DI 测试",
    "swiftui-patterns": "SwiftUI 模式",
    "tdd-workflow": "TDD 工作流",
    "team-builder": "团队构建",
    "terminal-ops": "终端运营",
    "tinystruct-patterns": "TinyStruct 模式",
    "token-budget-advisor": "Token 预算顾问",
    "ui-demo": "UI 演示",
    "ui-to-vue": "UI 转 Vue",
    "unified-notifications-ops": "统一通知运营",
    "verification-loop": "验证循环",
    "video-editing": "视频编辑",
    "videodb": "VideoDB",
    "visa-doc-translate": "签证文件翻译",
    "vite-patterns": "Vite 模式",
    "windows-desktop-e2e": "Windows 桌面 E2E",
    "workspace-surface-audit": "工作区表面审计",
    "x-api": "X API",
}

def translate_skill_category(category: str) -> str:
    """Translate skill category to Chinese."""
    return SKILL_CATEGORY_ZH.get(category, category)

# ============================================================================
# DATA LOADERS - Load ECC data from the project
# ============================================================================

def get_project_path() -> str:
    """Get the ECC project path - assumes this script is run from the project dir"""
    return os.path.dirname(os.path.abspath(__file__))


def load_agents(project_path: str) -> List[Dict]:
    """Load agents by scanning the agents/ directory.

    Parses YAML frontmatter (name, description) from each agent file.
    The directory is the source of truth; AGENTS.md is hand-maintained
    and drifts out of sync.
    """
    agents_dir = os.path.join(project_path, "agents")
    agents: List[Dict] = []

    if os.path.isdir(agents_dir):
        for item in sorted(os.listdir(agents_dir)):
            if not item.endswith('.md'):
                continue
            agent_path = os.path.join(agents_dir, item)
            name = os.path.splitext(item)[0]
            description = ''
            try:
                with open(agent_path, 'r', encoding='utf-8') as f:
                    content = f.read()
            except OSError:
                content = ''
            if content.startswith('---'):
                end = content.find('\n---', 3)
                if end != -1:
                    for fm_line in content[3:end].splitlines():
                        stripped = fm_line.strip()
                        if stripped.startswith('name:'):
                            name = stripped.split(':', 1)[1].strip().strip('"\'')
                        elif stripped.startswith('description:'):
                            description = stripped.split(':', 1)[1].strip().strip('"\'')
            agents.append(translate_agent_display({
                'name': name,
                'purpose': description,
                'when_to_use': description,
                'path': agent_path,
            }))

    # Fallback default agents if directory not found
    if not agents:
        agents = [
            {'name': 'planner', 'purpose': '实现规划', 'when_to_use': '复杂功能、重构'},
            {'name': 'architect', 'purpose': '系统设计与可扩展性', 'when_to_use': '架构决策'},
            {'name': 'tdd-guide', 'purpose': '测试驱动开发', 'when_to_use': '新功能、Bug 修复'},
            {'name': 'code-reviewer', 'purpose': '代码质量与可维护性', 'when_to_use': '编写/修改代码后'},
            {'name': 'security-reviewer', 'purpose': '漏洞检测', 'when_to_use': '提交前、敏感代码'},
            {'name': 'build-error-resolver', 'purpose': '修复构建/类型错误', 'when_to_use': '构建失败时'},
            {'name': 'e2e-runner', 'purpose': '端到端 Playwright 测试', 'when_to_use': '关键用户流程'},
            {'name': 'refactor-cleaner', 'purpose': '死代码清理', 'when_to_use': '代码维护'},
            {'name': 'doc-updater', 'purpose': '文档与代码地图', 'when_to_use': '更新文档'},
            {'name': 'go-reviewer', 'purpose': 'Go 代码审查', 'when_to_use': 'Go 项目'},
            {'name': 'python-reviewer', 'purpose': 'Python 代码审查', 'when_to_use': 'Python 项目'},
            {'name': 'typescript-reviewer', 'purpose': 'TypeScript/JavaScript 代码审查', 'when_to_use': 'TypeScript 项目'},
            {'name': 'rust-reviewer', 'purpose': 'Rust 代码审查', 'when_to_use': 'Rust 项目'},
            {'name': 'java-reviewer', 'purpose': 'Java 与 Spring Boot 代码审查', 'when_to_use': 'Java 项目'},
            {'name': 'kotlin-reviewer', 'purpose': 'Kotlin 代码审查', 'when_to_use': 'Kotlin 项目'},
            {'name': 'cpp-reviewer', 'purpose': 'C/C++ 代码审查', 'when_to_use': 'C/C++ 项目'},
            {'name': 'database-reviewer', 'purpose': 'PostgreSQL/Supabase 专家', 'when_to_use': '数据库相关'},
            {'name': 'loop-operator', 'purpose': '自主循环执行', 'when_to_use': '安全运行循环'},
            {'name': 'harness-optimizer', 'purpose': 'Harness 配置调优', 'when_to_use': '可靠性、成本、吞吐量'},
        ]
    
    return agents

def load_skills(project_path: str) -> List[Dict]:
    """Load skills from skills directory"""
    skills_dir = os.path.join(project_path, "skills")
    skills = []
    
    if os.path.exists(skills_dir):
        for item in os.listdir(skills_dir):
            skill_path = os.path.join(skills_dir, item)
            if os.path.isdir(skill_path):
                skill_file = os.path.join(skill_path, "SKILL.md")
                description = item.replace('-', ' ').title()
                
                if os.path.exists(skill_file):
                    try:
                        with open(skill_file, 'r', encoding='utf-8') as f:
                            content = f.read()
                            # Extract description from first lines
                            lines = content.split('\n')
                            for line in lines:
                                if line.strip() and not line.startswith('#'):
                                    description = line.strip()[:100]
                                    break
                                if line.startswith('# '):
                                    description = line[2:].strip()[:100]
                                    break
                    except:
                        pass
                
                # Determine category
                category = "通用"
                item_lower = item.lower()
                if 'python' in item_lower or 'django' in item_lower:
                    category = "Python"
                elif 'golang' in item_lower or 'go-' in item_lower:
                    category = "Go"
                elif 'frontend' in item_lower or 'react' in item_lower:
                    category = "前端"
                elif 'backend' in item_lower or 'api' in item_lower:
                    category = "后端"
                elif 'security' in item_lower:
                    category = "安全"
                elif 'testing' in item_lower or 'tdd' in item_lower:
                    category = "测试"
                elif 'docker' in item_lower or 'deployment' in item_lower:
                    category = "DevOps"
                elif 'swift' in item_lower or 'ios' in item_lower:
                    category = "iOS"
                elif 'java' in item_lower or 'spring' in item_lower:
                    category = "Java"
                elif 'rust' in item_lower:
                    category = "Rust"
                
                zh_name = SKILL_NAME_ZH.get(item, item.replace('-', ' ').title())
                skills.append({
                    'name': item,
                    'name_display': zh_name,
                    'description': description,
                    'category': category,
                    'path': skill_path
                })
    
    # Fallback if directory doesn't exist
    if not skills:
        skills = [
            {'name': 'tdd-workflow', 'description': '测试驱动开发工作流', 'category': '测试'},
            {'name': 'coding-standards', 'description': '基线编码规范', 'category': '通用'},
            {'name': 'security-review', 'description': '安全检查清单与模式', 'category': '安全'},
            {'name': 'frontend-patterns', 'description': 'React 与 Next.js 模式', 'category': '前端'},
            {'name': 'backend-patterns', 'description': 'API 与数据库模式', 'category': '后端'},
            {'name': 'api-design', 'description': 'REST API 设计模式', 'category': '后端'},
            {'name': 'docker-patterns', 'description': 'Docker 与容器模式', 'category': 'DevOps'},
            {'name': 'e2e-testing', 'description': 'Playwright E2E 测试模式', 'category': '测试'},
            {'name': 'verification-loop', 'description': '构建、测试、Lint 验证', 'category': '通用'},
            {'name': 'python-patterns', 'description': 'Python 惯用法与最佳实践', 'category': 'Python'},
            {'name': 'golang-patterns', 'description': 'Go 惯用法与最佳实践', 'category': 'Go'},
            {'name': 'django-patterns', 'description': 'Django 模式与最佳实践', 'category': 'Python'},
            {'name': 'springboot-patterns', 'description': 'Java Spring Boot 模式', 'category': 'Java'},
            {'name': 'laravel-patterns', 'description': 'Laravel 架构模式', 'category': 'PHP'},
        ]
    
    return skills

def load_commands(project_path: str) -> List[Dict]:
    """Load commands from commands directory"""
    commands_dir = os.path.join(project_path, "commands")
    commands = []
    
    if os.path.exists(commands_dir):
        for item in os.listdir(commands_dir):
            if item.endswith('.md'):
                cmd_name = item[:-3]
                description = ""
                
                try:
                    with open(os.path.join(commands_dir, item), 'r', encoding='utf-8') as f:
                        content = f.read()
                        lines = content.split('\n')
                        for line in lines:
                            if line.startswith('# '):
                                description = line[2:].strip()
                                break
                except:
                    pass
                
                commands.append({
                    'name': cmd_name,
                    'description': description or cmd_name.replace('-', ' ').title()
                })
    
    # Fallback commands
    if not commands:
        commands = [
            {'name': 'plan', 'description': '创建实现计划'},
            {'name': 'tdd', 'description': '测试驱动开发工作流'},
            {'name': 'code-review', 'description': '审查代码质量与安全'},
            {'name': 'build-fix', 'description': '修复构建与 TypeScript 错误'},
            {'name': 'e2e', 'description': '生成并运行 E2E 测试'},
            {'name': 'refactor-clean', 'description': '移除死代码'},
            {'name': 'verify', 'description': '运行验证循环'},
            {'name': 'eval', 'description': '按标准运行评估'},
            {'name': 'security', 'description': '运行全面安全审查'},
            {'name': 'test-coverage', 'description': '分析测试覆盖率'},
            {'name': 'update-docs', 'description': '更新文档'},
            {'name': 'setup-pm', 'description': '配置包管理器'},
            {'name': 'go-review', 'description': 'Go 代码审查'},
            {'name': 'go-test', 'description': 'Go TDD 工作流'},
            {'name': 'python-review', 'description': 'Python 代码审查'},
        ]
    
    return commands

RULE_NAME_ZH = {
    "coding-style": "编码风格",
    "git-workflow": "Git 工作流",
    "testing": "测试",
    "performance": "性能",
    "patterns": "通用模式",
    "security": "安全",
    "agents": "Agent 编排",
    "code-review": "代码审查",
    "development-workflow": "开发工作流",
    "hooks": "Hooks 系统",
    "everything-claude-code-guardrails": "ECC 护栏",
    "node": "Node.js",
    "typescript": "TypeScript",
    "python": "Python",
    "golang": "Go",
    "swift": "Swift",
    "php": "PHP",
    "java": "Java",
    "rust": "Rust",
    "kotlin": "Kotlin",
    "cpp": "C++",
    "csharp": "C#",
    "dart": "Dart/Flutter",
    "angular": "Angular",
    "arkts": "ArkTS",
    "react": "React",
}

RULE_LANGUAGE_ZH = {
    "common": "通用",
    "angular": "Angular",
    "arkts": "ArkTS",
    "cpp": "C++",
    "csharp": "C#",
    "dart": "Dart/Flutter",
    "golang": "Go",
    "java": "Java",
    "kotlin": "Kotlin",
    "php": "PHP",
    "python": "Python",
    "rust": "Rust",
    "swift": "Swift",
}

def load_rules(project_path: str) -> List[Dict]:
    """Load rules from rules directory"""
    rules_dir = os.path.join(project_path, "rules")
    rules = []

    if os.path.exists(rules_dir):
        for item in os.listdir(rules_dir):
            item_path = os.path.join(rules_dir, item)
            if os.path.isdir(item_path):
                lang_display = RULE_LANGUAGE_ZH.get(item.lower(), item.title())
                for file in os.listdir(item_path):
                    if file.endswith('.md'):
                        rule_name = file[:-3]
                        zh_name = RULE_NAME_ZH.get(rule_name, rule_name.replace('-', ' ').title())
                        # Try to load description from file
                        desc = ""
                        try:
                            with open(os.path.join(item_path, file), 'r', encoding='utf-8') as f:
                                for line in f:
                                    stripped = line.strip()
                                    if stripped.startswith('# ') and not stripped.startswith('## '):
                                        desc = stripped[2:].strip()
                                        break
                        except:
                            pass
                        rules.append({
                            'name': rule_name,
                            'name_display': zh_name,
                            'language': lang_display,
                            'description': desc,
                            'path': os.path.join(item_path, file)
                        })

    # Fallback rules
    if not rules:
        rules = [
            {'name': 'coding-style', 'name_display': '编码风格', 'language': '通用', 'description': '', 'path': ''},
            {'name': 'git-workflow', 'name_display': 'Git 工作流', 'language': '通用', 'description': '', 'path': ''},
            {'name': 'testing', 'name_display': '测试', 'language': '通用', 'description': '', 'path': ''},
            {'name': 'performance', 'name_display': '性能', 'language': '通用', 'description': '', 'path': ''},
            {'name': 'patterns', 'name_display': '通用模式', 'language': '通用', 'description': '', 'path': ''},
            {'name': 'security', 'name_display': '安全', 'language': '通用', 'description': '', 'path': ''},
            {'name': 'typescript', 'name_display': 'TypeScript', 'language': 'TypeScript', 'description': '', 'path': ''},
            {'name': 'python', 'name_display': 'Python', 'language': 'Python', 'description': '', 'path': ''},
            {'name': 'golang', 'name_display': 'Go', 'language': 'Go', 'description': '', 'path': ''},
            {'name': 'swift', 'name_display': 'Swift', 'language': 'Swift', 'description': '', 'path': ''},
            {'name': 'php', 'name_display': 'PHP', 'language': 'PHP', 'description': '', 'path': ''},
        ]
    
    return rules

# ============================================================================
# MAIN APPLICATION
# ============================================================================

class ECCDashboard(tk.Tk):
    """Main ECC Dashboard Application"""
    
    def __init__(self):
        super().__init__()
        
        self.project_path = get_project_path()
        self.title("ECC 控制台 - Everything Claude Code")
        
        maximize_window(self)
        
        try:
            self.icon_image = tk.PhotoImage(file='assets/images/ecc-logo.png')
            self.iconphoto(True, self.icon_image)
        except:
            pass
        
        self.minsize(800, 600)
        
        # Load data
        self.agents = load_agents(self.project_path)
        self.skills = load_skills(self.project_path)
        self.commands = load_commands(self.project_path)
        self.rules = load_rules(self.project_path)
        
        # Settings
        self.settings = {
            'project_path': self.project_path,
            'theme': 'light'
        }
        
        # Setup UI
        self.setup_styles()
        self.create_widgets()
        
        # Center window
        self.center_window()
    
    def setup_styles(self):
        """Setup ttk styles for modern look"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure tab style
        style.configure('TNotebook', background='#f0f0f0')
        style.configure('TNotebook.Tab', padding=[10, 5], font=('Arial', 10))
        style.map('TNotebook.Tab', background=[('selected', '#ffffff')])
        
        # Configure Treeview
        style.configure('Treeview', font=('Arial', 10), rowheight=25)
        style.configure('Treeview.Heading', font=('Arial', 10, 'bold'))
        
        # Configure buttons
        style.configure('TButton', font=('Arial', 10), padding=5)
    
    def center_window(self):
        """Center the window on screen"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_widgets(self):
        """Create all UI widgets"""
        # Main container
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Header
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        try:
            self.logo_image = tk.PhotoImage(file='assets/images/ecc-logo.png')
            self.logo_image = self.logo_image.subsample(2, 2)
            ttk.Label(header_frame, image=self.logo_image).pack(side=tk.LEFT, padx=(0, 10))
        except:
            pass
        
        self.title_label = ttk.Label(header_frame, text="ECC 控制台", font=('Open Sans', 18, 'bold'))
        self.title_label.pack(side=tk.LEFT)
        self.version_label = ttk.Label(header_frame, text="v1.10.0", font=('Open Sans', 10), foreground='gray')
        self.version_label.pack(side=tk.LEFT, padx=(10, 0))
        
        # Notebook (tabs)
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Create tabs
        self.create_agents_tab()
        self.create_skills_tab()
        self.create_commands_tab()
        self.create_rules_tab()
        self.create_settings_tab()
        
        # Status bar
        status_frame = ttk.Frame(main_frame)
        status_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.status_label = ttk.Label(status_frame,
                                       text=f"就绪 | 智能体: {len(self.agents)} | 技能: {len(self.skills)} | 命令: {len(self.commands)}",
                                       font=('Arial', 9), foreground='gray')
        self.status_label.pack(side=tk.LEFT)
    
    # =========================================================================
    # AGENTS TAB
    # =========================================================================
    
    def create_agents_tab(self):
        """Create Agents tab"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text=f"智能体 ({len(self.agents)})")
        
        # Search bar
        search_frame = ttk.Frame(frame)
        search_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(search_frame, text="搜索:").pack(side=tk.LEFT)
        self.agent_search = ttk.Entry(search_frame, width=30)
        self.agent_search.pack(side=tk.LEFT, padx=5)
        self.agent_search.bind('<KeyRelease>', self.filter_agents)

        ttk.Label(search_frame, text="数量:").pack(side=tk.LEFT, padx=(20, 0))
        self.agent_count_label = ttk.Label(search_frame, text=str(len(self.agents)))
        self.agent_count_label.pack(side=tk.LEFT)
        
        # Split pane: list + details
        paned = ttk.PanedWindow(frame, orient=tk.HORIZONTAL)
        paned.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        # Agent list
        list_frame = ttk.Frame(paned)
        paned.add(list_frame, weight=2)
        
        columns = ('name', 'purpose')
        self.agent_tree = ttk.Treeview(list_frame, columns=columns, show='tree headings')
        self.agent_tree.heading('#0', text='#')
        self.agent_tree.heading('name', text='智能体名称')
        self.agent_tree.heading('purpose', text='用途')
        self.agent_tree.column('#0', width=40)
        self.agent_tree.column('name', width=180)
        self.agent_tree.column('purpose', width=250)
        
        self.agent_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.agent_tree.yview)
        self.agent_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Details panel
        details_frame = ttk.Frame(paned)
        paned.add(details_frame, weight=1)
        
        ttk.Label(details_frame, text="详情", font=('Arial', 11, 'bold')).pack(anchor=tk.W, pady=5)
        
        self.agent_details = scrolledtext.ScrolledText(details_frame, wrap=tk.WORD, height=15)
        self.agent_details.pack(fill=tk.BOTH, expand=True)
        
        # Bind selection
        self.agent_tree.bind('<<TreeviewSelect>>', self.on_agent_select)
        
        # Populate list
        self.populate_agents(self.agents)
    
    def populate_agents(self, agents: List[Dict]):
        """Populate agents list"""
        for item in self.agent_tree.get_children():
            self.agent_tree.delete(item)
        
        for i, agent in enumerate(agents, 1):
            display_name = agent.get('name_display', agent['name'])
            self.agent_tree.insert('', tk.END, text=str(i), values=(display_name, agent['purpose']))
    
    def filter_agents(self, event=None):
        """Filter agents based on search"""
        query = self.agent_search.get().lower()
        
        if not query:
            filtered = self.agents
        else:
            filtered = [a for a in self.agents
                       if query in a['name'].lower() or query in a['purpose'].lower()
                       or query in a.get('name_display', '').lower()]
        
        self.populate_agents(filtered)
        self.agent_count_label.config(text=str(len(filtered)))
    
    def on_agent_select(self, event):
        """Handle agent selection"""
        selection = self.agent_tree.selection()
        if not selection:
            return
        
        item = self.agent_tree.item(selection[0])
        agent_name = item['values'][0]
        
        agent = next((a for a in self.agents if a['name'] == agent_name or a.get('name_display') == agent_name), None)
        if agent:
            display_name = agent.get('name_display', agent['name'])
            details = f"""智能体: {display_name} ({agent['name']})

用途: {agent['purpose']}

使用场景: {agent['when_to_use']}

---
在 Claude Code 中使用:
使用 /{agent['name']} 命令或通过智能体委派调用。"""
            self.agent_details.delete('1.0', tk.END)
            self.agent_details.insert('1.0', details)
    
    # =========================================================================
    # SKILLS TAB
    # =========================================================================
    
    def create_skills_tab(self):
        """Create Skills tab"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text=f"技能 ({len(self.skills)})")
        
        # Search and filter
        filter_frame = ttk.Frame(frame)
        filter_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(filter_frame, text="搜索:").pack(side=tk.LEFT)
        self.skill_search = ttk.Entry(filter_frame, width=25)
        self.skill_search.pack(side=tk.LEFT, padx=5)
        self.skill_search.bind('<KeyRelease>', self.filter_skills)

        ttk.Label(filter_frame, text="分类:").pack(side=tk.LEFT, padx=(20, 0))
        self.skill_category = ttk.Combobox(filter_frame, values=['全部'] + self.get_categories(), width=15)
        self.skill_category.set('全部')
        self.skill_category.pack(side=tk.LEFT, padx=5)
        self.skill_category.bind('<<ComboboxSelected>>', self.filter_skills)

        ttk.Label(filter_frame, text="数量:").pack(side=tk.LEFT, padx=(20, 0))
        self.skill_count_label = ttk.Label(filter_frame, text=str(len(self.skills)))
        self.skill_count_label.pack(side=tk.LEFT)
        
        # Split pane
        paned = ttk.PanedWindow(frame, orient=tk.HORIZONTAL)
        paned.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        # Skill list
        list_frame = ttk.Frame(paned)
        paned.add(list_frame, weight=1)
        
        columns = ('name', 'category', 'description')
        self.skill_tree = ttk.Treeview(list_frame, columns=columns, show='tree headings')
        self.skill_tree.heading('#0', text='#')
        self.skill_tree.heading('name', text='技能名称')
        self.skill_tree.heading('category', text='分类')
        self.skill_tree.heading('description', text='描述')
        
        self.skill_tree.column('#0', width=40)
        self.skill_tree.column('name', width=180)
        self.skill_tree.column('category', width=100)
        self.skill_tree.column('description', width=300)
        
        self.skill_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.skill_tree.yview)
        self.skill_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Details
        details_frame = ttk.Frame(paned)
        paned.add(details_frame, weight=1)
        
        ttk.Label(details_frame, text="描述", font=('Arial', 11, 'bold')).pack(anchor=tk.W, pady=5)
        
        self.skill_details = scrolledtext.ScrolledText(details_frame, wrap=tk.WORD, height=15)
        self.skill_details.pack(fill=tk.BOTH, expand=True)
        
        self.skill_tree.bind('<<TreeviewSelect>>', self.on_skill_select)
        
        self.populate_skills(self.skills)
    
    def get_categories(self) -> List[str]:
        """Get unique categories from skills"""
        categories = set(s['category'] for s in self.skills)
        return sorted(categories)
    
    def populate_skills(self, skills: List[Dict]):
        """Populate skills list"""
        for item in self.skill_tree.get_children():
            self.skill_tree.delete(item)
        
        for i, skill in enumerate(skills, 1):
            display_name = skill.get('name_display', skill['name'])
            self.skill_tree.insert('', tk.END, text=str(i),
                                  values=(display_name, skill['category'], skill['description']))
    
    def filter_skills(self, event=None):
        """Filter skills based on search and category"""
        search = self.skill_search.get().lower()
        category = self.skill_category.get()
        
        filtered = self.skills
        
        if category != '全部':
            filtered = [s for s in filtered if s['category'] == category]
        
        if search:
            filtered = [s for s in filtered
                       if search in s['name'].lower() or search in s['description'].lower()
                       or search in s.get('name_display', '').lower()]
        
        self.populate_skills(filtered)
        self.skill_count_label.config(text=str(len(filtered)))
    
    def on_skill_select(self, event):
        """Handle skill selection"""
        selection = self.skill_tree.selection()
        if not selection:
            return
        
        item = self.skill_tree.item(selection[0])
        skill_name = item['values'][0]
        
        skill = next((s for s in self.skills if s['name'] == skill_name or s.get('name_display') == skill_name), None)
        if skill:
            display_name = skill.get('name_display', skill['name'])
            details = f"""技能: {display_name} ({skill['name']})

分类: {skill['category']}

描述: {skill['description']}

路径: {skill['path']}

---
用法: 处理相关技术时自动激活此技能。"""
            self.skill_details.delete('1.0', tk.END)
            self.skill_details.insert('1.0', details)
    
    # =========================================================================
    # COMMANDS TAB
    # =========================================================================
    
    def create_commands_tab(self):
        """Create Commands tab"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text=f"命令 ({len(self.commands)})")
        
        # Info
        info_frame = ttk.Frame(frame)
        info_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(info_frame, text="Claude Code 斜杠命令:",
                  font=('Arial', 10, 'bold')).pack(anchor=tk.W)
        ttk.Label(info_frame, text="在 Claude Code 中输入 /命令名称 来使用这些命令",
                  foreground='gray').pack(anchor=tk.W)
        
        # Commands list
        list_frame = ttk.Frame(frame)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        columns = ('name', 'description')
        self.command_tree = ttk.Treeview(list_frame, columns=columns, show='tree headings')
        self.command_tree.heading('#0', text='#')
        self.command_tree.heading('name', text='命令')
        self.command_tree.heading('description', text='描述')
        
        self.command_tree.column('#0', width=40)
        self.command_tree.column('name', width=150)
        self.command_tree.column('description', width=400)
        
        self.command_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.command_tree.yview)
        self.command_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Populate
        for i, cmd in enumerate(self.commands, 1):
            self.command_tree.insert('', tk.END, text=str(i), 
                                   values=('/' + cmd['name'], cmd['description']))
    
    # =========================================================================
    # RULES TAB
    # =========================================================================
    
    def create_rules_tab(self):
        """Create Rules tab"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text=f"规则 ({len(self.rules)})")
        
        # Info
        info_frame = ttk.Frame(frame)
        info_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(info_frame, text="按语言分类的编码规则:",
                  font=('Arial', 10, 'bold')).pack(anchor=tk.W)
        ttk.Label(info_frame, text="这些规则会自动应用于 Claude Code",
                  foreground='gray').pack(anchor=tk.W)
        
        # Filter
        filter_frame = ttk.Frame(frame)
        filter_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(filter_frame, text="语言:").pack(side=tk.LEFT)
        self.rules_language = ttk.Combobox(filter_frame,
                                           values=['全部'] + self.get_rule_languages(),
                                           width=15)
        self.rules_language.set('全部')
        self.rules_language.pack(side=tk.LEFT, padx=5)
        self.rules_language.bind('<<ComboboxSelected>>', self.filter_rules)
        
        # Rules list
        list_frame = ttk.Frame(frame)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        columns = ('name', 'language', 'description')
        self.rules_tree = ttk.Treeview(list_frame, columns=columns, show='tree headings')
        self.rules_tree.heading('#0', text='#')
        self.rules_tree.heading('name', text='规则名称')
        self.rules_tree.heading('language', text='语言')
        self.rules_tree.heading('description', text='描述')

        self.rules_tree.column('#0', width=40)
        self.rules_tree.column('name', width=150)
        self.rules_tree.column('language', width=80)
        self.rules_tree.column('description', width=300)
        
        self.rules_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.rules_tree.yview)
        self.rules_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.populate_rules(self.rules)
    
    def get_rule_languages(self) -> List[str]:
        """Get unique languages from rules"""
        languages = set(r['language'] for r in self.rules)
        return sorted(languages)
    
    def populate_rules(self, rules: List[Dict]):
        """Populate rules list"""
        for item in self.rules_tree.get_children():
            self.rules_tree.delete(item)
        
        for i, rule in enumerate(rules, 1):
            display_name = rule.get('name_display', rule['name'])
            self.rules_tree.insert('', tk.END, text=str(i),
                                  values=(display_name, rule['language'], rule.get('description', '')))
    
    def filter_rules(self, event=None):
        """Filter rules by language"""
        language = self.rules_language.get()
        
        if language == '全部':
            filtered = self.rules
        else:
            filtered = [r for r in self.rules if r['language'] == language]
        
        self.populate_rules(filtered)
    
    # =========================================================================
    # SETTINGS TAB
    # =========================================================================
    
    def create_settings_tab(self):
        """Create Settings tab"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="设置")
        
        # Project path
        path_frame = ttk.LabelFrame(frame, text="项目路径", padding=10)
        path_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.path_entry = ttk.Entry(path_frame, width=60)
        self.path_entry.insert(0, self.project_path)
        self.path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        ttk.Button(path_frame, text="浏览...", command=self.browse_path).pack(side=tk.LEFT, padx=5)
        
        # Theme
        theme_frame = ttk.LabelFrame(frame, text="外观", padding=10)
        theme_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(theme_frame, text="主题:").pack(anchor=tk.W)
        self.theme_var = tk.StringVar(value='light')
        light_rb = ttk.Radiobutton(theme_frame, text="浅色", variable=self.theme_var,
                       value='light', command=self.apply_theme)
        light_rb.pack(anchor=tk.W)
        dark_rb = ttk.Radiobutton(theme_frame, text="深色", variable=self.theme_var,
                       value='dark', command=self.apply_theme)
        dark_rb.pack(anchor=tk.W)
        
        font_frame = ttk.LabelFrame(frame, text="字体", padding=10)
        font_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(font_frame, text="字体族:").pack(anchor=tk.W)
        self.font_var = tk.StringVar(value='Open Sans')
        
        fonts = ['Open Sans', 'Arial', 'Helvetica', 'Times New Roman', 'Courier New', 'Verdana', 'Georgia', 'Tahoma', 'Trebuchet MS']
        self.font_combo = ttk.Combobox(font_frame, textvariable=self.font_var, values=fonts, state='readonly')
        self.font_combo.pack(anchor=tk.W, fill=tk.X, pady=(5, 0))
        self.font_combo.bind('<<ComboboxSelected>>', lambda e: self.apply_theme())
        
        ttk.Label(font_frame, text="字号:").pack(anchor=tk.W, pady=(10, 0))
        self.size_var = tk.StringVar(value='10')
        sizes = ['8', '9', '10', '11', '12', '14', '16', '18', '20']
        self.size_combo = ttk.Combobox(font_frame, textvariable=self.size_var, values=sizes, state='readonly', width=10)
        self.size_combo.pack(anchor=tk.W, pady=(5, 0))
        self.size_combo.bind('<<ComboboxSelected>>', lambda e: self.apply_theme())
        
        # Quick Actions
        actions_frame = ttk.LabelFrame(frame, text="快捷操作", padding=10)
        actions_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        ttk.Button(actions_frame, text="在终端中打开项目",
                  command=self.open_terminal).pack(fill=tk.X, pady=2)
        ttk.Button(actions_frame, text="打开 README",
                  command=self.open_readme).pack(fill=tk.X, pady=2)
        ttk.Button(actions_frame, text="打开 AGENTS.md",
                  command=self.open_agents).pack(fill=tk.X, pady=2)
        ttk.Button(actions_frame, text="刷新数据",
                  command=self.refresh_data).pack(fill=tk.X, pady=2)
        
        # About
        about_frame = ttk.LabelFrame(frame, text="关于", padding=10)
        about_frame.pack(fill=tk.X, padx=10, pady=10)
        
        about_text = """ECC 控制台 v1.0.0
Everything Claude Code GUI

一个跨平台桌面应用，用于
管理和浏览 ECC 组件。

版本: 1.10.0
项目: github.com/affaan-m/everything-claude-code"""
        
        ttk.Label(about_frame, text=about_text, justify=tk.LEFT).pack(anchor=tk.W)
    
    def browse_path(self):
        """Browse for project path"""
        from tkinter import filedialog
        path = filedialog.askdirectory(initialdir=self.project_path)
        if path:
            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(0, path)
    
    def open_terminal(self):
        """Open terminal at project path"""
        path = os.path.realpath(self.path_entry.get())
        try:
            launch_terminal(path)
        except Exception as exc:
            messagebox.showerror("错误", f"无法打开终端: {exc}")

    def _open_project_doc(self, filename: str) -> None:
        """Open a project document safely, constrained to the project directory."""
        base = os.path.realpath(self.path_entry.get())
        target = os.path.realpath(os.path.join(base, filename))
        if os.path.commonpath([base, target]) != base:
            messagebox.showerror("错误", "拒绝访问: 路径超出项目目录")
            return
        if os.path.exists(target):
            webbrowser.open(Path(target).as_uri())
        else:
            messagebox.showerror("错误", f"未找到 {filename}")

    def open_readme(self):
        """Open README in default browser/reader"""
        self._open_project_doc('README.md')
    
    def open_agents(self):
        """Open AGENTS.md"""
        self._open_project_doc('AGENTS.md')
    
    def refresh_data(self):
        """Refresh all data"""
        self.project_path = self.path_entry.get()
        self.agents = load_agents(self.project_path)
        self.skills = load_skills(self.project_path)
        self.commands = load_commands(self.project_path)
        self.rules = load_rules(self.project_path)
        
        # Update tabs
        self.notebook.tab(0, text=f"智能体 ({len(self.agents)})")
        self.notebook.tab(1, text=f"技能 ({len(self.skills)})")
        self.notebook.tab(2, text=f"命令 ({len(self.commands)})")
        self.notebook.tab(3, text=f"规则 ({len(self.rules)})")
        
        # Repopulate
        self.populate_agents(self.agents)
        self.populate_skills(self.skills)
        
        # Update status
        self.status_label.config(
            text=f"就绪 | 智能体: {len(self.agents)} | 技能: {len(self.skills)} | 命令: {len(self.commands)}"
        )
        
        messagebox.showinfo("成功", "数据刷新成功！")

    def apply_theme(self):
        theme = self.theme_var.get()
        font_family = self.font_var.get()
        font_size = int(self.size_var.get())
        font_tuple = (font_family, font_size)
        
        if theme == 'dark':
            bg_color = '#2b2b2b'
            fg_color = '#ffffff'
            entry_bg = '#3c3c3c'
            frame_bg = '#2b2b2b'
            select_bg = '#0f5a9e'
        else:
            bg_color = '#f0f0f0'
            fg_color = '#000000'
            entry_bg = '#ffffff'
            frame_bg = '#f0f0f0'
            select_bg = '#e0e0e0'
        
        self.configure(background=bg_color)
        
        style = ttk.Style()
        style.configure('.', background=bg_color, foreground=fg_color, font=font_tuple)
        style.configure('TFrame', background=bg_color, font=font_tuple)
        style.configure('TLabel', background=bg_color, foreground=fg_color, font=font_tuple)
        style.configure('TNotebook', background=bg_color, font=font_tuple)
        style.configure('TNotebook.Tab', background=frame_bg, foreground=fg_color, font=font_tuple)
        style.map('TNotebook.Tab', background=[('selected', select_bg)])
        style.configure('Treeview', background=entry_bg, foreground=fg_color, fieldbackground=entry_bg, font=font_tuple)
        style.configure('Treeview.Heading', background=frame_bg, foreground=fg_color, font=font_tuple)
        style.configure('TEntry', fieldbackground=entry_bg, foreground=fg_color, font=font_tuple)
        style.configure('TButton', background=frame_bg, foreground=fg_color, font=font_tuple)
        
        self.title_label.configure(font=(font_family, 18, 'bold'))
        self.version_label.configure(font=(font_family, 10))
        
        def update_widget_colors(widget):
            try:
                widget.configure(background=bg_color)
            except:
                pass
            for child in widget.winfo_children():
                try:
                    child.configure(background=bg_color)
                except:
                    pass
                try:
                    update_widget_colors(child)
                except:
                    pass
        
        try:
            update_widget_colors(self)
        except:
            pass
        
        self.update()


# ============================================================================
# MAIN
# ============================================================================

def main():
    """Main entry point"""
    app = ECCDashboard()
    app.mainloop()


if __name__ == "__main__":
    main()
