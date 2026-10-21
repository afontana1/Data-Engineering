#!/usr/bin/env python3
"""
Structured Data Context Processing Lab
======================================

Context Engineering Course - Module 02: Context Processing
Production-ready knowledge graph and structured data integration.

Learning Objectives:
- Build and query knowledge graphs for context enhancement
- Implement schema-aware data processing and validation
- Create graph-enhanced retrieval and reasoning systems
- Deploy structured data pipelines for production contexts

Research Foundation:
- GraphRAG (Microsoft) - Knowledge graph enhanced retrieval
- Graph Neural Networks - Learning on graph structures
- Knowledge Graph Embeddings (TransE, ComplEx)
- Schema.org structured data standards
"""

import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import json
import time
from typing import Dict, List, Optional, Tuple, Any, Set, Union
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from enum import Enum
from collections import defaultdict, deque
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# CORE INTERFACES & UTILITIES
# ============================================================================

class EntityType(Enum):
    """Standard entity types for knowledge graphs."""
    PERSON = "person"
    ORGANIZATION = "organization"
    LOCATION = "location"
    EVENT = "event"
    CONCEPT = "concept"
    DOCUMENT = "document"
    PRODUCT = "product"

class RelationType(Enum):
    """Standard relation types for knowledge graphs."""
    IS_A = "is_a"
    PART_OF = "part_of"
    LOCATED_IN = "located_in"
    WORKS_FOR = "works_for"
    CREATED_BY = "created_by"
    RELATES_TO = "relates_to"
    SIMILAR_TO = "similar_to"
    CAUSED_BY = "caused_by"

@dataclass
class Entity:
    """Knowledge graph entity with embedding."""
    id: str
    name: str
    entity_type: EntityType
    properties: Dict[str, Any] = field(default_factory=dict)
    embedding: Optional[np.ndarray] = None
    
    def __hash__(self):
        return hash(self.id)
    
    def __eq__(self, other):
        return isinstance(other, Entity) and self.id == other.id

@dataclass
class Relation:
    """Knowledge graph relation/edge."""
    source: Entity
    target: Entity
    relation_type: RelationType
    weight: float = 1.0
    properties: Dict[str, Any] = field(default_factory=dict)
    
    def __hash__(self):
        return hash((self.source.id, self.target.id, self.relation_type.value))

@dataclass
class Schema:
    """Data schema definition with validation rules."""
    name: str
    entity_types: Set[EntityType]
    relation_types: Set[RelationType]
    constraints: Dict[str, Any] = field(default_factory=dict)
    
    def validate_entity(self, entity: Entity) -> bool:
        """Validate entity against schema."""
        return entity.entity_type in self.entity_types
    
    def validate_relation(self, relation: Relation) -> bool:
        """Validate relation against schema."""
        return (relation.relation_type in self.relation_types and
                self.validate_entity(relation.source) and
                self.validate_entity(relation.target))

# ============================================================================
# KNOWLEDGE GRAPH IMPLEMENTATION
# ============================================================================

