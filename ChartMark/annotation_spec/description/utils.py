# 动态获取文本数组和宽高
def calculate_texts_width_and_height(text_content_str):
    # 设置字符宽度和字符高度
    char_width = 6
    char_height = 12

    # 计算文本的总字符数（包括空格）
    total_chars = len(text_content_str)

    # 设置宽度和高度的比例
    # 假设宽度为字符总数 * 字符宽度的3倍， 高度为宽度的三分之一
    max_width = total_chars * char_width
    max_height = max_width / 3

    # 计算最大行数，最大行数的宽度是max_width，而最小行数是1行
    best_ratio = float("inf")  # 用来存储最接近3:1的长宽比
    best_lines = None
    best_width = None
    best_height = None

    # 计算分配到 n 行的情况，n 从 1 到最多需要的行数
    for num_lines in range(1, total_chars + 1):
        # 每行的字符数
        chars_per_line = (total_chars + num_lines - 1) // num_lines  # 向上取整

        # 计算每行的最大宽度
        line_width = chars_per_line * char_width

        # 确保总宽度不超过最大宽度
        if line_width > max_width:
            break

        # 计算总宽度和总高度
        width = line_width
        height = num_lines * char_height

        # 计算长宽比
        ratio = abs(width / height - 3)

        # 更新最接近3:1的长宽比
        if ratio < best_ratio:
            best_ratio = ratio
            best_lines = num_lines
            best_width = width
            best_height = height

    # 根据最佳行数重新分配单词
    words = text_content_str.split()
    lines = []
    # chars_per_line = (
    #     total_chars + best_lines - 1
    # ) // best_lines  # 重新计算最佳每行字符数
    chars_per_line = (best_width + 12) // char_width  # 重新计算最佳每行字符数
    current_line = []
    current_line_length = 0

    for word in words:
        # 检查当前行加上新单词后的长度是否超过限制
        if current_line_length + len(word) <= chars_per_line:
            current_line.append(word)
            current_line_length += len(word) + 1  # 单词间有空格
        else:
            # 如果超出，则开始新的一行
            lines.append(" ".join(current_line))
            current_line = [word]
            current_line_length = len(word) + 1  # 重置为当前单词长度 + 1（空格）

    # 如果最后一行有内容，添加它
    if current_line:
        lines.append(" ".join(current_line))

    if best_height < char_height * len(lines):
        best_height = char_height * len(lines)

    return lines, best_width, best_height
