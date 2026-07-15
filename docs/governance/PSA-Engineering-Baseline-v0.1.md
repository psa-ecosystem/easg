# PSA Engineering Baseline v0.1

**Status:** Release Candidate  
**Version:** 0.1.0  
**Date:** 2026-07-14  
**Owner:** PSA Governance

## 0. Document Status and Normative Language

This document is the normative PSA Engineering Baseline v0.1. It defines the minimum engineering rules and compliance expectations for all repositories participating in the PSA ecosystem.

The key words `MUST`, `MUST NOT`, `REQUIRED`, `SHALL`, `SHALL NOT`, `SHOULD`, `SHOULD NOT`, `RECOMMENDED`, `MAY`, and `OPTIONAL` in this document are to be interpreted as described in RFC 2119.

```yaml
rules:
  - rule_id: EB-STATUS-001
    category: baseline
    scope: document_status
    status: active
    compliance_level: 3
    owner: PSA Governance
    title: Normative language is mandatory
    requirement: All normative PSA Engineering Baseline rules MUST use RFC 2119 keywords.
    rationale: Ensures unambiguous interpretation by both humans and AI agents.
    check_method: manual
    severity: blocking
```

---

## 1. Purpose and Scope

### 1.1 Purpose

PSA Engineering Baseline v0.1 defines the minimum engineering rules, repository constraints, and compliance expectations for all projects in the PSA ecosystem. It exists to turn PSA from a collection of architecture documents into a runnable engineering ecosystem.

### 1.2 Scope

This baseline covers:

- Repository structure and required files
- Project charter model and boundaries
- Interface contract governance
- Version and compatibility strategy
- Documentation standards
- Testing and validation standards
- Release standards
- AI coding agent development rules
- Compliance validation methods

This baseline does not cover:

- Specific ontology content
- Runtime implementation internals
- Agent model behavior
- Business application UX
- Enterprise IAM or deployment architecture

```yaml
rules:
  - rule_id: EB-SCOPE-001
    category: baseline
    scope: baseline_scope
    status: active
    compliance_level: 3
    owner: PSA Governance
    title: Baseline applies to all PSA ecosystem repositories
    requirement: Every project registered in docs/governance/registry/projects.yaml MUST comply with PSA Engineering Baseline v0.1.
    rationale: Establishes a consistent engineering floor across independent projects.
    check_method: manual
    severity: blocking

  - rule_id: EB-SCOPE-002
    category: baseline
    scope: baseline_scope
    status: active
    compliance_level: 3
    owner: PSA Governance
    title: Baseline does not define domain content
    requirement: PSA Engineering Baseline MUST NOT specify domain ontology, runtime algorithms, agent models, or application workflows.
    rationale: Keeps governance distinct from implementation and domain expertise.
    check_method: manual
    severity: blocking
```

---

## 2. PSA Engineering Governance Model

### 2.1 Governance Stack

PSA engineering governance follows a layered model:

```text
PSA Ecosystem Charter
        |
        ↓
PSA Engineering Baseline
        |
        ↓
Project Charter
        |
        ↓
Repository Governance
        |
        ↓
AGENTS.md / CLAUDE.md
        |
        ↓
Coding Agent
        |
        ↓
Implementation
        |
        ↓
PSA Compliance Validator
```

### 2.2 Layer Responsibilities

| Layer | Owns |
|---|---|
| PSA Ecosystem Charter | Why PSA exists, ecosystem boundaries, success criteria |
| PSA Engineering Baseline | How all projects must engineer, validate, and release |
| Project Charter | What an individual project owns and does not own |
| Repository Governance | Repository structure, required files, local conventions |
| AGENTS.md / CLAUDE.md | Project-specific agent instructions |
| Coding Agent | Implementation within constraints |
| Implementation | Executable code, tests, documentation |
| PSA Compliance Validator | Automated verification of baseline rules |

```yaml
rules:
  - rule_id: EB-GOV-001
    category: governance
    scope: governance_model
    status: active
    compliance_level: 3
    owner: PSA Governance
    title: Baseline sits below charter and above project governance
    requirement: PSA Engineering Baseline MUST reference PSA Ecosystem Charter and MUST be referenced by Project Charters.
    rationale: Preserves governance hierarchy and prevents rule duplication.
    check_method: manual
    severity: blocking

  - rule_id: EB-GOV-002
    category: governance
    scope: governance_model
    status: active
    compliance_level: 3
    owner: PSA Governance
    title: Project charters must not weaken baseline rules
    requirement: A Project Charter MAY add project-specific constraints but MUST NOT relax PSA Engineering Baseline requirements.
    rationale: Baseline is the minimum engineering floor for the ecosystem.
    check_method: manual
    severity: blocking
```

---

## 3. Repository Governance

### 3.1 Repository Classification

Every PSA ecosystem repository belongs to one of the following categories:

| Category | Example | Primary Output |
|---|---|---|
| Governance Repository | psa-governance | Rules, templates, registry |
| Specification Repository | psa-specifications | Normative standards |
| Semantic Asset Repository | grid-ontology | Semantic packages |
| Mapping Repository | scr-metadata | Metadata mappings |
| Runtime Repository | easg-runtime | Executable runtime |
| Application Repository | powergenius-ai | Business applications |

### 3.2 Mandatory Repository Files

