# Few-Shot Learning Template

## Summary
A template for teaching AI systems through examples, enabling them to learn patterns and apply them to new cases without explicit instructions.

## Context & Application
Use this template when you want the AI to learn from examples rather than from explicit rules or instructions. Few-shot learning is powerful because it shows rather than tells, allowing the AI to infer patterns and apply them to new situations.

This template is ideal for:
- Tasks that are difficult to explain but easy to demonstrate
- Pattern-based tasks where examples communicate the pattern better than rules
- Situations where you want consistent formatting or style
- Teaching nuanced judgments or classifications

## Template Structure

```
# Task: {{task_description}}

## Examples

### Example 1
Input: {{input_1}}
Output: {{output_1}}

### Example 2
Input: {{input_2}}
Output: {{output_2}}

### Example 3
Input: {{input_3}}
Output: {{output_3}}

## Your Turn
Input: {{new_input}}
Output:
```

## Parameters

- `{{task_description}}`: Brief description of the task to perform (e.g., "Classify the sentiment of these reviews")
- `{{input_X}}`: Example inputs that demonstrate the pattern (3-5 examples recommended)
- `{{output_X}}`: Corresponding outputs that show the expected response for each input
- `{{new_input}}`: The new case you want the AI to handle using the pattern it learned

## Examples

### Example 1: Sentiment Classification

```
# Task: Classify the sentiment of customer feedback as positive, negative, or neutral

## Examples

### Example 1
Input: "The product arrived on time and works perfectly. Couldn't be happier with my purchase!"
Output: Positive

### Example 2
Input: "Delivery was quick but the product has several scratches on the surface."
Output: Neutral

### Example 3
Input: "Terrible customer service. Had to call three times and still haven't resolved my issue."
Output: Negative

## Your Turn
Input: "Package was delivered two days late, but the quality of the item exceeded my expectations."
Output:
```

### Example 2: Data Transformation

```
# Task: Convert the given product information into a standardized JSON format

## Examples

### Example 1
Input: 
Product: Wireless Headphones
Brand: SoundCore
Price: $79.99
Features: Noise cancellation, 30-hour battery, Bluetooth 5.0

Output:
```json
{
  "product_name": "Wireless Headphones",
  "manufacturer": "SoundCore",
  "price_usd": 79.99,
  "specifications": [
    "Noise cancellation",
    "30-hour battery",
    "Bluetooth 5.0"
  ]
}
```

### Example 2
Input:
Product: Smart Watch Pro
Brand: TechFit
Price: $129.95
Features: Heart rate monitor, GPS tracking, Water resistant

Output:
```json
{
  "product_name": "Smart Watch Pro",
  "manufacturer": "TechFit",
  "price_usd": 129.95,
  "specifications": [
    "Heart rate monitor",
    "GPS tracking",
    "Water resistant"
  ]
}
```

## Your Turn
Input:
Product: Portable Bluetooth Speaker
Brand: AudioMax
Price: $45.50
Features: Waterproof, 12-hour playback, Built-in microphone

Output:
```

## Variations

### Zero-Shot Extension
For when you have no examples but can describe the pattern:

```
# Task: {{task_description}}

## Pattern
{{detailed_pattern_description}}

## Format
{{output_format_specification}}

## Your Turn
Input: {{new_input}}
Output:
```

### One-Shot Learning
For simple patterns that can be communicated with a single example:

```
# Task: {{task_description}}

## Example
Input: {{input_example}}
Output: {{output_example}}

## Your Turn
Input: {{new_input}}
Output:
```

### Many-Shot Learning
For complex patterns requiring many examples:

```
# Task: {{task_description}}

## Examples
[Examples 1-10 formatted as input/output pairs]

## Test Cases
[Additional examples to validate understanding]

## Your Turn
Input: {{new_input}}
Output:
```

## Best Practices

- **Use diverse examples** that cover different cases and edge conditions
- **Order examples strategically** from simple to complex to build understanding
- **Include 3-5 examples** for most tasks (fewer for simple patterns, more for complex ones)
- **Ensure consistency** in formatting across all examples
- **Choose representative examples** that clearly demonstrate the pattern
- **Make examples distinct enough** to highlight the pattern rather than superficial similarities
- **For classification tasks**, include examples of all possible categories
- **For generative tasks**, show range in style, length, and content as appropriate
- **Test the pattern** by trying different inputs to ensure the AI has properly learned it

## Related Templates

- **Minimal Context Template**: When examples aren't necessary and direct instructions suffice
- **Chain of Thought Template**: When you need to demonstrate reasoning processes step-by-step
- **Pattern and Anti-Pattern Template**: When showing both good and bad examples helps clarify expectations
