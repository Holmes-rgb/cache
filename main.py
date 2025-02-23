import math
if __name__ == "__main__":
    # Define the configurable parameters for the simulator

    # Size of a memory address in bits
    MEMORY_ADDRESS_BITS = 16
    MEMORY_SIZE = 2 ** MEMORY_ADDRESS_BITS  # Total memory size in bytes

    # Size of the cache in bytes (must be a power of 2)
    CACHE_SIZE = 2 ** 10

    # Size of a cache block in bytes (must be a power of 2)
    CACHE_BLOCK_SIZE = 2 ** 6

    # Cache associativity (must be a power of 2)
    CACHE_ASSOCIATIVITY = 2 ** 0

    NUM_BLOCKS = CACHE_SIZE // CACHE_BLOCK_SIZE

    NUM_SETS = NUM_BLOCKS // CACHE_ASSOCIATIVITY

    OFFSET_LENGTH = int(math.log2(CACHE_BLOCK_SIZE))

    INDEX_LENGTH = int(math.log2(NUM_SETS))

    TAG_LENGTH = MEMORY_ADDRESS_BITS - (OFFSET_LENGTH + INDEX_LENGTH)

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
    cache = Cache(NUM_SETS, CACHE_ASSOCIATIVITY, CACHE_BLOCK_SIZE)

    def decode_address(A):
        block_offset = A & ((1 << OFFSET_LENGTH) - 1)
        index = (A >> OFFSET_LENGTH) & ((1 << INDEX_LENGTH) - 1)
        tag = A >> (OFFSET_LENGTH + INDEX_LENGTH)
        return [tag, index, block_offset]

    def read_word(A):
        [tag, index, block_offset] = decode_address(A)
        cache_set = cache.sets[index]
        memory_block_start = CACHE_BLOCK_SIZE * (A // CACHE_BLOCK_SIZE)

        for block_index, block in enumerate(cache_set.blocks):
            if block.tag == tag:
                # Cache hit: Extract the word from the block
                word = int.from_bytes(block.data[block_offset:block_offset + 4], 'little')
                print(f"read hit [addr={A} index={index} block_index={block_index} tag={tag} word={word} ({memory_block_start} - {memory_block_start + CACHE_BLOCK_SIZE - 1})]" )
                print(f"=> address = {A} <{format(A,f'0{MEMORY_ADDRESS_BITS}b')}>; word={word}")
                return word

        # Cache miss: Load block from memory
        # Read new data into first block in the set
        block = cache_set.blocks[0]
        block.tag = tag
        block.data = memory[memory_block_start : (memory_block_start + CACHE_BLOCK_SIZE)]

        # Return the requested word
        word = int.from_bytes(block.data[block_offset:block_offset + 4], 'little')
        print(f"read hit [addr={A} index={index} block_index={0} tag={tag} word={word} ({memory_block_start} - {memory_block_start + CACHE_BLOCK_SIZE - 1})]" )
        print(f"=> address = {A} <{format(A, f'0{MEMORY_ADDRESS_BITS}b')}>; word={word}")
        return word

    # Test Case 1:
    print("---------------")
    print(f"cache size = {CACHE_SIZE}")
    print(f"block size = {CACHE_BLOCK_SIZE}" )
    print(f"#blocks = {NUM_BLOCKS}")
    print(f"#sets = {NUM_SETS}")
    print(f"associativity = {CACHE_ASSOCIATIVITY}")
    print(f"tag length = {TAG_LENGTH}")
    print("---------------")


    Addresses = [0, 0, 60, 64, 1000, 1028, 12920, 12924, 12928]
    for add in Addresses:
        read_word(add)