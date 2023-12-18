__correct_solution_name_list = [
    'Bell Kassulke',
    'Simon Loidl',
    'Elias Jovanovic',
    'Hakim Botros',
    'Emilie Lorentsen',
    'Jake Wood',
    'Fatemeh Akhtar',
    'Kim Weston',
    'Yasmin Dar',
    'Viswamitra Upandhye',
    'Killian Kaufman',
    'Elwood Page',
    'Elodie Booker',
    'Adnan Chen',
    'Hank Spinka',
    'Hannah Bayer'
]


# assert sorted(student_grades())==sorted(__correct_solution_name_list), student_grades()  # noqa
if sorted(student_grades())==sorted(__correct_solution_name_list):
    print("NO ASSERTION CAUGHT!")
else:
    print(sorted(student_grades()))
