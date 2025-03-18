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

        # Selection box for choosing the distribution
        distribution = st.selectbox(
            "Choose a random number generator:",
            ["rand (Uniform)", "randn (Normal)", "randint (Random Integers)", "choice (Random Selection)",
             "beta (Beta Distribution)", "exponential (Exponential Distribution)", "poisson (Poisson Distribution)"]
        )

        sample_size = st.slider("Sample Size", min_value=10, max_value=1000, value=100, step=10)
        bins = st.slider("Number of Bins", min_value=5, max_value=50, value=20)

        data, title = self.generate_random_data(distribution, sample_size)

        # Plot the histogram
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.hist(data, bins=bins, density=True, alpha=0.7, color='peru', edgecolor='black')
        ax.set_title(title)
        ax.set_xlabel("Value")
        ax.set_ylabel("Density")
        st.pyplot(fig)

        # Additional feature: Find min/max indices in any random distribution
        random_array = data[:10]  # Take the first 10 elements for clarity
        st.write("Generated Random Array:", random_array)
        
        if st.button("Find Arg Max"):
            st.write("### Understanding Argmax")
            st.write("Argmax returns the index of the maximum value in an array. This is useful for finding where the highest value occurs.")
            max_value = random_array.max()
            max_index = random_array.argmax()
            st.write(f"Max Value: {max_value} at Index {max_index}")
        
        if st.button("Find Arg Min"):
            st.write("### Understanding Argmin")
            st.write("Argmin returns the index of the minimum value in an array. This helps locate the lowest value in the dataset.")
            min_value = random_array.min()
            min_index = random_array.argmin()
            st.write(f"Min Value: {min_value} at Index {min_index}")

    def generate_random_data(self, distribution, sample_size):
        """Generate random data based on selected distribution."""
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
        return np.array([]), "Unknown Distribution"

    def display_array_transformations(self):
        """Handle numpy array transformations and visualization."""
        st.title("Shape & Shift: NumPy Array Playground")
        st.write("Experiment with NumPy arrays! Generate sequences, reshape them into grids, and "
             "apply mathematical transformations. See how numbers shift and change in real-time.")

        array_size = st.slider("Select array size (0 to N):", min_value=5, max_value=100, value=25, step=5)
        arr = np.arange(array_size)

        st.write("Generated 1D array:")
        st.code(arr)

        rows = st.slider("Rows:", min_value=1, max_value=array_size, value=5)
        cols = st.slider("Columns:", min_value=1, max_value=array_size, value=5)

        reshaped_array = self.reshape_array(arr, rows, cols, array_size)

        operation = st.selectbox("Choose an operation:", ["None", "Multiply by 2", "Add 5", "Square Elements"])
        transformed_array = self.apply_operation(arr, operation)

        st.code(transformed_array)

        self.plot_array_transformation(arr, transformed_array)

if __name__ == "__main__":
    NumPyVizApp()
