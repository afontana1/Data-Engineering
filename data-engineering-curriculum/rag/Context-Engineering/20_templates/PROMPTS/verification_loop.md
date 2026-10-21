# Verification Loop Template

## Summary
A template for implementing self-verification processes that catch errors, validate results, and improve overall reliability through structured checking mechanisms.

## Context & Application
Use this template when accuracy is critical and you want to build explicit verification into the reasoning process. The verification loop reduces errors by encouraging systematic checking of assumptions, calculations, and conclusions before finalizing results.

This template is ideal for:
- Tasks with high stakes where errors could be costly
- Complex calculations or logical reasoning chains
- Situations prone to common reasoning fallacies
- Cases where thoroughness is more important than speed
- Any task where verifiability of results matters

## Template Structure

```
# Task: {{task_description}}

## Approach
Complete this task using a verification loop:

1. Initial Solution
   - {{solution_approach}}
   - Develop your initial answer

2. Verification Process
   - Check assumptions: {{assumption_verification}}
   - Verify calculations/logic: {{process_verification}}
   - Test edge cases: {{edge_case_verification}}
   - Consider alternatives: {{alternative_verification}}

3. Error Correction
   - Identify any issues found during verification
   - Make necessary corrections

4. Final Answer
   - Present your verified solution
   - Note any uncertainty or limitations

## Expected Output
Show your complete process including initial solution, verification steps, any corrections, and final verified answer.
```

## Parameters

- `{{task_description}}`: Clear description of the task to complete
- `{{solution_approach}}`: Method to use for initial solution (e.g., "Use algebraic equations")
- `{{assumption_verification}}`: How to verify assumptions (e.g., "Confirm all variables are correctly interpreted")
- `{{process_verification}}`: How to check calculations or logic (e.g., "Recalculate using a different method")
- `{{edge_case_verification}}`: Specific edge cases to check (e.g., "Test with boundary values")
- `{{alternative_verification}}`: Alternative approaches to verify results (e.g., "Solve using a different technique")

## Examples

### Example 1: Mathematical Problem Verification

```
# Task: Calculate the future value of an investment of $10,000 with an annual interest rate of 5% compounded monthly over 10 years.

## Approach
Complete this task using a verification loop:

1. Initial Solution
   - Use the compound interest formula: P(1 + r/n)^(nt)
   - Calculate the result with the given values

2. Verification Process
   - Check assumptions: Verify the formula is appropriate for this problem
   - Verify calculations: Recalculate step by step, checking each arithmetic operation
   - Test edge cases: Calculate for 1 year and confirm it matches expected growth
   - Consider alternatives: Calculate using the FV = P * e^(rt) formula as a cross-check

3. Error Correction
   - Identify any discrepancies between the two calculation methods
   - Check for common errors (decimal place mistakes, incorrect exponents)
   - Make corrections if needed

4. Final Answer
   - Present the verified future value
   - Express with appropriate precision and units

## Expected Output
Show your complete process including initial solution, verification steps, any corrections, and final verified answer.
```

### Example 2: Code Review Verification

```
# Task: Review the following Python function that calculates the factorial of a number and identify any bugs or issues.

```python
def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n-1)
```

## Approach
Complete this task using a verification loop:

1. Initial Review
   - Analyze the code line by line
   - Identify any potential issues in the implementation

2. Verification Process
   - Check assumptions: Verify the recursive approach is appropriate
   - Verify logic: Trace the execution for sample inputs (n=3, n=0)
   - Test edge cases: Consider negative numbers, large inputs, and non-integer inputs
   - Consider alternatives: Compare with an iterative implementation

3. Issue Identification
   - List any bugs, edge cases, or performance issues found
   - Categorize issues by severity (critical, moderate, minor)

4. Final Assessment
   - Provide a verified assessment of the code quality
   - Suggest specific improvements or fixes

## Expected Output
Show your complete process including initial review, verification steps, issues found, and final assessment with recommendations.
```

## Variations

### Triple Check Verification
For critical tasks requiring multiple verification approaches:

```
# Task: {{task_description}}

## Approach
Complete this task with triple verification:

1. Initial Solution
   - {{solution_approach}}

2. First Verification: Alternative Method
   - Solve the same problem using a different approach
   - Compare results with initial solution

3. Second Verification: Error Analysis
   - Identify potential error sources in both methods
   - Check for these specific errors

4. Third Verification: Test Cases
   - Test with {{test_case_1}}
   - Test with {{test_case_2}}

5. Final Answer
   - Reconcile any differences between verification methods
   - Present final verified solution

## Expected Output
Complete process with all three verification approaches and final reconciled answer.
```

### Peer Review Simulation
For stimulating different perspectives on the same problem:

```
# Task: {{task_description}}

## Approach
Simulate a peer review process:

1. Initial Solution
   - Solve the problem using {{primary_method}}

2. Reviewer A Perspective
   - Critically examine the solution from the perspective of {{reviewer_A_expertise}}
   - Identify potential issues or improvements

3. Reviewer B Perspective
   - Examine the solution from the perspective of {{reviewer_B_expertise}}
   - Identify different potential issues or improvements

4. Reconciliation
   - Address all raised concerns
   - Incorporate valid suggestions

5. Final Solution
   - Present the improved solution after review

## Expected Output
Initial solution, both reviewer perspectives, reconciliation process, and final improved solution.
```

### Progressive Refinement Verification
For iteratively improving solutions:

```
# Task: {{task_description}}

## Approach
Use progressive refinement:

1. Draft Solution (Version 1)
   - Quick first attempt at the problem

2. Analysis of Version 1
   - Identify weaknesses and improvement areas

3. Refined Solution (Version 2)
   - Address identified issues

4. Verification of Version 2
   - Test against original requirements
   - Check for new issues introduced

5. Final Solution (Version 3)
   - Make final refinements
   - Verify completeness and correctness

## Expected Output
All three versions with analyses and verification steps between versions.
```

## Best Practices

- **Use different methods for verification** than for the initial solution
- **Include both conceptual and computational verification** - check both the approach and the execution
- **Anticipate common errors** specific to the task type and verify against them
- **For mathematical problems**, verify with different formulas or approximation methods
- **For logical arguments**, check for fallacies and test with counterexamples
- **For complex tasks**, verify components separately before verifying the whole
- **Document verification steps explicitly** - don't just say "verified" but explain how
- **Consider both false positives and false negatives** in your verification
- **Use order-of-magnitude checks** for numerical problems to catch major errors
- **For critical tasks**, implement multiple independent verification methods

## Related Templates

- **Chain of Thought Template**: The foundation that verification loops build upon
- **Task Decomposition Template**: Useful for breaking complex verification into manageable parts
- **Adversarial Thinking Template**: For verification through challenging assumptions
- **Recursive Self-Improvement Template**: For iteratively enhancing verification processes