Every PSA repository MUST contain:

```text
repository/
├── AGENTS.md              # Project-specific agent instructions
├── project.yaml           # Machine-readable project metadata
├── README.md              # Human-readable project entry point
├── CHANGELOG.md           # Version history
├── VERSION                # Current semantic version
└── docs/
    ├── charter/
    │   └── Project-Charter.md
    ├── architecture/
    └── decisions/
```

For documentation-only repositories, mandatory code directories such as `src/` and `tests/` MAY be omitted and replaced by appropriate validation assets.

### 3.3 Charter Location

The authoritative Project Charter MUST live in the project repository at:

```text
docs/charter/Project-Charter.md
```

PSA governance repository MAY keep temporary handoff seeds under `docs/governance/handoffs/` while the target repository is unavailable, but these seeds MUST NOT be treated as authoritative.

```yaml
rules:
  - rule_id: EB-RG-001
    category: repository
    scope: repository_governance
    status: active
    compliance_level: 3
    owner: PSA Governance
    title: AGENTS.md must exist at repository root
    requirement: Every PSA project repository MUST contain AGENTS.md at the repository root.
    rationale: Ensures AI coding agents have project identity and boundary context before making changes.
    check_method: file_exists
    target: AGENTS.md
    severity: blocking

  - rule_id: EB-RG-002
    category: repository
    scope: repository_governance
    status: active
    compliance_level: 3
    owner: PSA Governance
    title: project.yaml must exist at repository root
    requirement: Every PSA project repository MUST contain project.yaml at the repository root.
    rationale: Provides machine-readable project metadata for validators and agents.
    check_method: file_exists
    target: project.yaml
    severity: blocking

  - rule_id: EB-RG-003
    category: repository
    scope: repository_governance
    status: active
    compliance_level: 1
    owner: PSA Governance
    title: README.md must exist at repository root
    requirement: Every PSA project repository MUST contain README.md at the repository root.
    rationale: Provides human-readable entry point and development instructions.
    check_method: file_exists
    target: README.md
    severity: blocking

  - rule_id: EB-RG-004
    category: repository
    scope: repository_governance
    status: active
    compliance_level: 2
    owner: PSA Governance
    title: CHANGELOG.md must exist at repository root
    requirement: Every PSA project repository MUST contain CHANGELOG.md at the repository root.
    rationale: Tracks evolution and supports release coordination.
    check_method: file_exists
    target: CHANGELOG.md
    severity: warning

  - rule_id: EB-RG-005
    category: repository
    scope: repository_governance
    status: active
    compliance_level: 1
    owner: PSA Governance
    title: VERSION file must exist at repository root
    requirement: Every PSA project repository MUST contain a VERSION file at the repository root with a semantic version string.
    rationale: Enables independent project release tracking.
    check_method: regex_match
    target: VERSION
    pattern: '^\d+\.\d+\.\d+(?:-[A-Za-z0-9.-]+)?$'
    severity: blocking

  - rule_id: EB-RG-006
    category: repository
    scope: repository_governance
    status: active
    compliance_level: 2
    owner: PSA Governance
    title: Project Charter must exist at docs/charter/Project-Charter.md
    requirement: Every PSA project repository MUST contain docs/charter/Project-Charter.md.
    rationale: Establishes project-local governance and boundaries.
    check_method: file_exists
    target: docs/charter/Project-Charter.md
    severity: blocking

  - rule_id: EB-RG-007
    category: repository
    scope: repository_governance
    status: active
    compliance_level: 2
    owner: PSA Governance
    title: Architecture documentation directory must exist
    requirement: Every PSA project repository MUST contain docs/architecture/.
    rationale: Ensures architectural decisions and component designs are documented.
    check_method: dir_exists
    target: docs/architecture
    severity: warning

  - rule_id: EB-RG-008
    category: repository
    scope: repository_governance
    status: active
    compliance_level: 2
    owner: PSA Governance
    title: Decision records directory must exist
    requirement: Every PSA project repository MUST contain docs/decisions/.
    rationale: Preserves technical decision rationale.
    check_method: dir_exists
    target: docs/decisions
    severity: warning
```

---

## 4. Project Charter Model

### 4.1 Two-Layer Charter Model

PSA uses a two-layer charter model:

- **PSA Ecosystem Layer**: Maintains ecosystem rules, project registry, templates, and boundaries.
- **Project-Local Layer**: Each project maintains its own `docs/charter/Project-Charter.md` describing mission, scope, outputs, roadmap, and local governance rules.

### 4.2 Required Charter Sections

Every Project Charter MUST contain:

1. Purpose
2. Strategic Position (PSA role)
3. Scope
4. Non-Responsibilities
5. PSA Relationship (primary contract)
6. Outputs
7. Repository Structure
8. Engineering Principles
9. Roadmap
10. Success Criteria
11. Governance Rules

### 4.3 Update Triggers

The PSA Project Registry MUST be updated when:

- A project joins or leaves the PSA ecosystem
- A project role changes
- A project crosses or changes an architectural boundary
- A project becomes an official implementation of a PSA contract
- A local charter version changes the project relationship to PSA

