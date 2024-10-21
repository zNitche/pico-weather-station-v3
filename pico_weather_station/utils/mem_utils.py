import gc


def reset_heap(threshold: int = 8192):
    """use before memory heavy operations like allocating large lists / dicts"""
    gc.collect()

    #gc.threshold(gc.mem_free() // 4 + gc.mem_alloc())
    gc.threshold(threshold)
