"""
Pydantic models for Concept Analysis feature.
Defines schemas for logical, inferential, and assumption analysis results.

Includes normalization validators to handle LLM drift (e.g., "medium-high" -> "medium").
"""

from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Literal, Optional, Any
from enum import Enum
import re


# =============================================================================
# Chain Taxonomy Enums (5 Classification Systems)
# =============================================================================

class InferentialMode(str, Enum):
    """Taxonomy 1: How conclusion follows from premises (Classical Logic)"""
    DEDUCTIVE = "deductive"
    INDUCTIVE = "inductive"
    ABDUCTIVE = "abductive"
    ANALOGICAL = "analogical"


class CausalStructure(str, Enum):
    """Taxonomy 2: What kind of causal explanation (Philosophy of Causation)"""
    MECHANISTIC = "mechanistic"
    COUNTERFACTUAL = "counterfactual"
    CONSTITUTIVE = "constitutive"
    TELEOLOGICAL = "teleological"
    DISPOSITIONAL = "dispositional"


class DialecticalFunction(str, Enum):
    """Taxonomy 3: Role in Hegelian dialectical movement"""
    THESIS_ESTABLISHING = "thesis_establishing"
    ANTITHETICAL = "antithetical"
    SYNTHETIC = "synthetic"
    IMMANENT_CRITIQUE = "immanent_critique"
    DETERMINATE_NEGATION = "determinate_negation"


class InferentialRole(str, Enum):
    """Taxonomy 4: Type of inferential binding (Brandom/Sellars)"""
    MATERIAL = "material"
    FORMAL = "formal"
    MODAL = "modal"
    NORMATIVE = "normative"
    COMMISSIVE = "commissive"


class ArgumentativeFunction(str, Enum):
    """Taxonomy 5: Role in building overall argument (Toulmin/Walton)"""
    FOUNDATIONAL = "foundational"
    ELABORATIVE = "elaborative"
    DEFENSIVE = "defensive"
    BRIDGE = "bridge"
    CULMINATIVE = "culminative"


# =============================================================================
# Normalization Helpers
# =============================================================================

def normalize_severity(value: Any) -> Literal['high', 'medium', 'low']:
    """
    Normalize severity values to handle LLM drift.

    Maps variations like:
    - "medium-high", "high-medium" -> "high"
    - "low-medium", "medium-low" -> "medium"
    - "Medium", "MEDIUM" -> "medium"
    """
    if value is None:
        return 'medium'

    v_lower = str(value).lower().strip()

    # Handle compound values - if "high" appears first or alone, it's high
    if v_lower == 'high':
        return 'high'
    if v_lower == 'low':
        return 'low'
    if v_lower == 'medium':
        return 'medium'

    # Handle compound values like "medium-high", "high-medium"
    if 'high' in v_lower and 'medium' not in v_lower:
        return 'high'
    if 'high' in v_lower:
        # "medium-high" or "high-medium" -> treat as high (err on the side of importance)
        return 'high'
    if 'low' in v_lower and 'medium' not in v_lower:
        return 'low'
    if 'medium' in v_lower:
        return 'medium'

    # Default fallback
    return 'medium'


def normalize_centrality(value: Any) -> Literal['core', 'important', 'peripheral']:
    """Normalize centrality values."""
    if value is None:
        return 'important'

    v_lower = str(value).lower().strip()

    if 'core' in v_lower or 'central' in v_lower or 'load' in v_lower:
        return 'core'
    if 'peripheral' in v_lower or 'minor' in v_lower:
        return 'peripheral'
    return 'important'


def normalize_argument_type(value: Any) -> Literal['deductive', 'inductive', 'abductive']:
    """Normalize argument type values."""
    if value is None:
        return 'deductive'

    v_lower = str(value).lower().strip()

    if 'deduct' in v_lower:
        return 'deductive'
    if 'induct' in v_lower:
        return 'inductive'
    if 'abduct' in v_lower:
        return 'abductive'

    return 'deductive'


