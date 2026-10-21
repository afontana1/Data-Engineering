# Attractor Design Template

## Summary
A template for creating semantic attractors that guide AI reasoning toward specific conceptual frameworks, approaches, or outcomes without explicit instruction.

## Context & Application
Use this template when you want to subtly guide AI reasoning toward specific types of responses by creating "attractors" in the semantic space—conceptual gravity wells that naturally pull thinking in certain directions. Unlike direct instructions, attractors work by establishing patterns that the AI naturally continues or completes.

This template is ideal for:
- Encouraging particular thinking styles or frameworks without explicitly requiring them
- Creating subtle guidance that feels natural rather than forced
- Establishing "centers of gravity" for reasoning to orbit around
- Guiding reasoning while preserving flexibility and creativity
- Influencing without dictating specific outcomes

## Template Structure

```
# Task: {{task_description}}

## Context
{{neutral_context}}

## Conceptual Framework
*The following concepts may be relevant to consider:*

{{primary_attractor_concept_1}}:
- {{supporting_element_1a}}
- {{supporting_element_1b}}
- {{supporting_element_1c}}

{{primary_attractor_concept_2}}:
- {{supporting_element_2a}}
- {{supporting_element_2b}}
- {{supporting_element_2c}}

{{resonant_concept}}:
- {{resonant_element_a}}
- {{resonant_element_b}}

## Approach
Consider the above concepts in your analysis, incorporating them as appropriate to the task.

## Expected Output
{{output_specifications}}
```

## Parameters

- `{{task_description}}`: Description of the task that doesn't explicitly mention the attractor concepts
- `{{neutral_context}}`: Background information that establishes context without biasing toward the attractors
- `{{primary_attractor_concept_X}}`: Main concept(s) you want to function as semantic attractors
- `{{supporting_element_X}}`: Elements that reinforce and define the attractor concept
- `{{resonant_concept}}`: A concept that resonates with and amplifies the primary attractors
- `{{output_specifications}}`: Format and structure specifications for the output

## Examples

### Example 1: Systems Thinking Attractor

```
# Task: Analyze the challenges facing urban transportation in growing cities

## Context
Urban areas worldwide are experiencing population growth, putting pressure on existing transportation infrastructure. Many cities are seeking solutions to mobility challenges.

## Conceptual Framework
*The following concepts may be relevant to consider:*

Interconnectedness:
- Relationship between transportation and land use
- Impact of transportation choices on environmental systems
- Connection between mobility and economic opportunity

Feedback Loops:
- How infrastructure investments shape development patterns
- Relationship between congestion and behavior adaptation
- Environmental impacts that affect future transportation choices

Emergence:
- Patterns that arise from individual transportation decisions
- Unexpected consequences of transportation policies
- Self-organizing aspects of urban mobility

## Approach
Consider the above concepts in your analysis, incorporating them as appropriate to the task.

## Expected Output
A comprehensive analysis of urban transportation challenges that identifies key issues, explores underlying dynamics, and suggests potential approaches. Include both short-term and long-term perspectives.
```

### Example 2: Creative Innovation Attractor

```
# Task: Suggest product improvement ideas for a smart home thermostat

## Context
Smart thermostats have become increasingly common in homes, allowing temperature programming, remote control, and some learning capabilities. The company is looking to develop their next generation product.

## Conceptual Framework
*The following concepts may be relevant to consider:*

Boundary Breaking:
- Extending functionality beyond traditional temperature control
- Integration with unexpected systems or services
- Challenging assumptions about what a thermostat should be

Recombination:
- Merging features from different product categories
- Novel combinations of existing technologies
- Unexpected applications of familiar capabilities

User-Centered Surprise:
- Features that anticipate needs users didn't know they had
- Delightful interactions that exceed expectations
- Transformative experiences rather than incremental improvements

## Approach
Consider the above concepts in your analysis, incorporating them as appropriate to the task.

## Expected Output
A list of 5-7 innovative product improvement ideas, each with a brief description, potential user benefit, and implementation considerations. Focus on distinctive ideas rather than obvious incremental improvements.
```

## Variations

### Multi-Attractor Field
For creating multiple attractors with different strengths:

```
# Task: {{task_description}}

## Context
{{neutral_context}}

## Conceptual Framework
*The following concepts may be relevant to consider (in no particular order):*

{{primary_attractor}} [strength: high]:
- {{supporting_elements}}

{{secondary_attractor}} [strength: medium]:
- {{supporting_elements}}

{{tertiary_attractor}} [strength: low]:
- {{supporting_elements}}

## Approach
Consider these concepts in your response, giving each appropriate consideration.

## Expected Output
{{output_specifications}}
```

### Attractor-Repeller Dynamics
For creating both attractive and repulsive conceptual forces:

```
# Task: {{task_description}}

## Context
{{neutral_context}}

## Conceptual Framework
*Consider the following as you develop your response:*

Relevant Approaches:
- {{attractor_concept_1}}
- {{attractor_concept_2}}
- {{attractor_concept_3}}

Approaches to Avoid:
- {{repeller_concept_1}}
- {{repeller_concept_2}}

## Approach
Develop your response drawing from the relevant approaches while avoiding the limitations of approaches to avoid.

## Expected Output
{{output_specifications}}
```

### Resonant Field Attractor
For creating mutually reinforcing concepts that amplify each other:

```
# Task: {{task_description}}

## Context
{{neutral_context}}

## Conceptual Framework
*The following interconnected concepts may be relevant:*

{{concept_1}} ↔ {{concept_2}}:
- How {{concept_1}} influences {{concept_2}}
- How {{concept_2}} reinforces {{concept_1}}

{{concept_2}} ↔ {{concept_3}}:
- Ways {{concept_2}} shapes {{concept_3}}
- Ways {{concept_3}} enhances {{concept_2}}

{{concept_3}} ↔ {{concept_1}}:
- The relationship between {{concept_3}} and {{concept_1}}
- Mutual amplification effects

## Approach
Consider these resonant relationships in your analysis.

## Expected Output
{{output_specifications}}
```

## Best Practices

- **Be subtle rather than heavy-handed** - attractors work best when they feel like natural considerations rather than forced requirements
- **Create coherent attractor fields** - use concepts that naturally complement each other
- **Balance specificity and openness** - too vague won't create enough pull, too specific becomes prescriptive
- **Use supporting elements to define attractors clearly** - help establish exactly what the attractor concept encompasses
- **Position attractors as "concepts to consider" rather than requirements** - preserves flexibility while creating subtle gravity
- **Use familiar concepts as bridges to unfamiliar ones** - helps create paths to novel thinking
- **For complex tasks, use multiple resonant attractors** - creates a rich conceptual field
- **Test attractor strength** - if too weak, enhance supporting elements; if too dominant, reduce specificity
- **Align attractors with the true goal** - the pull should lead toward genuinely useful approaches
- **Design attractors to be discovery-friendly** - they should feel like insights rather than instructions

## Related Templates

- **Field Boundary Establishment Template**: For creating conceptual boundaries to complement attractors
- **Resonance Prompting Template**: For creating resonant effects between concepts
- **Persona Attractor Template**: For using personas as semantic attractors
- **Emergence Engineering Template**: For fostering emergent properties through attractor fields