class KnowledgeGraph:
    """Production-ready knowledge graph with embeddings and reasoning."""
    
    def __init__(self, d_model: int = 256, schema: Optional[Schema] = None):
        self.d_model = d_model
        self.schema = schema
        
        # Graph storage
        self.entities: Dict[str, Entity] = {}
        self.relations: Set[Relation] = set()
        self.adjacency: Dict[str, List[Relation]] = defaultdict(list)
        
        # Embedding components
        self.entity_embeddings = np.random.randn(1000, d_model) * 0.02  # Pre-allocated
        self.relation_embeddings = {rt: np.random.randn(d_model) * 0.02 
                                  for rt in RelationType}
        
        # Graph neural network components
        self.entity_transform = np.random.randn(d_model, d_model) * 0.02
        self.relation_transform = np.random.randn(d_model, d_model) * 0.02
        self.message_aggregation = np.random.randn(d_model * 2, d_model) * 0.02
        
        # Indexing for fast lookups
        self.entity_index = {}  # id -> index mapping
        self.reverse_index = {}  # index -> id mapping
        self.next_index = 0
        
    def add_entity(self, entity: Entity) -> bool:
        """Add entity to knowledge graph."""
        # Schema validation
        if self.schema and not self.schema.validate_entity(entity):
            return False
        
        # Add to graph
        if entity.id not in self.entities:
            self.entities[entity.id] = entity
            self.entity_index[entity.id] = self.next_index
            self.reverse_index[self.next_index] = entity.id
            
            # Initialize embedding
            if entity.embedding is None:
                entity.embedding = self._generate_entity_embedding(entity)
            
            # Store in pre-allocated array
            if self.next_index < len(self.entity_embeddings):
                self.entity_embeddings[self.next_index] = entity.embedding
            
            self.next_index += 1
            return True
        
        return False
    
    def add_relation(self, relation: Relation) -> bool:
        """Add relation to knowledge graph."""
        # Schema validation
        if self.schema and not self.schema.validate_relation(relation):
            return False
        
        # Ensure entities exist
        self.add_entity(relation.source)
        self.add_entity(relation.target)
        
        # Add relation
        if relation not in self.relations:
            self.relations.add(relation)
            self.adjacency[relation.source.id].append(relation)
            return True
        
        return False
    
    def get_entity(self, entity_id: str) -> Optional[Entity]:
        """Get entity by ID."""
        return self.entities.get(entity_id)
    
    def get_neighbors(self, entity_id: str, relation_type: Optional[RelationType] = None) -> List[Entity]:
        """Get neighboring entities."""
        neighbors = []
        for relation in self.adjacency[entity_id]:
            if relation_type is None or relation.relation_type == relation_type:
                neighbors.append(relation.target)
        return neighbors
    
    def find_path(self, source_id: str, target_id: str, max_depth: int = 3) -> Optional[List[str]]:
        """Find shortest path between entities using BFS."""
        if source_id not in self.entities or target_id not in self.entities:
            return None
        
        if source_id == target_id:
            return [source_id]
        
        queue = deque([(source_id, [source_id])])
        visited = {source_id}
        
        while queue:
            current_id, path = queue.popleft()
            
            if len(path) > max_depth:
                continue
            
            for relation in self.adjacency[current_id]:
                neighbor_id = relation.target.id
                
                if neighbor_id == target_id:
                    return path + [neighbor_id]
                
                if neighbor_id not in visited:
                    visited.add(neighbor_id)
                    queue.append((neighbor_id, path + [neighbor_id]))
        
        return None
    
    def query_entities(self, entity_type: Optional[EntityType] = None,
                      properties: Optional[Dict[str, Any]] = None) -> List[Entity]:
        """Query entities by type and properties."""
        results = []
        
        for entity in self.entities.values():
            # Type filter
            if entity_type and entity.entity_type != entity_type:
                continue
            
            # Property filters
            if properties:
                match = True
                for key, value in properties.items():
                    if key not in entity.properties or entity.properties[key] != value:
                        match = False
                        break
                if not match:
                    continue
            
            results.append(entity)
        
        return results
    
    def get_subgraph(self, center_entity_id: str, radius: int = 2) -> 'KnowledgeGraph':
        """Extract subgraph around center entity."""
        subgraph = KnowledgeGraph(self.d_model, self.schema)
        visited = set()
        
        def explore(entity_id: str, depth: int):
            if depth > radius or entity_id in visited:
                return
            
            visited.add(entity_id)
            entity = self.entities[entity_id]
            subgraph.add_entity(entity)
            
            # Add relations and explore neighbors
            for relation in self.adjacency[entity_id]:
                subgraph.add_relation(relation)
                explore(relation.target.id, depth + 1)
        
        explore(center_entity_id, 0)
        return subgraph
    
    def compute_embeddings_gnn(self, num_iterations: int = 3) -> Dict[str, np.ndarray]:
        """Compute entity embeddings using graph neural network approach."""
        # Initialize with current embeddings
        current_embeddings = {}
        for entity_id, entity in self.entities.items():
            if entity.embedding is not None:
                current_embeddings[entity_id] = entity.embedding.copy()
            else:
                current_embeddings[entity_id] = np.random.randn(self.d_model) * 0.02
        
        # GNN iterations
        for iteration in range(num_iterations):
            new_embeddings = {}
            
            for entity_id, entity in self.entities.items():
                # Collect neighbor messages
                messages = []
                
                for relation in self.adjacency[entity_id]:
                    neighbor_embedding = current_embeddings[relation.target.id]
                    relation_embedding = self.relation_embeddings[relation.relation_type]
                    
                    # Transform neighbor embedding through relation
                    message = neighbor_embedding @ self.relation_transform
                    message = message + relation_embedding * relation.weight
                    messages.append(message)
                
                # Aggregate messages
                if messages:
                    aggregated_message = np.mean(messages, axis=0)
                    
                    # Combine with current embedding
                    combined = np.concatenate([current_embeddings[entity_id], aggregated_message])
                    new_embedding = np.tanh(combined @ self.message_aggregation)
                else:
                    # No neighbors - just transform current embedding
                    new_embedding = current_embeddings[entity_id] @ self.entity_transform
                
                new_embeddings[entity_id] = new_embedding
            
            current_embeddings = new_embeddings
        
        # Update entity embeddings
        for entity_id, embedding in current_embeddings.items():
            self.entities[entity_id].embedding = embedding
            
            # Update pre-allocated array
            if entity_id in self.entity_index:
                idx = self.entity_index[entity_id]
                if idx < len(self.entity_embeddings):
                    self.entity_embeddings[idx] = embedding
        
        return current_embeddings
    
    def similarity_search(self, query_embedding: np.ndarray, top_k: int = 5) -> List[Tuple[Entity, float]]:
        """Find most similar entities to query embedding."""
        similarities = []
        
        for entity in self.entities.values():
            if entity.embedding is not None:
                # Cosine similarity
                dot_product = np.dot(query_embedding, entity.embedding)
                norm_product = (np.linalg.norm(query_embedding) * 
                              np.linalg.norm(entity.embedding))
                
                if norm_product > 0:
                    similarity = dot_product / norm_product
                    similarities.append((entity, similarity))
        
        # Sort and return top-k
        similarities.sort(key=lambda x: x[1], reverse=True)
        return similarities[:top_k]
    
    def _generate_entity_embedding(self, entity: Entity) -> np.ndarray:
        """Generate initial embedding for entity."""
        # Base embedding from entity type
        type_embedding = np.random.randn(self.d_model) * 0.02
        
        # Add property-based features
        property_features = np.zeros(self.d_model)
        for key, value in entity.properties.items():
            # Simple hash-based feature generation
            feature_hash = hash(f"{key}:{value}") % self.d_model
            property_features[feature_hash] += 0.1
        
        # Combine and normalize
        embedding = type_embedding + property_features * 0.5
        return embedding / (np.linalg.norm(embedding) + 1e-8)
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get knowledge graph statistics."""
        entity_types = defaultdict(int)
        relation_types = defaultdict(int)
        
        for entity in self.entities.values():
            entity_types[entity.entity_type.value] += 1
        
        for relation in self.relations:
            relation_types[relation.relation_type.value] += 1
        
        return {
            'num_entities': len(self.entities),
            'num_relations': len(self.relations),
            'entity_types': dict(entity_types),
            'relation_types': dict(relation_types),
            'average_degree': len(self.relations) / max(1, len(self.entities)),
            'schema_name': self.schema.name if self.schema else None
        }

# ============================================================================
# GRAPH-ENHANCED RAG SYSTEM
# ============================================================================

class GraphRAG:
    """Graph-enhanced Retrieval-Augmented Generation system."""
    
    def __init__(self, d_model: int = 256):
        self.d_model = d_model
        self.knowledge_graph = KnowledgeGraph(d_model)
        self.document_embeddings = {}
        self.entity_document_map = defaultdict(set)  # entity_id -> document_ids
        
        # Query processing components
        self.query_encoder = np.random.randn(d_model, d_model) * 0.02
        self.context_fusion = np.random.randn(d_model * 3, d_model) * 0.02
        
    def add_document(self, document_id: str, content: str, 
                    entities: List[Entity], relations: List[Relation],
                    document_embedding: np.ndarray):
        """Add document with extracted entities and relations."""
        
        # Store document embedding
        self.document_embeddings[document_id] = document_embedding
        
        # Add entities and relations to knowledge graph
        for entity in entities:
            self.knowledge_graph.add_entity(entity)
            self.entity_document_map[entity.id].add(document_id)
        
        for relation in relations:
            self.knowledge_graph.add_relation(relation)
    
    def retrieve_context(self, query: str, query_embedding: np.ndarray,
                        top_k_entities: int = 5, top_k_documents: int = 3) -> Dict[str, Any]:
        """Retrieve graph-enhanced context for query."""
        
        # Transform query embedding
        transformed_query = query_embedding @ self.query_encoder
        
        # Step 1: Find relevant entities
        relevant_entities = self.knowledge_graph.similarity_search(
            transformed_query, top_k=top_k_entities
        )
        
        # Step 2: Get entity neighborhoods
        entity_context = []
        for entity, similarity in relevant_entities:
            # Get local subgraph
            subgraph = self.knowledge_graph.get_subgraph(entity.id, radius=1)
            entity_context.append({
                'entity': entity,
                'similarity': similarity,
                'subgraph': subgraph,
                'neighbors': self.knowledge_graph.get_neighbors(entity.id)
            })
        
        # Step 3: Find documents through entities
        candidate_documents = set()
        for entity, _ in relevant_entities:
            candidate_documents.update(self.entity_document_map[entity.id])
        
        # Step 4: Rank documents by embedding similarity
        document_similarities = []
        for doc_id in candidate_documents:
            if doc_id in self.document_embeddings:
                doc_embedding = self.document_embeddings[doc_id]
                similarity = np.dot(transformed_query, doc_embedding)
                similarity /= (np.linalg.norm(transformed_query) * 
                             np.linalg.norm(doc_embedding) + 1e-8)
                document_similarities.append((doc_id, similarity))
        
        document_similarities.sort(key=lambda x: x[1], reverse=True)
        top_documents = document_similarities[:top_k_documents]
        
        # Step 5: Create unified context
        unified_context = self._create_unified_context(
            query_embedding, entity_context, top_documents
        )
        
        return {
            'query': query,
            'relevant_entities': relevant_entities,
            'entity_context': entity_context,
            'relevant_documents': top_documents,
            'unified_context': unified_context,
            'retrieval_stats': {
                'entities_found': len(relevant_entities),
                'documents_found': len(top_documents),
                'subgraphs_explored': len(entity_context)
            }
        }
    
    def _create_unified_context(self, query_embedding: np.ndarray,
                              entity_context: List[Dict], 
                              document_similarities: List[Tuple[str, float]]) -> np.ndarray:
        """Create unified context embedding from graph and document information."""
        
        # Aggregate entity embeddings
        if entity_context:
            entity_embeddings = [ctx['entity'].embedding for ctx in entity_context 
                               if ctx['entity'].embedding is not None]
            entity_repr = np.mean(entity_embeddings, axis=0) if entity_embeddings else np.zeros(self.d_model)
        else:
            entity_repr = np.zeros(self.d_model)
        
        # Aggregate document embeddings
        if document_similarities:
            doc_embeddings = []
            for doc_id, similarity in document_similarities:
                doc_embedding = self.document_embeddings[doc_id]
                doc_embeddings.append(doc_embedding * similarity)  # Weight by similarity
            document_repr = np.mean(doc_embeddings, axis=0) if doc_embeddings else np.zeros(self.d_model)
        else:
            document_repr = np.zeros(self.d_model)
        
        # Fuse query, entity, and document representations
        combined = np.concatenate([query_embedding, entity_repr, document_repr])
        unified_context = np.tanh(combined @ self.context_fusion)
        
        return unified_context

# ============================================================================
# SCHEMA PROCESSING & VALIDATION
# ============================================================================

class StructuredDataProcessor:
    """Process and validate structured data against schemas."""
    
    def __init__(self):
        self.schemas = {}
        self.validators = {}
        
    def register_schema(self, schema: Schema):
        """Register a data schema."""
        self.schemas[schema.name] = schema
        self.validators[schema.name] = self._create_validator(schema)
    
    def validate_data(self, schema_name: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate data against schema."""
        if schema_name not in self.schemas:
            return {'valid': False, 'error': f'Schema {schema_name} not found'}
        
        schema = self.schemas[schema_name]
        validator = self.validators[schema_name]
        
        try:
            validation_result = validator(data)
            return {
                'valid': validation_result['valid'],
                'errors': validation_result.get('errors', []),
                'warnings': validation_result.get('warnings', []),
                'normalized_data': validation_result.get('normalized_data', data)
            }
        except Exception as e:
            return {'valid': False, 'error': str(e)}
    
    def extract_entities_from_structured_data(self, schema_name: str, 
                                            data: Dict[str, Any]) -> List[Entity]:
        """Extract entities from validated structured data."""
        if schema_name not in self.schemas:
            return []
        
        schema = self.schemas[schema_name]
        entities = []
        
        # Entity extraction rules based on schema
        for entity_type in schema.entity_types:
            if entity_type.value in data:
                entity_data = data[entity_type.value]
                
                if isinstance(entity_data, list):
                    for i, item in enumerate(entity_data):
                        entity = Entity(
                            id=f"{entity_type.value}_{i}",
                            name=item.get('name', f'{entity_type.value}_{i}'),
                            entity_type=entity_type,
                            properties=item
                        )
                        entities.append(entity)
                elif isinstance(entity_data, dict):
                    entity = Entity(
                        id=entity_data.get('id', entity_type.value),
                        name=entity_data.get('name', entity_type.value),
                        entity_type=entity_type,
                        properties=entity_data
                    )
                    entities.append(entity)
        
        return entities
    
    def _create_validator(self, schema: Schema) -> callable:
        """Create validator function for schema."""
        
        def validator(data: Dict[str, Any]) -> Dict[str, Any]:
            errors = []
            warnings = []
            normalized_data = data.copy()
            
            # Check required entity types
            for entity_type in schema.entity_types:
                if entity_type.value not in data:
                    warnings.append(f'Optional entity type {entity_type.value} not found')
            
            # Validate constraints
            for constraint_name, constraint_rule in schema.constraints.items():
                if constraint_name == 'required_fields':
                    for field in constraint_rule:
                        if field not in data:
                            errors.append(f'Required field {field} missing')
                
                elif constraint_name == 'field_types':
                    for field, expected_type in constraint_rule.items():
                        if field in data:
                            if not isinstance(data[field], expected_type):
                                errors.append(f'Field {field} has wrong type, expected {expected_type.__name__}')
            
            return {
                'valid': len(errors) == 0,
                'errors': errors,
                'warnings': warnings,
                'normalized_data': normalized_data
            }
        
        return validator

