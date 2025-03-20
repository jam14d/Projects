import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

class DataVizApp:
    def __init__(self):
        """Initialize the app"""
        self.option = st.sidebar.radio("Choose a section:", [
            "Exploring Probability: Random Data Generator", 
            "Shape & Shift: NumPy Array Playground",
            "Code Your Vision: Image Processing and OOP"
        ])
        self.run_app()

    def run_app(self):
        """Run the selected section of the app"""
        if self.option == "Exploring Probability: Random Data Generator":
            self.display_random_distributions()
        elif self.option == "Shape & Shift: NumPy Array Playground":
            self.display_array_transformations()
        elif self.option == "Code Your Vision: Image Processing and OOP":
            self.code_your_vision()

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
        
    def code_your_vision(self):
        """Upload an image and extract its color channels"""
        st.title("Code Your Vision: Image Processing and OOP")
        uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
        
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image", use_column_width=True)
            
            image_array = np.array(image)
            st.write("### Image Array Shape:")
            st.code(image_array.shape)
            
            if st.button("Extract Red Channel"):
                red_channel = image_array[:, :, 0]
                self.display_channel(red_channel, "Red Channel")
            
            if st.button("Extract Green Channel"):
                green_channel = image_array[:, :, 1]
                self.display_channel(green_channel, "Green Channel")
            
            if st.button("Extract Blue Channel"):
                blue_channel = image_array[:, :, 2]
                self.display_channel(blue_channel, "Blue Channel")
        
        # OOP Learning Section
        st.title("Learn Object-Oriented Programming with Image Processing")
        st.write("This section will guide you through OOP concepts by working with images in Python.")
        
        st.markdown("""
        ## Step 1: Define the Class
        - Define functions inside the class using `def`
        - Think about what your class needs to run when you create `__init__` (like an image path).
        - Use `self` to store attributes that belong to the object.
        """)
        user_class_code = st.text_area("Write your class definition and `__init__` method:")
        
        st.markdown("""
        ## Step 2: Load an Image
        - Create a method called `load_image`.
        - This function should open an image using `PIL.Image.open`.
        - Convert it into a NumPy array using `np.array()` and store it as an attribute.
        """)
        user_load_code = st.text_area("Write your `load_image` function:")

        st.markdown("""
        ## Step 3: Extract Color Channels
        - Create a function `extract_channel(self, channel_index)`.
        - Use NumPy slicing to select the correct channel (`image[:, :, channel_index]`).
        - The function should return `None` if the image is not loaded.
        """)
        user_extract_code = st.text_area("Write your `extract_channel` function:")

        st.markdown("""
        ## Step 4: Display a Channel
        - Define a function `display_channel(self, channel, title)`.
        - Use Matplotlib’s `imshow()` with `cmap="gray"` to show the extracted channel.
        - Make sure to turn off the axis for a cleaner display.
        """)
        user_display_code = st.text_area("Write your `display_channel` function:")
        
        solution_code = """import numpy as np\nimport matplotlib.pyplot as plt\nfrom PIL import Image\n\nclass ImageProcessor:\n    def __init__(self, image_path=None):\n        \"\"\"Initialize the class with an optional image path.\"\"\"\n        self.image_path = image_path\n        self.image_array = None\n        if image_path:\n            self.load_image()\n\n    def load_image(self):\n        \"\"\"Load an image and convert it to a NumPy array.\"\"\"\n        image = Image.open(self.image_path)\n        self.image_array = np.array(image)\n\n    def extract_channel(self, channel_index):\n        \"\"\"Extract a specific color channel (0: Red, 1: Green, 2: Blue).\"\"\"\n        if self.image_array is not None:\n            return self.image_array[:, :, channel_index]\n        return None\n\n    def display_channel(self, channel, title):\n        \"\"\"Display an extracted channel in grayscale.\"\"\"\n        fig, ax = plt.subplots()\n        ax.imshow(channel, cmap=\"gray\")\n        ax.set_title(title)\n        ax.axis(\"off\")\n        plt.show()\n"""
        st.download_button("Download Solution", solution_code, file_name="oop_image_processing_solution.txt", mime="text/plain")

    def display_channel(self, channel, title):
        """Display an extracted color channel in grayscale"""
        fig, ax = plt.subplots()
        ax.imshow(channel, cmap="gray")
        ax.set_title(title)
        ax.axis("off")
        st.pyplot(fig)
# Run the app
if __name__ == "__main__":
    DataVizApp()