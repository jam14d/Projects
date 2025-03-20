import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

class NumPyVizApp:
    def __init__(self):
        """Initialize the app"""
        self.option = st.sidebar.radio("Choose a section:", [
            "Exploring Probability: Random Data Generator", 
            "Shape & Shift: NumPy Array Playground",
            "Image Channel Extractor"
        ])
        self.run_app()

    def run_app(self):
        """Run the selected section of the app"""
        if self.option == "Exploring Probability: Random Data Generator":
            self.display_random_distributions()
        elif self.option == "Shape & Shift: NumPy Array Playground":
            self.display_array_transformations()
        elif self.option == "Image Channel Extractor":
            self.image_channel_extractor()

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


    ##image stuff
    def image_channel_extractor(self):
        """Upload an image and extract its color channels"""
        st.title("Image Channel Extractor")
        uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
        
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image", use_column_width=True)
            
            image_array = np.array(image)
            st.write("### Image Array Shape:")
            st.code(image_array.shape)

            st.write("### Understanding the Image Array Shape")
            st.markdown(
                """An image is stored as a NumPy array with three values:
                Height (number of rows), Width (number of columns), Channels (color layers: Red, Green, Blue)
                
                Example: (256, 256, 3) means:
                - 256 pixels tall
                - 256 pixels wide
                - 3 color channels (Red, Green, Blue)
                
                Each pixel's value ranges from 0 (dark) to 255 (bright).
                """
            )
            
            if st.button("Extract Red Channel"):
                red_channel = image_array[:, :, 0]
                self.display_channel(red_channel, "Red Channel")
                st.markdown(
                    """A higher red value makes the pixel appear redder and brighter.
                    A lower red value means less red is present, making the pixel darker or influenced by the other channels.
                    (255, 0, 0) = Pure red, 
                    (0, 0, 0) = No red (black)."""
                )
            
            if st.button("Extract Green Channel"):
                green_channel = image_array[:, :, 1]
                self.display_channel(green_channel, "Green Channel")
                st.markdown(
                    """A higher green value makes the pixel appear greener and brighter.
                    A lower green value reduces green intensity, affecting the overall color mix.
                    (0, 255, 0) = Pure green, (0, 0, 0) = No green (black)."""
                )
            
            if st.button("Extract Blue Channel"):
                blue_channel = image_array[:, :, 2]
                self.display_channel(blue_channel, "Blue Channel")
                st.markdown(
                    """A higher blue value makes the pixel appear bluer and brighter.
                    A lower blue value reduces blue intensity, allowing other colors to dominate.
                    (0, 0, 255) = Pure blue, (0, 0, 0) = No blue (black)"""
                )

            if st.button("Show RGB Channels Side by Side"):
                self.display_rgb_channels(image_array)
    
    def display_channel(self, channel, title):
        """Display extracted color channel in grayscale"""
        st.write(f"### {title} Array:")
        st.code(channel)
        fig, ax = plt.subplots()
        ax.imshow(channel, cmap="gray")  # Use grayscale colormap
        ax.axis("off")
        st.pyplot(fig)
    
    def display_rgb_channels(self, image_array):
        """Display all RGB channels side by side"""
        red_channel = image_array[:, :, 0]
        green_channel = image_array[:, :, 1]
        blue_channel = image_array[:, :, 2]
        
        fig, axes = plt.subplots(1, 3, figsize=(12, 4))
        axes[0].imshow(red_channel, cmap="gray")
        axes[0].set_title("Red Channel")
        axes[0].axis("off")
        
        axes[1].imshow(green_channel, cmap="gray")
        axes[1].set_title("Green Channel")
        axes[1].axis("off")
        
        axes[2].imshow(blue_channel, cmap="gray")
        axes[2].set_title("Blue Channel")
        axes[2].axis("off")
        
        st.pyplot(fig)



# Run the Streamlit App
if __name__ == "__main__":
    NumPyVizApp()