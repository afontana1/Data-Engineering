# Structured Context Processing
## Graph and Relational Data Integration for Context Engineering

> **Module 02.4** | *Context Engineering Course: From Foundations to Frontier Systems*
> 
> Building on [Context Engineering Survey](https://arxiv.org/pdf/2507.13334) | Advancing Knowledge Graph-Enhanced Context Systems

---

## Learning Objectives

By the end of this module, you will understand and implement:

- **Graph-Based Context Representation**: Modeling complex relationships as connected knowledge structures
- **Relational Reasoning Systems**: Understanding how entities and relationships create meaning
- **Knowledge Graph Integration**: Incorporating structured knowledge into context assembly
- **Hierarchical Information Organization**: Managing nested and recursive data structures for optimal context

---

## Conceptual Progression: From Linear Text to Network Intelligence

Think of structured context processing like the difference between reading a dictionary (linear, alphabetical) versus understanding a living ecosystem (networked, relational, interdependent).

### Stage 1: Linear Information Processing
```
Text: "Alice works at Google. Google is a tech company. Tech companies develop software."

Processing: Alice → works_at → Google → is_a → tech_company → develops → software

Understanding: Sequential, limited connections
```
**Context**: Like reading facts one by one from a textbook. You get information, but miss the rich web of relationships that create deeper understanding.

**Limitations**:
- Information processed in isolation
- Relationships not explicitly modeled
- Difficult to reason about connections
- No hierarchical organization

### Stage 2: Simple Entity-Relationship Recognition
```
Entities: [Alice, Google, tech_company, software]
Relationships: [works_at(Alice, Google), is_a(Google, tech_company), develops(tech_company, software)]

Basic Graph:
Alice --works_at--> Google --is_a--> tech_company --develops--> software
```
**Context**: Like creating a simple org chart or family tree. You can see direct connections, but complex patterns remain hidden.

**Improvements**:
- Entities and relationships explicitly identified
- Basic graph structure emerges
- Can answer simple relational queries

**Remaining Issues**:
- Flat relationship structure
- No inference or reasoning
- Limited context propagation

### Stage 3: Knowledge Graph Integration
```
Rich Knowledge Graph:

    Alice (Person)
      ├─ works_at → Google (Company)
      ├─ skills → [Programming, AI]
      └─ location → Mountain_View

    Google (Company)  
      ├─ is_a → Tech_Company
      ├─ founded → 1998
      ├─ headquarters → Mountain_View  
      ├─ develops → [Search, Android, AI]
      ├─ employees → 150000
      └─ competes_with → [Apple, Microsoft]

    Tech_Company (Category)
      ├─ characteristics → [Innovation, Software, Digital]
      └─ examples → [Google, Apple, Microsoft]
```
**Context**: Like having access to Wikipedia's entire knowledge network. Rich, interconnected information that supports complex reasoning and inference.

**Capabilities**:
- Multi-hop reasoning across relationships
- Hierarchical categorization and inheritance
- Context enrichment through graph traversal
- Support for complex queries and inference

### Stage 4: Dynamic Hierarchical Context Networks
```
┌─────────────────────────────────────────────────────────────────┐
│                HIERARCHICAL CONTEXT NETWORK                     │
│                                                                 │
│  Domain Level: Technology Industry                              │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                                                         │   │
│  │  Company Level: Google                                  │   │
│  │  ├─ Business Model: Advertising, Cloud, Hardware       │   │
│  │  ├─ Core Technologies: AI, Search, Mobile              │   │
│  │  └─ Market Position: Leader in Search, Growing in AI   │   │
│  │                                                         │   │
│  │    Individual Level: Alice                              │   │
│  │    ├─ Role Context: AI Researcher                      │   │
│  │    ├─ Skill Context: Machine Learning, Python          │   │
│  │    └─ Project Context: Large Language Models           │   │
│  │                                                         │   │
│  │      Task Level: Current Assignment                     │   │
│  │      ├─ Objective: Improve Model Safety               │   │
│  │      ├─ Methods: Constitutional AI, RLHF               │   │
│  │      └─ Timeline: Q3-Q4 2024                          │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  Cross-Level Connections:                                       │
│  • Industry trends influence company strategy                   │
│  • Company resources enable individual projects               │  
│  • Individual expertise shapes project approaches             │
│  • Project outcomes affect company positioning                │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```
**Context**: Like having a master strategist who understands how individual actions connect to team dynamics, organizational goals, and industry trends simultaneously.

### Stage 5: Adaptive Graph Intelligence with Emergent Structure Discovery
```
┌─────────────────────────────────────────────────────────────────┐
│              ADAPTIVE GRAPH INTELLIGENCE SYSTEM                 │
│                                                                 │
│  Self-Organizing Knowledge Networks:                            │
│                                                                 │
│  🔍 Pattern Recognition Engine:                                │
│    • Discovers implicit relationships in data                  │
│    • Identifies recurring structural patterns                  │
│    • Learns optimal graph organization strategies             │
│                                                                 │
│  🧠 Emergent Structure Formation:                              │
│    • Creates new relationship types not in original data      │
│    • Forms meta-relationships between relationship patterns    │
│    • Develops hierarchical abstractions automatically         │
│                                                                 │
│  🌐 Dynamic Context Adaptation:                               │
│    • Restructures graphs based on query patterns             │
│    • Optimizes information paths for different reasoning types │
│    • Evolves representation based on usage and feedback       │
│                                                                 │
│  ⚡ Real-time Inference and Reasoning:                        │
│    • Multi-hop reasoning across complex relationship chains   │
│    • Analogical reasoning between similar graph patterns      │
│    • Causal inference from structural relationships           │
│    • Temporal reasoning about relationship evolution          │
│                                                                 │
│  🔄 Self-Improvement Mechanisms:                              │
│    • Learns better graph construction strategies             │
│    • Improves relationship extraction and classification     │
│    • Enhances reasoning algorithms based on outcomes         │
│    • Optimizes structure for computational efficiency        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```
**Context**: Like having an AI scientist who not only understands existing knowledge networks but discovers new patterns, creates novel organizational structures, and continuously improves its own understanding and reasoning capabilities.

---

## Mathematical Foundations

### Graph-Based Context Representation
```
Knowledge Graph: G = (E, R, T)
Where:
- E = set of entities {e₁, e₂, ..., eₙ}
- R = set of relation types {r₁, r₂, ..., rₖ}  
- T = set of triples {(eᵢ, rⱼ, eₖ)} representing facts

Context Assembly from Graph:
C(q, G) = TraversePath(q, G, depth=d, strategy=s)

Where:
- q = query or information need
- G = knowledge graph
- d = maximum traversal depth
- s = traversal strategy (BFS, DFS, relevance-guided)
```
**Intuitive Explanation**: A knowledge graph is like a map of information where entities are locations and relationships are paths between them. Context assembly becomes a navigation problem - finding the most relevant paths from query to answer through the knowledge network.

### Mathematical Foundations 

### Hierarchical Information Encoding
```
Hierarchical Context Tree: H = (N, P, C)
Where:
- N = set of nodes representing information units
- P = parent-child relationships (taxonomic structure)
- C = cross-links (associative relationships)

Information Propagation:
I(n) = Local(n) + α·∑ᵢ Parent(i)·w(i→n) + β·∑ⱼ Child(j)·w(n→j) + γ·∑ₖ CrossLink(k)·w(n↔k)

Where:
- Local(n) = information directly at node n
- α, β, γ = propagation weights for different relationship types
- w(·) = relationship strength weights
```
**Intuitive Explanation**: Information in hierarchies doesn't just exist at individual nodes - it flows between levels. A concept inherits meaning from its parents (categories it belongs to), children (specific instances), and cross-links (related concepts). Like how your understanding of "dog" is informed by "animal" (parent), "golden retriever" (child), and "companion" (cross-link).

### Relational Reasoning Optimization
```
Multi-Hop Path Reasoning:
P(answer | query, graph) = ∑ paths π P(answer | π) · P(π | query, graph)

Where a path π = (e₀, r₁, e₁, r₂, e₂, ..., rₙ, eₙ)

Path Probability:
P(π | query, graph) = ∏ᵢ P(rᵢ₊₁ | eᵢ, query) · P(eᵢ₊₁ | eᵢ, rᵢ₊₁, query)

Optimized Traversal:
π* = argmax_π P(π | query, graph) subject to |π| ≤ max_hops
```
**Intuitive Explanation**: When reasoning through a knowledge graph, there are many possible paths from question to answer. We want to find the most probable path that connects the query to relevant information, considering both the likelihood of each relationship and the overall path coherence.

---

## Software 3.0 Paradigm 1: Prompts (Structured Reasoning Templates)

### Knowledge Graph Reasoning Template

```markdown
# Knowledge Graph Reasoning Framework

## Graph Context Analysis
You are reasoning through structured information represented as a knowledge graph. Use systematic traversal and relationship analysis to build comprehensive understanding.

## Graph Structure Assessment
**Available Entities**: {entities_in_current_graph}
**Relationship Types**: {relation_types_and_their_meanings}
**Graph Depth**: {maximum_relationship_chain_length}
**Query Context**: {specific_question_or_reasoning_goal}

### Entity Analysis
For each relevant entity in the reasoning path:

**Entity**: {entity_name}
- **Type/Category**: {entity_classification}
- **Direct Properties**: {attributes_directly_associated_with_entity}
- **Outgoing Relationships**: {relationships_where_entity_is_subject}
- **Incoming Relationships**: {relationships_where_entity_is_object}
- **Hierarchical Context**: {parent_and_child_entities_in_taxonomy}

### Relationship Chain Construction

#### Single-Hop Reasoning
**Direct Connections**: {entity1} --{relationship}--> {entity2}
- **Relationship Strength**: {confidence_or_weight_of_relationship}
- **Context Relevance**: {how_relevant_to_current_query}
- **Information Content**: {what_this_relationship_tells_us}

#### Multi-Hop Reasoning Paths
**Path 1**: {entity1} --{rel1}--> {entity2} --{rel2}--> {entity3} --{rel3}--> {target}
- **Path Coherence**: {how_logically_consistent_is_this_chain}
- **Cumulative Evidence**: {strength_of_evidence_along_path}
- **Alternative Interpretations**: {other_ways_to_understand_this_path}

**Path 2**: {alternative_reasoning_path}
**Path 3**: {additional_reasoning_path_if_relevant}

### Reasoning Strategy Selection

#### Bottom-Up Reasoning (From Specific to General)
```
IF query_requires_generalization:
    START WITH specific_instances
    IDENTIFY common_patterns_and_properties
    TRAVERSE upward_through_hierarchical_relationships
    SYNTHESIZE general_principles_or_categories
```

#### Top-Down Reasoning (From General to Specific)
```
IF query_requires_specific_information:
    START WITH general_categories_or_principles
    TRAVERSE downward_through_specialization_relationships
    IDENTIFY relevant_specific_instances
    EXTRACT detailed_information_about_instances
```

#### Lateral Reasoning (Across Same Level)
```
IF query_requires_comparison_or_analogy:
    IDENTIFY entities_at_similar_hierarchical_levels
    TRAVERSE cross_links_and_associative_relationships
    COMPARE properties_and_relationship_patterns
    IDENTIFY similarities_and_differences
```

### Hierarchical Context Integration

#### Local Context (Immediate Neighborhood)
- **Direct Properties**: {properties_of_focus_entity}
- **Immediate Relations**: {one_hop_relationships}
- **Local Constraints**: {rules_or_constraints_in_immediate_context}

#### Intermediate Context (2-3 Hops)
- **Extended Relationships**: {multi_hop_connections}
- **Pattern Recognition**: {recurring_structures_in_extended_neighborhood}
- **Contextual Modifiers**: {how_intermediate_context_affects_interpretation}

#### Global Context (Full Graph Perspective)
- **Domain-Level Patterns**: {large_scale_structures_and_patterns}
- **Cross-Domain Connections**: {relationships_spanning_different_knowledge_areas}
- **System-Level Constraints**: {global_rules_or_principles}

### Inference and Reasoning Execution

#### Deductive Reasoning
**Given Facts**: {explicit_relationships_and_properties_in_graph}
**Logical Rules**: {if_then_rules_that_can_be_applied}
**Conclusions**: {what_can_be_logically_derived}

Example:
```
IF Alice works_at Google AND Google is_a Tech_Company
THEN Alice works_at a Tech_Company (transitivity of employment and classification)
```

#### Inductive Reasoning
**Observed Patterns**: {recurring_structures_or_relationships_in_graph}
**Generalized Rules**: {patterns_that_might_apply_more_broadly}
**Confidence Levels**: {how_certain_are_we_about_these_generalizations}

#### Abductive Reasoning (Best Explanation)
**Observed Evidence**: {facts_that_need_explanation}
**Candidate Explanations**: {possible_reasons_for_observed_evidence}
**Best Explanation**: {most_likely_explanation_given_graph_structure}

### Context Assembly Strategy

#### Query-Driven Assembly
1. **Parse Query**: Identify key entities and relationships mentioned
2. **Seed Selection**: Choose starting points in the graph
3. **Expansion Strategy**: Decide how to grow context from seeds
4. **Relevance Filtering**: Keep most relevant information, prune irrelevant
5. **Coherence Verification**: Ensure assembled context forms coherent narrative

#### Structure-Driven Assembly
1. **Identify Key Structures**: Find important subgraphs or patterns
2. **Extract Hierarchies**: Build taxonomic and part-whole relationships
3. **Map Cross-Links**: Include important associative relationships
4. **Context Layering**: Organize information by levels of abstraction
5. **Integration Synthesis**: Combine different structural views

### Quality Assessment

#### Completeness Check
- **Required Information Coverage**: {percentage_of_necessary_information_included}
- **Key Relationship Coverage**: {important_relationships_represented}
- **Hierarchical Completeness**: {coverage_across_different_abstraction_levels}

#### Coherence Verification
- **Logical Consistency**: {absence_of_contradictions_in_assembled_context}
- **Relationship Validity**: {all_relationships_are_meaningful_and_correct}
- **Narrative Flow**: {information_flows_logically_from_premise_to_conclusion}

#### Relevance Optimization
- **Query Alignment**: {how_well_context_addresses_original_query}
- **Information Density**: {ratio_of_useful_to_total_information}
- **Focus Appropriateness**: {correct_level_of_detail_for_query_type}

## Structured Context Output

**Primary Reasoning Path**: {most_confident_reasoning_chain}
**Supporting Evidence**: {additional_relationships_that_support_conclusion}
**Alternative Interpretations**: {other_possible_ways_to_understand_the_information}
**Uncertainty Factors**: {areas_where_reasoning_confidence_is_lower}

**Hierarchical Summary**:
- **High-Level Concepts**: {general_categories_and_principles}
- **Mid-Level Relationships**: {specific_connections_and_patterns}
- **Detailed Facts**: {specific_properties_and_instances}

**Cross-References**: {related_information_that_provides_additional_context}
```

**Ground-up Explanation**: This template works like a detective investigating a case through a network of interconnected clues. The detective doesn't just look at individual pieces of evidence but maps out how they connect, builds reasoning chains from clue to clue, and considers multiple possible explanations before reaching conclusions.

---

## Software 3.0 Paradigm 2: Programming (Structured Context Implementation)

### Knowledge Graph Context Engine

```python
import numpy as np
from typing import Dict, List, Tuple, Set, Optional, Any
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from collections import defaultdict, deque
import networkx as nx
from enum import Enum
import json

class RelationType(Enum):
    """Types of relationships in knowledge graph"""
    IS_A = "is_a"
    PART_OF = "part_of"
    RELATED_TO = "related_to"
    INSTANCE_OF = "instance_of"
    HAS_PROPERTY = "has_property"
    WORKS_AT = "works_at"
    LOCATED_IN = "located_in"
    CAUSES = "causes"
    ENABLES = "enables"
    SIMILAR_TO = "similar_to"

@dataclass
class Entity:
    """Knowledge graph entity with properties"""
    id: str
    name: str
    entity_type: str
    properties: Dict[str, Any] = field(default_factory=dict)
    embeddings: Optional[np.ndarray] = None
    confidence: float = 1.0

@dataclass
class Relationship:
    """Knowledge graph relationship"""
    subject: str
    predicate: RelationType
    object: str
    weight: float = 1.0
    confidence: float = 1.0
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ReasoningPath:
    """Path through knowledge graph for reasoning"""
    entities: List[str]
    relationships: List[Relationship]
    path_score: float
    reasoning_type: str
    evidence_strength: float

class KnowledgeGraph:
    """Core knowledge graph representation and operations"""
    
    def __init__(self):
        self.entities: Dict[str, Entity] = {}
        self.relationships: List[Relationship] = []
        self.graph = nx.MultiDiGraph()
        self.entity_types: Dict[str, Set[str]] = defaultdict(set)
        self.relation_index: Dict[RelationType, List[Relationship]] = defaultdict(list)
        
    def add_entity(self, entity: Entity):
        """Add entity to knowledge graph"""
        self.entities[entity.id] = entity
        self.graph.add_node(entity.id, **entity.properties)
        self.entity_types[entity.entity_type].add(entity.id)
        
    def add_relationship(self, relationship: Relationship):
        """Add relationship to knowledge graph"""
        self.relationships.append(relationship)
        self.graph.add_edge(
            relationship.subject, 
            relationship.object,
            predicate=relationship.predicate,
            weight=relationship.weight,
            confidence=relationship.confidence
        )
        self.relation_index[relationship.predicate].append(relationship)
    
    def get_neighbors(self, entity_id: str, relation_type: Optional[RelationType] = None,
                     direction: str = "outgoing") -> List[Tuple[str, Relationship]]:
        """Get neighboring entities connected by specific relationship type"""
        neighbors = []
        
        if direction in ["outgoing", "both"]:
            for target in self.graph.successors(entity_id):
                edges = self.graph[entity_id][target]
                for edge_data in edges.values():
                    if relation_type is None or edge_data['predicate'] == relation_type:
                        rel = Relationship(
                            subject=entity_id,
                            predicate=edge_data['predicate'],
                            object=target,
                            weight=edge_data['weight'],
                            confidence=edge_data['confidence']
                        )
                        neighbors.append((target, rel))
        
        if direction in ["incoming", "both"]:
            for source in self.graph.predecessors(entity_id):
                edges = self.graph[source][entity_id]
                for edge_data in edges.values():
                    if relation_type is None or edge_data['predicate'] == relation_type:
                        rel = Relationship(
                            subject=source,
                            predicate=edge_data['predicate'],
                            object=entity_id,
                            weight=edge_data['weight'],
                            confidence=edge_data['confidence']
                        )
                        neighbors.append((source, rel))
        
        return neighbors
    
    def find_paths(self, start_entity: str, end_entity: str, 
                   max_depth: int = 3) -> List[ReasoningPath]:
        """Find reasoning paths between two entities"""
        paths = []
        
        try:
            # Find all simple paths up to max_depth
            nx_paths = nx.all_simple_paths(self.graph, start_entity, end_entity, cutoff=max_depth)
            
            for path in nx_paths:
                reasoning_path = self._convert_to_reasoning_path(path)
                if reasoning_path:
                    paths.append(reasoning_path)
                    
        except nx.NetworkXNoPath:
            pass  # No path exists
        
        # Sort by path score
        paths.sort(key=lambda p: p.path_score, reverse=True)
        return paths[:10]  # Return top 10 paths
    
    def _convert_to_reasoning_path(self, node_path: List[str]) -> Optional[ReasoningPath]:
        """Convert networkx path to reasoning path"""
        if len(node_path) < 2:
            return None
            
        relationships = []
        path_score = 1.0
        
        for i in range(len(node_path) - 1):
            source, target = node_path[i], node_path[i + 1]
            
            # Find the relationship between these nodes
            edges = self.graph[source][target]
            if not edges:
                return None
            
            # Take the edge with highest confidence
            best_edge = max(edges.values(), key=lambda e: e['confidence'])
            
            rel = Relationship(
                subject=source,
                predicate=best_edge['predicate'],
                object=target,
                weight=best_edge['weight'],
                confidence=best_edge['confidence']
            )
            relationships.append(rel)
            
            # Update path score based on relationship confidence
            path_score *= rel.confidence
        
        return ReasoningPath(
            entities=node_path,
            relationships=relationships,
            path_score=path_score,
            reasoning_type="multi_hop",
            evidence_strength=path_score
        )
    
    def get_entity_context(self, entity_id: str, depth: int = 2) -> Dict[str, Any]:
        """Get rich context for an entity including neighbors at specified depth"""
        if entity_id not in self.entities:
            return {}
        
        context = {
            'entity': self.entities[entity_id],
            'immediate_neighbors': {},
            'extended_context': {},
            'hierarchical_context': {}
        }
        
        # Get immediate neighbors (depth 1)
        immediate = self.get_neighbors(entity_id, direction="both")
        context['immediate_neighbors'] = {
            'outgoing': [(target, rel) for target, rel in immediate if rel.subject == entity_id],
            'incoming': [(source, rel) for source, rel in immediate if rel.object == entity_id]
        }
        
        # Get extended context (depth 2+)
        if depth > 1:
            extended_entities = set()
            queue = deque([(entity_id, 0)])
            visited = {entity_id}
            
            while queue:
                current_entity, current_depth = queue.popleft()
                
                if current_depth >= depth:
                    continue
                    
                neighbors = self.get_neighbors(current_entity, direction="both")
                for neighbor_id, rel in neighbors:
                    if neighbor_id not in visited:
                        extended_entities.add(neighbor_id)
                        visited.add(neighbor_id)
                        queue.append((neighbor_id, current_depth + 1))
            
            context['extended_context'] = {
                eid: self.entities[eid] for eid in extended_entities if eid in self.entities
            }
        
        # Get hierarchical context (is_a relationships)
        hierarchical = self._get_hierarchical_context(entity_id)
        context['hierarchical_context'] = hierarchical
        
        return context
    
    def _get_hierarchical_context(self, entity_id: str) -> Dict[str, List[str]]:
        """Get hierarchical context (parents and children in taxonomy)"""
        parents = []
        children = []
        
        # Find parents (things this entity is_a instance of)
        parent_rels = self.get_neighbors(entity_id, RelationType.IS_A, "outgoing")
        parents.extend([target for target, _ in parent_rels])
        
        instance_rels = self.get_neighbors(entity_id, RelationType.INSTANCE_OF, "outgoing")
        parents.extend([target for target, _ in instance_rels])
        
        # Find children (things that are instances of this entity)
        child_rels = self.get_neighbors(entity_id, RelationType.IS_A, "incoming")
        children.extend([source for source, _ in child_rels])
        
        instance_child_rels = self.get_neighbors(entity_id, RelationType.INSTANCE_OF, "incoming")
        children.extend([source for source, _ in instance_child_rels])
        
        return {
            'parents': parents,
            'children': children
        }

class StructuredContextAssembler:
    """Assembles context from structured knowledge representations"""
    
    def __init__(self, knowledge_graph: KnowledgeGraph):
        self.kg = knowledge_graph
        self.reasoning_strategies = {
            'deductive': self._deductive_reasoning,
            'inductive': self._inductive_reasoning,
            'abductive': self._abductive_reasoning,
            'analogical': self._analogical_reasoning
        }
        
    def assemble_context(self, query: str, entities: List[str], 
                        max_context_size: int = 2000,
                        reasoning_strategy: str = "deductive") -> Dict[str, Any]:
        """Main context assembly process"""
        
        print(f"Assembling structured context for query: {query}")
        print(f"Starting entities: {entities}")
        
        # Extract key information from query
        query_analysis = self._analyze_query(query)
        
        # Collect relevant subgraphs around seed entities
        relevant_subgraphs = []
        for entity_id in entities:
            if entity_id in self.kg.entities:
                subgraph = self._extract_relevant_subgraph(entity_id, query_analysis, depth=3)
                relevant_subgraphs.append(subgraph)
        
        # Apply reasoning strategy
        reasoning_results = self.reasoning_strategies[reasoning_strategy](
            query_analysis, relevant_subgraphs
        )
        
        # Assemble final context
        assembled_context = self._integrate_reasoning_results(
            query, query_analysis, reasoning_results, max_context_size
        )
        
        return assembled_context
    
    def _analyze_query(self, query: str) -> Dict[str, Any]:
        """Analyze query to understand information needs"""
        query_lower = query.lower()
        
        analysis = {
            'query_text': query,
            'query_type': 'factual',  # Default
            'entities_mentioned': [],
            'relationships_implied': [],
            'reasoning_depth': 'shallow',
            'answer_type': 'descriptive'
        }
        
        # Determine query type
        if any(word in query_lower for word in ['why', 'because', 'cause', 'reason']):
            analysis['query_type'] = 'causal'
            analysis['reasoning_depth'] = 'deep'
        elif any(word in query_lower for word in ['how', 'process', 'method', 'way']):
            analysis['query_type'] = 'procedural'
        elif any(word in query_lower for word in ['compare', 'difference', 'similar', 'versus']):
            analysis['query_type'] = 'comparative'
            analysis['reasoning_depth'] = 'medium'
        elif any(word in query_lower for word in ['what is', 'define', 'definition']):
            analysis['query_type'] = 'definitional'
        
        # Extract mentioned entities (simplified)
        for entity_id, entity in self.kg.entities.items():
            if entity.name.lower() in query_lower:
                analysis['entities_mentioned'].append(entity_id)
        
        # Infer required relationships
        if analysis['query_type'] == 'causal':
            analysis['relationships_implied'].append(RelationType.CAUSES)
        elif analysis['query_type'] == 'comparative':
            analysis['relationships_implied'].append(RelationType.SIMILAR_TO)
        
        return analysis
    
    def _extract_relevant_subgraph(self, start_entity: str, query_analysis: Dict,
                                 depth: int = 3) -> Dict[str, Any]:
        """Extract relevant subgraph around an entity"""
        
        # Start with entity context
        entity_context = self.kg.get_entity_context(start_entity, depth=depth)
        
        # Score relevance of different parts
        relevance_scores = self._score_context_relevance(entity_context, query_analysis)
        
        # Filter based on relevance
        filtered_context = self._filter_by_relevance(entity_context, relevance_scores, threshold=0.3)
        
        return {
            'root_entity': start_entity,
            'context': filtered_context,
            'relevance_scores': relevance_scores,
            'subgraph_summary': self._summarize_subgraph(filtered_context)
        }
    
    def _score_context_relevance(self, context: Dict, query_analysis: Dict) -> Dict[str, float]:
        """Score relevance of different context elements to query"""
        scores = {}
        
        # Score immediate neighbors
        for direction in ['outgoing', 'incoming']:
            for target_id, rel in context['immediate_neighbors'][direction]:
                score = 0.5  # Base score
                
                # Boost score if relationship type is implied by query
                if rel.predicate in query_analysis['relationships_implied']:
                    score += 0.3
                
                # Boost score if target entity is mentioned in query
                if target_id in query_analysis['entities_mentioned']:
                    score += 0.4
                
                scores[f"{direction}_{target_id}"] = score
        
        # Score extended context entities
        for entity_id, entity in context['extended_context'].items():
            score = 0.3  # Lower base score for extended context
            
            if entity_id in query_analysis['entities_mentioned']:
                score += 0.4
            
            # Boost based on entity type relevance
            if entity.entity_type in query_analysis.get('relevant_types', []):
                score += 0.2
            
            scores[f"extended_{entity_id}"] = score
        
        # Score hierarchical context
        for parent_id in context['hierarchical_context']['parents']:
            scores[f"parent_{parent_id}"] = 0.4
        
        for child_id in context['hierarchical_context']['children']:
            scores[f"child_{child_id}"] = 0.3
        
        return scores
    
    def _filter_by_relevance(self, context: Dict, relevance_scores: Dict, 
                           threshold: float) -> Dict[str, Any]:
        """Filter context based on relevance scores"""
        filtered = {
            'entity': context['entity'],
            'immediate_neighbors': {'outgoing': [], 'incoming': []},
            'extended_context': {},
            'hierarchical_context': {'parents': [], 'children': []}
        }
        
        # Filter immediate neighbors
        for direction in ['outgoing', 'incoming']:
            for target_id, rel in context['immediate_neighbors'][direction]:
                score_key = f"{direction}_{target_id}"
                if relevance_scores.get(score_key, 0) >= threshold:
                    filtered['immediate_neighbors'][direction].append((target_id, rel))
        
        # Filter extended context
        for entity_id, entity in context['extended_context'].items():
            score_key = f"extended_{entity_id}"
            if relevance_scores.get(score_key, 0) >= threshold:
                filtered['extended_context'][entity_id] = entity
        
        # Filter hierarchical context
        for parent_id in context['hierarchical_context']['parents']:
            if relevance_scores.get(f"parent_{parent_id}", 0) >= threshold:
                filtered['hierarchical_context']['parents'].append(parent_id)
        
        for child_id in context['hierarchical_context']['children']:
            if relevance_scores.get(f"child_{child_id}", 0) >= threshold:
                filtered['hierarchical_context']['children'].append(child_id)
        
        return filtered
    
    def _summarize_subgraph(self, context: Dict) -> str:
        """Create summary of subgraph structure"""
        entity = context['entity']
        
        summary_parts = [f"Entity: {entity.name} ({entity.entity_type})"]
        
        # Count connections
        outgoing_count = len(context['immediate_neighbors']['outgoing'])
        incoming_count = len(context['immediate_neighbors']['incoming'])
        extended_count = len(context['extended_context'])
        
        summary_parts.append(f"Direct connections: {outgoing_count + incoming_count}")
        summary_parts.append(f"Extended network: {extended_count} entities")
        
        # Hierarchical position
        parent_count = len(context['hierarchical_context']['parents'])
        child_count = len(context['hierarchical_context']['children'])
        
        if parent_count > 0 or child_count > 0:
            summary_parts.append(f"Hierarchical: {parent_count} parents, {child_count} children")
        
        return "; ".join(summary_parts)
    
    def _deductive_reasoning(self, query_analysis: Dict, subgraphs: List[Dict]) -> Dict[str, Any]:
        """Apply deductive reasoning to extract logical conclusions"""
        
        reasoning_chains = []
        
        for subgraph in subgraphs:
            context = subgraph['context']
            root_entity = subgraph['root_entity']
            
            # Find logical inference chains
            chains = self._find_inference_chains(context, query_analysis)
            reasoning_chains.extend(chains)
        
        # Rank reasoning chains by strength
        reasoning_chains.sort(key=lambda c: c['confidence'], reverse=True)
        
        return {
            'reasoning_type': 'deductive',
            'chains': reasoning_chains[:5],  # Top 5 chains
            'conclusions': [chain['conclusion'] for chain in reasoning_chains[:3]],
            'confidence': np.mean([chain['confidence'] for chain in reasoning_chains[:3]]) if reasoning_chains else 0
        }
    
    def _find_inference_chains(self, context: Dict, query_analysis: Dict) -> List[Dict]:
        """Find logical inference chains in context"""
        chains = []
        
        # Simple transitivity chains
        entity = context['entity']
        
        # For each outgoing relationship, see if we can chain it
        for target_id, rel1 in context['immediate_neighbors']['outgoing']:
            if target_id in context['extended_context']:
                # Look for relationships from this target
                target_context = self.kg.get_entity_context(target_id, depth=1)
                
                for final_target, rel2 in target_context['immediate_neighbors']['outgoing']:
                    # Check if this creates a meaningful chain
                    if self._is_valid_inference_chain(rel1, rel2):
                        chains.append({
                            'premises': [f"{entity.name} {rel1.predicate.value} {target_id}",
                                       f"{target_id} {rel2.predicate.value} {final_target}"],
                            'conclusion': f"{entity.name} (transitively) {rel2.predicate.value} {final_target}",
                            'confidence': rel1.confidence * rel2.confidence,
                            'chain_length': 2
                        })
        
        return chains
    
    def _is_valid_inference_chain(self, rel1: Relationship, rel2: Relationship) -> bool:
        """Check if two relationships can form valid inference chain"""
        # Valid transitivity patterns
        valid_patterns = [
            (RelationType.IS_A, RelationType.IS_A),
            (RelationType.PART_OF, RelationType.PART_OF),
            (RelationType.LOCATED_IN, RelationType.LOCATED_IN),
            (RelationType.WORKS_AT, RelationType.LOCATED_IN)
        ]
        
        return (rel1.predicate, rel2.predicate) in valid_patterns
    
    def _inductive_reasoning(self, query_analysis: Dict, subgraphs: List[Dict]) -> Dict[str, Any]:
        """Apply inductive reasoning to identify patterns"""
        
        patterns = []
        
        # Look for recurring relationship patterns across subgraphs
        for subgraph in subgraphs:
            context = subgraph['context']
            local_patterns = self._identify_local_patterns(context)
            patterns.extend(local_patterns)
        
        # Generalize patterns
        generalized_patterns = self._generalize_patterns(patterns)
        
        return {
            'reasoning_type': 'inductive',
            'patterns': generalized_patterns,
            'generalizations': [p['generalization'] for p in generalized_patterns],
            'confidence': np.mean([p['support'] for p in generalized_patterns]) if generalized_patterns else 0
        }
    
    def _identify_local_patterns(self, context: Dict) -> List[Dict]:
        """Identify patterns in local context"""
        patterns = []
        
        # Pattern: entities of same type often have similar relationships
        entity_type = context['entity'].entity_type
        
        for target_id, rel in context['immediate_neighbors']['outgoing']:
            if target_id in context['extended_context']:
                target_entity = context['extended_context'][target_id]
                patterns.append({
                    'pattern_type': 'entity_type_relationship',
                    'entity_type': entity_type,
                    'relationship': rel.predicate,
                    'target_type': target_entity.entity_type,
                    'instance': f"{entity_type} entities often have {rel.predicate.value} relationships with {target_entity.entity_type} entities"
                })
        
        return patterns
    
    def _generalize_patterns(self, patterns: List[Dict]) -> List[Dict]:
        """Generalize patterns across multiple instances"""
        pattern_counts = defaultdict(list)
        
        # Group similar patterns
        for pattern in patterns:
            if pattern['pattern_type'] == 'entity_type_relationship':
                key = (pattern['entity_type'], pattern['relationship'], pattern['target_type'])
                pattern_counts[key].append(pattern)
        
        # Create generalizations
        generalizations = []
        for key, instances in pattern_counts.items():
            if len(instances) >= 2:  # Need at least 2 instances to generalize
                entity_type, relationship, target_type = key
                generalizations.append({
                    'generalization': f"{entity_type} entities typically have {relationship.value} relationships with {target_type} entities",
                    'support': len(instances) / len(patterns),
                    'instances': len(instances),
                    'confidence': min(1.0, len(instances) / 5)  # More instances = higher confidence
                })
        
        return generalizations
    
    def _abductive_reasoning(self, query_analysis: Dict, subgraphs: List[Dict]) -> Dict[str, Any]:
        """Apply abductive reasoning to find best explanations"""
        
        # Look for phenomena that need explanation
        phenomena = self._identify_phenomena(query_analysis, subgraphs)
        
        # Generate candidate explanations
        explanations = []
        for phenomenon in phenomena:
            candidates = self._generate_explanations(phenomenon, subgraphs)
            explanations.extend(candidates)
        
        # Rank explanations by plausibility
        explanations.sort(key=lambda e: e['plausibility'], reverse=True)
        
        return {
            'reasoning_type': 'abductive',
            'phenomena': phenomena,
            'explanations': explanations[:3],  # Top 3 explanations
            'best_explanation': explanations[0] if explanations else None,
            'confidence': explanations[0]['plausibility'] if explanations else 0
        }
    
    def _identify_phenomena(self, query_analysis: Dict, subgraphs: List[Dict]) -> List[Dict]:
        """Identify phenomena that need explanation"""
        phenomena = []
        
        # Look for unusual patterns or relationships
        for subgraph in subgraphs:
            context = subgraph['context']
            
            # Phenomenon: entity has unusually many relationships of one type
            outgoing_rels = context['immediate_neighbors']['outgoing']
            rel_counts = defaultdict(int)
            for _, rel in outgoing_rels:
                rel_counts[rel.predicate] += 1
            
            for rel_type, count in rel_counts.items():
                if count > 3:  # Arbitrary threshold
                    phenomena.append({
                        'type': 'high_relationship_count',
                        'entity': context['entity'].name,
                        'relationship_type': rel_type,
                        'count': count,
                        'description': f"{context['entity'].name} has {count} {rel_type.value} relationships"
                    })
        
        return phenomena
    
    def _generate_explanations(self, phenomenon: Dict, subgraphs: List[Dict]) -> List[Dict]:
        """Generate candidate explanations for a phenomenon"""
        explanations = []
        
        if phenomenon['type'] == 'high_relationship_count':
            entity_name = phenomenon['entity']
            rel_type = phenomenon['relationship_type']
            count = phenomenon['count']
            
            # Find the entity in subgraphs
            entity_context = None
            for subgraph in subgraphs:
                if subgraph['context']['entity'].name == entity_name:
                    entity_context = subgraph['context']
                    break
            
            if entity_context:
                entity_type = entity_context['entity'].entity_type
                
                # Generate explanations based on entity type
                if entity_type == 'Company' and rel_type == RelationType.HAS_PROPERTY:
                    explanations.append({
                        'explanation': f"{entity_name} is a large company with many diverse attributes",
                        'plausibility': 0.8,
                        'evidence': f"Companies typically have many properties; {count} is reasonable for a major company"
                    })
                
                if entity_type == 'Person' and rel_type == RelationType.WORKS_AT:
                    explanations.append({
                        'explanation': f"{entity_name} may have had multiple jobs or consulting roles",
                        'plausibility': 0.6,
                        'evidence': f"People can work at multiple organizations throughout their career"
                    })
        
        return explanations
    
    def _analogical_reasoning(self, query_analysis: Dict, subgraphs: List[Dict]) -> Dict[str, Any]:
        """Apply analogical reasoning to find similar patterns"""
        
        analogies = []
        
        # Compare subgraphs to find structural similarities
        for i, subgraph1 in enumerate(subgraphs):
            for j, subgraph2 in enumerate(subgraphs[i+1:], i+1):
                analogy = self._find_structural_analogy(subgraph1, subgraph2)
                if analogy:
                    analogies.append(analogy)
        
        return {
            'reasoning_type': 'analogical',
            'analogies': analogies,
            'insights': [a['insight'] for a in analogies],
            'confidence': np.mean([a['similarity'] for a in analogies]) if analogies else 0
        }
    
    def _find_structural_analogy(self, subgraph1: Dict, subgraph2: Dict) -> Optional[Dict]:
        """Find structural analogy between two subgraphs"""
        context1 = subgraph1['context']
        context2 = subgraph2['context']
        
        entity1 = context1['entity']
        entity2 = context2['entity']
        
        # Skip if same entity
        if entity1.id == entity2.id:
            return None
        
        # Compare relationship patterns
        rels1 = [rel.predicate for _, rel in context1['immediate_neighbors']['outgoing']]
        rels2 = [rel.predicate for _, rel in context2['immediate_neighbors']['outgoing']]
        
        # Calculate similarity
        common_rels = set(rels1) & set(rels2)
        total_rels = set(rels1) | set(rels2)
        
        if total_rels:
            similarity = len(common_rels) / len(total_rels)
            
            if similarity > 0.5:  # Threshold for considering analogy
                return {
                    'entity1': entity1.name,
                    'entity2': entity2.name,
                    'similarity': similarity,
                    'common_patterns': list(common_rels),
                    'insight': f"{entity1.name} and {entity2.name} have similar relationship patterns, suggesting they may belong to the same category or serve similar roles"
                }
        
        return None
    
    def _integrate_reasoning_results(self, query: str, query_analysis: Dict,
                                   reasoning_results: Dict, max_size: int) -> Dict[str, Any]:
        """Integrate reasoning results into final context"""
        
        # Start with reasoning conclusions
        context_parts = []
        
        if reasoning_results['reasoning_type'] == 'deductive':
            context_parts.append("Deductive reasoning conclusions:")
            for conclusion in reasoning_results['conclusions']:
                context_parts.append(f"• {conclusion}")
        
        elif reasoning_results['reasoning_type'] == 'inductive':
            context_parts.append("Identified patterns:")
            for generalization in reasoning_results['generalizations']:
                context_parts.append(f"• {generalization}")
        
        elif reasoning_results['reasoning_type'] == 'abductive':
            if reasoning_results['best_explanation']:
                context_parts.append("Best explanation:")
                context_parts.append(f"• {reasoning_results['best_explanation']['explanation']}")
        
        elif reasoning_results['reasoning_type'] == 'analogical':
            context_parts.append("Analogical insights:")
            for insight in reasoning_results['insights']:
                context_parts.append(f"• {insight}")
        
        # Assemble final context
        integrated_context = "\n".join(context_parts)
        
        # Truncate if too long
        if len(integrated_context) > max_size:
            integrated_context = integrated_context[:max_size] + "..."
        
        return {
            'query': query,
            'reasoning_type': reasoning_results['reasoning_type'],
            'context': integrated_context,
            'confidence': reasoning_results.get('confidence', 0),
            'reasoning_details': reasoning_results,
            'query_analysis': query_analysis
        }

# Example usage and demonstration
def create_sample_knowledge_graph() -> KnowledgeGraph:
    """Create sample knowledge graph for demonstration"""
    kg = KnowledgeGraph()
    
    # Add entities
    entities = [
        Entity("alice", "Alice", "Person", {"age": 30, "location": "San Francisco"}),
        Entity("google", "Google", "Company", {"founded": 1998, "employees": 150000}),
        Entity("tech_company", "Technology Company", "Category", {"industry": "Technology"}),
        Entity("ai_researcher", "AI Researcher", "Role", {"field": "Artificial Intelligence"}),
        Entity("machine_learning", "Machine Learning", "Field", {"domain": "Computer Science"}),
        Entity("python", "Python", "Programming Language", {"type": "interpreted"}),
        Entity("san_francisco", "San Francisco", "City", {"state": "California"})
    ]
    
    for entity in entities:
        kg.add_entity(entity)
    
    # Add relationships
    relationships = [
        Relationship("alice", RelationType.WORKS_AT, "google", weight=1.0, confidence=0.95),
        Relationship("alice", RelationType.IS_A, "ai_researcher", weight=1.0, confidence=0.9),
        Relationship("alice", RelationType.LOCATED_IN, "san_francisco", weight=1.0, confidence=0.85),
        Relationship("google", RelationType.IS_A, "tech_company", weight=1.0, confidence=1.0),
        Relationship("google", RelationType.LOCATED_IN, "san_francisco", weight=1.0, confidence=1.0),
        Relationship("ai_researcher", RelationType.RELATED_TO, "machine_learning", weight=0.8, confidence=0.8),
        Relationship("machine_learning", RelationType.ENABLES, "python", weight=0.7, confidence=0.7),
        Relationship("tech_company", RelationType.HAS_PROPERTY, "machine_learning", weight=0.6, confidence=0.6)
    ]
    
    for rel in relationships:
        kg.add_relationship(rel)
    
    return kg

def demonstrate_structured_context():
    """Demonstrate structured context processing"""
    print("Structured Context Processing Demonstration")
    print("=" * 50)
    
    # Create knowledge graph
    kg = create_sample_knowledge_graph()
    
    print(f"Knowledge Graph created with {len(kg.entities)} entities and {len(kg.relationships)} relationships")
    
    # Create context assembler
    assembler = StructuredContextAssembler(kg)
    
    # Test queries
    test_queries = [
        ("What can you tell me about Alice?", ["alice"]),
        ("How is Google related to technology?", ["google", "tech_company"]),
        ("What is the connection between Alice and machine learning?", ["alice", "machine_learning"])
    ]
    
    for query, seed_entities in test_queries:
        print(f"\nQuery: {query}")
        print(f"Seed entities: {seed_entities}")
        print("-" * 40)
        
        # Test different reasoning strategies
        for strategy in ['deductive', 'inductive', 'abductive', 'analogical']:
            print(f"\n{strategy.upper()} REASONING:")
            
            result = assembler.assemble_context(query, seed_entities, reasoning_strategy=strategy)
            
            print(f"Context: {result['context']}")
            print(f"Confidence: {result['confidence']:.3f}")
            
            if result['reasoning_details']:
                details = result['reasoning_details']
                if strategy == 'deductive' and 'chains' in details:
                    print(f"Reasoning chains found: {len(details['chains'])}")
                elif strategy == 'inductive' and 'patterns' in details:
                    print(f"Patterns identified: {len(details['patterns'])}")
                elif strategy == 'abductive' and 'explanations' in details:
                    print(f"Explanations generated: {len(details['explanations'])}")
                elif strategy == 'analogical' and 'analogies' in details:
                    print(f"Analogies found: {len(details['analogies'])}")
    
    # Demonstrate graph traversal
    print(f"\n" + "=" * 50)
    print("GRAPH TRAVERSAL DEMONSTRATION")
    print("=" * 50)
    
    # Find paths between entities
    paths = kg.find_paths("alice", "machine_learning", max_depth=3)
    print(f"\nPaths from Alice to Machine Learning:")
    for i, path in enumerate(paths[:3]):
        print(f"Path {i+1}: {' -> '.join(path.entities)}")
        print(f"  Relationships: {[rel.predicate.value for rel in path.relationships]}")
        print(f"  Score: {path.path_score:.3f}")
    
    # Show entity context
    print(f"\nAlice's Context:")
    alice_context = kg.get_entity_context("alice", depth=2)
    print(f"Entity: {alice_context['entity'].name} ({alice_context['entity'].entity_type})")
    print(f"Immediate connections: {len(alice_context['immediate_neighbors']['outgoing']) + len(alice_context['immediate_neighbors']['incoming'])}")
    print(f"Extended network: {len(alice_context['extended_context'])} entities")
    print(f"Hierarchical: {len(alice_context['hierarchical_context']['parents'])} parents, {len(alice_context['hierarchical_context']['children'])} children")
    
    return kg, assembler

# Run demonstration
if __name__ == "__main__":
    kg, assembler = demonstrate_structured_context()
```

**Ground-up Explanation**: This structured context system works like a research librarian who not only knows where information is stored but understands how different pieces of knowledge connect to each other. The system can trace relationships through multiple steps, identify patterns across different domains, and apply various reasoning strategies to extract insights that aren't explicitly stated in the data.

---

## Research Connections and Future Directions

### Connection to Context Engineering Survey

This structured context module directly implements and extends key concepts from the [Context Engineering Survey](https://arxiv.org/pdf/2507.13334):

**Knowledge Graph Integration (Referenced throughout)**:
- Implements StructGPT and GraphFormers approaches for structured data processing
- Extends KG Integration concepts to comprehensive context assembly
- Addresses structured context challenges through systematic graph reasoning

**Context Processing Innovation (§4.2)**:
- Applies context processing principles to graph-structured information
- Extends self-refinement concepts to knowledge graph optimization
- Implements structured context approaches for relational data

**Novel Research Contributions**:
- **Multi-Strategy Reasoning**: Systematic integration of deductive, inductive, abductive, and analogical reasoning
- **Hierarchical Context Networks**: Dynamic organization of information across multiple abstraction levels
- **Adaptive Graph Intelligence**: Self-improving systems that optimize their own knowledge representation

### Future Research Directions

**Temporal Knowledge Graphs**: Extending static knowledge graphs to capture how relationships and entities evolve over time, enabling temporal reasoning and prediction.

**Probabilistic Graph Reasoning**: Incorporating uncertainty and probabilistic inference into knowledge graph reasoning for more robust context assembly.

**Multi-Modal Knowledge Graphs**: Integrating the multimodal processing from the previous module with structured knowledge representation for richer, more comprehensive context.

**Emergent Relationship Discovery**: Systems that automatically discover new relationship types and patterns not explicitly programmed, extending beyond current knowledge graph limitations.

---

## Summary and Next Steps

**Core Concepts Mastered**:
- Graph-based context representation and traversal algorithms
- Multi-strategy reasoning systems (deductive, inductive, abductive, analogical)
- Hierarchical information organization and propagation
- Knowledge graph integration for context assembly

**Software 3.0 Integration**:
- **Prompts**: Structured reasoning templates for systematic graph traversal
- **Programming**: Knowledge graph engines with multi-strategy reasoning capabilities
- **Protocols**: Adaptive graph intelligence systems that optimize their own reasoning

**Implementation Skills**:
- Knowledge graph construction and management systems
- Multi-hop reasoning and path-finding algorithms
- Structured context assembly with relevance filtering
- Comprehensive reasoning strategy implementations

**Research Grounding**: Direct implementation of knowledge graph research with novel extensions into multi-strategy reasoning, hierarchical context networks, and adaptive graph intelligence systems.

**Next Module**: Long Context Processing Lab - Hands-on implementation of attention mechanisms, memory systems, and hierarchical processing architectures through interactive coding exercises.

---

*This module demonstrates the evolution from linear information processing to networked intelligence, embodying the Software 3.0 principle of systems that not only store and retrieve information but understand and reason about the complex relationships that create meaning and enable insight.*
