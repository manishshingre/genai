import tiktoken

enc = tiktoken.encoding_for_model("gpt-4o")

text = "Hey there! I am Manish Shingre."

encoded = enc.encode(text)
print("Encoded Tokens: ", encoded)

decoded = enc.decode(encoded)
print("Decoded String: ", decoded)