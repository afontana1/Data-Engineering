# ✨ All RL Algorithms from Scratch

This repository is a collection of Python implementations of various Reinforcement Learning (RL) algorithms. The *primary* goal is **educational**: to get a deep and intuitive understanding of how these algorithms work under the hood. 🧠 Due to the recent explosion in the AI domain especially Large Language Models, and many more applications it is important to understand core reinforcement learning algorithms.

This repository also includes a [comprehensive cheat sheet](cheatsheet.md) summarizing key concepts and algorithms for quick reference.

**This is *not* a performance-optimized library!** I prioritize readability and clarity over speed and advanced features. Think of it as your interactive textbook for RL.


## 🌟 Why This Repo?

- **Focus on Fundamentals:** Learn the core logic *without* the abstraction of complex RL libraries. We use basic libraries (NumPy, Matplotlib, PyTorch) to get our hands dirty. 🛠️
- **Beginner-Friendly:** Step-by-step explanations guide you through each algorithm, even if you're new to RL. 👶
- **Interactive Learning:** Jupyter Notebooks provide a playground for experimentation. Tweak hyperparameters, modify the code, and *see* what happens! 🧪
- **Clear and Concise Code:** We strive for readable code that closely mirrors the mathematical descriptions of the algorithms. No unnecessary complexity! 👌
- **Quick Reference:** Includes a detailed [Cheat Sheet](cheatsheet.md) for fast lookups of formulas, pseudocode, and concepts.

## 📚 RL Cheat Sheet

Complementing the detailed notebooks, a comprehensive **[RL Cheat Sheet](cheatsheet.md)** is included in this repository. It serves as a quick reference guide covering:

*   Core RL Concepts (MDPs, Bellman Equations, etc.)
*   Algorithm Summaries (Core Idea, Math, Pseudocode)
*   Key Hyperparameters and Tuning Tips
*   Pros & Cons and Use Cases
*   Code Snippets for key update rules

>➡️ **[View the RL Cheat Sheet here](cheatsheet.md)**

## 🛠️ Installation and Setup  

Follow these steps to get started:  

1. **Clone the repository:**  

   ```bash
   git clone https://github.com/fareedkhan-dev/all-rl-algorithms.git
   cd all-rl-algorithms
   ```

2.  **Create a virtual environment (using uv):**
(⚡ faster alternative to python -m venv)

    ```bash
    # Initialize a new project (⭐ only if starting fresh, not when cloning)
    uv init  

    # Create a virtual environment
    uv venv  
    ```
3. **Activate the virtual environment:**
   
    ```bash
    # Windows
    .venv\Scripts\activate  

    # macOS / Linux
    source .venv/bin/activate
    ```

4.  **Install dependencies:**

    ```bash
    uv add -r requirements.txt
    ```
5.  **Multiprocessing in A3C:** Please run `a3c_training.py` in the terminal instead of the jupyter notebook to avoid any complication from multiprocessing.

> 💡 Note: If you don’t have uv installed yet, you can install it via:
```bash
pip install uv
```

## 🧑‍🏫 How to Use This Repo: A Learning Guide

1.  **Start with the Basics (`01_simple_rl.ipynb`):** This notebook introduces fundamental RL concepts like states, actions, rewards, and policies.
2.  **Explore Core Algorithms:** Dive into the individual notebooks for Q-Learning (`02_q_learning.ipynb`), SARSA (`03_sarsa.ipynb`), and REINFORCE (`06_reinforce.ipynb`). Understand their update rules, strengths, and limitations.
3.  **Analyze the Code:** Carefully read the code comments, which explain the purpose of each function and variable.
4.  **Experiment!:** This is where the real learning begins. Try these:
    *   Change hyperparameters (learning rate, discount factor, exploration rate) and observe the effect on learning curves.
    *   Modify the environment (e.g., change the grid size, add obstacles) and see how the algorithms adapt.
    *   Extend the algorithms (e.g., implement epsilon decay, add a baseline to REINFORCE).
5.  **Consult the Cheat Sheet:** Refer to the **[RL Cheat Sheet](cheatsheet.md)** for quick summaries, formulas, and pseudocode while studying the notebooks.
6.  **Tackle Advanced Methods:** Gradually work through the more complex notebooks on DQN (`13_dqn.ipynb`), Actor-Critic (`08_a2c.ipynb`), PPO (`07_ppo.ipynb`), Model-Based RL with PlaNet (`18_planet.ipynb`), and multi-agent learning with MADDPG (`14_maddpg.ipynb`) and QMIX (`15_qmix.ipynb`).
7.  **Run the A3C Implementation:** Due to complexities with multiprocessing in Jupyter Notebooks, the A3C implementation is in `a3c_training.py`. Run it from the command line: `python a3c_training.py`

## 🖼️ What You'll See: Visualizing Learning

Each notebook includes visualizations to help you understand the agent's behavior:

-   **Learning Curves:** Plots of episode rewards, episode lengths, and loss functions.
-   **Q-Table Visualizations:** Heatmaps to visualize Q-values across the state space (tabular methods).
-   **Policy Grids:** Arrows showing the learned policy (action choice) in each state.
-   **More Advanced Visualizations:** Visualizations may depend on each particular algorithm.