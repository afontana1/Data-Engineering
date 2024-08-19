import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


def data_for_3d(num_years=50, num_cols=5):
    np.random.seed(42)
    year = {"Year": list(range(2010, 2010 + num_years))}
    data = {
        f"Column{i}": np.random.randint(0, 100, size=num_years)
        for i in range(0, num_cols)
    }
    data.update(year)
    df = pd.DataFrame(data)
    df.set_index("Year", inplace=True)
    return df


def generate_linear_data(training_points, noise):
    """Generate Linear data.

    Basic Usage in Notebook:
        from ipywidgets import interactive

        training_points = 250    #  Number of training points
        noise = 0.1   # Noise level

        # This will call the interactive widget with the data generating function, which also plots the data real-time
        l=interactive(generate_linear_data,training_points={'50 samples':50,'200 samples':200},noise =(0,1,0.2))
        display(l)
    """
    # generate random data-set
    np.random.seed(0)
    x = np.random.rand(training_points, 1)
    m = 3  # Slope
    c = 1  # Intercept
    y = c + m * x + np.random.rand(training_points, 1) * noise  # y = mx + c + noise
    # plot
    plt.scatter(x, y, s=25, marker="o")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title("Generated data")
    plt.show()
    return (x, y)


def generate_poly_data(training_points, x_min, x_max, noise):
    """Generate Polynomial data.

    Basic Usage in Notebook:
        from ipywidgets import interactive

        x_min = -5
        x_max = 5
        noise = 0.1

        # This will call the interactive widget with the data generating function, which also plots the data real-time
        p=interactive(generate_poly_data,training_points={'50 samples':50,'200 samples':200},noise =(0,1,0.2),x_min=(-5,0,1), x_max=(0,5,1))
        display(p)
    """
    x1 = np.linspace(x_min, x_max, training_points * 5)
    x = np.random.choice(x1, size=training_points)
    y = np.sin(x) + noise * np.random.normal(size=training_points)
    plt.scatter(x, y, edgecolors="k", c="red", s=60)
    plt.grid(True)
    plt.show()
    return (x, y)


def generate_power_lognormal_array(
    size, mean_log=3.0, sigma_log=0.5, clip_range=(0, 100), plot=False
):
    """
    Generate an array of random numbers from a power log-normal distribution.

    Parameters:
    - size: Size of the array.
    - mean_log: Mean of the natural logarithm of the distribution.
    - sigma_log: Standard deviation of the natural logarithm of the distribution.
    - clip_range: Tuple specifying the range to clip the values.

    Returns:
    - Array of random numbers.
    """
    random_numbers = np.random.lognormal(mean_log, sigma_log, size)
    clipped_numbers = np.clip(random_numbers, clip_range[0], clip_range[1])
    clipped_numbers = clipped_numbers.astype(int)
    if plot:
        sns.displot(clipped_numbers, kde=True, bins=15)
    return clipped_numbers


def create_guassian(mean=50, std_dev=25, plot=False):
    """Generate an array of random numbers from a Gaussian distribution.

    Example:
    create_guassian(plot = True)
    """
    # Set the mean and standard deviation for the Gaussian distribution
    mean = 50  # Mean value
    std_dev = 25  # Standard deviation

    # Generate an array of 100 random Gaussian numbers
    random_gaussian_numbers = np.random.normal(loc=mean, scale=std_dev, size=100)
    random_gaussian_numbers = np.round(random_gaussian_numbers)
    # Clip the values to be within the range [0, 100]
    random_gaussian_numbers = np.clip(
        random_gaussian_numbers, 0, max(random_gaussian_numbers)
    )
    random_gaussian_numbers = random_gaussian_numbers.astype(int)
    if plot:
        sns.displot(random_gaussian_numbers, kde=True, bins=15)
    return random_gaussian_numbers


def generate_pareto_array(size, alpha=1.0, scale=4.0, clip_range=(0, 100), plot=False):
    """
    Generate an array of random numbers from a Pareto distribution.

    Parameters:
    - size: Size of the array.
    - alpha: Shape parameter of the distribution.
    - scale: Scale parameter of the distribution.
    - clip_range: Tuple specifying the range to clip the values.

    Returns:
    - Array of random numbers.
    """
    random_numbers = np.random.pareto(alpha, size) * scale
    clipped_numbers = np.clip(random_numbers, clip_range[0], clip_range[1])
    clipped_numbers = clipped_numbers.astype(int)
    if plot:
        sns.displot(clipped_numbers, kde=True, bins=15)
    return clipped_numbers


def create_site_data(years=list(range(2020, 2051))):

    np.random.seed(42)
    # Create column names
    locations = {
        "program1": ["site1", "site2", "site3", "site4"],
        "program2": [
            "site1.1",
            "site2.1",
            "site3.1",
            "site4.1",
            "site5.1",
            "site6.1",
            "site7.1",
        ],
        "program3": [
            "site1.2",
            "site2.2",
            "site3.2",
            "site4.2",
            "site5.2",
            "site6.2",
            "site7.2",
            "site8.2",
            "site9.2",
        ],
        "program4": [
            "site1.3",
            "site2.3",
            "site3.3",
            "site4.3",
            "site5.3",
            "site6.3",
            "site7.3",
            "site8.3",
            "",
        ],
    }

    # Create a DataFrame with random values
    data = {
        "program1": np.random.choice(locations["program1"], size=100),
        "program2": np.random.choice(
            locations["program2"], size=100
        ),  # Set size to 100 for program2
        "program3": np.random.choice(
            locations["program3"], size=100
        ),  # Set size to 100 for program3
        "program4": np.random.choice(
            locations["program4"], size=100
        ),  # Set size to 100 for program4
        **{f"FY{year}": generate_pareto_array(size=100) for year in years},
    }

    return pd.DataFrame(data)


def create_prog_data(years=list(range(2020, 2051))):

    np.random.seed(42)
    # Create column names
    locations = {
        "program1": ["site1", "site2", "site3", "site4"],
        "program2": [
            "site1.1",
            "site2.1",
            "site3.1",
            "site4.1",
            "site5.1",
            "site6.1",
            "site7.1",
        ],
    }

    # Create a DataFrame with random values
    data = {
        "program1": np.random.choice(locations["program1"], size=100),
        "program2": np.random.choice(locations["program2"], size=100),
        **{f"{year}": create_guassian() for year in years},
    }

    return pd.DataFrame(data)
