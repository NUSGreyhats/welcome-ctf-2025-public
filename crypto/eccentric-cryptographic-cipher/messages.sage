from Crypto.Util.number import long_to_bytes

def get_messages(p, q, e):
    return [
        b"According to all known laws of aviation, ",
        b"there is no way a bee should be able to fly.",
        b"The bee, of course, flies anyway because bees don't care what humans think is impossible.",
        b"Water. Earth. Fire. Air. Long ago, the four nations lived together in harmony.",
        b"Then, everything changed when the Fire Nation attacked.",
        b"Only the Avatar, master of all four elements, could stop them, ",
        b"but when the world needed him most, he vanished.",
        long_to_bytes(q + 1), # Leak the fixed point.
        b"grey{d3j4_vu_b3caus3_1v3_pl4y3ed_th3s3_g4m3s_b4}",
        b"That which is done out of love always takes place beyond good and evil.",
        b"Is man merely a mistake of God's? Or God merely a mistake of man?",
        b"Consider the cattle, grazing as they pass you by. They do not know what is meant ",
        b"by yesterday or today, they leap about, eat, rest, digest, leap about again, ",
        b"and so from morn till night and from day to day, ",
        b"fettered to the moment and its pleasure or displeasure, ",
        b"and thus neither melancholy nor bored.",
        b"I have my self-consciousness not in myself but in the other.",
        b"`I'm sure you can find a lot of stupid quotes about philosophy` ~sqrt963",
        b"`Something something amor fati` ~sqrt963",
        b"Just because you don't take interest in politics doesn't mean politics won't take an interest in you.",
        b"All animals are equal, but some animals are more equal than others.",
        b"`Nietzsche, nitchi, I don't even know how to say his name` ~sqrt963",
    ]
