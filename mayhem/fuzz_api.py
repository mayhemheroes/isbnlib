#! /usr/bin/env python3
import atheris
import sys
import fuzz_helpers

with atheris.instrument_imports(include=["isbnlib"]):
    import isbnlib

def TestOneInput(data):
    fdp = fuzz_helpers.EnhancedFuzzedDataProvider(data)
    test = fdp.ConsumeIntInRange(0, 13)
    try:
        if test == 0:
            isbnlib.is_isbn10(fdp.ConsumeRemainingString())
        elif test == 1:
            isbnlib.is_isbn13(fdp.ConsumeRemainingString())
        elif test == 2:
            isbnlib.to_isbn10(fdp.ConsumeRemainingString())
        elif test == 3:
            isbnlib.to_isbn13(fdp.ConsumeRemainingString())
        elif test == 4:
            isbnlib.canonical(fdp.ConsumeRemainingString())
        elif test == 5:
            isbnlib.clean(fdp.ConsumeRemainingString())
        elif test == 6:
            isbnlib.notisbn(fdp.ConsumeRemainingString(), level='strict')
        elif test == 7:
            isbnlib.get_isbnlike(fdp.ConsumeRemainingString(), level='normal')
        elif test == 8:
            isbnlib.get_canonical_isbn(fdp.ConsumeRemainingString(), output='bouth')
        elif test == 9:
            isbnlib.ean13(fdp.ConsumeRemainingString())
        elif test == 10:
            isbnlib.info(fdp.ConsumeRemainingString())
        elif test == 11:
            isbnlib.info(fdp.ConsumeRemainingString())
        elif test == 12:
            isbnlib.mask(fdp.ConsumeRandomString(), separator=fdp.ConsumeUnicodeNoSurrogates(1))
    except (isbnlib.NotValidISBNError):
        return -1



def main():
    atheris.Setup(sys.argv, TestOneInput)
    atheris.Fuzz()


if __name__ == "__main__":
    main()
