def count_even(vals):
    """Returns the amount of even numbers."""
    c=0
    for v in vals:
        if (v % 2) == 0:
            c=c+1
    return c

x = [-2, -4, 3, 6, 88, 76, -7]

y=count_even(x)

print("The list {} contains {} even numbers.".format(x,y))
