import json
import os
from datetime import datetime


class EpisodicMemory:

    def __init__(self):

        self.memory_dir = os.path.join(
            os.path.dirname(__file__),
            "episodes"
        )

        os.makedirs(self.memory_dir, exist_ok=True)

    # ---------------------------------
    # GENERATE EPISODE ID
    # ---------------------------------
    def _generate_episode_id(self):

        files = [
            f for f in os.listdir(self.memory_dir)
            if f.startswith("episode_") and f.endswith(".json")
        ]

        if not files:
            return "episode_001.json"

        numbers = []

        for f in files:
            try:
                n = int(f.replace("episode_", "").replace(".json", ""))
                numbers.append(n)
            except:
                continue

        next_id = max(numbers) + 1

        return f"episode_{next_id:03d}.json"

    # ---------------------------------
    # SAVE EPISODE
    # ---------------------------------
    def save_episode(
        self,
        request,
        strategy,
        plan,
        result,
        execution_time,
        capabilities_used=None
    ):

        if capabilities_used is None:
            capabilities_used = []

        episode = {
            "timestamp": datetime.utcnow().isoformat(),
            "request": request,
            "strategy": strategy,
            "plan": plan,
            "result": result,
            "execution_time": execution_time,
            "capabilities_used": capabilities_used
        }

        file_name = self._generate_episode_id()

        file_path = os.path.join(self.memory_dir, file_name)

        try:

            with open(file_path, "w") as f:
                json.dump(episode, f, indent=2)

        except Exception as e:
            print(f"⚠️ Failed to save episode: {e}")

    # ---------------------------------
    # LOAD ALL EPISODES
    # ---------------------------------
    def load_all_episodes(self):

        episodes = []

        files = sorted(os.listdir(self.memory_dir))

        for file in files:

            if not file.endswith(".json"):
                continue

            path = os.path.join(self.memory_dir, file)

            try:

                with open(path, "r") as f:
                    data = json.load(f)

                    data["_file"] = file

                    episodes.append(data)

            except:
                continue

        return episodes

    # ---------------------------------
    # GET RECENT EPISODES
    # ---------------------------------
    def get_recent_episodes(self, limit=10):

        episodes = self.load_all_episodes()

        return episodes[-limit:]

    # ---------------------------------
    # SEARCH EPISODES BY REQUEST
    # ---------------------------------
    def search_by_request(self, request):

        episodes = self.load_all_episodes()

        results = []

        for ep in episodes:

            if ep.get("request") == request:
                results.append(ep)

        return results