def normalize_mechanism_detail(value: Any) -> Literal['low', 'medium', 'high']:
    """Normalize mechanism detail levels."""
    if value is None:
        return 'medium'

    v_lower = str(value).lower().strip()

    if 'high' in v_lower:
        return 'high'
    if 'low' in v_lower:
        return 'low'
    return 'medium'


def normalize_causal_weight(value: Any) -> Literal['heavy', 'moderate', 'light']:
    """Normalize causal weight values."""
    if value is None:
        return 'moderate'

    v_lower = str(value).lower().strip()

    if 'heavy' in v_lower or 'high' in v_lower:
        return 'heavy'
    if 'light' in v_lower or 'low' in v_lower:
        return 'light'
    return 'moderate'


def normalize_change_type(value: Any) -> Literal['strengthened', 'weakened', 'abandoned', 'introduced']:
    """Normalize textual shift change types."""
    if value is None:
        return 'introduced'

    v_lower = str(value).lower().strip()

    if 'strength' in v_lower:
        return 'strengthened'
    if 'weak' in v_lower:
        return 'weakened'
    if 'abandon' in v_lower or 'drop' in v_lower:
        return 'abandoned'
    return 'introduced'


def normalize_vulnerability_type(value: Any) -> Literal['unstated_premise', 'inferential_gap', 'equivocation', 'question_begging', 'false_dichotomy']:
    """Normalize vulnerability type values."""
    if value is None:
        return 'inferential_gap'

    v_lower = str(value).lower().strip().replace(' ', '_').replace('-', '_')

    valid_types = ['unstated_premise', 'inferential_gap', 'equivocation', 'question_begging', 'false_dichotomy']

    if v_lower in valid_types:
        return v_lower  # type: ignore

    # Handle variations
    if 'premise' in v_lower or 'unstated' in v_lower:
        return 'unstated_premise'
    if 'gap' in v_lower or 'inferential' in v_lower:
        return 'inferential_gap'
    if 'equivoc' in v_lower:
        return 'equivocation'
    if 'beg' in v_lower or 'circular' in v_lower:
        return 'question_begging'
    if 'dichot' in v_lower or 'false' in v_lower:
        return 'false_dichotomy'

    return 'inferential_gap'


# =============================================================================
# Chain Taxonomy Normalizers
# =============================================================================

def normalize_inferential_mode(value: Any) -> Optional[str]:
    """Normalize inferential mode values."""
    if value is None:
        return None

    v_lower = str(value).lower().strip().replace('-', '_').replace(' ', '_')
    valid = ['deductive', 'inductive', 'abductive', 'analogical']

    if v_lower in valid:
        return v_lower

    if 'deduct' in v_lower:
        return 'deductive'
    if 'induct' in v_lower:
        return 'inductive'
    if 'abduct' in v_lower:
        return 'abductive'
    if 'analog' in v_lower:
        return 'analogical'

    return None


def normalize_causal_structure(value: Any) -> Optional[str]:
    """Normalize causal structure values."""
    if value is None:
        return None

    v_lower = str(value).lower().strip().replace('-', '_').replace(' ', '_')
    valid = ['mechanistic', 'counterfactual', 'constitutive', 'teleological', 'dispositional']

    if v_lower in valid:
        return v_lower

    if 'mechan' in v_lower:
        return 'mechanistic'
    if 'counterfact' in v_lower:
        return 'counterfactual'
    if 'constit' in v_lower:
        return 'constitutive'
    if 'teleolog' in v_lower or 'purpose' in v_lower or 'means_end' in v_lower:
        return 'teleological'
    if 'disposit' in v_lower or 'capacity' in v_lower:
        return 'dispositional'

    return None


