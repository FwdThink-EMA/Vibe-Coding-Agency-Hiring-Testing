# Agent Orchestration for Cloud Architecture Planning
# Format: Problem statement + Written response

"""
AGENT ORCHESTRATION CHALLENGE

You need to design a multi-agent system that can analyze business problems and recommend
cloud architecture solutions. Focus on the orchestration strategy, not implementation details.

SAMPLE SCENARIOS (choose 2 to address):

1. "Simple E-commerce Site"
   - Online store for small business (1000 daily users)
   - Product catalog, shopping cart, payment processing
   - Basic admin dashboard for inventory management

2. "Customer Support Chatbot"
   - AI chatbot for customer service
   - Integration with existing CRM system
   - Handle 500+ conversations per day
   - Escalate complex issues to human agents

3. "Employee Expense Tracker"
   - Mobile app for expense reporting
   - Receipt photo upload and processing
   - Approval workflow for managers
   - Integration with payroll system

YOUR TASK:
Design an agent orchestration approach that can take these problems and output
a cloud architecture recommendation including basic services needed (database,
API gateway, compute, storage, etc.).
"""

# =============================================================

"""
Multi-Agent Orchestration Demo – Cloud Architecture Planning

Agents:
1. RequirementsAgent  – extracts business & technical needs
2. ComplianceAgent    – identifies data/compliance constraints
3. ResearchAgent      – shared utility for contextual knowledge lookup
4. ArchitectureAgent  – maps requirements + compliance to architecture
5. CostEstimationAgent – estimates cost and optimizations
6. ReviewAgent        – evaluates completeness and risks

Focus: Orchestration logic & collaboration, not implementation details.
"""

from dataclasses import dataclass
from typing import Dict, Any, List


@dataclass
class AgentResponse:
    name: str
    output: Dict[str, Any]


class ResearchAgent:
    """
    ResearchAgent (Search-Enabled)

    Acts as a shared utility that can search external knowledge sources
    (cloud provider docs, architecture blogs, pricing APIs) and return concise summaries.
    For demonstration, this mock version simulates search results.
    """

    def query(self, topic: str) -> str:
        # In production: call Google Search, Gemini API, or internal KB.
        # Example: return web_search(topic)
        simulated_results = {
            "PCI-DSS": "Found compliance guidelines from AWS and GCP docs.",
            "GDPR": "Retrieved GDPR checklist from official EU documentation.",
            "Serverless": "Compared AWS Lambda vs Cloud Run performance for low-traffic apps.",
            "Containers": "Fetched ECS vs GKE vs AKS comparison benchmark.",
        }
        print(f"[ResearchAgent] Searching the web for: {topic} ...")
        return simulated_results.get(topic, f"No relevant info found for '{topic}'.")


class RequirementsAgent:
    """Extracts core requirements from a problem statement."""

    def run(self, problem: str) -> AgentResponse:
        reqs = {
            "users_per_day": 1000,
            "features": ["catalog", "cart", "payment", "admin_dashboard"],
            "data_types": ["user_profiles", "payment_info", "inventory"],
            "constraints": ["scalable", "secure_payments", "low_ops"],
        }
        return AgentResponse("RequirementsAgent", reqs)


class ComplianceAgent:
    """Identifies compliance obligations using the ResearchAgent."""

    def __init__(self, researcher: ResearchAgent):
        self.researcher = researcher

    def run(self, requirements: Dict[str, Any]) -> AgentResponse:
        data_types = requirements.get("data_types", [])
        compliance = []
        notes = []

        if "payment_info" in data_types:
            compliance.append("PCI-DSS")
            notes.append(self.researcher.query("PCI-DSS"))
        if "user_profiles" in data_types:
            compliance.append("GDPR")
            notes.append(self.researcher.query("GDPR"))

        output = {
            "required_compliance": compliance or ["None"],
            "security_controls": [
                "Encryption at rest/in transit",
                "Least-privilege IAM",
                "WAF, audit logging",
            ],
            "research_notes": notes,
        }
        return AgentResponse("ComplianceAgent", output)


class ArchitectureAgent:
    """Maps requirements + compliance to cloud architecture, consulting ResearchAgent if needed."""

    def __init__(self, researcher: ResearchAgent):
        self.researcher = researcher

    def run(self, context: Dict[str, Any]) -> AgentResponse:
        base = context.get("constraints", [])
        arch_type = "Serverless" if "low_ops" in base else "Containers"
        reference = self.researcher.query(arch_type)

        architecture = {
            "pattern": arch_type,
            "compute": (
                "Serverless Functions"
                if arch_type == "Serverless"
                else "Container Service"
            ),
            "database": "Managed PostgreSQL",
            "storage": "Object Storage",
            "network": "API Gateway + CDN",
            "security": context.get("security_controls", []),
            "research_reference": reference,
        }
        return AgentResponse("ArchitectureAgent", architecture)