# ============================================================================
# GRAPH REASONING ENGINE
# ============================================================================

class GraphReasoner:
    """Reasoning engine for knowledge graph inference."""
    
    def __init__(self, knowledge_graph: KnowledgeGraph):
        self.knowledge_graph = knowledge_graph
        self.inference_rules = []
        
    def add_inference_rule(self, rule_name: str, 
                          premise_pattern: List[Tuple[str, RelationType, str]],
                          conclusion_pattern: Tuple[str, RelationType, str]):
        """Add logical inference rule."""
        self.inference_rules.append({
            'name': rule_name,
            'premise': premise_pattern,
            'conclusion': conclusion_pattern
        })
    
    def infer_new_relations(self) -> List[Relation]:
        """Apply inference rules to discover new relations."""
        new_relations = []
        
        for rule in self.inference_rules:
            # Find all matches for the premise pattern
            matches = self._find_pattern_matches(rule['premise'])
            
            for match in matches:
                # Generate conclusion relation
                conclusion = rule['conclusion']
                source_var, relation_type, target_var = conclusion
                
                if source_var in match and target_var in match:
                    source_entity = match[source_var]
                    target_entity = match[target_var]
                    
                    # Create new relation
                    new_relation = Relation(
                        source=source_entity,
                        target=target_entity,
                        relation_type=relation_type,
                        weight=0.8,  # Inferred relations have lower confidence
                        properties={'inferred': True, 'rule': rule['name']}
                    )
                    
                    # Check if relation doesn't already exist
                    if new_relation not in self.knowledge_graph.relations:
                        new_relations.append(new_relation)
        
        return new_relations
    
    def answer_query(self, query: str, query_entities: List[str]) -> Dict[str, Any]:
        """Answer structured query using graph reasoning."""
        
        # Simple query patterns
        if 'connected' in query.lower():
            return self._handle_connectivity_query(query_entities)
        elif 'similar' in query.lower():
            return self._handle_similarity_query(query_entities)
        elif 'path' in query.lower():
            return self._handle_path_query(query_entities)
        else:
            return self._handle_general_query(query, query_entities)
    
    def _find_pattern_matches(self, pattern: List[Tuple[str, RelationType, str]]) -> List[Dict[str, Entity]]:
        """Find all matches for a relation pattern."""
        matches = []
        
        # Simple pattern matching (can be extended for complex patterns)
        if len(pattern) == 1:
            # Single relation pattern
            var_source, relation_type, var_target = pattern[0]
            
            for relation in self.knowledge_graph.relations:
                if relation.relation_type == relation_type:
                    match = {
                        var_source: relation.source,
                        var_target: relation.target
                    }
                    matches.append(match)
        
        return matches
    
    def _handle_connectivity_query(self, entity_ids: List[str]) -> Dict[str, Any]:
        """Handle connectivity queries between entities."""
        if len(entity_ids) != 2:
            return {'error': 'Connectivity queries require exactly 2 entities'}
        
        source_id, target_id = entity_ids
        path = self.knowledge_graph.find_path(source_id, target_id)
        
        return {
            'query_type': 'connectivity',
            'entities': entity_ids,
            'connected': path is not None,
            'path': path,
            'path_length': len(path) - 1 if path else None
        }
    
    def _handle_similarity_query(self, entity_ids: List[str]) -> Dict[str, Any]:
        """Handle similarity queries between entities."""
        similarities = []
        
        for i, entity_id_1 in enumerate(entity_ids):
            for j, entity_id_2 in enumerate(entity_ids[i+1:], i+1):
                entity_1 = self.knowledge_graph.get_entity(entity_id_1)
                entity_2 = self.knowledge_graph.get_entity(entity_id_2)
                
                if entity_1 and entity_2 and entity_1.embedding is not None and entity_2.embedding is not None:
                    similarity = np.dot(entity_1.embedding, entity_2.embedding)
                    similarity /= (np.linalg.norm(entity_1.embedding) * 
                                 np.linalg.norm(entity_2.embedding) + 1e-8)
                    
                    similarities.append({
                        'entity_1': entity_id_1,
                        'entity_2': entity_id_2,
                        'similarity': float(similarity)
                    })
        
        return {
            'query_type': 'similarity',
            'entities': entity_ids,
            'similarities': similarities
        }
    
    def _handle_path_query(self, entity_ids: List[str]) -> Dict[str, Any]:
        """Handle path queries between entities."""
        if len(entity_ids) != 2:
            return {'error': 'Path queries require exactly 2 entities'}
        
        source_id, target_id = entity_ids
        path = self.knowledge_graph.find_path(source_id, target_id, max_depth=5)
        
        # Get path details
        path_relations = []
        if path and len(path) > 1:
            for i in range(len(path) - 1):
                current_id = path[i]
                next_id = path[i + 1]
                
                # Find relation between current and next
                for relation in self.knowledge_graph.adjacency[current_id]:
                    if relation.target.id == next_id:
                        path_relations.append({
                            'source': current_id,
                            'target': next_id,
                            'relation_type': relation.relation_type.value,
                            'weight': relation.weight
                        })
                        break
        
        return {
            'query_type': 'path',
            'entities': entity_ids,
            'path': path,
            'path_relations': path_relations,
            'path_exists': path is not None
        }
    
    def _handle_general_query(self, query: str, entity_ids: List[str]) -> Dict[str, Any]:
        """Handle general queries about entities."""
        results = {}
        
        for entity_id in entity_ids:
            entity = self.knowledge_graph.get_entity(entity_id)
            if entity:
                neighbors = self.knowledge_graph.get_neighbors(entity_id)
                results[entity_id] = {
                    'entity_type': entity.entity_type.value,
                    'properties': entity.properties,
                    'neighbor_count': len(neighbors),
                    'neighbors': [n.id for n in neighbors[:5]]  # Top 5 neighbors
                }
        
        return {
            'query_type': 'general',
            'query': query,
            'entities': entity_ids,
            'results': results
        }

