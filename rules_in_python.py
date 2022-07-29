def predict(feature0, feature1, feature2, feature4, feature5, feature6, feature7, feature8, feature9, feature10, feature12, feature15, feature16, feature17, feature18, feature20, feature21, feature22, feature23, feature27):
    if feature4 <= 1.5:
        return "[[0. 0. 3. 0. 0. 0. 0. 0. 0. 0.]]"
    else:  # if feature4 > 1.5
        if feature9 <= 21.5:
            if feature18 <= 1.5:
                return "[[0. 0. 0. 0. 0. 2. 0. 0. 0. 0.]]"
            else:  # if feature18 > 1.5
                if feature5 <= 6.5:
                    if feature9 <= 6.0:
                        return "[[3. 0. 0. 0. 0. 0. 0. 0. 0. 0.]]"
                    else:  # if feature9 > 6.0
                        if feature16 <= 16.5:
                            return "[[0. 0. 0. 0. 0. 0. 0. 0. 0. 1.]]"
                        else:  # if feature16 > 16.5
                            return "[[0. 0. 0. 1. 0. 0. 0. 0. 0. 0.]]"
                else:  # if feature5 > 6.5
                    if feature22 <= 4.0:
                        if feature10 <= 3.5:
                            return "[[0. 0. 0. 0. 0. 0. 0. 0. 1. 0.]]"
                        else:  # if feature10 > 3.5
                            return "[[0. 3. 0. 0. 0. 0. 0. 0. 0. 0.]]"
                    else:  # if feature22 > 4.0
                        if feature18 <= 19.5:
                            if feature2 <= 22.5:
                                if feature0 <= 23.5:
                                    if feature0 <= 2.5:
                                        return "[[0. 0. 0. 0. 0. 0. 0. 1. 0. 0.]]"
                                    else:  # if feature0 > 2.5
                                        return "[[0. 0. 0. 0. 0. 0. 3. 0. 0. 0.]]"
                                else:  # if feature0 > 23.5
                                    if feature21 <= 7.5:
                                        return "[[0. 0. 0. 1. 0. 0. 0. 0. 0. 0.]]"
                                    else:  # if feature21 > 7.5
                                        return "[[0. 0. 0. 0. 0. 0. 0. 0. 0. 1.]]"
                            else:  # if feature2 > 22.5
                                return "[[0. 0. 0. 0. 0. 0. 0. 0. 2. 0.]]"
                        else:  # if feature18 > 19.5
                            return "[[0. 0. 2. 0. 0. 0. 0. 0. 0. 0.]]"
        else:  # if feature9 > 21.5
            if feature22 <= 8.5:
                return "[[0. 0. 0. 0. 4. 0. 0. 0. 0. 0.]]"
            else:  # if feature22 > 8.5
                if feature27 <= 23.0:
                    return "[[1. 0. 0. 0. 0. 0. 0. 0. 0. 0.]]"
                else:  # if feature27 > 23.0
                    return "[[0. 0. 0. 0. 0. 0. 0. 1. 0. 0.]]"
