def load_data(data, config):
    output_path = config['path']
    data.to_csv(output_path, index=False)
