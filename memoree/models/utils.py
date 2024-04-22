def tinh_do_tuong_dong(ky_tu_1, ky_tu_2):
    if len(ky_tu_1) == 0 and len(ky_tu_2) == 0:
        return 100.0
    max_length = max(len(ky_tu_1), len(ky_tu_2))
    min_distance = levenshtein(ky_tu_1, ky_tu_2)
    similarity_ratio = ((max_length - min_distance) / max_length) * 100
    return similarity_ratio


def levenshtein(s1, s2):
    if len(s1) < len(s2):
        return levenshtein(s2, s1)
    if len(s2) == 0:
        return len(s1)
    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    return previous_row[-1]
