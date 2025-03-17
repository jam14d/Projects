import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# App title
st.title("NumPy Random Number Generator Visualizer")

# Dropdown menu for selecting distribution
distribution = st.selectbox(
    "Choose a random number generator:",
    ["rand (Uniform)", "randn (Normal)", "randint (Random Integers)", 
     "choice (Random Selection)", "beta (Beta Distribution)", 
     "exponential (Exponential Distribution)", "poisson (Poisson Distribution)"]
)

# User selects sample size and bins for histogram
sample_size = st.slider("Sample Size", min_value=100, max_value=100000, value=10000, step=100)
bins = st.slider("Number of Bins", min_value=5, max_value=50, value=20)

# Dictionary of explanations for each random function
explanations = {
    "rand (Uniform)": "The `np.random.rand()` function generates random numbers from a **uniform distribution** "
                      "in the range **[0,1]**. Each number has an equal probability of appearing. "
                      "\n\n**Use case**: Useful for simulations, Monte Carlo methods, and initializing random weights in machine learning.",
    
    "randn (Normal)": "The `np.random.randn()` function generates random numbers from a **standard normal distribution** "
                      "with **mean = 0** and **standard deviation = 1**. It follows the bell-shaped Gaussian curve. "
                      "\n\n**Use case**: Commonly used in statistics, signal processing, and data science applications.",
    
    "randint (Random Integers)": "The `np.random.randint()` function generates **random integers** from a specified range. "
                                 "For example, `np.random.randint(0, 100, size)` produces numbers between 0 and 99. "
                                 "\n\n**Use case**: Useful for random sampling, simulations, and selecting indices randomly.",
    
    "choice (Random Selection)": "The `np.random.choice()` function selects random elements from a given array or list. "
                                 "For example, `np.random.choice([10, 20, 30, 40], size)` picks values randomly from `[10, 20, 30, 40]`."
                                 "\n\n **Use case**: Useful for creating random samples from a predefined dataset.",
    
    "beta (Beta Distribution)": "The `np.random.beta(a, b, size)` function generates numbers from a **beta distribution**, "
                                "which is often used in Bayesian statistics and probability modeling. "
                                "\n\n**Use case**: Used in Bayesian inference, A/B testing, and modeling probabilities between 0 and 1.",
    
    "exponential (Exponential Distribution)": "The `np.random.exponential(scale, size)` function generates numbers from an "
                                              "**exponential distribution**, which models the time between independent events occurring "
                                              "at a constant rate. \n\n**Use case**: Used in queueing theory, finance, and reliability analysis.",
    
    "poisson (Poisson Distribution)": "The `np.random.poisson(lam, size)` function generates numbers from a **Poisson distribution**, "
                                      "which represents the probability of a given number of events occurring in a fixed time or space. "
                                      "\n\n**Use case**: Used in event modeling, epidemiology, and traffic flow analysis."
}

# Generate data based on selection
if distribution == "rand (Uniform)":
    data = np.random.rand(sample_size)
    title = "Uniform Distribution (rand)"
elif distribution == "randn (Normal)":
    data = np.random.randn(sample_size)
    title = "Normal Distribution (randn)"
elif distribution == "randint (Random Integers)":
    data = np.random.randint(0, 100, sample_size)
    title = "Random Integers (randint)"
elif distribution == "choice (Random Selection)":
    choices = np.array([10, 20, 30, 40, 50])
    data = np.random.choice(choices, sample_size)
    title = "Random Selection (choice)"
elif distribution == "beta (Beta Distribution)":
    a, b = 2, 5  # Beta distribution parameters
    data = np.random.beta(a, b, sample_size)
    title = "Beta Distribution (beta)"
elif distribution == "exponential (Exponential Distribution)":
    scale = 1.0  # Lambda = 1
    data = np.random.exponential(scale, sample_size)
    title = "Exponential Distribution (exponential)"
elif distribution == "poisson (Poisson Distribution)":
    lam = 5  # Average rate of occurrence
    data = np.random.poisson(lam, sample_size)
    title = "Poisson Distribution (poisson)"

# Display explanation
st.markdown(f"###Explanation: {distribution}")
st.write(explanations[distribution])

# Plot the histogram
fig, ax = plt.subplots(figsize=(8, 4))
ax.hist(data, bins=bins, density=True, alpha=0.7, color='blue', edgecolor='black')
ax.set_title(title)
ax.set_xlabel("Value")
ax.set_ylabel("Density")

st.pyplot(fig)

# Sources
st.markdown("###References:")
st.markdown(
    """
    - [NumPy Random Documentation](https://numpy.org/doc/stable/reference/random/index.html)
    - [Scipy Statistical Distributions](https://docs.scipy.org/doc/scipy/tutorial/stats.html)
    """
)
