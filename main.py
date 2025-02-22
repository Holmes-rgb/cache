import math

if __name__ == "__main__":
    # Define the configurable parameters for the simulator

    # Size of a memory address in bits
    memory_address_bits = 16
    MEMORY_SIZE = 2 ** memory_address_bits  # Total memory size in bytes

    # Size of the cache in bytes (must be a power of 2)
    CACHE_SIZE = 2 ** 10

    # Size of a cache block in bytes (must be a power of 2)
    CACHE_BLOCK_SIZE = 2 ** 6

    # Cache associativity (must be a power of 2)
    cache_associativity = 2 ** 0

    num_blocks = CACHE_SIZE // CACHE_BLOCK_SIZE

    NUM_SETS = num_blocks // cache_associativity

    offset_length = int(math.log2(CACHE_BLOCK_SIZE))

    index_length = int(math.log2(NUM_SETS))

    tag_length = memory_address_bits - (offset_length + index_length)

    # Initialize memory so that reading from address A returns A
    memory = bytearray(MEMORY_SIZE)
    for i in range(MEMORY_SIZE - 4):
        if i % 4 == 0:
            memory[i] = i % 256

            memory[i + 1] = (i // 256) % 256

            memory[i + 2] = ((i // 256) // 256) % 256

            memory[i + 3] = (((i // 256) // 256) // 256) % 256


    class CacheBlock:
        def __init__(self, cache_block_size):
            self.tag = -1
            self.dirty = False  # not needed for Part One
            self.valid = False  # not needed for Part One
            self.data = bytearray(cache_block_size)


    class CacheSet:
        def __init__(self, cache_block_size, associativity):
            self.blocks = [CacheBlock(cache_block_size) for i in range(associativity)]
            self.tag_queue = [-1 for i in range(associativity)]  # not needed for Part One


    class Cache:
        def __init__(self, num_sets, associativity, cache_block_size):

            self.write_through = False  # not needed for Part One
            self.sets = [CacheSet(cache_block_size, associativity) for i in range(num_sets)]
            memory_size_bits = math.log2(MEMORY_SIZE)
            self.cache_size_bits = math.log2(CACHE_SIZE)
            self.cache_block_size_bits = math.log2(CACHE_BLOCK_SIZE)
            self.index_length = math.log2(NUM_SETS)
            self.block_offset_length = math.log2(CACHE_BLOCK_SIZE)


    # Initialize cache as a list of sets
    cache = Cache(NUM_SETS, cache_associativity, CACHE_BLOCK_SIZE)


    def decode_address(A):
        block_offset = A & ((1 << offset_length) - 1)
        index = (A >> offset_length) & ((1 << index_length) - 1)
        tag = A >> (offset_length + index_length)
        return [tag, index, block_offset]


    def read_word(A):
        [tag, index, block_offset] = decode_address(A)
        cache_set = cache.sets[index]

        for block in cache_set.blocks:
            if block.tag == tag:
                # Cache hit: Extract the word from the block
                print(f"read hit [addr= {A} index= {index} tag= {tag}]")
                word = int.from_bytes(block.data[block_offset:block_offset + 4], 'little')
                print(f"word: {word}")
                return word

        # Cache miss: Load block from memory
        print(f"read miss [index= {index} tag= {tag}]")
        memory_block_start = CACHE_BLOCK_SIZE * (A // CACHE_BLOCK_SIZE)

        # Read new data into first block in the set
        block = cache_set.blocks[0]
        block.tag = tag
        block.data = memory[memory_block_start : (memory_block_start + CACHE_BLOCK_SIZE)]

        # Return the requested word
        word = int.from_bytes(block.data[block_offset:block_offset + 4], 'little')
        print(f"word: {word}")
        return word

    # Test Case 1:
    print("---------------")
    print("cache size = " + str(CACHE_SIZE))
    print("block size = " + str(CACHE_BLOCK_SIZE))
    print("#blocks = " + str(num_blocks))
    print("#sets = " + str(NUM_SETS))
    print("associativity = " + str(cache_associativity))
    print("tag length = " + str(tag_length))
    print("---------------")


    Addresses = [0, 0, 60, 64, 1000, 1028, 12920, 12924, 12928]
    for add in Addresses:
        read_word(add)