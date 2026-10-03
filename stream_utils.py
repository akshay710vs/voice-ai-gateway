import re

SENTENCE_END = re.compile(r'([.!?])\s+')

def sentence_chunks(token_stream):

    buffer = ""
    for piece in token_stream:
        buffer += piece
        while True:
            match = SENTENCE_END.search(buffer)
            if not match:
                break
            end = match.end()
            sentence = buffer[:end].strip()
            buffer = buffer[end:]
            if sentence:
                yield sentence
    if buffer.strip():
        yield buffer.strip()
        
         