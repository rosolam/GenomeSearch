import decimal

def encode_base4(number, precision=100):
    # Set precision for decimal operations
    decimal.getcontext().prec = precision + 50  # Extra precision to ensure accuracy

    # Split the number into its integer and fractional parts
    number = decimal.Decimal(number)
    integer_part = int(number)
    fractional_part = number - integer_part

    # Convert the integer part to base 4
    base4_integer = ''
    if integer_part == 0:
        base4_integer = '0'
    else:
        while integer_part > 0:
            base4_integer = str(integer_part % 4) + base4_integer
            integer_part //= 4

    # Convert the fractional part to base 4 with extra precision
    base4_fractional = ''
    for _ in range(precision + 50):  # Adding extra digits for accuracy
        fractional_part *= 4
        digit = int(fractional_part)
        base4_fractional += str(digit)
        fractional_part -= digit
        if fractional_part == 0:
            break

    # Truncate to the requested precision
    base4_fractional = base4_fractional[:precision]

    return base4_integer + '.' + base4_fractional if base4_fractional else base4_integer

def base4_to_decimal(base4_str):
    # Split the base 4 string into integer and fractional parts
    if '.' in base4_str:
        integer_part, fractional_part = base4_str.split('.')
    else:
        integer_part, fractional_part = base4_str, ''

    # Convert the integer part
    integer_value = 0
    for i, digit in enumerate(reversed(integer_part)):
        integer_value += int(digit) * (4 ** i)

    # Convert the fractional part
    fractional_value = decimal.Decimal(0)
    for i, digit in enumerate(fractional_part):
        fractional_value += int(digit) * (decimal.Decimal(4) ** -(i + 1))

    return integer_value + fractional_value

# Example usage
number = '3.14159265358979323846264338327950288419716939937510'
precision = 100
encoded_value = encode_base4(number, precision)
print(f"Base 4 representation of {number} with precision {precision}: {encoded_value}")

# Verify by converting back to decimal
decoded_value = base4_to_decimal(encoded_value)
print(f"Converted back to decimal: {decoded_value}")
