from pwn import xor

ct_flag = "c3bfe842c2a270ece9d7463a5636df8e6262a76c7c15b66125fc1e6e121fdc06f4841819b5df5a78d23e0e3db067075487cf3d67a433e20e2891766cd39c3c1a"
ct_m = "d88ec94b98e96fbab88e1677046894d83233b83a300aec3079b1582159458719bcd2534eaaa101318c6f5267eb787d05dbc04a19de54836e06cc0c03b3f65366b4e9802a7ec347f4a8fe15d63ea3d666"

ct_flag = bytes.fromhex(ct_flag)
ct_m = bytes.fromhex(ct_m)
m = b'Secret information is encrypted with Advanced Encryption Standards.'

print(xor(m, ct_m, ct_flag))

ct_flag = "36fdb2d97d0a5bcf0225586a1e8abfc62d3057273aab5ae5309d8c4ade060a236aed070d817b2c14110e590b1b27ef5d4d35ddc001b47d6c2bca00101c25039a"
ct_flag = bytes.fromhex(ct_flag)
ct_m = "2dcc93d07c4a16c833375f2b00d894c62c2d442d3cf90cd43183c559c10006372cea2c1595487c0f4314091c0c268b120f3aaabe7bd31c0c05977a7f7c4f6ce6f59392e0e522e66500e153f7a6f914c7"
ct_m = bytes.fromhex(ct_m)

print(xor(m, ct_m, ct_flag))
