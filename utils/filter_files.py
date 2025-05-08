def filter_data(data, data_type=None, folder_name=None):
    results = []

    def recursive_search(contents, path=""):
        for item in contents:
            current_path = f"{path}/{item['name']}"
            if item['type'] == 'directory' and 'contents' in item:
                    recursive_search(item['contents'], current_path)
            elif item['type'] == 'file':
                if folder_name and folder_name in current_path:
                    if data_type:
                        if item['name'].endswith(data_type):
                            results.append(current_path)
                    else:
                        results.append(current_path)
                elif not folder_name:
                    if data_type:
                        if item['name'].endswith(data_type):
                            results.append(current_path)
                    else:
                        results.append(current_path)

    recursive_search(data[0]['contents'])
    return results
