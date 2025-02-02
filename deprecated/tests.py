
def test_opinion_matrix_experiment(tmp_path):
    """Test the opinion_matrix_experiment function and ensure it saves a CSV file."""
    n_runs = 3
    n_nodes = 10
    time_steps = 50
    mu_values = [0.1, 0.3, 0.5]
    epsilon_values = [0.1, 0.3, 0.5]
    
    output_file = tmp_path / "opinion_matrix.csv"
    
    # Run the experiment
    opinion_matrix_experiment(n_runs, n_nodes, time_steps, mu_values, epsilon_values, str(output_file))
    
    # Ensure the file was created
    assert output_file.exists(), f"Expected CSV file at {output_file}, but it does not exist."
    
    # Load the CSV file to ensure it's not empty
    df = pd.read_csv(output_file, index_col=0)
    assert not df.empty, "The resulting CSV file is empty."
    
    # Ensure the dimensions of the DataFrame match the expected matrix size
    assert df.shape == (len(mu_values), len(epsilon_values)), "Matrix dimensions do not match the expected size."

    # Optionally, check if the values in the CSV are within a valid range
    for value in df.values.flatten():
        assert 0 <= value <= 1, f"Similarity value should be between 0 and 1, but found {value}"
