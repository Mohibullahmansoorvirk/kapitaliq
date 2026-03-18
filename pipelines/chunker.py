class Chunker:
    def __init__ (self, chunk_size:int = 300, overlap: int = 45) -> None:
        self.chunk_size=chunk_size
        self.overlap=overlap


    def chunk(self, content: str) -> list[str]:
        words = content.split()
        step = self.chunk_size - self.overlap
        start = 0
        if len(words) <= self.chunk_size:
            return [content]

        else:
            all_chunks=[]
            while start < len(words):
                end = start + self.chunk_size
                chunk = words[start:end]
                all_chunks.append(" ".join(chunk))
                start = start + step

            return all_chunks
        

if __name__ == "__main__":
    chunker = Chunker()
    test_content = " ".join([f"word{i}" for i in range(600)])  # 600 fake words
    chunks = chunker.chunk(test_content)
    print(f"Total chunks: {len(chunks)}")
    print(f"Chunk 1 word count: {len(chunks[0].split())}")
    print(f"Chunk 2 word count: {len(chunks[1].split())}")
    print(f"Chunk 3 word count: {len(chunks[2].split())}")
    print(f"Last 45 words of chunk 1 == first 45 words of chunk 2: {chunks[0].split()[-45:] == chunks[1].split()[:45]}")