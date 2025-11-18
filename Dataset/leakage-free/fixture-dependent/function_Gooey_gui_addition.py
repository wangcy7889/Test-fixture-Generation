from gooey import Gooey, GooeyParser

@Gooey(program_name="Addition GUI Tool", default_size=(600, 400))
def launch_addition_gui():

    parser = GooeyParser(description="Enter two numbers to add")

    parser.add_argument("--num1", type=str, help="First number", widget="DecimalField")
    parser.add_argument("--num2", type=str, help="Second number", widget="DecimalField")
    args = parser.parse_args()

    try:
        first_number = float(args.num1)
        second_number = float(args.num2)
        sum_result = first_number + second_number
        detailed_result = f"Computed sum of {first_number} and {second_number} equals {sum_result}"
        print(f"Total: {sum_result}")
        print(detailed_result)
    except Exception as error:
        print("An error occurred during computation:", error)