# ============================================================================
# PRACTICAL APPLICATIONS
# ============================================================================

def create_sample_knowledge_graph() -> KnowledgeGraph:
    """Create sample knowledge graph for demonstration."""
    
    # Create schema
    schema = Schema(
        name="tech_company_schema",
        entity_types={EntityType.PERSON, EntityType.ORGANIZATION, EntityType.PRODUCT, EntityType.LOCATION},
        relation_types={RelationType.WORKS_FOR, RelationType.CREATED_BY, RelationType.LOCATED_IN, RelationType.IS_A}
    )
    
    kg = KnowledgeGraph(d_model=256, schema=schema)
    
    # Add entities
    entities = [
        Entity("person_1", "Alice Johnson", EntityType.PERSON, 
               {"role": "CEO", "experience": 15}),
        Entity("person_2", "Bob Chen", EntityType.PERSON, 
               {"role": "CTO", "experience": 12}),
        Entity("company_1", "TechCorp", EntityType.ORGANIZATION,
               {"industry": "AI", "size": "startup", "founded": 2020}),
        Entity("product_1", "AIAssistant", EntityType.PRODUCT,
               {"category": "software", "version": "2.0"}),
        Entity("location_1", "San Francisco", EntityType.LOCATION,
               {"country": "USA", "state": "CA"})
    ]
    
    for entity in entities:
        kg.add_entity(entity)
    
    # Add relations
    relations = [
        Relation(entities[0], entities[2], RelationType.WORKS_FOR),  # Alice works for TechCorp
        Relation(entities[1], entities[2], RelationType.WORKS_FOR),  # Bob works for TechCorp
        Relation(entities[3], entities[1], RelationType.CREATED_BY), # AIAssistant created by Bob
        Relation(entities[2], entities[4], RelationType.LOCATED_IN), # TechCorp located in SF
        Relation(entities[3], entities[2], RelationType.CREATED_BY)  # AIAssistant created by TechCorp
    ]
    
    for relation in relations:
        kg.add_relation(relation)
    
    return kg