def normalize_dialectical_function(value: Any) -> Optional[str]:
    """Normalize dialectical function values."""
    if value is None:
        return None

    v_lower = str(value).lower().strip().replace('-', '_').replace(' ', '_')
    valid = ['thesis_establishing', 'antithetical', 'synthetic', 'immanent_critique', 'determinate_negation']

    if v_lower in valid:
        return v_lower

    if 'thesis' in v_lower or 'establish' in v_lower or 'affirm' in v_lower:
        return 'thesis_establishing'
    if 'antithes' in v_lower or 'negate' in v_lower or 'oppos' in v_lower:
        return 'antithetical'
    if 'synthe' in v_lower or 'sublat' in v_lower or 'aufheb' in v_lower:
        return 'synthetic'
    if 'immanent' in v_lower or 'internal_contra' in v_lower:
        return 'immanent_critique'
    if 'determinate' in v_lower or 'specific_negat' in v_lower:
        return 'determinate_negation'

    return None


def normalize_inferential_role(value: Any) -> Optional[str]:
    """Normalize inferential role values (Brandom/Sellars)."""
    if value is None:
        return None

    v_lower = str(value).lower().strip().replace('-', '_').replace(' ', '_')
    valid = ['material', 'formal', 'modal', 'normative', 'commissive']

    if v_lower in valid:
        return v_lower

    if 'material' in v_lower or 'content_based' in v_lower or 'meaning' in v_lower:
        return 'material'
    if 'formal' in v_lower or 'structure_based' in v_lower or 'topic_neutral' in v_lower:
        return 'formal'
    if 'modal' in v_lower or 'necessit' in v_lower or 'possibil' in v_lower:
        return 'modal'
    if 'normativ' in v_lower or 'ought' in v_lower or 'should' in v_lower:
        return 'normative'
    if 'commissiv' in v_lower or 'commitment' in v_lower or 'entitlement' in v_lower:
        return 'commissive'

    return None


def normalize_argumentative_function(value: Any) -> Optional[str]:
    """Normalize argumentative function values (Toulmin/Walton)."""
    if value is None:
        return None

    v_lower = str(value).lower().strip().replace('-', '_').replace(' ', '_')
    valid = ['foundational', 'elaborative', 'defensive', 'bridge', 'culminative']

    if v_lower in valid:
        return v_lower

    if 'foundation' in v_lower or 'ground' in v_lower or 'basic' in v_lower or 'warrant' in v_lower:
        return 'foundational'
    if 'elaborat' in v_lower or 'implicat' in v_lower or 'extend' in v_lower:
        return 'elaborative'
    if 'defens' in v_lower or 'rebut' in v_lower or 'object' in v_lower:
        return 'defensive'
    if 'bridge' in v_lower or 'cross_domain' in v_lower or 'connect' in v_lower:
        return 'bridge'
    if 'culminat' in v_lower or 'final' in v_lower or 'ultimate' in v_lower:
        return 'culminative'

    return None


# =============================================================================
# Logical Analysis Models
# =============================================================================

class LogicalForm(BaseModel):
    """Logical structure of an argument."""
    premises: list[str]
    conclusion: str
    argument_type: Literal['deductive', 'inductive', 'abductive']
    form_name: Optional[str] = None

    @field_validator('argument_type', mode='before')
    @classmethod
    def normalize_arg_type(cls, v):
        return normalize_argument_type(v)


class LogicalArgument(BaseModel):
    """A single argument in the inventory."""
    id: str
    source: str
    quote: str
    logical_form: LogicalForm
    unstated_premises: list[str] = Field(default_factory=list)
    concept_role: str


class ArgumentDependency(BaseModel):
    """Dependency between arguments in a chain."""
    from_arg: str = Field(alias='from')
    to_arg: str = Field(alias='to')
    relationship: str

    class Config:
        populate_by_name = True