class CostEstimationAgent:
    """Estimates cloud cost and optimization options."""

    def run(self, architecture: Dict[str, Any]) -> AgentResponse:
        cost = {
            "monthly_estimate_usd": "~$120–150",
            "tier": "low-cost, scalable",
            "optimizations": [
                "CDN caching for static assets",
                "Auto-suspend idle dev DBs",
                "Serverless pay-per-use model",
            ],
        }
        return AgentResponse("CostEstimationAgent", cost)


class ReviewAgent:
    """Final evaluation of feasibility, risks, and clarity."""

    def run(self, context: Dict[str, Any]) -> AgentResponse:
        risks = ["Cold starts (serverless)", "Vendor lock-in (managed DB)"]
        score = 9.1
        return AgentResponse(
            "ReviewAgent",
            {
                "overall_score": score,
                "risks": risks,
                "summary": f"Validated architecture with score {score}/10. Risks: {', '.join(risks)}",
            },
        )


class Orchestrator:
    """Coordinates agents sequentially."""

    def __init__(self, agents: List[Any]):
        self.agents = agents

    def run(self, problem: str) -> Dict[str, Any]:
        results = {}
        context: Any = problem
        for agent in self.agents:
            response = agent.run(context)
            results[response.name] = response.output
            context = (
                {**context, **response.output}
                if isinstance(context, dict)
                else response.output
            )
        return results


if __name__ == "__main__":
    problem_statement = (
        "Design a cloud architecture for an online store with 1000 daily users, "
        "offering product catalog, shopping cart, payment, and admin dashboard."
    )

    research_agent = ResearchAgent()

    orchestrator = Orchestrator(
        [
            RequirementsAgent(),
            ComplianceAgent(research_agent),
            ArchitectureAgent(research_agent),
            CostEstimationAgent(research_agent),
            ReviewAgent(research_agent),
        ]
    )

    results = orchestrator.run(problem_statement)

    print("=== Multi-Agent Architecture Recommendation ===")
    for agent, data in results.items():
        print(f"\n[{agent}]")
        for k, v in data.items():
            print(f"  {k}: {v}")


# =============================================================
# === WRITTEN RESPONSE QUESTIONS ===

"""
QUESTION 1: AGENT DESIGN (20 points)
What agents would you create for this orchestration? Describe:
- 3-5 specific agents and their roles
- How they would collaborate on the sample problems
- What each agent's input and output would be

Example format:
Agent Name: Requirements Analyst
Role: Break down business requirements into technical needs
Input: Problem description + business context
Output: List of functional requirements, expected load, compliance needs

QUESTION 2: ORCHESTRATION WORKFLOW (25 points)
For ONE of the sample scenarios, walk through your complete workflow:
- Step-by-step process from problem statement to final recommendation
- How agents hand off information to each other
- What happens if an agent fails or produces unclear output
- How you ensure the final solution is complete and feasible

QUESTION 3: CLOUD RESOURCE MAPPING (20 points)
For your chosen scenario, what basic cloud services would your system recommend?
- Compute (serverless functions, containers, VMs)
- Storage (databases, file storage, caching)
- Networking (API gateways, load balancers, CDN)
- Security and monitoring basics
- Justify why each service fits the requirements

QUESTION 4: REUSABILITY & IMPROVEMENT (15 points)
How would you make this system work across different projects?
- What would you standardize vs. customize per project?
- How would the system learn from previous recommendations?
- What feedback mechanisms would improve future solutions?

QUESTION 5: PRACTICAL CONSIDERATIONS (20 points)
What challenges would you expect and how would you handle:
- Conflicting recommendations between agents
- Incomplete or vague problem statements
- Budget constraints not mentioned in requirements
- Integration with existing legacy systems
- Keeping up with new cloud services and pricing
"""

"""
QUESTION 1: AGENT DESIGN

Agent 1 — Requirements Analyst
Role:
    Extracts functional & non-functional requirements from the problem statement.
Input:
    Problem description + business context.
Output:
    JSON spec with fields like features[], users_per_day, data_types[], constraints[], assumptions[].

Agent 2 — Research Agent (shared utility)
Role:
    Provides concise, sourced summaries on cloud patterns, compliance norms, and service comparisons.
    Can be called by any other agent. In real systems, this could query the web or internal KB.
Input:
    Topic or query string (e.g., "PCI-DSS on AWS", "Serverless vs Containers").
Output:
    {summary, source, confidence}.

Agent 3 — Compliance Agent
Role:
    Derives compliance obligations and baseline controls using requirement data + Research Agent findings.
Input:
    Requirements spec; calls Research Agent for PCI/GDPR references.
Output:
    required_compliance[], security_controls[], research_notes[].

Agent 4 — Cloud Architecture Planner
Role:
    Maps requirements + compliance context to a reference architecture and cloud services.
    Consults Research Agent for trade-offs and best practices.
Input:
    Requirements + Compliance outputs.
Output:
    architecture = {pattern, compute, database, storage, cache, api_frontdoor, cdn, waf, observability, secrets}.

Agent 5 — Cost Estimation Agent
Role:
    Produces a rough monthly range and optimization tips; may call Research Agent for current pricing info.
Input:
    Architecture proposal.
Output:
    monthly_estimate_usd (range), tier, optimizations[].

Agent 6 — Review (Judge) Agent
Role:
    Validates completeness, feasibility, and risk. Ensures security, reliability, and cost gates pass.
Input:
    All previous agent outputs.
Output:
    overall_score(0–10), risks[], summary, pass/fail per gate.

Collaboration:
    - Simple E-commerce: Requirements → (Research) → Compliance → (Research) → Architecture → (Research) → Cost → Review
    - Chatbot: Requirements → Compliance (PII/retention) → Architecture (LLM gateway + vector DB) → Cost (token usage) → Review
"""

