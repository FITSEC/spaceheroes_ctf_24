An agent of the Hidden found some weird transmissions on a satellite that is from before the golden-age.

Can you pick up where they left off and decrypt the data?

Author: [B0n3h34d](https://github.com/password987654321)

Solution: The satellite uses [Magma-CBC](https://en.wikipedia.org/wiki/GOST_(block_cipher)) (specifically the GOST R 34.12-2015 version), an encryption scheme dating back to the soviet-era, to encrypt the message. You can use the given information do a known-plaintext attack on the message.