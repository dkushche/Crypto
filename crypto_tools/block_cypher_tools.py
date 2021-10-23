from .general_tools import supl_to_mult


def block_generator(data, block_size):
    if block_size < 2 or block_size % 2:
        raise ValueError("Block size must be bigger then 1 and be pair")

    supl_to_mult(data, block_size)

    for block_id in range(len(data) // block_size):
        left_start = block_id * block_size
        left_end = left_start + (block_size // 2)
        left = data[left_start:left_end:1]

        right_start = left_end
        right_end = right_start + (block_size // 2)
        right = data[right_start:right_end:1]

        yield left, right
