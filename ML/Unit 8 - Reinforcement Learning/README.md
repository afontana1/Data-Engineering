# ✨ All RL Algorithms from Scratch

<div align="center">

![made-with-Python](https://img.shields.io/badge/Made%20with-Python-blue)
![made-with-Jupyter](https://img.shields.io/badge/Made%20with-Jupyter-orange)
![Educational](https://img.shields.io/badge/Purpose-Educational-green)
![RL Algorithms](https://img.shields.io/badge/RL%20Algorithms-18-brightgreen)
![Language](https://img.shields.io/github/languages/top/fareedkhan-dev/all-rl-algorithms)
![Maintained](https://img.shields.io/maintenance/yes/2025)
![Last Commit](https://img.shields.io/github/last-commit/fareedkhan-dev/all-rl-algorithms)
![Size](https://img.shields.io/github/repo-size/fareedkhan-dev/all-rl-algorithms)
[![contributions welcome](https://img.shields.io/static/v1.svg?label=Contributions&message=Welcome&color=0059b3&style=flat-square)](https://github.com/fareedkhan-dev/all-rl-algorithms)
![License](https://img.shields.io/github/license/fareedkhan-dev/all-rl-algorithms)
![Stars](https://img.shields.io/github/stars/fareedkhan-dev/all-rl-algorithms?style=social)

</div>


This repository is a collection of Python implementations of various Reinforcement Learning (RL) algorithms. The *primary* goal is **educational**: to get a deep and intuitive understanding of how these algorithms work under the hood. 🧠 Due to the recent explosion in the AI domain especially Large Language Models, and many more applications it is important to understand core reinforcement learning algorithms.

This repository also includes a [comprehensive cheat sheet](cheatsheet.md) summarizing key concepts and algorithms for quick reference.

**This is *not* a performance-optimized library!** I prioritize readability and clarity over speed and advanced features. Think of it as your interactive textbook for RL.


## 📌 Updates

| Date | Update |
|------|--------|
| **2 April 2025** | Added a comprehensive [RL Cheat Sheet](cheatsheet.md) summarizing all implemented algorithms and core concepts. Repository now includes **18 algorithm notebooks**. |
| **30 March 2025** | Added **18 new algorithms**. |





## 🌟 Why This Repo?

- **Focus on Fundamentals:** Learn the core logic *without* the abstraction of complex RL libraries. We use basic libraries (NumPy, Matplotlib, PyTorch) to get our hands dirty. 🛠️
- **Beginner-Friendly:** Step-by-step explanations guide you through each algorithm, even if you're new to RL. 👶
- **Interactive Learning:** Jupyter Notebooks provide a playground for experimentation. Tweak hyperparameters, modify the code, and *see* what happens! 🧪
- **Clear and Concise Code:** We strive for readable code that closely mirrors the mathematical descriptions of the algorithms. No unnecessary complexity! 👌
- **Quick Reference:** Includes a detailed [Cheat Sheet](cheatsheet.md) for fast lookups of formulas, pseudocode, and concepts.

## 🗺️ Roadmap: Algorithms Covered (and Coming Soon)

The repository currently includes implementations of the following RL algorithms, with more planned:

**Algorithm Quick Reference**

| #  | Algorithm | Type | Description | Notebook |
|----|-----------|------|-------------|----------|
| 01 | **Simple Exploration Bot** | Basic | Demonstrates the core loop: interacting with the environment and storing experienced rewards for later action selection. *Does not actually learn in a true RL sense*. | [![Open Notebook](https://img.shields.io/badge/Open-Notebook-blue)](01_simple_rl.ipynb) |
| 02 | **Q-Learning** | Value-Based | Learns an optimal action-value function (Q-function) through the Bellman equation, enabling goal-directed behavior. | [![Open Notebook](https://img.shields.io/badge/Open-Notebook-blue)](02_q_learning.ipynb) |
| 03 | **SARSA** | Value-Based | On-policy learning algorithm that updates Q-values based on the actions actually taken, often resulting in more cautious behavior. | [![Open Notebook](https://img.shields.io/badge/Open-Notebook-blue)](03_sarsa.ipynb) |
| 04 | **Expected SARSA** | Value-Based | On-policy with reduced variance, updates Q-values using the expected value of next actions, balancing exploration and exploitation. | [![Open Notebook](https://img.shields.io/badge/Open-Notebook-blue)](04_expected_sarsa.ipynb) |
| 05 | **Dyna-Q** | Model-Based | Combines direct RL (Q-learning) with planning via a learned environment model, improving sample efficiency. | [![Open Notebook](https://img.shields.io/badge/Open-Notebook-blue)](05_dyna_q.ipynb) |
| 06 | **REINFORCE** | Policy-Based | A Monte Carlo policy gradient method that directly optimizes a parameterized policy based on complete episode returns. | [![Open Notebook](https://img.shields.io/badge/Open-Notebook-blue)](06_reinforce.ipynb) |
| 07 | **Proximal Policy Optimization (PPO)** | Actor-Critic | State-of-the-art, stabilizes policy updates via clipped surrogate objective. Balances exploration and exploitation efficiently. | [![Open Notebook](https://img.shields.io/badge/Open-Notebook-blue)](07_ppo.ipynb) |
| 08 | **Advantage Actor-Critic (A2C)** | Actor-Critic | Uses a critic to estimate advantages, reducing variance compared to REINFORCE. Synchronous updates. | [![Open Notebook](https://img.shields.io/badge/Open-Notebook-blue)](08_a2c.ipynb) |
| 09 | **Asynchronous Advantage Actor-Critic (A3C)** | Actor-Critic | An asynchronous version of A2C, using multiple workers to collect data and update the global network. | [![Open Notebook](https://img.shields.io/badge/Open-Notebook-blue)](09_a3c.ipynb) |
| 10 | **Deep Deterministic Policy Gradient (DDPG)** | Actor-Critic | Uses a separate action function to estimate Q-values, allowing operation in continuous action spaces. | [![Open Notebook](https://img.shields.io/badge/Open-Notebook-blue)](10_ddpg.ipynb) |
| 11 | **Soft Actor-Critic (SAC)** | Actor-Critic | Off-policy actor-critic for continuous action spaces, based on maximum entropy RL. | [![Open Notebook](https://img.shields.io/badge/Open-Notebook-blue)](11_sac.ipynb) |
| 12 | **Trust Region Policy Optimization (TRPO)** | On-Policy | Imposes a limit on how much the policy distribution can change in a single step. | [![Open Notebook](https://img.shields.io/badge/Open-Notebook-blue)](12_trpo.ipynb) |
| 13 | **Deep Q-Network (DQN)** | Value-Based | Combines Q-learning with deep neural networks to handle high-dimensional state spaces. | [![Open Notebook](https://img.shields.io/badge/Open-Notebook-blue)](13_dqn.ipynb) |
| 14 | **Multi-Agent DDPG (MADDPG)** | Actor-Critic | Extends DDPG to multi-agent settings, addressing non-stationarity problems. | [![Open Notebook](https://img.shields.io/badge/Open-Notebook-blue)](14_maddpg.ipynb) |
| 15 | **QMIX** | On-Policy Actor-Critic | Value-based MARL algorithm for cooperative tasks with value function factorization. | [![Open Notebook](https://img.shields.io/badge/Open-Notebook-blue)](15_qmix.ipynb) |
| 16 | **Hierarchical Actor-Critic (HAC)** | Hierarchical | Decomposes long, complex tasks into manageable sub-problems. | [![Open Notebook](https://img.shields.io/badge/Open-Notebook-blue)](16_hac.ipynb) |
| 17 | **Monte Carlo Tree Search (MCTS)** | Planning | Best-first search algorithm guided by Monte Carlo rollouts. | [![Open Notebook](https://img.shields.io/badge/Open-Notebook-blue)](17_mcts.ipynb) |
| 18 | **PlaNet (Deep Planning Network)** | Planning | Model-based RL agent that learns a world model to plan future actions. | [![Open Notebook](https://img.shields.io/badge/Open-Notebook-blue)](18_planet.ipynb) |


Each algorithm has its own Jupyter Notebook (`.ipynb`) file with a detailed explanation and implementation.

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

## ⚠️ Disclaimer: Bugs and Incomplete Implementations

This repository is primarily for learning! While effort has been taken, some notebooks (especially the more complex ones like HAC) may contain bugs, incomplete implementations, or simplifications for clarity. If you find any issues, feel free to create a pull request.


## 🤝 Contributing

Contributions are welcome! Here's how you can help:

- 🐞 **Fix Bugs:** Found an error or a way to improve the code? Submit a pull request!
- ✍️ **Improve Explanations:** Clarify confusing sections in the notebooks or add more helpful comments.
- ⚡ **Add More Algorithms:** Implement algorithms currently marked as "Planned."
- 📊 **Create More Visualizations:** Develop insightful visualizations to better understand the learning process.
- 🌍 **Add More Environment Examples:** Implement known RL tasks.
- 📐 **Follow Guidelines:** Please follow the project's coding style and documentation guidelines.  
- 📝 **Open Discussions:** Create a new issue to discuss your contribution before starting work.


## Contributor Wall of Fame

[![Contributors](https://contrib.rocks/image?repo=FareedKhan-dev/all-rl-algorithms)](https://github.com/FareedKhan-dev/all-rl-algorithms/graphs/contributors)