def benchmark_graph_operations():
    """Benchmark knowledge graph operations."""
    
    print("="*60)
    print("STRUCTURED DATA PROCESSING BENCHMARK")
    print("="*60)
    
    # Create test knowledge graphs of different sizes
    graph_sizes = [100, 500, 1000, 2000]
    results = {}
    
    for size in graph_sizes:
        print(f"\nTesting graph with {size} entities:")
        
        # Create random graph
        kg = KnowledgeGraph(d_model=256)
        
        # Add entities
        start_time = time.time()
        entities = []
        for i in range(size):
            entity = Entity(
                id=f"entity_{i}",
                name=f"Entity {i}",
                entity_type=EntityType.CONCEPT,
                properties={"index": i, "category": f"cat_{i % 10}"}
            )
            entities.append(entity)
            kg.add_entity(entity)
        
        entity_creation_time = time.time() - start_time
        
        # Add relations (create connected graph)
        start_time = time.time()
        relations_added = 0
        for i in range(size):
            # Connect to 2-5 random other entities
            num_connections = min(np.random.randint(2, 6), size - 1)
            targets = np.random.choice(size, num_connections, replace=False)
            
            for target_idx in targets:
                if target_idx != i:
                    relation = Relation(
                        source=entities[i],
                        target=entities[target_idx],
                        relation_type=RelationType.RELATES_TO,
                        weight=np.random.random()
                    )
                    if kg.add_relation(relation):
                        relations_added += 1
        
        relation_creation_time = time.time() - start_time
        
        # Test embedding computation
        start_time = time.time()
        embeddings = kg.compute_embeddings_gnn(num_iterations=3)
        embedding_time = time.time() - start_time
        
        # Test path finding
        start_time = time.time()
        paths_found = 0
        for _ in range(min(100, size)):
            source_idx = np.random.randint(0, size)
            target_idx = np.random.randint(0, size)
            path = kg.find_path(f"entity_{source_idx}", f"entity_{target_idx}")
            if path:
                paths_found += 1
        
        pathfinding_time = time.time() - start_time
        
        # Test similarity search
        start_time = time.time()
        query_embedding = np.random.randn(256)
        similar_entities = kg.similarity_search(query_embedding, top_k=10)
        similarity_time = time.time() - start_time
        
        # Store results
        stats = kg.get_statistics()
        results[size] = {
            'entity_creation_time': entity_creation_time,
            'relation_creation_time': relation_creation_time,
            'relations_added': relations_added,
            'embedding_time': embedding_time,
            'pathfinding_time': pathfinding_time,
            'paths_found': paths_found,
            'similarity_time': similarity_time,
            'similar_entities_found': len(similar_entities),
            'average_degree': stats['average_degree']
        }
        
        print(f"  Entity creation: {entity_creation_time*1000:.2f}ms")
        print(f"  Relations added: {relations_added} ({relation_creation_time*1000:.2f}ms)")
        print(f"  GNN embeddings: {embedding_time*1000:.2f}ms")
        print(f"  Path finding: {paths_found}/100 found ({pathfinding_time*1000:.2f}ms)")
        print(f"  Similarity search: {len(similar_entities)} found ({similarity_time*1000:.2f}ms)")
    
    return results

