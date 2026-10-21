![](https://europe-west1-atp-views-tracker.cloudfunctions.net/working-analytics?notebook=contributing-guide)

# 🚀 Contributing to Agents Towards Production

Thank you for your interest in contributing! This guide covers our standards for creating high-quality tutorials.

## 📢 IMPORTANT: Signup and Tracking

**If your tutorial requires users to sign up for a service:**
1. Place signup instructions prominently at the beginning
2. Provide clear, step-by-step signup guidance
3. Always use UTM-tagged links: `https://service.com/?utm_source=agents-towards-production&utm_medium=github&utm_campaign=tutorial`
4. Include screenshots of the signup process

## 📂 Tutorial Structure

### Required Files
Each tutorial folder must contain:

1. **README.md** - High-level overview explaining:
   - What the tutorial covers
   - Motivation and benefits
   - Key methods and concepts
   - What you will learn
   - Link to the full tutorial notebook

2. **Documentation** (choose one):
   - **Jupyter notebook (`.ipynb`)** - Interactive guide with code cells (use informative filename)
   - **OR `tutorial.md`** - Comprehensive guide with extensive screenshots

3. **Working Code**: `app.py` or equivalent main file (well-commented)

4. **Dependencies**: `requirements.txt` with specific versions

5. **Assets**: `assets/` folder for images, videos, and media

### Example Structure
```
tutorials/your-tutorial-name/
├── README.md                     # High-level overview and motivation
├── app.py                        # Main application code
├── tutorial.md or .ipynb         # Documentation
├── requirements.txt              # Dependencies
└── assets/                       # Media files
    ├── step1_screenshot.png      # Screenshots for each step
    └── final_result.png          # End result
```

## 📝 Tutorial Content Structure

1. **README.md** - High-level overview with motivation, benefits, key methods, and what you'll learn
2. **Title and Overview** - Clear motivation, benefits, and key methods
3. **Detailed Explanation** - Cover key components and method details
4. **Visual Representation** - Include diagrams (use Mermaid → SVG in assets/)
5. **Implementation** - Step-by-step with code blocks and screenshots
6. **Usage Example** - Practical demonstration
7. **External Tool Integration** - Screenshots for each action
8. **Additional Considerations** - Limitations and improvements

## 🎯 Content Quality Standards

### Overview and Motivation
- Start with comprehensive overview explaining motivation, benefits, and methods
- Help readers understand they're learning horizontal concepts applicable to their use cases
- Clarify implementations are specific examples of broader ideas
- Make explanations detailed enough to understand without running code

### Code Quality
- Break down code into small, clear, well-documented blocks
- Add explanations before every code cell describing what happens and why
- Remove unnecessary outputs (pip logs, debug prints)
- Ensure thorough commenting and readability

### Content Structure
- Keep tutorials focused and optimal length
- Remove non-essential sections
- Maintain logical flow from concept to implementation
- Avoid overly verbose descriptions

### Links and References
- Minimize promotional linking that may cause user drop-off
- Each link appears only once
- All external links must use UTM tracking parameters
- No external blog references
- Focus on high-value content over promotional linking

### Visual Elements
- Only include directly relevant logos
- Maintain clean, professional appearance
- Use consistent formatting throughout

## ✨ Best Practices

### For Notebooks
- Each code cell preceded by explanatory markdown
- Clear unnecessary outputs before committing
- Maintain consistent formatting

### For Markdown
- Include screenshots for every significant step
- Ensure visual clarity throughout the process

## 💻 Code Standards

1. Write clean, readable code following best practices
2. Add clear comments explaining complex logic
3. Use consistent formatting
4. Consider language model review for additional improvements

## 📚 Contribution Process

1. Fork the repository
2. Create feature branch: `git checkout -b feature/AmazingFeature`
3. Commit changes: `git commit -m 'Add some AmazingFeature'`
4. Push to branch: `git push origin feature/AmazingFeature`
5. Open pull request

## ✅ Pre-PR Checklist

- [ ] Tutorial follows required structure with all required files
- [ ] **README.md** included with high-level overview, motivation, key methods, and what you'll learn
- [ ] Code runs without errors and is well-commented
- [ ] Dependencies listed with appropriate versions
- [ ] No sensitive information (API keys, etc.)
- [ ] **Content Quality:**
  - [ ] Clear overview and motivation at beginning
  - [ ] Appropriately sized, well-documented code blocks
  - [ ] Each code cell has explanatory text
  - [ ] Optimal tutorial length
  - [ ] All links use UTM tracking
  - [ ] No excessive/promotional linking or external blog references
  - [ ] Self-contained, educational content
- [ ] **Visual Elements:**
  - [ ] Only relevant logos included
  - [ ] Clean, professional appearance
  - [ ] Consistent formatting throughout


**Happy contributing!** 🚀
