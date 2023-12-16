import json

class TreeConverter:
    @staticmethod
    def tree_to_json(tree):
        """
        Convert a tree structure to JSON format.

        :param tree: A tuple representing the tree structure.
        :return: A string representing the tree in JSON format.
        """
        def convert_node(node):
            if node is None:
                return None
            if isinstance(node, tuple):
                question, yes_branch, no_branch = node
                return {
                    "question": question,
                    "yes": convert_node(yes_branch),
                    "no": convert_node(no_branch)
                }
            else:  # Leaf node
                name, coordinates = node[0]
                return {"name": name, "coordinates": coordinates}

        tree_json = convert_node(tree)
        return json.dumps(tree_json, indent=4)

    @staticmethod
    def json_to_tree(json_file_path):
        """
        Convert JSON data to a tree structure.

        :param json_data: A string representing the tree in JSON format.
        :return: A tuple representing the tree structure.
        """
        def convert_json(node):
            if node is None:
                return None
            if "name" in node:  # Leaf node
                return ([node["name"], node["coordinates"]], None, None)
            else:  # Internal node
                return (node["question"], convert_json(node["yes"]), convert_json(node["no"]))
        with open(json_file_path, 'r') as file:
            tree_data = json.load(file)
        return convert_json(tree_data)

if __name__ == "__main__":
    startTree = (
    "Do you like places that snow all the time?",
    (["Minnesota", "-96.075269,46.012721,-92.863071,48.611106"], None, None),
    (["California", "-118.512951,33.505042,-115.300753,36.103427"], None, None)
)
    converter = TreeConverter()

    # Convert tree to JSON
    json_data = converter.tree_to_json(startTree)
    print("JSON Format:\n", json_data)

    # Convert JSON file back to tree and save to file
    converted_tree = converter.json_to_tree("log1.json")
    print("\nConverted Tree:", converted_tree)