def visualize_graph_performance(results: Dict):
    """Visualize graph processing performance."""
    
    sizes = list(results.keys())
    
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    fig.suptitle('Knowledge Graph Performance Analysis', fontsize=16, fontweight='bold')
    
    # Plot 1: Entity and relation creation times
    ax = axes[0, 0]
    entity_times = [results[size]['entity_creation_time'] * 1000 for size in sizes]
    relation_times = [results[size]['relation_creation_time'] * 1000 for size in sizes]
    
    ax.plot(sizes, entity_times, 'b-o', label='Entity Creation', linewidth=2, markersize=6)
    ax.plot(sizes, relation_times, 'r-s', label='Relation Creation', linewidth=2, markersize=6)
    ax.set_xlabel('Graph Size (entities)')
    ax.set_ylabel('Time (ms)')
    ax.set_title('Graph Construction Performance')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Plot 2: GNN embedding computation
    ax = axes[0, 1]
    embedding_times = [results[size]['embedding_time'] * 1000 for size in sizes]
    ax.plot(sizes, embedding_times, 'g-^', linewidth=2, markersize=6)
    ax.set_xlabel('Graph Size (entities)')
    ax.set_ylabel('Time (ms)')
    ax.set_title('GNN Embedding Computation')
    ax.grid(True, alpha=0.3)
    
    # Plot 3: Path finding performance
    ax = axes[0, 2]
    pathfinding_times = [results[size]['pathfinding_time'] * 1000 for size in sizes]
    paths_found = [results[size]['paths_found'] for size in sizes]
    
    ax2 = ax.twinx()
    line1 = ax.plot(sizes, pathfinding_times, 'purple', linewidth=2, marker='d', markersize=6, label='Time')
    line2 = ax2.plot(sizes, paths_found, 'orange', linewidth=2, marker='x', markersize=8, label='Paths Found')
    
    ax.set_xlabel('Graph Size (entities)')
    ax.set_ylabel('Time (ms)', color='purple')
    ax2.set_ylabel('Paths Found (out of 100)', color='orange')
    ax.set_title('Path Finding Performance')
    ax.grid(True, alpha=0.3)
    
    # Combine legends
    lines = line1 + line2
    labels = [l.get_label() for l in lines]
    ax.legend(lines, labels, loc='upper left')
    
    # Plot 4: Similarity search performance
    ax = axes[1, 0]
    similarity_times = [results[size]['similarity_time'] * 1000 for size in sizes]
    similar_found = [results[size]['similar_entities_found'] for size in sizes]
    
    ax2 = ax.twinx()
    line1 = ax.plot(sizes, similarity_times, 'teal', linewidth=2, marker='o', markersize=6, label='Time')
    line2 = ax2.plot(sizes, similar_found, 'coral', linewidth=2, marker='s', markersize=6, label='Entities Found')
    
    ax.set_xlabel('Graph Size (entities)')
    ax.set_ylabel('Time (ms)', color='teal')
    ax2.set_ylabel('Similar Entities Found', color='coral')
    ax.set_title('Similarity Search Performance')
    ax.grid(True, alpha=0.3)
    
    lines = line1 + line2
    labels = [l.get_label() for l in lines]
    ax.legend(lines, labels, loc='upper left')
    
    # Plot 5: Graph connectivity
    ax = axes[1, 1]
    relations_added = [results[size]['relations_added'] for size in sizes]
    average_degrees = [results[size]['average_degree'] for size in sizes]
    
    ax2 = ax.twinx()
    line1 = ax.bar([str(s) for s in sizes], relations_added, alpha=0.7, color='lightblue', label='Relations')
    line2 = ax2.plot(range(len(sizes)), average_degrees, 'red', linewidth=3, marker='o', markersize=8, label='Avg Degree')
    
    ax.set_xlabel('Graph Size (entities)')
    ax.set_ylabel('Relations Added', color='blue')
    ax2.set_ylabel('Average Degree', color='red')
    ax.set_title('Graph Connectivity')
    
    # Plot 6: Overall efficiency
    ax = axes[1, 2]
    total_times = [(results[size]['entity_creation_time'] + 
                   results[size]['relation_creation_time'] + 
                   results[size]['embedding_time']) * 1000 for size in sizes]
    
    throughput = [size / (total_time / 1000) for size, total_time in zip(sizes, total_times)]
    
    ax.plot(sizes, throughput, 'navy', linewidth=3, marker='D', markersize=8)
    ax.set_xlabel('Graph Size (entities)')
    ax.set_ylabel('Throughput (entities/sec)')
    ax.set_title('Overall Processing Throughput')
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()