```yaml
rules:
  - rule_id: EB-PC-001
    category: project
    scope: project_charter
    status: active
    compliance_level: 2
    owner: PSA Governance
    title: Charter must declare PSA role
    requirement: Every Project Charter MUST declare the project's role in the PSA ecosystem.
    rationale: Clarifies integration position and prevents responsibility overlap.
    check_method: regex_match
    target: docs/charter/Project-Charter.md
    pattern: '(?i)PSA role|strategic position|ecosystem role'
    severity: blocking

  - rule_id: EB-PC-002
    category: project
    scope: project_charter
    status: active
    compliance_level: 2
    owner: PSA Governance
    title: Charter must declare non-responsibilities
    requirement: Every Project Charter MUST list responsibilities the project does not own, especially PSA contracts owned by other layers.
    rationale: Prevents scope creep and dependency reversal.
    check_method: regex_match
    target: docs/charter/Project-Charter.md
    pattern: '(?i)non-responsibilities|does not own|must not own'
    severity: blocking

  - rule_id: EB-PC-003
    category: project
    scope: project_charter
    status: active
    compliance_level: 2
    owner: PSA Governance
    title: Charter must declare primary PSA contract
    requirement: Every Project Charter MUST declare the primary PSA contract the project consumes or implements.
    rationale: Makes integration path explicit.
    check_method: regex_match
    target: docs/charter/Project-Charter.md
    pattern: '(?i)primary PSA contract|PSA relationship'
    severity: blocking

  - rule_id: EB-PC-004
    category: project
    scope: project_charter
    status: active
    compliance_level: 2
    owner: PSA Governance
    title: Charter updates must trigger registry updates
    requirement: When a Project Charter changes role, boundary, or primary PSA contract, the PSA Project Registry MUST be updated in the same PR or changeset.
    rationale: Keeps ecosystem registry synchronized with project governance.
    check_method: manual
    severity: warning
```

---

## 5. Interface Contract Governance

### 5.1 Contract-Based Integration

PSA projects integrate through explicit contracts, not through shared code, direct database access, or undocumented interfaces.

### 5.2 PSA Contract Stack

The primary integration contracts are:

| Contract | Owner | Purpose |
|---|---|---|
| PSA Core Semantic Model | PSA | Canonical semantic primitives |
| PSA Semantic Package Specification | PSA | Exchange semantic assets |
| PSA Semantic Registry Specification | PSA | Register and discover packages |
| PSA Runtime Contract | PSA | Execute semantic assets |
| PSA Agent Semantic Contract | PSA | Agent-facing integration |
| Metadata Mapping Contract | SCR-Metadata | Connect semantics to data |

### 5.3 Dependency Direction

Dependencies MUST flow outward from PSA contracts:

```text
PSA Specifications
        ↓
Semantic Assets / Metadata Mappings
        ↓
Semantic Registry
        ↓
Runtime
        ↓
Agent
        ↓
Application
```

Forbidden: Applications defining semantic primitives, Runtime modifying ontology meaning, Agents creating independent knowledge models.

```yaml
rules:
  - rule_id: EB-IC-001
    category: contract
    scope: interface_contract
    status: active
    compliance_level: 3
    owner: PSA Governance
    title: Projects must declare consumed PSA contracts
    requirement: Every Project Charter MUST declare which PSA contracts the project consumes.
    rationale: Makes integration boundaries explicit and testable.
    check_method: manual
    severity: blocking

  - rule_id: EB-IC-002
    category: contract
    scope: interface_contract
    status: active
    compliance_level: 3
    owner: PSA Governance
    title: Reverse semantic dependencies are forbidden
    requirement: Application projects MUST NOT define or modify PSA Core Semantic Model primitives, Semantic Package schemas, or Runtime semantics.
    rationale: Prevents implementation from redefining contracts.
    check_method: manual
    severity: blocking

  - rule_id: EB-IC-003
    category: contract
    scope: interface_contract
    status: active
    compliance_level: 3
    owner: PSA Governance
    title: Contract changes require ADR and specification update
    requirement: Any change to a PSA-owned contract MUST be approved through an ADR and reflected in the relevant specification before implementation.
    rationale: Preserves contract authority over implementation.
    check_method: manual
    severity: blocking
```

---

## 6. Version and Compatibility Strategy

### 6.1 Semantic Versioning

All PSA normative contracts, packages, registry records, runtime contracts, agent contracts, and CTS suites MUST use semantic versioning:

```text
MAJOR.MINOR.PATCH
```

- `MAJOR`: incompatible contract change
- `MINOR`: backward-compatible extension
- `PATCH`: clarification or non-breaking fix

### 6.2 Compatibility Declarations

Semantic Packages MUST declare required versions of:

- PSA Core Semantic Model
- PSA Semantic Package Specification
- Required package dependencies
- Expected CTS profile
- Minimum Runtime Contract (when runtime loading is claimed)

