class TestCapability:

    def execute(self, data=None):

        print("🧪 TestCapability ejecutándose")

        return {
            "capability": "test_capability",
            "status": "executed",
            "data_received": data
        }


def get_capability():

    return TestCapability()