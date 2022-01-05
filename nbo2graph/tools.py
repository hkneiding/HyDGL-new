class Tools:

    @staticmethod
    def get_one_hot_encoded_feature_lists(feature_lists):

        """Takes a list of feature lists and replaces non-numerical values with appropriate one-hot encoded representations.

        Raises:
            ValueError: If the individual feature lists have different lengths.

        Returns:
            list[float]: Returns the corresponding feature list with one-hot encoded values.
        """

        # check that all feature lists have the same length
        for feature_list in feature_lists:
            if len(feature_list) != len(feature_lists[0]):
                raise ValueError('The provided feature lists have differing lengths.')

        # get indices of features that are not numeric and need to be one-hot encoded
        class_feature_indices = []
        for i in range(len(feature_lists[0])):
            if not type(feature_lists[0][i]) == int and not type(feature_lists[0][i]) == float:
                class_feature_indices.append(i)

        # replace features with one-hot encoding
        for class_feature_index in class_feature_indices:

            # get the individual feature list
            feature_list = [x[class_feature_index] for x in feature_lists]
            # get its one-hot encoding
            one_hot_feature_list = Tools.get_one_hot_encoded_list(feature_list)

            # change feature lists in place
            for i in range(len(feature_lists)):
                feature_lists[i][class_feature_index] = one_hot_feature_list[i]

        # flatten all individual feature lists
        for i in range(len(feature_lists)):
            feature_lists[i] = Tools.flatten_list(feature_lists[i])

        return feature_lists

    @staticmethod
    def get_one_hot_encoded_list(input_list: list[str]):

        """Gets the one-hot encoded version of of a list of class features of the same type.

        Returns:
            list[list[int]]: The one-hot encoded feature list.
        """

        # get all classes
        class_list = []
        for item in input_list:
            if item not in class_list:
                class_list.append(item)

        # build one-hot encoded list
        output_list = []
        for item in input_list:
            output_list.append(Tools.get_one_hot_encoding(len(class_list), class_list.index(item)))

        return output_list

    @staticmethod
    def get_one_hot_encoding(n_classes: int, class_number: int):

        """Helper function that the one hot encoding for one specific element by specifying the number of classes and the class of the current element.

        Raises:
            ValueError: If a class number is requested that is higher than the maximum number of classes.

        Returns:
            list[int]: The one hot encoding of one element.
        """

        if class_number >= n_classes:
            raise ValueError('Cannot get one hot encoding for a class number higher than the number of classes.')

        return [1 if x == class_number else 0 for x in list(range(n_classes))]

    @staticmethod
    def flatten_list(input_list):

        """Flattens a irregular list. Embeds any sublist as individual values in main list.

        Returns:
            list[]: The flattend list.
        """

        flattend_list = []
        for element in input_list:
            if isinstance(element, list):
                flattend_list.extend(Tools.flatten_list(element))
            else:
                flattend_list.append(element)

        return flattend_list