```yaml
rules:
  - rule_id: EB-VS-001
    category: version
    scope: version_strategy
    status: active
    compliance_level: 1
    owner: PSA Governance
    title: VERSION file must use semantic versioning
    requirement: The VERSION file MUST contain a version string matching MAJOR.MINOR.PATCH format, optionally with a pre-release identifier.
    rationale: Enables predictable compatibility reasoning.
    check_method: regex_match
    target: VERSION
    pattern: '^\d+\.\d+\.\d+(?:-[A-Za-z0-9.-]+)?$'
    severity: blocking

  - rule_id: EB-VS-002
    category: version
    scope: version_strategy
    status: active
    compliance_level: 3
    owner: PSA Governance
    title: Packages must declare PSA contract versions
    requirement: Every Semantic Package manifest.yaml MUST declare psa.core_semantic_model and psa.semantic_package_spec versions.
    rationale: Allows runtime and registry to reason about compatibility.
    check_method: yaml_path
    target: manifest.yaml
    path: psa.core_semantic_model
    severity: blocking

  - rule_id: EB-VS-003
    category: version
    scope: version_strategy
    status: active
    compliance_level: 2
    owner: PSA Governance
    title: Breaking changes require major version increment
    requirement: Any incompatible contract change MUST increment the MAJOR version.
    rationale: Communicates breaking change to consumers.
    check_method: manual
    severity: blocking
```

---

## 7. Documentation Standard

### 7.1 Required Documents

Every PSA repository MUST maintain:

| Document | Purpose |
|---|---|
| README.md | Human entry point and development guide |
| CHANGELOG.md | Version history and migration notes |
| docs/charter/Project-Charter.md | Project governance |
| docs/architecture/ | Architecture decisions and component designs |
| docs/decisions/ | Decision records (ADRs) |

### 7.2 README Minimum Content

README.md SHOULD include:

- Project purpose
- PSA role
- How to build/test/run
- Link to Project Charter
- Link to architecture docs
- Contribution guidelines

```yaml
rules:
  - rule_id: EB-DOC-001
    category: documentation
    scope: documentation
    status: active
    compliance_level: 1
    owner: PSA Governance
    title: README should link to charter
    requirement: README.md SHOULD contain a link to docs/charter/Project-Charter.md.
    rationale: Connects human readers to project governance.
    check_method: regex_match
    target: README.md
    pattern: '(?i)charter|Project-Charter\.md'
    severity: info

  - rule_id: EB-DOC-002
    category: documentation
    scope: documentation
    status: active
    compliance_level: 1
    owner: PSA Governance
    title: README must describe build/test commands
    requirement: README.md MUST describe how to validate the repository.
    rationale: Enables both humans and agents to run quality gates.
    check_method: regex_match
    target: README.md
    pattern: '(?i)test|validate|run|build|pytest|make test|npm test'
    severity: warning

  - rule_id: EB-DOC-003
    category: documentation
    scope: documentation
    status: active
    compliance_level: 2
    owner: PSA Governance
    title: Architecture docs directory must not be empty
    requirement: docs/architecture/ SHOULD contain at least one architecture document.
    rationale: Ensures architectural intent is recorded.
    check_method: dir_not_empty
    target: docs/architecture
    severity: warning
```

---

## 8. Testing and Validation Standard

### 8.1 Validation by Project Type

Different project types have different validation requirements:

| Project Type | Required Validation |
|---|---|
| Semantic Asset | Package validation, semantic consistency checks, CTS |
| Mapping | Mapping validation, lineage checks, evidence validation |
| Runtime | Unit tests, integration tests, Runtime Contract CTS |
| Agent | Capability tests, contract tests, evidence validation |
| Application | Scenario tests, workflow validation, end-to-end tests |

### 8.2 Validation Entry Point

Every repository MUST define a validation entry point in README.md.

### 8.3 CTS Integration

All projects claiming PSA compatibility MUST run the relevant CTS profiles and retain conformance reports as evidence.

```yaml
rules:
  - rule_id: EB-TEST-001
    category: testing
    scope: testing
    status: active
    compliance_level: 1
    owner: PSA Governance
    title: Repository must define validation command
    requirement: README.md MUST describe a command that runs the repository's validation suite.
    rationale: Provides a repeatable quality gate.
    check_method: regex_match
    target: README.md
    pattern: '(?i)```bash.*\n.*(?:test|validate|check|pytest|make|npm|python3).*\n```'
    severity: blocking

  - rule_id: EB-TEST-002
    category: testing
    scope: testing
    status: active
    compliance_level: 3
    owner: PSA Governance
    title: PSA-compatible projects must run CTS
    requirement: Any project claiming PSA compatibility MUST execute the relevant CTS profiles and produce evidence-based conformance reports.
    rationale: Verifies contract conformance with evidence.
    check_method: manual
    severity: blocking

  - rule_id: EB-TEST-003
    category: testing
    scope: testing
    status: active
    compliance_level: 3
    owner: PSA Governance
    title: Conformance reports must be evidence-based
    requirement: CTS or compliance reports MUST include input artifacts, validator identity, timestamp, and failure evidence.
    rationale: Enables auditability and traceability.
    check_method: manual
    severity: blocking
```

---

## 9. Release Standard

### 9.1 Independent Releases

Each project controls its own release cadence and version.

### 9.2 Ecosystem Releases

PSA coordinates ecosystem releases that declare compatible component versions:

```yaml
release:
  version: 0.2.0
  components:
    grid-ontology: 0.2.0
    scr-metadata: 0.2.0
    easg-runtime: 0.2.0
    agent-framework: 0.2.0
    powergenius-ai: 0.2.0
```

### 9.3 Release Order

Release order follows dependency direction:

```text
PSA Specification → Semantic Package → CTS → Registry → Runtime → Agent → Application
```

```yaml
rules:
  - rule_id: EB-REL-001
    category: release
    scope: release
    status: active
    compliance_level: 2
    owner: PSA Governance
    title: Releases must update CHANGELOG
    requirement: Every release MUST update CHANGELOG.md with version, date, changes, and migration notes.
    rationale: Communicates evolution to consumers.
    check_method: regex_match
    target: CHANGELOG.md
    pattern: '(?i)##?\s*\[?\d+\.\d+\.\d+\]?'
    severity: warning

  - rule_id: EB-REL-002
    category: release
    scope: release
    status: active
    compliance_level: 3
    owner: PSA Governance
    title: Ecosystem releases must declare component versions
    requirement: Every PSA ecosystem release MUST declare the version of each participating component.
    rationale: Coordinates multi-project compatibility.
    check_method: manual
    severity: blocking
```

---

## 10. Agent Development Standard

### 10.1 Agent Role

AI coding agents are engineering executors, not architecture owners. Agents implement approved designs, follow project architecture, maintain contracts, and improve implementation quality.

### 10.2 Instruction Priority

When multiple instructions exist, agents MUST resolve conflicts using this priority order:

1. User explicit instruction
2. PSA Governance Rules (including this Baseline)
3. Project Charter
4. Repository AGENTS.md / CLAUDE.md
5. Architecture documentation
6. Existing code convention
7. Agent default behavior

### 10.3 Core Agent Rules

- **Read Before Write**: Agents MUST read AGENTS.md, project.yaml, README.md, charter, architecture docs, and tests before modifying code.
- **Minimal Change**: Agents MUST prefer minimal, reviewable changes and avoid unnecessary refactoring.
- **Architecture Boundary Protection**: Agents MUST preserve PSA dependency direction and must not introduce reverse dependencies.
- **Semantic Protection**: Agents MUST NOT silently add or modify PSA Core Semantic Model primitives.
- **Evidence-Based Completion**: Agents MUST provide evidence for completion, including changed files, tests, validation results, and known limitations.
- **Normative Document Protection**: Agents MUST NOT modify normative PSA documents without explicit approval.
- **Pre-Submission Validation**: Agents SHOULD run psa-validator before submitting changes.

```yaml
rules:
  - rule_id: EB-AGENT-001
    category: agent
    scope: agent_development
    status: active
    compliance_level: 3
    owner: PSA Governance
    title: Agent must read governance files before changes
    requirement: AI coding agents MUST read AGENTS.md, project.yaml, README.md, and Project Charter before modifying code, specifications, tests, or governance files.
    rationale: Prevents agents from acting without project context.
    check_method: manual
    severity: blocking

  - rule_id: EB-AGENT-002
    category: agent
    scope: agent_development
    status: active
    compliance_level: 3
    owner: PSA Governance
    title: Agent must not redefine architecture
    requirement: AI coding agents MUST NOT create new modules, change dependency direction, modify interfaces, or add semantic primitives without ADR or specification review.
    rationale: Preserves architecture ownership by humans.
    check_method: manual
    severity: blocking

  - rule_id: EB-AGENT-003
    category: agent
    scope: agent_development
    status: active
    compliance_level: 3
    owner: PSA Governance
    title: Agent must provide evidence for completion
    requirement: AI coding agents MUST report changed files, test results, validation results, and known limitations when claiming a task is complete.
    rationale: Prevents unsubstantiated completion claims.
    check_method: manual
    severity: blocking

  - rule_id: EB-AGENT-004
    category: agent
    scope: agent_development
    status: active
    compliance_level: 3
    owner: PSA Governance
    title: Agent must prefer minimal changes
    requirement: AI coding agents SHOULD modify existing components and reuse abstractions rather than rewriting modules or replacing frameworks.
    rationale: Reduces review risk and preserves stability.
    check_method: manual
    severity: warning

  - rule_id: EB-AGENT-005
    category: agent
    scope: agent_development
    status: active
    compliance_level: 3
    owner: PSA Governance
    title: Agent must not modify normative PSA documents without approval
    requirement: AI coding agents MUST NOT modify PSA Engineering Baseline, PSA specifications, ADRs, or Project Charters without explicit human approval.
    rationale: Prevents agents from silently altering governance authority and contracts.
    check_method: manual
    severity: blocking

  - rule_id: EB-AGENT-006
    category: agent
    scope: agent_development
    status: active
    compliance_level: 3
    owner: PSA Governance
    title: Agent should run psa-validator before submitting changes
    requirement: AI coding agents SHOULD run psa-validator before submitting changes.
    rationale: Catches baseline regressions before they reach review.
    check_method: manual
    severity: warning
```

---

## 11. Compliance Validation

### 11.1 Three-Level Compliance Model

PSA Engineering Baseline compliance follows a hybrid model:

| Level | Actor | Checks |
|---|---|---|
| Level 1 — Automated | PSA Compliance Validator | File existence, directory structure, version format, YAML paths, regex matches |
| Level 2 — Agent Assisted | AI Coding Agent | Architecture boundary, dependency direction, semantic change impact, documentation synchronization |
| Level 3 — Human Governance | PSA Governance Review | New architecture, new projects, standard changes, release coordination |

### 11.2 Compliance Report

Compliance checks MUST produce a report consistent with the CTS report format:

```yaml
report_id: psa-eb-check-<repo>-<timestamp>
generated_at: ISO-8601 timestamp
baseline_version: 0.1.0
target: <repository-path>
summary:
  overall_status: passed | failed | passed_with_warnings
  passed: 0
  failed: 0
  warnings: 0
  info: 0
  manual: 0
  skipped: 0
  max_compliance_level: 3
  achieved_compliance_level: 0
results:
  - rule_id: EB-RG-001
    category: repository
    severity: blocking
    compliance_level: 3
    status: passed | failed | warning | info | skipped | not_applicable
    summary: AGENTS.md exists
    evidence:
      path: AGENTS.md
```

### 11.3 Validator Tooling

PSA provides a compliance validator under `tools/` that:

- Reads PSA Engineering Baseline Markdown
- Extracts all YAML rule blocks
- Validates each rule against the Rule Schema (Appendix D)
- Executes rules with `check_method` other than `manual`
- Produces a compliance report
- Returns non-zero exit code when blocking rules fail

```yaml
rules:
  - rule_id: EB-COMP-001
    category: compliance
    scope: compliance
    status: active
    compliance_level: 3
    owner: PSA Governance
    title: Baseline must be machine-parseable
    requirement: PSA Engineering Baseline MUST use standard Markdown YAML fenced code blocks for rules so that validators can extract them without custom syntax.
    rationale: Enables automated rule extraction and validation.
    check_method: manual
    severity: blocking

  - rule_id: EB-COMP-002
    category: compliance
    scope: compliance
    status: active
    compliance_level: 3
    owner: PSA Governance
    title: Validator must produce evidence-based reports
    requirement: The PSA Compliance Validator MUST produce reports containing rule_id, status, summary, and evidence for each checked rule.
    rationale: Supports auditability and debugging.
    check_method: manual
    severity: blocking

  - rule_id: EB-COMP-003
    category: compliance
    scope: compliance
    status: active
    compliance_level: 3
    owner: PSA Governance
    title: Manual rules must be documented for Agent review
    requirement: "Every rule with check_method: manual MUST include clear prose rationale so that AI agents can apply judgment."
    rationale: Bridges automated and human/agent governance.
    check_method: manual
    severity: warning
```

---

## Appendix A: Rule Registry

This appendix lists all rule IDs defined in this baseline for traceability.

| Rule ID | Category | Section | Title | Check Method | Severity | Level |
|---|---|---|---|---|---|---|
| EB-STATUS-001 | baseline | 0 | Normative language is mandatory | manual | blocking | 3 |
| EB-SCOPE-001 | baseline | 1 | Baseline applies to all PSA ecosystem repositories | manual | blocking | 3 |
| EB-SCOPE-002 | baseline | 1 | Baseline does not define domain content | manual | blocking | 3 |
| EB-GOV-001 | governance | 2 | Baseline sits below charter and above project governance | manual | blocking | 3 |
| EB-GOV-002 | governance | 2 | Project charters must not weaken baseline rules | manual | blocking | 3 |
| EB-RG-001 | repository | 3 | AGENTS.md must exist at repository root | file_exists | blocking | 3 |
| EB-RG-002 | repository | 3 | project.yaml must exist at repository root | file_exists | blocking | 3 |
| EB-RG-003 | repository | 3 | README.md must exist at repository root | file_exists | blocking | 1 |
| EB-RG-004 | repository | 3 | CHANGELOG.md must exist at repository root | file_exists | warning | 2 |
| EB-RG-005 | repository | 3 | VERSION file must exist at repository root | regex_match | blocking | 1 |
| EB-RG-006 | repository | 3 | Project Charter must exist at docs/charter/Project-Charter.md | file_exists | blocking | 2 |
| EB-RG-007 | repository | 3 | Architecture documentation directory must exist | dir_exists | warning | 2 |
| EB-RG-008 | repository | 3 | Decision records directory must exist | dir_exists | warning | 2 |
| EB-PC-001 | project | 4 | Charter must declare PSA role | regex_match | blocking | 2 |
| EB-PC-002 | project | 4 | Charter must declare non-responsibilities | regex_match | blocking | 2 |
| EB-PC-003 | project | 4 | Charter must declare primary PSA contract | regex_match | blocking | 2 |
| EB-PC-004 | project | 4 | Charter updates must trigger registry updates | manual | warning | 2 |
| EB-IC-001 | contract | 5 | Projects must declare consumed PSA contracts | manual | blocking | 3 |
| EB-IC-002 | contract | 5 | Reverse semantic dependencies are forbidden | manual | blocking | 3 |
| EB-IC-003 | contract | 5 | Contract changes require ADR and specification update | manual | blocking | 3 |
| EB-VS-001 | version | 6 | VERSION file must use semantic versioning | regex_match | blocking | 1 |
| EB-VS-002 | version | 6 | Packages must declare PSA contract versions | yaml_path | blocking | 3 |
| EB-VS-003 | version | 6 | Breaking changes require major version increment | manual | blocking | 2 |
| EB-DOC-001 | documentation | 7 | README should link to charter | regex_match | info | 1 |
| EB-DOC-002 | documentation | 7 | README must describe build/test commands | regex_match | warning | 1 |
| EB-DOC-003 | documentation | 7 | Architecture docs directory must not be empty | dir_not_empty | warning | 2 |
| EB-TEST-001 | testing | 8 | Repository must define validation command | regex_match | blocking | 1 |
| EB-TEST-002 | testing | 8 | PSA-compatible projects must run CTS | manual | blocking | 3 |
| EB-TEST-003 | testing | 8 | Conformance reports must be evidence-based | manual | blocking | 3 |
| EB-REL-001 | release | 9 | Releases must update CHANGELOG | regex_match | warning | 2 |
| EB-REL-002 | release | 9 | Ecosystem releases must declare component versions | manual | blocking | 3 |
| EB-AGENT-001 | agent | 10 | Agent must read governance files before changes | manual | blocking | 3 |
| EB-AGENT-002 | agent | 10 | Agent must not redefine architecture | manual | blocking | 3 |
| EB-AGENT-003 | agent | 10 | Agent must provide evidence for completion | manual | blocking | 3 |
| EB-AGENT-004 | agent | 10 | Agent must prefer minimal changes | manual | warning | 3 |
| EB-AGENT-005 | agent | 10 | Agent must not modify normative PSA documents without approval | manual | blocking | 3 |
| EB-AGENT-006 | agent | 10 | Agent should run psa-validator before submitting changes | manual | warning | 3 |
| EB-COMP-001 | compliance | 11 | Baseline must be machine-parseable | manual | blocking | 3 |
| EB-COMP-002 | compliance | 11 | Validator must produce evidence-based reports | manual | blocking | 3 |
| EB-COMP-003 | compliance | 11 | Manual rules must be documented for Agent review | manual | warning | 3 |
| EB-BASELINE-001 | baseline | E | Baseline rule IDs must be unique | manual | blocking | 3 |
| EB-BASELINE-002 | baseline | E | Baseline rule registry must match rule blocks | manual | blocking | 3 |
| EB-BASELINE-003 | baseline | E | Baseline rule blocks must match Rule Schema | manual | blocking | 3 |

