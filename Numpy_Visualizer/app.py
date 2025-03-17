import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

class NumPyVizApp:
    def __init__(self):
        """initialize app"""
        self.option = st.sidebar.radio("Choose a section:", ["Exploring Probability: Random Data Generator", "Shape & Shift: NumPy Array Playground"])
        self.run_app()

    def run_app(self):
        """run the selected section of app"""
        if self.option == "Exploring Probability: Random Data Generator":
            self.display_random_distributions()
        elif self.option == "Shape & Shift: NumPy Array Playground":
            self.display_array_transformations()

    def display_random_distributions(self):
        """Handle visualization of different NumPy random distributions."""
        
        st.title("Exploring Probability: Random Data Generator")
        st.write("Visualize different probability distributions and understand randomness in data. "
                "Choose from uniform, normal, Poisson, and more to generate and explore random samples.")

        # Dictionary for explanations
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

        # Selection box for choosing the distribution
        distribution = st.selectbox(
            "Choose a random number generator:",
            list(explanations.keys())
        )

        # Show description dynamically based on selection
        st.markdown(f"### 📌 About {distribution}")
        st.markdown(explanations[distribution])

        # Controls for generating the data
        sample_size = st.slider("Sample Size", min_value=100, max_value=100000, value=10000, step=100)
        bins = st.slider("Number of Bins", min_value=5, max_value=50, value=20)

        data, title = self.generate_random_data(distribution, sample_size)

        # Plot the histogram
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.hist(data, bins=bins, density=True, alpha=0.7, color='peru', edgecolor='black')
        ax.set_title(title)
        ax.set_xlabel("Value")
        ax.set_ylabel("Density")
        st.pyplot(fig)

        # 📚 References Section
        st.markdown("### 📚 References:")
        st.markdown(
            """
            - [NumPy Random Documentation](https://numpy.org/doc/stable/reference/random/index.html)
            - [Scipy Statistical Distributions](https://docs.scipy.org/doc/scipy/tutorial/stats.html)
            """
        )

    def generate_random_data(self, distribution, sample_size):
        """generate random data based on what was selected"""
        if distribution == "rand (Uniform)":
            return np.random.rand(sample_size), "Uniform Distribution (rand)"
        elif distribution == "randn (Normal)":
            return np.random.randn(sample_size), "Normal Distribution (randn)"
        elif distribution == "randint (Random Integers)":
            return np.random.randint(0, 100, sample_size), "Random Integers (randint)"
        elif distribution == "choice (Random Selection)":
            choices = np.array([10, 20, 30, 40, 50])
            return np.random.choice(choices, sample_size), "Random Selection (choice)"
        elif distribution == "beta (Beta Distribution)":
            return np.random.beta(2, 5, sample_size), "Beta Distribution (beta)"
        elif distribution == "exponential (Exponential Distribution)":
            return np.random.exponential(1.0, sample_size), "Exponential Distribution (exponential)"
        elif distribution == "poisson (Poisson Distribution)":
            return np.random.poisson(5, sample_size), "Poisson Distribution (poisson)"
        return None, ""

    def display_array_transformations(self):
        """handle numpy array transformations and viz."""
        st.title("Shape & Shift: NumPy Array Playground")
        st.write("Experiment with NumPy arrays! Generate sequences, reshape them into grids, and "
             "apply mathematical transformations. See how numbers shift and change in real-time.")

        # Step 1: Generate a NumPy array
        array_size = st.slider("Select array size (0 to N):", min_value=5, max_value=100, value=25, step=5)
        arr = np.arange(array_size)

        st.write("Generated 1D array:")
        st.code(arr)

        # Step 2: Reshaping the array
        rows = st.slider("Rows:", min_value=1, max_value=array_size, value=5)
        cols = st.slider("Columns:", min_value=1, max_value=array_size, value=5)

        reshaped_array = self.reshape_array(arr, rows, cols, array_size)

        # Step 3: Apply mathematical operations
        operation = st.selectbox("Choose an operation:", ["None", "Multiply by 2", "Add 5", "Square Elements"])
        transformed_array = self.apply_operation(arr, operation)

        st.code(transformed_array)

        # Step 4: Visualization
        self.plot_array_transformation(arr, transformed_array)

    def reshape_array(self, arr, rows, cols, array_size):
        """Reshapes an array if the dimensions match."""
        if rows * cols == array_size:
            reshaped_array = arr.reshape(rows, cols)
            st.write(f"Reshaped Array ({rows}x{cols}):")
            st.code(reshaped_array)
            return reshaped_array
        else:
            st.warning("Rows × Columns must equal the total number of elements in the array.")
            return arr  # Return original array if reshape isn't possible

    def apply_operation(self, arr, operation):
        """apply selected math operations"""
        if operation == "Multiply by 2":
            return arr * 2
        elif operation == "Add 5":
            return arr + 5
        elif operation == "Square Elements":
            return arr ** 2
        return arr  # Return unchanged array if no operation is selected

    def plot_array_transformation(self, original, transformed):
    
        fig, ax = plt.subplots(figsize=(6, 4))

        # Define exact colors
        original_color = 'tan'
        transformed_color = 'saddlebrown'

        # Plot the original array
        line1, = ax.plot(original, marker='o', linestyle='--', color=original_color, markersize=6, label="Original Array")

        # Only plot transformed array if it's different
        if not np.array_equal(original, transformed):
            line2, = ax.plot(transformed, marker='s', linestyle='-', color=transformed_color, markersize=6, label="Transformed Array")
        else:
            line2 = None  # No transformed array to show

        ax.set_title("Array Transformation", fontsize=12, color='sienna')
        ax.set_xlabel("Index", fontsize=10, color='peru')
        ax.set_ylabel("Value", fontsize=10, color='peru')

        ax.grid(True, linestyle=":", linewidth=0.6, color="tan")

        # Explicitly set the legend colors
        handles = [line1] if line2 is None else [line1, line2]
        ax.legend(handles=handles, loc="upper left", fontsize=10, frameon=True)

        st.pyplot(fig)






# Run the Streamlit App
if __name__ == "__main__":
    NumPyVizApp()