class ArgumentChain(BaseModel):
    """Chain of connected arguments with 5-taxonomy classification."""
    chain_id: str
    sequence: list[str]
    dependencies: list[ArgumentDependency] = Field(default_factory=list)
    ultimate_conclusion: str
    visualization: str = ""

    # 5 Taxonomy Classifications
    inferential_mode: Optional[Literal['deductive', 'inductive', 'abductive', 'analogical']] = None
    causal_structure: Optional[Literal['mechanistic', 'counterfactual', 'constitutive', 'teleological', 'dispositional']] = None
    dialectical_function: Optional[Literal['thesis_establishing', 'antithetical', 'synthetic', 'immanent_critique', 'determinate_negation']] = None
    inferential_role: Optional[Literal['material', 'formal', 'modal', 'normative', 'commissive']] = None
    argumentative_function: Optional[Literal['foundational', 'elaborative', 'defensive', 'bridge', 'culminative']] = None

    @field_validator('inferential_mode', mode='before')
    @classmethod
    def normalize_inf_mode(cls, v):
        return normalize_inferential_mode(v)

    @field_validator('causal_structure', mode='before')
    @classmethod
    def normalize_caus_struct(cls, v):
        return normalize_causal_structure(v)

    @field_validator('dialectical_function', mode='before')
    @classmethod
    def normalize_dial_func(cls, v):
        return normalize_dialectical_function(v)

    @field_validator('inferential_role', mode='before')
    @classmethod
    def normalize_inf_role(cls, v):
        return normalize_inferential_role(v)

    @field_validator('argumentative_function', mode='before')
    @classmethod
    def normalize_arg_func(cls, v):
        return normalize_argumentative_function(v)


class CausalClaim(BaseModel):
    """A causal claim about the concept."""
    effect: Optional[str] = None
    cause: Optional[str] = None
    mechanism: str
    evidence_quote: str
    source: str


class InterventionistClaim(BaseModel):
    """An interventionist claim - can be string or structured object."""
    intervention: str
    expected_effect: str = ""
    evidence_quote: str = ""
    source: str = ""


class CausalArchitecture(BaseModel):
    """Causal architecture of the concept."""
    concept_as_cause: list[CausalClaim] = Field(default_factory=list)
    concept_as_effect: list[CausalClaim] = Field(default_factory=list)
    mechanism_detail: Literal['low', 'medium', 'high'] = 'medium'
    interventionist_claims: list[str | InterventionistClaim] = Field(default_factory=list)

    @field_validator('mechanism_detail', mode='before')
    @classmethod
    def normalize_mech_detail(cls, v):
        return normalize_mechanism_detail(v)

    @field_validator('interventionist_claims', mode='before')
    @classmethod
    def normalize_interventionist_claims(cls, v):
        """Accept both strings and structured objects for interventionist claims."""
        if not v:
            return []
        result = []
        for item in v:
            if isinstance(item, str):
                result.append(item)
            elif isinstance(item, dict):
                # Convert dict to InterventionistClaim
                result.append(InterventionistClaim(**item))
            else:
                result.append(item)
        return result


class ConditionalUse(BaseModel):
    """A conditional use of the concept.

    Handles LLM variations where:
    - 'structure' may be used instead of 'conditional'
    - 'evidence' may be used instead of 'quote'
    """
    conditional: str = ""
    quote: str = ""
    source: str = ""

    def __init__(self, **data):
        # Handle field aliases manually
        if 'structure' in data and 'conditional' not in data:
            data['conditional'] = data.pop('structure')
        if 'evidence' in data and 'quote' not in data:
            data['quote'] = data.pop('evidence')
        super().__init__(**data)


class ConditionalWeb(BaseModel):
    """Conditional relationships involving the concept."""
    antecedent_uses: list[ConditionalUse] = Field(default_factory=list)
    consequent_uses: list[ConditionalUse] = Field(default_factory=list)
    biconditionals: list[ConditionalUse] = Field(default_factory=list)
    nested_conditionals: list[ConditionalUse] = Field(default_factory=list)


class ArgumentativeWeight(BaseModel):
    """Weight/importance of arguments."""
    load_bearing: list[str] = Field(default_factory=list)
    supporting: list[str] = Field(default_factory=list)
    defensive: list[str] = Field(default_factory=list)
    illustrative: list[str] = Field(default_factory=list)


class LogicalVulnerability(BaseModel):
    """A logical vulnerability in the argument structure."""
    vulnerability_type: Literal['unstated_premise', 'inferential_gap', 'equivocation', 'question_begging', 'false_dichotomy']
    argument_id: str
    description: str
    potential_challenge: str
    severity: Literal['high', 'medium', 'low']

    @field_validator('vulnerability_type', mode='before')
    @classmethod
    def normalize_vuln_type(cls, v):
        return normalize_vulnerability_type(v)

    @field_validator('severity', mode='before')
    @classmethod
    def normalize_sev(cls, v):
        return normalize_severity(v)


class TextualShift(BaseModel):
    """Shift in argument between texts."""
    argument_id: str
    change_type: Literal['strengthened', 'weakened', 'abandoned', 'introduced']
    nlr_version: str
    response_version: str
    analysis: str

    @field_validator('change_type', mode='before')
    @classmethod
    def normalize_change(cls, v):
        return normalize_change_type(v)


class LogicalSynthesis(BaseModel):
    """Synthesis of logical analysis."""
    argument_density: str | int
    logical_centrality: Literal['core', 'important', 'peripheral']
    causal_weight: Literal['heavy', 'moderate', 'light']
    strongest_arguments: list[str] = Field(default_factory=list)
    weakest_arguments: list[str] = Field(default_factory=list)
    vulnerability_summary: str
    overall_assessment: str

    @field_validator('logical_centrality', mode='before')
    @classmethod
    def normalize_cent(cls, v):
        return normalize_centrality(v)

    @field_validator('causal_weight', mode='before')
    @classmethod
    def normalize_caus_weight(cls, v):
        return normalize_causal_weight(v)


class LogicalAnalysisResult(BaseModel):
    """Complete logical analysis result."""
    concept: str
    analysis_type: Literal['logical'] = 'logical'
    framework: str = "Logical Structure Analysis"
    argument_inventory: list[LogicalArgument] = Field(default_factory=list)
    argument_chains: list[ArgumentChain] = Field(default_factory=list)
    causal_architecture: Optional[CausalArchitecture] = None
    conditional_web: Optional[ConditionalWeb] = None
    argumentative_weight: Optional[ArgumentativeWeight] = None
    logical_vulnerabilities: list[LogicalVulnerability] = Field(default_factory=list)
    textual_shifts: list[TextualShift] = Field(default_factory=list)
    synthesis: Optional[LogicalSynthesis] = None
    thinking_preview: Optional[str] = None
    analyzed_at: str = Field(default_factory=lambda: datetime.now().isoformat())

    class Config:
        json_schema_extra = {
            "example": {
                "concept": "efficiency",
                "argument_inventory": [],
                "logical_vulnerabilities": [
                    {
                        "vulnerability_type": "unstated_premise",
                        "argument_id": "A1",
                        "description": "Example vulnerability",
                        "potential_challenge": "Challenge text",
                        "severity": "high"
                    }
                ]
            }
        }


# =============================================================================
# Inferential Analysis Models (for completeness)
# =============================================================================

class KeyQuote(BaseModel):
    """Key quote with source and analysis."""
    quote: str
    source: str
    analysis: str


class TheDeceptivelySimple(BaseModel):
    """The deceptively simple surface appearance."""
    surface_presentation: str
    hidden_weight: str
    key_quotes: list[KeyQuote] = Field(default_factory=list)


class TextualEvidence(BaseModel):
    """Textual evidence with quote and source."""
    quote: str
    source: str


class CommitmentChain(BaseModel):
    """Chain of commitments."""
    immediate: list[str] = Field(default_factory=list)
    downstream: list[str] = Field(default_factory=list)
    practical: list[str] = Field(default_factory=list)


class CommitmentRelation(BaseModel):
    """Relation between commitments."""
    if_you_endorse: str
    you_are_committed_to: CommitmentChain
    strength: Literal['strict', 'strong', 'defeasible'] = 'strong'
    commonly_recognized: bool = True
    textual_evidence: Optional[TextualEvidence] = None

    @field_validator('strength', mode='before')
    @classmethod
    def normalize_strength(cls, v):
        if v is None:
            return 'strong'
        v_lower = str(v).lower().strip()
        if 'strict' in v_lower:
            return 'strict'
        if 'defeas' in v_lower or 'weak' in v_lower:
            return 'defeasible'
        return 'strong'


class HiddenCommitment(BaseModel):
    """Hidden normative commitment."""
    commitment: str
    why_hidden: str
    textual_evidence: str


class CommitmentCascade(BaseModel):
    """Cascade of commitment relations."""
    commitment_relations: list[CommitmentRelation] = Field(default_factory=list)
    hidden_commitments: list[HiddenCommitment] = Field(default_factory=list)


class IncompatibilityRelation(BaseModel):
    """Incompatibility between positions."""
    concept_a: str
    concept_b: str
    severity: Literal['strict', 'strong', 'weak'] = 'strong'
    why_incompatible: str
    who_is_caught: str = ""
    textual_evidence: str = ""

    @field_validator('severity', mode='before')
    @classmethod
    def normalize_sev(cls, v):
        if v is None:
            return 'strong'
        v_lower = str(v).lower().strip()
        if 'strict' in v_lower:
            return 'strict'
        if 'weak' in v_lower:
            return 'weak'
        return 'strong'


class IncompatibilityMap(BaseModel):
    """Map of incompatibilities."""
    incompatibility_relations: list[IncompatibilityRelation] = Field(default_factory=list)
    unstable_combinations: str = ""


class UnresolvedTension(BaseModel):
    """An unresolved tension in the concept."""
    conflicting_commitments: list[str] = Field(default_factory=list)
    source_of_tension: str
    stability: Literal['unstable', 'precarious', 'unresolved'] = 'unresolved'
    textual_evidence: list[TextualEvidence] = Field(default_factory=list)
    why_it_resists_resolution: str

    @field_validator('stability', mode='before')
    @classmethod
    def normalize_stability(cls, v):
        if v is None:
            return 'unresolved'
        v_lower = str(v).lower().strip()
        if 'unstable' in v_lower:
            return 'unstable'
        if 'precarious' in v_lower:
            return 'precarious'
        return 'unresolved'


class Tensions(BaseModel):
    """Tensions in the concept."""
    unresolved_tensions: list[UnresolvedTension] = Field(default_factory=list)
    intellectual_fault_lines: str = ""


class PracticalStakes(BaseModel):
    """Practical stakes of the concept."""
    obligations: list[str] = Field(default_factory=list)
    prohibitions: list[str] = Field(default_factory=list)
    affected_decisions: list[str] = Field(default_factory=list)
    normative_entanglements: str = ""


class CommitmentPackage(BaseModel):
    """Package of commitments."""
    package_name: str
    core_commitments: list[str] = Field(default_factory=list)
    incompatible_packages: list[str] = Field(default_factory=list)
    who_endorses: str = ""


class InferentialSynthesis(BaseModel):
    """Synthesis of inferential analysis."""
    inferential_definition: str
    centrality_score: float = 0.0
    stability_score: float = 0.0
    most_consequential_commitment: str
    key_revelation: str


class InferentialAnalysisResult(BaseModel):
    """Complete inferential analysis result."""
    concept: str
    analysis_type: Literal['inferential'] = 'inferential'
    framework: str = "Brandomian Inferential Role Analysis"
    the_deceptively_simple: Optional[TheDeceptivelySimple] = None
    commitment_cascade: Optional[CommitmentCascade] = None
    incompatibility_map: Optional[IncompatibilityMap] = None
    tensions: Optional[Tensions] = None
    practical_stakes: Optional[PracticalStakes] = None
    commitment_packages: list[CommitmentPackage] = Field(default_factory=list)
    synthesis: Optional[InferentialSynthesis] = None
    thinking_preview: Optional[str] = None
    analyzed_at: str = Field(default_factory=lambda: datetime.now().isoformat())