---

## Appendix B: Compliance Levels

### Level 1 — Basic

Requirements:

- README.md exists
- VERSION file exists
- Tests can be run

### Level 2 — Governed

Additional requirements:

- Project Charter exists
- Architecture documentation exists
- ADR directory exists
- CHANGELOG.md exists

### Level 3 — PSA Native

Additional requirements:

- AGENTS.md exists
- project.yaml exists
- Automated validation entry point exists
- Compliance with PSA Engineering Baseline

PSA ecosystem repositories SHOULD target Level 3.

---

## Appendix C: Validator Specification

### C.1 Location

The PSA Compliance Validator will be implemented under:

```text
tools/psa_compliance_validator.py
```

Future expansion may create:

```text
tools/psa-validator/
├── baseline_validator.py
├── contract_validator.py
├── package_validator.py
└── report_generator.py
```

### C.2 Rule Extraction

The validator MUST:

1. Read the PSA Engineering Baseline Markdown file.
2. Find all fenced YAML code blocks.
3. Filter blocks whose parsed content is a mapping with a top-level `rules:` key that maps to a list of rule dictionaries. Reject scalar, mapping, or metadata-only `rules:` values.
4. Merge all rule lists into a single rule registry.
5. Validate each extracted rule against the Rule Schema (Appendix D).

### C.3 Supported Check Methods

| Method | Description |
|---|---|
| `file_exists` | Verify target file exists relative to repository root |
| `dir_exists` | Verify target directory exists |
| `dir_not_empty` | Verify target directory contains at least one file |
| `regex_match` | Search target file content for pattern |
| `yaml_path` | Verify target YAML file contains a path |
| `manual` | No automated check; documented for Agent/human review |

### C.4 Command Line Interface

```bash
# Validate current repository
python3 tools/psa_compliance_validator.py

# Validate another repository
python3 tools/psa_compliance_validator.py --repo /path/to/project

# Output report to file
python3 tools/psa_compliance_validator.py --report /path/to/report.json

# Check only a specific scope
python3 tools/psa_compliance_validator.py --scope repository_governance

# Validate the baseline itself
python3 tools/psa_compliance_validator.py --self-check
```

### C.5 Exit Codes

- `0`: All blocking rules passed, no blocking failures
- `1`: One or more blocking rules failed
- `2`: Validator error (e.g., baseline file unreadable)

---

## Appendix D: Rule Schema

Every rule block embedded in PSA Engineering Baseline MUST conform to this schema:

```yaml
RuleSchema:
  required:
    - rule_id
    - category
    - scope
    - status
    - compliance_level
    - owner
    - title
    - requirement
    - rationale
    - check_method
    - severity
  fields:
    rule_id:
      type: string
      pattern: '^EB-[A-Z]{2,}-\d{3}$'
      description: Globally unique rule identifier.
    category:
      type: string
      enum: [baseline, governance, repository, project, contract, version, documentation, testing, release, agent, compliance]
      description: High-level classification for rule organization and filtering.
    scope:
      type: string
      description: Functional area within the baseline.
    status:
      type: string
      enum: [active, draft, deprecated]
      description: Lifecycle status of the rule.
    compliance_level:
      type: integer
      enum: [1, 2, 3]
      description: Minimum compliance level at which this rule applies.
    owner:
      type: string
      description: Responsible governance body or project.
    title:
      type: string
      description: Short human-readable rule title.
    requirement:
      type: string
      description: Normative requirement statement using RFC 2119 keywords.
    rationale:
      type: string
      description: Explanation of why the rule exists.
    check_method:
      type: string
      enum: [file_exists, dir_exists, dir_not_empty, regex_match, yaml_path, manual]
      description: Automated or manual verification method.
    target:
      type: string
      required_when: "check_method in [file_exists, dir_exists, dir_not_empty, regex_match, yaml_path]"
      description: File or directory path to inspect.
    path:
      type: string
      required_when: "check_method == yaml_path"
      description: YAML path expression for yaml_path checks.
    pattern:
      type: string
      required_when: "check_method == regex_match"
      description: Regular expression for regex_match checks.
    severity:
      type: string
      enum: [blocking, warning, info]
      description: Consequence level of a rule failure.
```

