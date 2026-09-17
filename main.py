from src.runtime import JUFERuntime


def main() -> None:

    runtime = JUFERuntime()

    while True:

        print("\n" + "=" * 60)
        print("JUFE FOUNDATION RUNTIME")
        print("=" * 60)
        print("1. Boot Runtime")
        print("2. Evaluate")
        print("3. Exit")

        choice = input("\nSelection: ").strip()

        if choice == "1":

            try:

                result = runtime.boot()

                print("\nJUFE Boot Successful\n")
                print(f"Specification : {result['specification']}")
                print(f"Engine        : {result['engine']}")
                print(f"Status        : {result['status']}")

            except Exception as error:

                print(f"\nBoot Error: {error}")

        elif choice == "2":

            raw = input(
                "\nEnter values separated by commas\n\n> "
            )

            try:

                values = [
                    float(value.strip())
                    for value in raw.split(",")
                    if value.strip()
                ]

                result = runtime.evaluate(values)

                print("\n" + "=" * 60)
                print("JUFE RESULTS")
                print("=" * 60)

                if "states" in result:

                    print(
                        f"\nEvaluated {len(result['states'])} Local Field State(s)\n"
                    )

                    for index, state in enumerate(result["states"], start=1):

                        print(f"State {index}")
                        print("-" * 30)

                        for name, value in state["state"].items():
                            print(f"{name:>2} : {value}")

                        print(f"Phase        : {state['phase']}")
                        print(f"Conservation : {state['local_conservation']}")
                        print(f"Equilibrium  : {state['equilibrium']}")
                        print(f"Stable       : {state['stable']}")

                        if "status" in state:
                            print(f"Status       : {state['status']}")

                        print()

                    if result.get("remaining"):

                        print("Remaining Values")
                        print("----------------")
                        print(result["remaining"])

                else:

                    for name, value in result["state"].items():
                        print(f"{name:>2} : {value}")

                    print(f"\nPhase        : {result['phase']}")
                    print(f"Conservation : {result['local_conservation']}")
                    print(f"Equilibrium  : {result['equilibrium']}")
                    print(f"Stable       : {result['stable']}")

                    if "status" in result:
                        print(f"Status       : {result['status']}")

            except Exception as error:

                print(f"\nEvaluation Error: {error}")

        elif choice == "3":

            print("\nGoodbye.\n")
            break

        else:

            print("\nInvalid selection.")


if __name__ == "__main__":
    main()