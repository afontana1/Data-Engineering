# Minimal Context Template

## Summary
A streamlined template for creating minimal but effective context for AI systems, focusing on clarity and essential information.
## Context & Application
Use this template when you need to provide just enough context for an AI system to perform effectively without unnecessary information. It establishes clear boundaries, expectations, and essential information in a structured format.

This template is ideal for:
- First-time interactions with AI systems
- Well-defined tasks with clear deliverables
- Situations where minimizing prompt length is important
- Establishing a baseline for more complex prompts

## Template Structure

```
# Task: {{specific_task}}

## Context
- {{key_background_point_1}}
- {{key_background_point_2}}
- {{additional_context_if_needed}}

## Constraints
- {{constraint_1}}
- {{constraint_2}}

## Expected Output
- Format: {{output_format}}
- Length: {{approximate_length}}
- Style: {{style_guidelines}}

## Examples
{{optional_example}}
```

## Parameters

- `{{specific_task}}`: Clear description of what you want the AI to do (e.g., "Write a product description" or "Analyze the following data")
- `{{key_background_point_X}}`: Essential information needed to complete the task correctly (limit to 2-4 points)
- `{{constraint_X}}`: Limitations or requirements that must be followed (e.g., "Do not include pricing information")
- `{{output_format}}`: The structure, format or file type for the output (e.g., "Bulleted list" or "JSON object")
- `{{approximate_length}}`: Guidelines on how extensive the output should be (e.g., "300-400 words" or "5 bullet points")
- `{{style_guidelines}}`: Tone, voice, and stylistic expectations (e.g., "Professional and formal" or "Conversational and engaging")
- `{{optional_example}}`: A sample of the expected output (highly recommended for first-time tasks)

## Examples

### Example 1: Data Analysis Report

```
# Task: Analyze the provided sales data and create a summary report

## Context
- Data represents quarterly sales figures for 2022
- Company has 3 product lines: Basic, Premium, and Enterprise
- Previous year showed seasonal trends with Q4 strongest

## Constraints
- Focus on significant changes year-over-year
- Do not speculate beyond what the data shows
- Include at least one actionable recommendation

## Expected Output
- Format: Executive summary followed by bullet points
- Length: Approximately 300-400 words
- Style: Professional, data-focused, actionable

## Examples
Executive Summary:
Q2 2022 shows a 15% increase in overall sales compared to Q2 2021, with the Premium product line showing the strongest growth at 23%. This continues the upward trend observed in Q1...
```

### Example 2: Creative Content Creation

```
# Task: Write a product description for our new wireless headphones

## Context
- Target audience: tech-savvy professionals ages 25-40
- Key features: noise cancellation, 30-hour battery life, voice assistant integration
- Main selling points: comfort for all-day wear, premium sound quality

## Constraints
- Keep technical specifications to a minimum
- Don't mention competitors by name
- Focus on benefits, not just features

## Expected Output
- Format: Two paragraphs of flowing text
- Length: 150-200 words
- Style: Modern, enthusiastic but not overly promotional

## Examples
Experience music as it was meant to be heard with our new XDR Wireless Headphones. Designed for professionals who demand the best, these headphones deliver crystal-clear sound while intelligent noise cancellation technology creates your own personal sanctuary of sound—whether you're in a busy office or on a crowded commute...
```

## Variations

### Technical Specification Template
For technical tasks requiring precise instructions:

```
# Task: {{specific_technical_task}}

## Context
- {{technical_background_point_1}}
- {{technical_background_point_2}}
- {{system_dependencies}}

## Requirements
- {{functional_requirement_1}}
- {{functional_requirement_2}}
- {{performance_requirement}}

## Technical Constraints
- {{technical_limitation_1}}
- {{compatibility_requirement}}

## Expected Output
- Format: {{technical_format}}
- Testing Criteria: {{validation_method}}
- Documentation: {{documentation_requirements}}

## Examples
{{technical_example}}
```

### Creative Brief Template
For creative tasks like writing or design:

```
# Task: {{creative_task}}

## Context
- Audience: {{target_audience}}
- Purpose: {{communication_goal}}
- Brand Voice: {{brand_personality}}

## Creative Direction
- {{inspiration_point_1}}
- {{inspiration_point_2}}
- {{emotional_response_desired}}

## Constraints
- {{brand_guideline_1}}
- {{content_restriction}}
- {{technical_limitation}}

## Expected Output
- Format: {{creative_format}}
- Length/Size: {{dimension_guidelines}}
- Style: {{stylistic_direction}}

## Examples
{{creative_example}}
```

## Best Practices

- **Be specific about the task** - Avoid vague instructions like "write something about headphones"; instead use "write a product description for wireless headphones targeting young professionals"
- **Provide only necessary context** - Excessive information can dilute focus and lead to less relevant outputs
- **Use bullet points for clarity** - Breaking information into bullet points makes it easier to process than dense paragraphs
- **Include at least one example** whenever possible - Examples dramatically improve understanding of expectations
- **List constraints explicitly** rather than embedding them in paragraphs - Makes them harder to miss
- **For complex tasks, break down into clear steps** or components - Helps maintain focus and structure
- **Match context to output expectations** - Ensure the context provided supports the expected output format and style

## Related Templates

- **Few-Shot Learning Template**: When you need to teach the AI through multiple examples
- **Chain of Thought Template**: When the task requires step-by-step reasoning
- **Persona-Based Context Template**: When adopting a specific role or perspective would improve results