### D.1 Severity Definitions

| Severity | Meaning | Typical Mapping |
|---|---|---|
| `blocking` | MUST / REQUIRED failure; fails compliance | RFC 2119 MUST / SHALL |
| `warning` | SHOULD / RECOMMENDED failure; tolerated but flagged | RFC 2119 SHOULD |
| `info` | Informational observation; best practice or hint | RFC 2119 MAY / optional recommendation |

### D.2 Rule Lifecycle

| Status | Meaning | Validator Behavior |
|---|---|---|
| `active` | Rule is in force and MUST be checked | Execute or require manual review |
| `draft` | Rule is proposed but not yet binding | Report as draft, do not fail compliance |
| `deprecated` | Rule is retired | Skip unless running historical checks |

### D.3 Rule ID Prefix Convention

Every `rule_id` MUST use a prefix that corresponds to its `category`. A validator MUST reject a rule whose prefix does not match its category.

| Category | Allowed Prefixes |
|---|---|
| `baseline` | `STATUS`, `SCOPE`, `BASELINE` |
| `governance` | `GOV` |
| `repository` | `RG` |
| `project` | `PC` |
| `contract` | `IC` |
| `version` | `VS` |
| `documentation` | `DOC` |
| `testing` | `TEST` |
| `release` | `REL` |
| `agent` | `AGENT` |
| `compliance` | `COMP` |

---

## Appendix E: Baseline Self Validation

PSA Engineering Baseline MUST be self-consistent. The validator MUST support a `--self-check` mode that verifies the baseline document itself.

### E.1 Required Self-Checks

```yaml
rules:
  - rule_id: EB-BASELINE-001
    category: baseline
    scope: baseline_validation
    status: active
    compliance_level: 3
    owner: PSA Governance
    title: Baseline rule IDs must be unique
    requirement: Every rule_id defined in PSA Engineering Baseline MUST appear exactly once across all YAML rule blocks.
    rationale: Prevents duplicate or conflicting rules.
    check_method: manual
    severity: blocking

  - rule_id: EB-BASELINE-002
    category: baseline
    scope: baseline_validation
    status: active
    compliance_level: 3
    owner: PSA Governance
    title: Baseline rule registry must match rule blocks
    requirement: Appendix A Rule Registry MUST contain exactly the same rule_ids as the YAML rule blocks in the document body.
    rationale: Ensures traceability and prevents registry drift.
    check_method: manual
    severity: blocking

  - rule_id: EB-BASELINE-003
    category: baseline
    scope: baseline_validation
    status: active
    compliance_level: 3
    owner: PSA Governance
    title: Baseline rule blocks must match Rule Schema
    requirement: Every YAML rule block in PSA Engineering Baseline MUST conform to the Rule Schema defined in Appendix D.
    rationale: Guarantees machine-parseability and validator stability.
    check_method: manual
    severity: blocking
```

### E.2 Self-Check Report

The `--self-check` report MUST include:

- Rule ID uniqueness result
- Registry vs. rule block consistency result
- Rule Schema conformance result
- Any duplicate, missing, or malformed rules

---

## Design Notes

### Relationship to Existing Documents

- `PSA-Project-Charter-v0.1.md`: Baseline references it as the ecosystem charter.
- `PSA-Ecosystem-Charter-Model-v0.1.md`: Baseline implements the two-layer charter model and repository requirements.
- `docs/governance/templates/Project-Charter-Template-v0.1.md`: Baseline mandates its use.
- `docs/governance/registry/projects.yaml`: Baseline applies to all registered projects.
- GPT governance drafts (`PSA Project Governance Model`, `PSA Repository Governance Specification`, `PSA Integration Contract Specification`, `PSA Agent Engineering Standard`, `PSA Ecosystem Operating Model`): Treated as source material and detailed input, not as authoritative baseline content.

### Deferred Topics

The following are intentionally deferred beyond v0.1:

- Package signing and trust chain
- Automated contract compatibility resolver
- Multi-package dependency resolution
- CI/CD integration profile
- Performance benchmark profile
- Security scanning profile

### Success Criteria

PSA Engineering Baseline v0.1 is successful when:

1. The baseline document is accepted and stored in `docs/governance/`.
2. A compliance validator can extract and execute at least the automated rules.
3. The PSA repository itself passes Level 3 compliance.
4. Each ecosystem project has a clear path to Level 3 compliance.
5. AI coding agents can use the baseline to guide repository changes.