# ============================================================================
# MAIN DEMONSTRATION
# ============================================================================

def main():
    """Main demonstration of structured data processing capabilities."""
    
    print("="*80)
    print("STRUCTURED DATA CONTEXT PROCESSING LAB")
    print("Context Engineering Course - Module 02")
    print("="*80)
    print()
    
    # 1. Basic knowledge graph demonstration
    print("1. Knowledge Graph Construction and Querying")
    print("-" * 60)
    
    # Create sample knowledge graph
    kg = create_sample_knowledge_graph()
    stats = kg.get_statistics()
    
    print("Knowledge Graph Statistics:")
    print(f"  Entities: {stats['num_entities']}")
    print(f"  Relations: {stats['num_relations']}")
    print(f"  Entity types: {list(stats['entity_types'].keys())}")
    print(f"  Relation types: {list(stats['relation_types'].keys())}")
    print(f"  Average degree: {stats['average_degree']:.2f}")
    
    # Test path finding
    print("\nPath Finding Examples:")
    paths = [
        ("person_1", "product_1"),
        ("person_2", "location_1"),
        ("company_1", "person_1")
    ]
    
    for source, target in paths:
        path = kg.find_path(source, target)
        print(f"  {source} → {target}: {' → '.join(path) if path else 'No path found'}")
    
    # Test entity queries
    print("\nEntity Queries:")
    people = kg.query_entities(entity_type=EntityType.PERSON)
    print(f"  Found {len(people)} people: {[p.name for p in people]}")
    
    orgs = kg.query_entities(entity_type=EntityType.ORGANIZATION)
    print(f"  Found {len(orgs)} organizations: {[o.name for o in orgs]}")
    
    # 2. Graph Neural Network embeddings
    print("\n2. Graph Neural Network Embeddings")
    print("-" * 60)
    
    print("Computing GNN embeddings...")
    start_time = time.time()
    embeddings = kg.compute_embeddings_gnn(num_iterations=3)
    embedding_time = time.time() - start_time
    
    print(f"  Computed embeddings for {len(embeddings)} entities")
    print(f"  Processing time: {embedding_time*1000:.2f}ms")
    
    # Test similarity search
    alice_entity = kg.get_entity("person_1")
    if alice_entity and alice_entity.embedding is not None:
        similar_entities = kg.similarity_search(alice_entity.embedding, top_k=3)
        print("\nSimilar entities to Alice Johnson:")
        for entity, similarity in similar_entities:
            print(f"  {entity.name} ({entity.entity_type.value}): {similarity:.3f}")
    
    # 3. GraphRAG demonstration
    print("\n3. Graph-Enhanced RAG System")
    print("-" * 60)
    
    graph_rag = GraphRAG(d_model=256)
    
    # Add sample documents
    sample_docs = [
        {
            'id': 'doc_1',
            'content': 'Alice Johnson founded TechCorp in San Francisco',
            'entities': [
                Entity('alice_doc', 'Alice Johnson', EntityType.PERSON),
                Entity('techcorp_doc', 'TechCorp', EntityType.ORGANIZATION),
                Entity('sf_doc', 'San Francisco', EntityType.LOCATION)
            ],
            'relations': [
                Relation(Entity('alice_doc', 'Alice', EntityType.PERSON),
                        Entity('techcorp_doc', 'TechCorp', EntityType.ORGANIZATION),
                        RelationType.WORKS_FOR)
            ]
        }
    ]
    
    for doc in sample_docs:
        doc_embedding = np.random.randn(256) * 0.1
        graph_rag.add_document(
            doc['id'], doc['content'], 
            doc['entities'], doc['relations'],
            doc_embedding
        )
    
    # Test retrieval
    query = "Tell me about TechCorp's founder"
    query_embedding = np.random.randn(256) * 0.1
    
    retrieval_result = graph_rag.retrieve_context(
        query, query_embedding, top_k_entities=3, top_k_documents=2
    )
    
    print(f"Query: {query}")
    print(f"Relevant entities found: {retrieval_result['retrieval_stats']['entities_found']}")
    print(f"Relevant documents found: {retrieval_result['retrieval_stats']['documents_found']}")
    
    for entity, similarity in retrieval_result['relevant_entities']:
        print(f"  Entity: {entity.name} (similarity: {similarity:.3f})")
    
    # 4. Schema processing demonstration
    print("\n4. Schema Processing and Validation")
    print("-" * 60)
    
    # Create schema processor
    processor = StructuredDataProcessor()
    
    # Define sample schema
    tech_schema = Schema(
        name="tech_company_data",
        entity_types={EntityType.PERSON, EntityType.ORGANIZATION, EntityType.PRODUCT},
        relation_types={RelationType.WORKS_FOR, RelationType.CREATED_BY},
        constraints={
            'required_fields': ['company_name', 'founder'],
            'field_types': {'company_name': str, 'founded_year': int}
        }
    )
    
    processor.register_schema(tech_schema)
    
    # Test data validation
    test_data = [
        {'company_name': 'TestCorp', 'founder': 'John Doe', 'founded_year': 2021},
        {'company_name': 'BadCorp', 'founder': 'Jane Smith'},  # Missing founded_year
        {'founder': 'Bob Wilson', 'founded_year': 2020}        # Missing company_name
    ]
    
    print("Schema Validation Results:")
    for i, data in enumerate(test_data):
        result = processor.validate_data('tech_company_data', data)
        print(f"  Data {i+1}: {'Valid' if result['valid'] else 'Invalid'}")
        if not result['valid']:
            print(f"    Errors: {result.get('errors', [])}")
    
    # 5. Graph reasoning demonstration
    print("\n5. Graph Reasoning Engine")
    print("-" * 60)
    
    reasoner = GraphReasoner(kg)
    
    # Add simple inference rule
    reasoner.add_inference_rule(
        "transitivity",
        [("?x", RelationType.WORKS_FOR, "?y"), ("?y", RelationType.LOCATED_IN, "?z")],
        ("?x", RelationType.LOCATED_IN, "?z")
    )
    
    # Test reasoning queries
    queries = [
        ("Are Alice and Bob connected?", ["person_1", "person_2"]),
        ("What is the similarity between TechCorp and Alice?", ["company_1", "person_1"]),
        ("Find path from Bob to San Francisco", ["person_2", "location_1"])
    ]
    
    for query_text, entities in queries:
        print(f"\nQuery: {query_text}")
        result = reasoner.answer_query(query_text, entities)
        
        if result.get('query_type') == 'connectivity':
            print(f"  Connected: {result['connected']}")
            if result['path']:
                print(f"  Path: {' → '.join(result['path'])}")
        
        elif result.get('query_type') == 'similarity':
            for sim in result.get('similarities', []):
                print(f"  {sim['entity_1']} ↔ {sim['entity_2']}: {sim['similarity']:.3f}")
        
        elif result.get('query_type') == 'path':
            if result['path_exists']:
                print(f"  Path: {' → '.join(result['path'])}")
                for rel in result['path_relations']:
                    print(f"    {rel['source']} --{rel['relation_type']}--> {rel['target']}")
            else:
                print("  No path found")
    
    # 6. Performance benchmark
    print("\n6. Performance Benchmark")
    print("-" * 60)
    
    benchmark_results = benchmark_graph_operations()
    
    # 7. Visualizations
    print("\n7. Generating Performance Visualizations...")
    print("-" * 60)
    
    visualize_graph_performance(benchmark_results)
    
    print("\n" + "="*80)
    print("STRUCTURED DATA CONTEXT PROCESSING LAB COMPLETE")
    print("="*80)
    print("\nKey Takeaways:")
    print("• Knowledge graphs provide rich structured context")
    print("• GNN embeddings capture relational information effectively")
    print("• Graph-enhanced RAG improves retrieval quality")
    print("• Schema validation ensures data consistency")
    print("• Graph reasoning enables logical inference")
    
    print("\nPractical Applications:")
    print("• Enterprise knowledge management systems")
    print("• Intelligent search with relationship understanding")
    print("• Automated fact-checking and verification")
    print("• Recommendation systems with graph-based features")
    print("• Legal and regulatory compliance systems")

if __name__ == "__main__":
    main()
