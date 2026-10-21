# Chain of Thought Template

## Summary
A template for guiding AI systems through explicit step-by-step reasoning processes, improving accuracy and transparency for complex tasks.

## Context & Application
Use this template when a task requires careful reasoning or when the process of reaching a conclusion is as important as the conclusion itself. By breaking down complex thinking into explicit steps, chain of thought prompting improves accuracy, enables verification, and makes the reasoning process transparent.

This template is ideal for:
- Complex problem-solving tasks
- Situations requiring logical reasoning
- Multi-step calculations or analyses
- Tasks where explaining the "why" is important
- Reducing errors on challenging problems

## Template Structure

```
# Task: {{task_description}}

## Approach
Think through this step-by-step:

1. {{first_reasoning_step}}
2. {{second_reasoning_step}}
3. {{additional_steps_as_needed}}
4. Formulate your conclusion based on this reasoning.

## Expected Output
Provide your complete reasoning process and then your final answer.
```

## Parameters

- `{{task_description}}`: Clear description of the problem to solve or question to answer
- `{{first_reasoning_step}}`: Initial step in the reasoning process (e.g., "Identify the key variables")
- `{{second_reasoning_step}}`: Next logical step (e.g., "Determine the relationships between variables")
- `{{additional_steps_as_needed}}`: Further steps to guide complete reasoning

## Examples

### Example 1: Mathematical Problem Solving

```
# Task: Solve the following word problem

A store sells notebooks for $4 each and pens for $2 each. Emma bought some notebooks and twice as many pens. If she spent $24 in total, how many notebooks did she buy?

## Approach
Think through this step-by-step:

1. Define variables for what we're looking for
2. Set up equations based on the given information
3. Solve the equations to find the unknown values
4. Verify your answer makes sense with the original conditions

## Expected Output
Provide your complete reasoning process and then your final answer.
```

### Example 2: Ethical Decision Analysis

```
# Task: Analyze the ethical implications of the following scenario

A pharmaceutical company has developed a drug that shows promise for treating a rare disease. The clinical trials indicate 70% efficacy but also reveal potentially serious side effects in 15% of patients. The company needs to decide whether to bring this drug to market.

## Approach
Think through this step-by-step:

1. Identify the key stakeholders in this scenario
2. Analyze the potential benefits of making the drug available
3. Consider the potential harms and risks involved
4. Evaluate alternative options that might be available
5. Balance competing ethical principles (beneficence, non-maleficence, autonomy, justice)
6. Formulate a nuanced recommendation with potential safeguards or conditions

## Expected Output
Provide your complete reasoning process and then your final recommendation.
```

## Variations

### Self-Prompted Chain of Thought
For encouraging the AI to develop its own reasoning steps:

```
# Task: {{task_description}}

## Approach
- First, break this problem down into logical steps
- Work through each step systematically
- Show your complete reasoning process
- Only then provide your final answer

## Expected Output
Step-by-step reasoning followed by conclusion.
```

### Guided Problem Decomposition
For highly complex problems requiring more structured guidance:

```
# Task: {{task_description}}

## Problem Decomposition
1. Sub-problem 1: {{sub_problem_description}}
   - Consider: {{relevant_factor_1}}
   - Consider: {{relevant_factor_2}}

2. Sub-problem 2: {{sub_problem_description}}
   - Consider: {{relevant_factor_1}}
   - Consider: {{relevant_factor_2}}

3. Integration: Combine your analyses from the sub-problems

## Expected Output
Analysis of each sub-problem, integration of insights, and final conclusion.
```

### Scenario Analysis Chain of Thought
For decisions requiring consideration of multiple scenarios:

```
# Task: {{decision_task}}

## Approach
Think through this step-by-step:

1. Scenario A: If {{condition_A}} happens
   - Probable outcomes:
   - Benefits:
   - Risks:

2. Scenario B: If {{condition_B}} happens
   - Probable outcomes:
   - Benefits:
   - Risks:

3. Compare scenarios and determine the most robust approach

## Expected Output
Analysis of each scenario and reasoned recommendation.
```

## Best Practices

- **Match reasoning steps to the problem type** - Different problems require different reasoning approaches
- **Be explicit about the reasoning process** - Clearly articulate what thinking should happen at each step
- **Include verification steps** - Add steps to check work or validate conclusions
- **For mathematical problems**, include steps for checking units and order of magnitude
- **For ethical or subjective analyses**, include steps for considering multiple perspectives
- **Don't skip steps** - Breaking reasoning into smaller steps improves accuracy
- **Use 3-7 steps** for most problems - Too few lacks guidance, too many becomes overwhelming
- **Encourage metacognition** - Include steps that prompt reflection on the reasoning process itself
- **For complex problems**, consider breaking into sub-problems before integration

## Related Templates

- **Verification Loop Template**: Extends chain of thought with explicit verification steps
- **Few-Shot Learning Template**: Can be combined to show examples of chain of thought reasoning
- **Metacognitive Reflection Template**: For deeper thinking about the reasoning process itself