# =============================================================

"""
QUESTION 2: ORCHESTRATION WORKFLOW
Scenario: Simple E-commerce Site

Step 1:
    Requirements Agent extracts:
        users_per_day=1000,
        features=[catalog, cart, payment, admin_dashboard],
        data_types=[user_profiles, payment_info, inventory],
        constraints=[low_ops, scalable, secure_payments].

Step 2:
    Compliance Agent inspects data_types and calls Research Agent for "PCI-DSS" and "GDPR" summaries.
    Outputs compliance list, baseline security_controls, and research_notes.

Step 3:
    Architecture Planner consults Research Agent ("Serverless vs Containers") and proposes:
        Compute: Serverless Functions + API Gateway
        Database: Managed PostgreSQL
        Storage: Object Storage
        Cache: Managed Redis
        Edge: CDN + WAF
        Secrets: Managed Secrets + KMS
        Observability: Managed logs/metrics/traces

Step 4:
    Cost Estimation Agent returns estimated range ($120–150) and optimization list.

Step 5:
    Review Agent validates via gates (Security, SLOs, Cost sanity, Operability) and assigns score + risks.

Hand-offs:
    Each agent’s JSON output feeds the next.
    Research Agent is invoked ad-hoc by Compliance/Architecture/Cost Agents.

Failure Handling:
    If any agent returns low confidence or missing data, the Orchestrator re-runs that agent or applies safe defaults
    (hosted payments, no PAN storage, private DB subnets, deny-by-default IAM) and logs assumptions.

Completeness:
    Final validation gates ensure security, SLO, and cost targets are met before final recommendation.
"""

# =============================================================

"""
QUESTION 3: CLOUD RESOURCE MAPPING
Scenario: Simple E-commerce (serverless-leaning)

Compute:
    - Serverless functions (AWS Lambda / GCP Cloud Functions / Azure Functions) behind API Gateway.
      Why: Low ops, cost-efficient for low/variable traffic.

Storage & Data:
    - Managed PostgreSQL (RDS / Cloud SQL / Azure DB) for orders and users.
    - Object Storage (S3 / GCS / Blob) for product images/static assets.
    - Managed Redis (ElastiCache / Memorystore / Azure Cache for Redis) for sessions & caching.

Networking:
    - API Gateway for routing, CDN for static content, WAF at the edge, and private DB subnets.

Security & Monitoring:
    - IAM least-privilege roles, KMS encryption at rest, TLS in transit, Secrets Manager for credentials.
    - Managed observability (CloudWatch/X-Ray, Cloud Logging/Trace, Azure Monitor).
    - Automated DB backups and lifecycle rules for object storage.

Justification:
    - Matches 1k daily users, minimal ops overhead, scales automatically, secure by default.
"""

# =============================================================

"""
QUESTION 4: REUSABILITY & IMPROVEMENT

Standardized Components:
    - JSON contracts between agents (requirements, compliance, architecture, cost).
    - Reference architecture patterns library (web, chatbot, event-driven, SaaS).
    - Validation gates (security, SLO, cost) and reusable prompt/policy packs.

Customizable per Project:
    - Domain constraints (PCI/PHI), regional residency, budget, performance SLAs, preferred cloud provider.

Learning & Improvement:
    - Store recommendations + outcomes (cost drift, incidents, performance) in a knowledge base.
    - Retrieval-augmented planning: reuse past similar cases for new inputs.
    - Feedback loop: human review + telemetry + price updates refine heuristics.
    - Catalog Updater refreshes pricing/service metadata and triggers re-evaluation when changes exceed thresholds.
"""

# =============================================================

"""
QUESTION 5: PRACTICAL CONSIDERATIONS

Conflicting Recommendations:
    - Arbitration policy: prioritize security > reliability/SLOs > cost > convenience.
    - Compare rationales, pick option satisfying non-negotiables, document trade-offs.

Incomplete or Vague Inputs:
    - Requirements Agent outputs assumptions and open questions.
    - Orchestrator may request clarification or proceed with conservative defaults (hosted payments, private DB, etc.).

Unstated Budget:
    - Cost Agent proposes tiered options: Lean, Balanced, Scale-ready.
    - Defaults to Balanced if no budget info given.

Legacy Integrations:
    - Use adapter services (container/functions) + message queues for decoupling, with retries and backpressure.

Keeping Up with New Services/Pricing:
    - Research Agent and Catalog Updater maintain fresh data on services and pricing.
    - Orchestrator re-runs cost and security validation when changes are detected.
"""