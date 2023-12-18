__correct_solution_dict = {
    'male': 0.009675583380762664,
    'female': 0.0077918259335489565
}


# assert chickenpox_by_sex()==__correct_solution_dict, chickenpox_by_sex()  # noqa
if chickenpox_by_sex()==__correct_solution_dict:
    print("NO ASSERTION CAUGHT!")
else:
    print(chickenpox_by_sex())
