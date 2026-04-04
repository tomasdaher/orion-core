from infrastructure.repositories.user_repository import UserRepository


class UserCreator:

    def __init__(self):
        self.name = "user_creator"
        self.user_repository = UserRepository()

    def execute(self, state):

        data = state.get("data", {})

        name = data.get("name", "Unknown")
        email = data.get("email", "no-email")

        try:
            existing_user = self.user_repository.find_by_email(email)

            # ---------------------------------
            # USER EXISTS
            # ---------------------------------

            if existing_user:

                print(f"⚠️ User already exists: {email}")

                score = existing_user.get("score")

                # 🧠 FIX: si el usuario nunca tuvo score real
                if score is None or score == 0:
                    score = 10

                score += 1

                # mejora de nombre
                if existing_user["name"] == "Unknown" and name != "Unknown":
                    print(f"🧠 Updating user name → {name}")
                    self.user_repository.update_user_name(
                        existing_user["id"],
                        name
                    )
                    existing_user["name"] = name
                    score += 5

                self.user_repository.update_score(
                    existing_user["id"],
                    score
                )

                existing_user["score"] = score

                state["user"] = existing_user
                state["last_capability"] = self.name

                return {
                    "status": "exists",
                    "user": existing_user
                }

            # ---------------------------------
            # NEW USER
            # ---------------------------------

            score = 10

            if name != "Unknown":
                score += 5

            user = self.user_repository.create_user(name, email)

            self.user_repository.update_score(user["id"], score)

            user["score"] = score

            print(f"✅ New user created: {email} | score={score}")

            state["user"] = user
            state["last_capability"] = self.name

            return {
                "status": "success",
                "user": user
            }

        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }