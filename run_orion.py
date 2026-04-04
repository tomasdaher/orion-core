from bootstrap import build_system


def main():

    # ---------------------------------
    # BUILD ORION SYSTEM
    # ---------------------------------

    orion = build_system()

    # ---------------------------------
    # TEST INPUT EVENT
    # ---------------------------------

    state = {
        "data": {
            "trigger": "new_customer",
            "customer_name": "Test User",
            "email": "test@example.com"
        }
    }

    print("\n🚀 Starting Orion execution...\n")

    result = orion.run(state)

    print("\n✅ Orion execution finished\n")

    print("Final State:")
    print(result)


if __name__ == "__main__":
    main()